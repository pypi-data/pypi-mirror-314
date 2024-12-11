#!/usr/bin/env python

import os, sys, json, time, argparse, subprocess

# Scipy and numpy env parameters that limit the threads
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

with open('config.json') as json_file:
    config = json.load(json_file)

import logging
from logging import handlers

import shutil
import pickle
import random 

from datetime import datetime
from pathlib import Path
from pycondor import Job, Dagman
from multiprocessing import Process , Queue , Pool

import numpy as np
import pandas as pd

# Input creation
    
from mly.tools import dirlist, internalLags
from mly.datatools import DataSet, DataPod
# Data assemble
from mly.offlinefar import assembleDataSet

def held_jobs_to_list():
    output = str(subprocess.check_output("condor_q -hold -autoformat:j RequestMemory",shell=True))
    output = output[2:-3]
    logger.debug(f"held_jobs output: {output} and the lenght {len(output)}")
    if len(output)!=0:
        lines = output.split('\\n')
        thelist = list(line.split(' ') for line in lines)
        return(thelist) 
    else:
        return([])


def dataToQueue(dataSet_Q, dataSetName_Q): # Depricated until Hermes issue solved

    already_used=[]
    while (1):

        fileList = dirlist(config["falseAlarmRates"]+"/temp/")

        for file in fileList:

            t0 = time.time()

            if file in already_used: 
                logger.debug(f"File already used {file}")
                continue 

            while dataSet_Q.qsize() > 5:
                time.sleep(0.1)
            t0 = time.time()

            logger.debug(f"Does file exist? {os.path.isfile(config['falseAlarmRates']+'/temp/'+file), file}")
            try:
                set_ = DataSet.load(config["falseAlarmRates"]+"/temp/"+file)
                dataSet_Q.put(set_)
                dataSetName_Q.put(file)
            except Exception as e:
                logger.debug(f"Loading Exception: {e}")

            logger.info(f"Load to Queue time: {time.time()-t0}")

            #os.remove(config["falseAlarmRates"]+"/temp/"+file)

            #sys.stdout.flush()

        time.sleep(1)



def load_data_file(filename):

    t0 = time.time()

    logger.debug(f"Does file exist? {os.path.isfile(config['falseAlarmRates']+'/temp/'+filename), filename}")
    try:
        set_ = DataSet.load(config["falseAlarmRates"]+"/temp/"+filename)
        logger.info(f"Loading time for {filename} : {time.time()-t0}")

        #sys.stdout.flush()
        return(set_)
    except Exception as e:
        logger.debug(f"Loading Exception: {e}")


    
    
def subGeneration(dataSet           # The DataSet
                  , batchNumber     # The number
                  , batches  =   config['far_config']['batches']    # Number of parallel subscripts running
                  , masterDirectory = config['masterDirectory']
                  , lags = config['far_config']['lags'] ):
    
    """ This is a function that is used to assemble a dataset from zero-laged 
    data. Used by generation function to assemble the data in parallel. The 
    generation function will split the job to a number of jobs equal to 
    'batches', each job will have a number 'batchNumber' focusing the jobs on a
    specific part. 
    
    dataSet : DataSet
        This is the original zero-lagged dataSet to be used as source.
    
    batches : int
        The number of parallel function are running along with the current one.
        
    batchNumber : int
        The order number of the current function running. 
        
    masterDirectory : str (path)
        The directory where the zero-lagged scripts are located.
        
    lags : int
        The number of time-shifts (lags) to be used. If not specified it will 
        use all the available lags. By default zero-lag is not included.
        
    Return
    ------
    
    dataset : DataSet
        A dataset with all the timelaged instances.
    
    
    """
    
    np.random.seed(config['seed'] + batchNumber)
    random.seed(config['seed'] + batchNumber)

    out = assembleDataSet( masterDirectory = masterDirectory
                        , dataSets = dataSet
                        , detectors = detectors #dirlist(kwdict['masterDirectory']+'temp')
                        , batches = batches
                        , batchNumber = batchNumber
                        , lags=lags
                        , includeZeroLag=False)
    
    
    out_name = dataSet.split('_')[0]+"_"+str(batchNumber)+"_TOKEN"
    out.save(out_name)
    

def condorGeneration( batches = config['far_config']['batches']     # Number of parallel subscripts scripts to run 
                     , masterDirectory = config['masterDirectory'] # The directory where to source the data
                     , lags = config['far_config']['lags']):     # Lags to use
            
    
    """ This main generation function that is used to assemble a dataset from 
    zero-laged data. It will split the generation to a number of jobs equal to 
    'batches'.
    
        
    batches : int
        The number of parallel function to use for the assemble.
        
    masterDirectory : str (path)
        The directory where the zero-lagged scripts are located.
        
    lags : int
        The number of time-shifts (lags) to be used. If not specified it will 
        use all the available lags. By default zero-lag is not included.
        
    Return
    ------
    
    This function does not return anything. All outputs are transfere to the 
    dataSet_q.
    
    Note
    ----
    
    This function is meant to run parallel to inference and it does not stop
    until the user kills it.
    
    """

    jobsAndDagsRunning = 0

    # The hourly files already created 
    hourly_files =  [file_ for file_ in os.listdir(f"{config['falseAlarmRates']}/hourly") if file_.endswith(".pkl")]
    # Their suffixes used to identify files that belong tho this hour
    hourly_groups= list(file.split("_")[0] for file in hourly_files)

    condor_files =  dirlist(config["falseAlarmRates"]+"/condor")
    # Their suffixes used to identify files that belong tho this hour
    condor_groups= list(file.split("_")[0] for file in condor_files)

    # Files that were created by inference but not yet included to their hourly group
    inference_temp_files =  dirlist(config["falseAlarmRates"])
    for directory in ['hourly', 'condor', 'FARfile','temp']:
        if directory in inference_temp_files: inference_temp_files.remove(directory)
    
    # Identifing which groups of files have yet to be merged with their hourly group
    # (Usually these files are the most recent ones)
    inference_temp_files_groups = list(file.split("_")[0] for file in inference_temp_files)
    inference_temp_files_groups = list(dict.fromkeys(inference_temp_files_groups))
    
    # All the suffixes from the zero-lag files used in inference. We will
    # use these suffixes to identify files that are already used.
    all_files = dirlist(masterDirectory+'/'+detectors[0])
    all_files_groups = list(file.split("_")[0] for file in all_files)

    # The temporary time-lagged files waiting to go through inference.
    timelag_temp_files =  dirlist(config['falseAlarmRates']+"/temp/")
    timelag_temp_files_groups = list(file.split("_")[0] for file in timelag_temp_files)
    timelag_temp_files_groups = list(dict.fromkeys(timelag_temp_files_groups))

    # In case this script has already run once for this search, we need
    # to make sure that we will not generate duplicate files for the FAR
    # calculation. So before it starts, it skips any inference attempts that
    # have been done before.

    pastfiles = []

    for agroup, afile in zip(all_files_groups,all_files):
        
        # If the file group is already in hourly groups, 
        # and there is not any file in the inference output files waiting to be merged with the hourly,
        # and there is not any dagmans that already started to produce files from this group
        # it is safe to assume that inference for this group is completed. So we added
        # to past files.
        if ((agroup in hourly_groups) 
            or (agroup in condor_groups)
            or (agroup in inference_temp_files_groups) 
            or (agroup in timelag_temp_files_groups)):
            pastfiles.append(afile)
                        

    while (1):
        
        # if the dataSet_q is not cloging, continue assembling
        jobsAndDagsRunning = int(subprocess.check_output("condor_q -autoformat RequestMemory | wc -l",shell=True))

        # Newly created dataSets in the masterDirectory
        listOfInputs = dirlist(masterDirectory+'/'+detectors[0])

        files_to_remove = [] # Check this again
        # for i , file in enumerate(listOfInputs):
        #     if not all(file in dirlist(masterDirectory+'/'+det) for det in detectors[1:]):
        #         files_to_remove.append(file)

        for file in files_to_remove:
            for det in detectors:
                os.system("rm "+masterDirectory+"/"+det+"/"+file)
            listOfInputs.remove(file)

        for file in pastfiles:
            if file in listOfInputs: listOfInputs.remove(file)

        for file in listOfInputs: 
            
            # releaseJobsTrials = 0

            filesInTemp = int(subprocess.check_output("ls "+config["falseAlarmRates"]+"/temp | wc -l",shell=True))
            #sys.stdout.flush()
            while (jobsAndDagsRunning >= batches*(parallelGenerations-1)) or filesInTemp >= parallelGenerations*batches:
                time.sleep(60)
                jobsAndDagsRunning = int(subprocess.check_output("condor_q -autoformat RequestMemory | wc -l",shell=True))
                filesInTemp = int(subprocess.check_output("ls "+config["falseAlarmRates"]+"/temp | wc -l",shell=True))

                logger.info(f"Jobs and Dags running: {jobsAndDagsRunning}, Files in temp: ,{filesInTemp}")

                heldJobs = held_jobs_to_list()

                for held_job in heldJobs:
                    
                    if int(held_job[1])<(12*2048):

                        logger.info(f"Held Jobs: {len(heldJobs)}")
                        os.system(f"condor_qedit {held_job[0]} RequestMemory {int(held_job[1])+2048}")
                        os.system(f"condor_release {held_job[0]}")

                    else:

                        logger.warning(f"Held Job: {held_job[0]} needs more than {12*2048} which is above the automated memory increase limit")

            time.sleep(15)
            
            
                            
            # Inferring the set size from the name of the file
            setSize = int(file.split('_')[-1].split('.')[0])
            
            # Setting the lag parameter incase of None
            if lags==None:
                lags = setSize


            accounting_group_user=config['accounting_group_user']
            accounting_group = config["accounting_group"]

            # These are writen on the condor node so the need a path that works
            # on the condor node independently from the submition node.
            error = f"./{config['falseAlarmRates']}/condor/{file[:-4]}/error"
            output = f"./{config['falseAlarmRates']}/condor/{file[:-4]}/output"
            # These two are not writen from the condor node so relative path is fine.
            log = f"{config['falseAlarmRates']}/condor/{file[:-4]}/log"
            submit = f"{config['falseAlarmRates']}/condor/{file[:-4]}/submit"

            dagman = Dagman(name=config['path'].split('/')[-1]+'_'+file[:-4]+"_DAG",submit=submit)
            
            job_list=[]
            
            python_path = str(subprocess.check_output("which python",shell=True))[2:-3]
            logger.debug(f"Python path used: {python_path}")


            master_directory_input_files = ""
            for det in detectors: 
                master_directory_input_files += f"{masterDirectory}/{det}/{file},"
            print(master_directory_input_files)

            for batch in np.arange(batches):

                jobname = file[:-4]+"_"+str(batch)
                output_file_name = file.split('_')[0]+"_"+str(batch)+"_TOKEN.pkl"


                thearguments = ("-m mly_pipeline.continuous_FAR"
                                +" --mode=sub_generation" 
                                +" --dataSet="+file
                                +" --batchNumber="+str(batch))
                
                job = Job(name = jobname
                        ,executable = python_path 
                        ,retry = 3
                        ,arguments = thearguments
                        ,submit=submit
                        ,error=error
                        ,output=output
                        ,log=log
                        ,getenv=True
                        ,dag=dagman
                        ,requirements=" && ".join(config['condor_submit_requirements'])
                        ,extra_lines=["accounting_group_user="+accounting_group_user
                                        ,"accounting_group="+accounting_group
                                        ,"preserve_relative_paths = TRUE"                                       
                                        ,f"transfer_input_files    = {master_directory_input_files}config.json"
                                        ,f"transfer_output_files   = {output_file_name}"
                                        ,f"transfer_output_remaps = \"{output_file_name} = {config['falseAlarmRates']}/temp/{output_file_name}\""
                                        ,"should_transfer_files   = YES"
                                        ,"success_exit_code = 0"
                                        ,"when_to_transfer_output = ON_SUCCESS"] + config['condor_submit_extra_lines'])


                job_list.append(job)

            dagman.build_submit()

            jobsAndDagsRunning += (len(job_list)+1)
        
            pastfiles.append(file)




def inference(batch_size = config['far_config']['batch_size']): #dataSet_Q, dataSetName_Q,

    import tensorflow as tf
    from tensorflow.keras.models import load_model
    from tensorflow.config import threading

    threading.set_inter_op_parallelism_threads(1)
    threading.set_intra_op_parallelism_threads(1)

    from hermes import quiver as qv
    from hermes.aeriel.client import InferenceClient
    from hermes.aeriel.serve import serve


    logger.debug(f"PROCESSES hermes imports: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")


    logger.debug(f"PROCESSES at the start of inference: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

    
    # now load in our existing neural networks
    model1 = load_model(config['model1_path'])
    model2 = load_model(config['model2_path'])

    # let's make sure we're starting with a fresh repo
    repo_path = str("./.testhermes")
    try:
        shutil.rmtree(repo_path)
    except FileNotFoundError:
        pass
    repo = qv.ModelRepository(repo_path)

    # make a dummy model that we'll use to pass the strain
    # input tensor to both models
    input_s = tf.keras.Input(name="strain", shape=(1024, 3))
    output_s = tf.identity(input_s)
    input_model = tf.keras.Model(inputs=input_s, outputs=output_s)

    # create another model for the backend of the service
    # to combine the outputs from both models
    output1 = tf.keras.Input(name="output1", shape=(2,))
    output2 = tf.keras.Input(name="output2", shape=(2,))
    final_output = output1 * output2
    output_model = tf.keras.Model(inputs=[output1, output2], outputs=final_output)

    # add all these models to our model repo
    qv_model1 = repo.add("model1", platform=qv.Platform.SAVEDMODEL)
    qv_model2 = repo.add("model2", platform=qv.Platform.SAVEDMODEL)
    qv_input_model = repo.add("input-model", platform=qv.Platform.SAVEDMODEL)
    qv_output_model = repo.add("output-model", platform=qv.Platform.SAVEDMODEL)

    # add concurrent versions of models 1 and 2 to support our inference rate
    qv_model1.config.add_instance_group(count=2)
    qv_model2.config.add_instance_group(count=2)

    # now export the current versions of these models
    # to their corresponding entry in the model repo
    qv_model1.export_version(model1)
    qv_model2.export_version(model2)
    qv_input_model.export_version(input_model)
    qv_output_model.export_version(output_model)

    # finally, create an ensemble model which will pipe the outputs
    # of models into inputs of the next ones in the pipeline
    ensemble = repo.add("ensemble", platform=qv.Platform.ENSEMBLE)

    # this ensemble will have two inputs, one for the strain data
    # and one for the correlation data. The strain data will get fed
    # to our "input" model so that we can pipe the output of that
    # to the inputs of models 1 and 2
    ensemble.add_input(qv_input_model.inputs["strain"])
    ensemble.add_input(qv_model2.inputs["correlation"])

    # these lines will do the aforementioned routing of the
    # strain input model to the inputs of the two NNs
    ensemble.pipe(
        qv_input_model.outputs["tf.identity"],
        qv_model1.inputs["strain"],
    )
    ensemble.pipe(
        qv_input_model.outputs["tf.identity"],
        qv_model2.inputs["strain"],
    )

    # now route the outputs of these models to the
    # input of the output combiner model
    ensemble.pipe(
        qv_model1.outputs["main_output"],
        qv_output_model.inputs["output1"],
        key="model1_output",
    )
    ensemble.pipe(
        qv_model2.outputs["main_output"],
        qv_output_model.inputs["output2"],
        key="model2_output"
    )

    # finally, expose the output of this combiner model
    # as the output of the ensemble
    ensemble.add_output(qv_output_model.outputs["tf.math.multiply"])

    # export None to indicate that there's no NN we need
    # to export, but rather a DAG routing different NNs
    # to one another. The path of this DAG is contained
    # in the Triton config that hermes has built for you
    ensemble.export_version(None)

    logger.debug(f"PROCESSES after ensemble: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

    # set up a new directory just for our metrics
    metrics_dir = Path(".metrics")
    metrics_dir.mkdir(exist_ok=True)
    metrics_file = metrics_dir / "non-streaming_single-model.csv"

    # reset CUDA_VISIBLE_DEVICES so that we can expose the
    # correct GPUs to Triton
    os.environ["CUDA_VISIBLE_DEVICES"] = cuda_visible_devices



    # now serve a local Triton instance on GPU 0 using Singularity

    openingclientT0 = time.time()
    with serve(repo_path, image="hermes/tritonserver:22.12"
             , gpus=selectedGPUs, log_file="./server.log",server_args=["--allow-gpu-metrics false --grpc-port 8003 --http-thread-count 1 --model-load-thread-count 1"]) as instance:
        
        threading.set_inter_op_parallelism_threads(1)
        threading.set_intra_op_parallelism_threads(1)
        logger.debug(f"PROCESSES at the start of server: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")
        

        instance.wait(endpoint="localhost:8003")
        threading.set_inter_op_parallelism_threads(1)
        threading.set_intra_op_parallelism_threads(1)
        logger.debug(f"PROCESSES after instance waiting: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

        client = InferenceClient(
            "localhost:8003",
            model_name="ensemble",
            model_version=1,
            batch_size=batch_size,
        )
        # monitor = ServerMonitor(
        #     model_name="ensemble",
        #     ips="localhost",
        #     filename=metrics_file,
        #     model_version=1 ,
        #     name="monitor",
        #     rate=4
        # )
        logger.debug(f"PROCESSES at client creation: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

        logger.debug(f"OPENING CLIENT TIME: {time.time()-openingclientT0}")

        with client:#, monitor:

            already_used=[]

            while (1):
                
                fileList = list(file for file in dirlist(config["falseAlarmRates"]+"/temp/") 
                                if file not in already_used)

                if len(fileList)==0: 
                    time.sleep(1)
                    continue
                
                for file in fileList:
                
                    if file.split("_")[-1][:-4]=="0":
                        logger.warning(f"File with zero entries: {file}")
                        os.remove(config["falseAlarmRates"]+"/temp/"+file)
                        continue

                    t0datasetget = time.time()
                    
                    out = load_data_file(file)
                    if out is None: continue
                    out_name = file

                    # model parameters
                    NUM_IFOS = 3  # number of interferometers analyzed by our model
                    SAMPLE_RATE = 1  # rate at which input data to the model is sampled
                    KERNEL_LENGTH = 1  # length of the input to the model in seconds

                    # inference parameters
                    INFERENCE_DATA_LENGTH = len(out) # 8192 * 16  # amount of data to analyze at inference time
                    INFERENCE_SAMPLING_RATE = 1  # rate at which we'll sample input windows from the inference data
                    INFERENCE_RATE = 12000  # seconds of data we'll try to analyze per second

                    kernel_size = int(SAMPLE_RATE * KERNEL_LENGTH)
                    inference_stride = int(SAMPLE_RATE / INFERENCE_SAMPLING_RATE)
                    inference_data_size = int(SAMPLE_RATE * INFERENCE_DATA_LENGTH)

                    # define some parameters which apply to both data streams
                    num_kernels = inference_data_size // inference_stride
                    num_inferences = num_kernels // batch_size
                    kernels_per_second = INFERENCE_RATE * INFERENCE_SAMPLING_RATE
                    batches_per_second = kernels_per_second / batch_size

                    time_exportS0=time.time()

                    strainList      = out.exportData('strain', shape = (None, 1024, NUM_IFOS)).astype("float32")
                    #print('Exporting time STRAIN: ',time.time()-time_exportS0)
                    time_exportC0=time.time()

                    correlationList = out.exportData('correlation', shape = (None, 60, NUM_IFOS)).astype("float32")
                    #print('Exporting time CORRELATION: ',time.time()-time_exportC0)
                    time_exportG0=time.time()

                    gpsTimes = out.exportGPS()

                    #print('Exporting time GPS: ',time.time()-time_exportG0)
                    #print('Exporting time TOTAL: ',time.time()-time_exportS0)



                    inferencet0 = time.time()
                    results = np.array([])
                    for i in range(int(num_inferences)):
                        #print(i,'/',num_inferences)
                        start = i * 1 * batch_size
                        stop = start + 1 * batch_size
                        c_start = i * 1 * batch_size
                        c_stop = c_start + 1 * batch_size

                        kernel = {'strain' : strainList[ start : stop ]
                                    ,'correlation' : correlationList[ c_start : c_stop ]}
                        
                        client.infer(kernel, request_id=i)

                        # sleep to roughly maintain our inference rate
                        time.sleep(0.9 / batches_per_second)

                        if i < 5:
                            response_ = client.get()
                            trials = 1
                            while response_ is None and trials<5000:
                                response_ = client.get()

                                time.sleep(1e-2)
                                trials+=1
                                if trials>=5000: raise(Exception("Trials exceeded 5000."))

                            response, _, __ = response_
                            results = np.append(results,response[:,1])

                    for i in range(int(num_inferences)-5):
                        trials = 1
                        response_ = client.get()
                        while response_ is None:
                            time.sleep(1e-2)

                            trials+=1
                            response_ = client.get()
                            if trials>=5000: raise(Exception("Trials exceeded 5000."))

                        response, _, __ = response_
                        #print(i,'response type ', type(response) , response.shape ,trials)
                        results = np.append(results,response[:,1])

                    logger.info(f"Inference time: {time.time() - inferencet0} s/s")
                    logger.info(f"Throughput: {len(results)/(time.time() - inferencet0)} s/s")

                    #print(np.expand_dims(results,axis=1).shape, np.array(gpsTimes).shape,np.array(gpsTimes)[:len(results)].shape)
                    result=np.hstack((np.expand_dims(results,axis=1),np.array(gpsTimes)[:len(results)]))
                    logger.info(f"Size of the result {len(result)}")
                    #print(result)

                    name = '_'.join(out_name[:-4].split('_')[:2])+'_'+str(len(result))

                    if 'V' not in detectors:
                        if isinstance(detectors,str):
                            temp_detectors = detectors+'V'
                        else:
                            temp_detectors = detectors + ['V']
                    else:
                        temp_detectors = detectors

                    result_pd = pd.DataFrame(result ,columns = ['score']+list('GPS'+str(det) for det in temp_detectors))
                    logger.info(f"len before restriction: {len(result_pd)}")
                    result_pd = result_pd[result_pd['score'] >= config['far_config']['restriction'] ]
                    logger.info(f"len after restriction: {len(result_pd)}")

                    with open(config["falseAlarmRates"]+"/"+name+'.pkl', 'wb') as output:
                        pickle.dump(result_pd, output, 4)
                    
                    try:
                        os.remove(config["falseAlarmRates"]+"/temp/"+out_name)
                    except Exception as e:
                        logger.debug(f"removing exception: {e}")
                    logger.info(f"loop time: {time.time() - t0datasetget}")
                    
                    already_used.append(file)
                    
                    #qsys.stdout.flush()






if __name__ == "__main__":

    arguments = ["mode",
                "dataSet",
                "batchNumber"

    ]
    #Construct argument parser:
    parser = argparse.ArgumentParser()
    #[parser.add_argument(f"--{argument}") for argument in arguments]

    parser.add_argument('--mode')

    parser.add_argument('--dataSet', type=str, default=None)
    parser.add_argument('--batchNumber', type=int, default = 0)


    # Pass arguments:
    args = parser.parse_args()

    # Store arguments in dictionary:
    kwdict = {}
    for argument in arguments:
        kwdict[argument] = getattr(args, argument)




    mode = kwdict['mode']
    masterDirectory = config['masterDirectory']
    detectors = config['detectors'] #to get from config
    dataSet = kwdict['dataSet']

    batches =  config['far_config']['batches']
    batchNumber = kwdict['batchNumber']

    lags = config['far_config']['lags']
    selectedGPUs = config['far_config']['selectedGPUs']
    batch_size = config['far_config']['batch_size']
    parallelGenerations = config["far_config"]["parallelGenerations"]
    log_level = logging.getLevelName(config["log_level"])



    if config['far_config']['visible_gpu_devices']=="local":
        try:
            cuda_visible_devices = os.environ["CUDA_VISIBLE_DEVICES"] 
        except KeyError:
            print("No visible GPU devices detected, setting index to 0.")
            cuda_visible_devices = '0'
    else:
        cuda_visible_devices = config['far_config']["visible_gpu_devices"]
    



    # create console handler and set level to debug

    print(mode)
    if mode == 'generation':
        # # # Initialising logging
        # create logger
        logger = logging.getLogger("logger_for_continious_FAR")
        logger.setLevel(log_level)
        ch = logging.handlers.TimedRotatingFileHandler('log/continuousFAR-generation.log', when='H',interval=1, backupCount=1,)
        log_level = logging.getLevelName(config["log_level"])

        ch.setLevel(log_level)

        # create formatter
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
    elif mode == 'inference':
        # # # Initialising logging
        # create logger
        logger = logging.getLogger("logger_for_continious_FAR")
        logger.setLevel(log_level)
        ch = logging.handlers.TimedRotatingFileHandler('log/continuousFAR-inference.log', when='H',interval=1, backupCount=1,)
        log_level = logging.getLevelName(config["log_level"])

        ch.setLevel(log_level)

        # create formatter
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
    elif mode == 'sub_generation':
        pass
    else: 
        raise ValueError(f"Mode {mode} not found")

    
    if mode == 'generation':

        condorGeneration(batches, masterDirectory , lags) 

    elif mode == 'sub_generation':

        subGeneration(dataSet      
                  , batchNumber         
                  , batches     
                  , masterDirectory
                  , lags)
    
    elif mode == 'inference':

        inference()   



