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



masterDirectory = config['masterDirectory']
detectors = config['detectors'] #to get from config

batches =  config['far_config']['batches']

lags = config['far_config']['lags']
selectedGPUs = config['far_config']['selectedGPUs']
batch_size = config['far_config']['batch_size']
parallelGenerations = config["far_config"]["parallelGenerations"]


# # # Initialising logging

# create logger
logger = logging.getLogger("logger_for_manager")
logger.setLevel(logging.DEBUG)


# create console handler and set level to debug
ch = logging.handlers.TimedRotatingFileHandler('log/continuousFAR_test.log', when='H',interval=12, backupCount=1,)
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

logger.debug(f"PROCESSES after  logger: {subprocess.check_output(['pgrep','-c', '-w','-u','vasileios.skliris']) }")

import shutil
logger.debug(f"PROCESSES after  shutil: {subprocess.check_output(['pgrep','-c', '-w','-u','vasileios.skliris']) }")

import pickle

logger.debug(f"PROCESSES after  pickle: {subprocess.check_output(['pgrep','-c', '-w','-u','vasileios.skliris']) }")

from datetime import datetime

logger.debug(f"PROCESSES after  datetime: {subprocess.check_output(['pgrep','-c', '-w','-u','vasileios.skliris']) }")

from pathlib import Path

logger.debug(f"PROCESSES after  pathlib: {subprocess.check_output(['pgrep','-c', '-w','-u','vasileios.skliris']) }")

from pycondor import Job, Dagman

logger.debug(f"PROCESSES after  pycondor: {subprocess.check_output(['pgrep','-c', '-w','-u','vasileios.skliris']) }")

import numpy as np

logger.debug(f"PROCESSES after  numpy: {subprocess.check_output(['pgrep','-c', '-w','-u','vasileios.skliris']) }")

import pandas as pd

logger.debug(f"PROCESSES after  pandas: {subprocess.check_output(['pgrep','-c', '-w','-u','vasileios.skliris']) }")

import multiprocessing

logger.debug(f"PROCESSES after  multiprocessing: {subprocess.check_output(['pgrep','-c', '-w','-u','vasileios.skliris']) }")

from multiprocessing import Process , Queue , Pool

logger.debug(f"PROCESSES after  subprocess: {subprocess.check_output(['pgrep','-c', '-w','-u','vasileios.skliris']) }")





if config['far_config']['visible_gpu_devices']=="local":
    try:
        cuda_visible_devices = os.environ["CUDA_VISIBLE_DEVICES"] 
    except KeyError:
        cuda_visible_devices = '0'
else:
    cuda_visible_devices = config['far_config']["visible_gpu_devices"]

print("cuda_visible_devices ", cuda_visible_devices, ",type: ", type(cuda_visible_devices))

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"



logger.debug(f"PROCESSES hermes imports: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")



import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.config import threading

threading.set_inter_op_parallelism_threads(1)
threading.set_intra_op_parallelism_threads(1)

from hermes import quiver as qv
from hermes.aeriel.client import InferenceClient
from hermes.aeriel.serve import serve

logger.debug(f"PROCESSES after hermes imports: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")






def inference(batch_size = config['far_config']['batch_size']): #dataSet_Q, dataSetName_Q,
    

    
    logger.debug(f"PROCESSES at the start of inference: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

    
    # now load in our existing neural networks
    model1 = load_model(config['model1_path'])
    model2 = load_model(config['model2_path'])


    ###
    ### MODEL REFORMATING WITH HERMES.QUIVER
    ###

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

    # adding_tf_thread_limit()
    
    ###
    ### MODEL REFORMATING WITH HERMES.QUIVER - END
    ###
    
    logger.debug(f"PROCESSES after ensemble: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")





    # reset CUDA_VISIBLE_DEVICES so that we can expose the
    # correct GPUs to Triton
    os.environ["CUDA_VISIBLE_DEVICES"] = cuda_visible_devices

    # now serve a local Triton instance on GPU 0 using Singularity


    ###
    ### INTIALISING TRITON SERVER
    ###
    openingclientT0 = time.time()
    with serve(repo_path, image="hermes/tritonserver:22.12"
             , gpus=selectedGPUs
             , log_file="./server.log"
             ,server_args=["--allow-gpu-metrics false --grpc-port 8003 --http-thread-count 1 --model-load-thread-count 1"]) as instance:

        logger.debug(f"PROCESSES at the start of server: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

        instance.wait(endpoint="localhost:8003")

        logger.debug(f"PROCESSES after instance waiting: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

        time.sleep(5) # Just to make sure the threads are not from waiting

        logger.debug(f"PROCESSES after instance extra waiting: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")


    ###
    ### INTIALISING TRITON SERVER - END
    ###

        client = InferenceClient(
            "localhost:8003",
            model_name="ensemble",
            model_version=1,
            batch_size=batch_size,
        )
    
    return

        # monitor = ServerMonitor(
        #     model_name="ensemble",
        #     ips="localhost",
        #     filename=metrics_file,
        #     model_version=1 ,
        #     name="monitor",
        #     rate=4
        # )
        # logger.debug(f"PROCESSES at client creation: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

        # logger.debug(f"OPENING CLIENT TIME: {time.time()-openingclientT0}")

        # with client:#, monitor:

        #     already_used=[]

        #     while (1):
                
        #         fileList = list(file for file in dirlist(config["falseAlarmRates"]+"/temp/") 
        #                         if file not in already_used)

        #         if len(fileList)==0: 
        #             time.sleep(1)
        #             continue
                
        #         for file in fileList:
                
        #             if file.split("_")[-1][:-4]=="0":
        #                 logger.warning(f"File with zero entries: {file}")
        #                 os.remove(config["falseAlarmRates"]+"/temp/"+file)
        #                 continue
        #             t0datasetget = time.time()
                    

        #             out = load_data_file(file)
        #             if out is None: continue
        #             out_name = file

        #             # model parameters
        #             NUM_IFOS = 3  # number of interferometers analyzed by our model
        #             SAMPLE_RATE = 1  # rate at which input data to the model is sampled
        #             KERNEL_LENGTH = 1  # length of the input to the model in seconds

        #             # inference parameters
        #             INFERENCE_DATA_LENGTH = len(out) # 8192 * 16  # amount of data to analyze at inference time
        #             INFERENCE_SAMPLING_RATE = 1  # rate at which we'll sample input windows from the inference data
        #             INFERENCE_RATE = 12000  # seconds of data we'll try to analyze per second

        #             kernel_size = int(SAMPLE_RATE * KERNEL_LENGTH)
        #             inference_stride = int(SAMPLE_RATE / INFERENCE_SAMPLING_RATE)
        #             inference_data_size = int(SAMPLE_RATE * INFERENCE_DATA_LENGTH)

        #             # define some parameters which apply to both data streams
        #             num_kernels = inference_data_size // inference_stride
        #             num_inferences = num_kernels // batch_size
        #             kernels_per_second = INFERENCE_RATE * INFERENCE_SAMPLING_RATE
        #             batches_per_second = kernels_per_second / batch_size

        #             time_exportS0=time.time()

        #             strainList      = out.exportData('strain', shape = (None, 1024, NUM_IFOS)).astype("float32")
        #             #print('Exporting time STRAIN: ',time.time()-time_exportS0)
        #             time_exportC0=time.time()

        #             correlationList = out.exportData('correlation', shape = (None, 60, NUM_IFOS)).astype("float32")
        #             #print('Exporting time CORRELATION: ',time.time()-time_exportC0)
        #             time_exportG0=time.time()

        #             gpsTimes = out.exportGPS()

        #             #print('Exporting time GPS: ',time.time()-time_exportG0)
        #             #print('Exporting time TOTAL: ',time.time()-time_exportS0)



        #             inferencet0 = time.time()
        #             results = np.array([])
        #             for i in range(int(num_inferences)):
        #                 #print(i,'/',num_inferences)
        #                 start = i * 1 * batch_size
        #                 stop = start + 1 * batch_size
        #                 c_start = i * 1 * batch_size
        #                 c_stop = c_start + 1 * batch_size

        #                 kernel = {'strain' : strainList[ start : stop ]
        #                             ,'correlation' : correlationList[ c_start : c_stop ]}
                        
        #                 client.infer(kernel, request_id=i)

        #                 # sleep to roughly maintain our inference rate
        #                 time.sleep(0.9 / batches_per_second)

        #                 if i < 5:
        #                     response_ = client.get()
        #                     trials = 1
        #                     while response_ is None and trials<5000:
        #                         response_ = client.get()

        #                         time.sleep(1e-2)
        #                         trials+=1
        #                         if trials>=5000: raise(Exception("Trials exceeded 5000."))

        #                     response, _, __ = response_
        #                     logger.debug(f"{i} response type {type(response)} ,with shape {response.shape} and {trials} trials")
        #                     results = np.append(results,response[:,1])

        #             for i in range(int(num_inferences)-5):
        #                 trials = 1
        #                 response_ = client.get()
        #                 while response_ is None:
        #                     time.sleep(1e-2)
        #                     logger.debug(f"PROCESSES client.get {i}: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

        #                     trials+=1
        #                     response_ = client.get()
        #                     if trials>=5000: raise(Exception("Trials exceeded 5000."))

        #                 response, _, __ = response_
        #                 #print(i,'response type ', type(response) , response.shape ,trials)
        #                 results = np.append(results,response[:,1])

        #             logger.info(f"Inference time: {time.time() - inferencet0} s/s")
        #             logger.info(f"Throughput: {len(results)/(time.time() - inferencet0)} s/s")

        #             #print(np.expand_dims(results,axis=1).shape, np.array(gpsTimes).shape,np.array(gpsTimes)[:len(results)].shape)
        #             result=np.hstack((np.expand_dims(results,axis=1),np.array(gpsTimes)[:len(results)]))
        #             logger.info(f"Size of the result {len(result)}")
        #             #print(result)

        #             name = '_'.join(out_name[:-4].split('_')[:2])+'_'+str(len(result))

        #             if 'V' not in detectors:
        #                 if isinstance(detectors,str):
        #                     temp_detectors = detectors+'V'
        #                 else:
        #                     temp_detectors = detectors + ['V']
        #             else:
        #                 temp_detectors = detectors

        #             result_pd = pd.DataFrame(result ,columns = ['score']+list('GPS'+str(det) for det in temp_detectors))
        #             logger.info(f"len before restriction: {len(result_pd)}")
        #             result_pd = result_pd[result_pd['score'] >= config['far_config']['restriction'] ]
        #             logger.info(f"len after restriction: {len(result_pd)}")

        #             with open(config["falseAlarmRates"]+"/"+name+'.pkl', 'wb') as output:
        #                 pickle.dump(result_pd, output, 4)
                    
        #             try:
        #                 os.remove(config["falseAlarmRates"]+"/temp/"+out_name)
        #             except Exception as e:
        #                 logger.debug(f"removing exception: {e}")
        #             logger.info(f"loop time: {time.time() - t0datasetget}")
                    
        #             already_used.append(file)
                    
        #             sys.stdout.flush()




def adding_tf_thread_limit():

    config_list = ['.testhermes/model1/config.pbtxt'
                ,'.testhermes/ensemble/config.pbtxt'
                ,'.testhermes/model2/config.pbtxt'
                ,'.testhermes/output-model/config.pbtxt'
                ,'.testhermes/input-model/config.pbtxt']

    for cnf in config_list:
        with open("/home/vasileios.skliris/mysearch/"+cnf,"a+") as file:	
            file.write("parameters: {\n ")
            file.write("  key: \"TF_NUM_INTRA_THREADS\"\n ")
            file.write("  value: {\n ")
            file.write("    string_value:\"2\"\n ")
            file.write("  }\n ")
            file.write("}\n ")


if __name__ == "__main__":

        inference()   