#! /usr/bin/env python
import subprocess, argparse, os, shutil, gwdatafind
import time, sys ,pickle, json, datetime, math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import astropy_healpix as ah
import healpy as hp

from gwpy.timeseries import TimeSeries
from ligo.skymap.io import fits
from ligo.skymap.moc import nest2uniq 
from mly.skymap_utils import skymap_plugin, containment_region
from pycondor import Job, Dagman

from mly.datatools import DataPod
from mly.validators import Validator
from mly.createFileSystem import createFileSysem
from mly.plugins import PlugIn
from .search_functions import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["GWDATAFIND_SERVER"]="datafind.ldas.cit:80"
os.environ["DEFAULT_SEGMENT_SERVER"]="http://segments.ldas.cit"

from tensorflow.keras.models import load_model
from tensorflow.config import threading

threading.set_inter_op_parallelism_threads(1)
threading.set_intra_op_parallelism_threads(1)

which_python = str(subprocess.check_output(['which','python']))[2:-3]

def main(**kwargs):
    """ Main functionality of the search script. Given the arguments
    provided it conducts a real time search on gravitational wave data. It
    uses a predefined given model for iference.

    Parameters
    ----------

    detectors: {'HL','HLV'}
        It specifies which detectors to use to conduct the search. If 'HL' is
        chosen, it generates gaussian noise that follows Virgo background(x32),
        to provide nominal data for Virgo.

    channels: {'NOISE','MDC'}
        It specifies which channel to use for the search.
        'NOISE' represents a predefined set of channels without injections.
        'MDC' represents a predifned set of channels with injections for the MDC

    threshold : float
        The minimum score for witch the search will issue a trigger event.

    output_directory: str (path, optional)
        The path of the directory where the search will save the output of the model
        for each instance processed. If not specified it doesn't save the outputs.

    trigger_directory: str (path, optional)
        The path of the directory where the search will save the output of the model
        for each instance that was above the threshold value. If not specified
        it doesn't save anything. It is important to have this directory specified if
        you want to send triggers to GraceDB (using mly_to_grace.py).

    trigger_destination: {'test, 'playground', 'dev1', None}
        The GraceDB domain for the triggers to be uploaded. Each option represent
        a corresponding url. If equals to None, it will not issue an GraceDB event.
        
    splitter: list
        A way to split the search into different parallel jobs. The list must have
        two parameters. The first is the amount of scripts this search is split into.
        The second is which part of the split this function will run. For example a 
        splitter value of [4,1] means that we will splitted the search into 4 scripts
        where each script processes every other 4 seconds, and that this function will
        run the every 4 plus 1 seconds part. For a full search we will have to run the
        same function for splitter values of: [4,0], [4,1], [4,2], [4,3]. If not 
        specified it is equal to [1,0]
        
    skymap: bool
        If True it will allow the creation of a skymap whenever it issues events. This
        is passed to another function 'mly_to_grace'.
    
    time_reference: float
        A unix time reference so that should be the same among different functions when
        used splitter. It is suggested to use `unixtime=$(date +%s)` at the beggining of
        the script and pass `$unixtime` as time_reference.    
        
    fileSystem: str/path
        A path to a valid file system directory. A valid file system
        directory needs to have subfolders with the initials of all
        detectors used and a 'temp' file that also includes subfolders
        with initials of all detectors. This is used for the calculation
        of continues false alarm rates. If not specified, it will not save data 
        into the file system.
        
    bufferDirectory: str/path
        A directory path where it will save the buffer data around each second
        to be used for the calculation of efficiencies. If not specified, it 
        will not save the buffer data.
        
    Note
    ----

    This function doesn't return anything. It runs until it is stoped or until it
    raises an Exception.
    """
    
    with open('config.json') as json_file:
        config = json.load(json_file)
    
    config = { **config , **kwargs }
    # # # Command line arguments processing
    
    # Check arguments and set values in config dict:

    print(config["frames_directory"])
    
    check_functions = [
        checkDetectorArguments, 
        checkChannelArguments, 
        checkThresholdArguments,
        checkSkymapArguments,

        
        check_segment_list,
        stackVirgo, 
        check_filename_prefix
    ]
    
    for function in check_functions:
        config = function(config)

    # # # Setup parameters for the models
    
    subconfig = config.copy()
    for key in ['detectors','fs','duration','restriction','prefixes','frames','channels','size']:
        subconfig.pop(key,None)
    
    detectors = config["detectors"]
    prefix = config['prefix']
    frames_dir = config['frames_directory']
    channels = config['channels']
    segment_list = config['segment_list']

    accounting_group_user = config['accounting_group_user']
    accounting_group = config['accounting_group']

    if kwargs['mode'] == 'condor':

        error = './condor/error'
        output = './condor/output'
        log = './condor/log'
        submit = './condor/submit'

        dagman = Dagman(name=config['path'].split('/')[-1]+'_'+'offline_search',submit=submit)

        # # # Main Loop

        
        for i, segment in enumerate(segment_list):

            start_gps = int(segment[0])
            segment_size = int(segment[1] - segment[0])
            file_name_output = f"{start_gps + (config['required_buffer'] - config['duration'])/2 }-{start_gps + segment_size -(config['required_buffer'] - config['duration'])/2 }_{segment_size}"

            jobname = file_name_output.replace('.','_')+"_"+str(i) 


            output_file_name = f"{file_name_output}.pkl"

            if config['prefix']=='noprefix':
                master_directory_input_files = ""
            else:
                master_directory_input_files = "YOU NEED TO SORT THIS CASE OUT FOR CONDOR"
    
            thearguments = ("-m mly_pipeline.offline_search --mode job "+"--i "+str(i))

            print(f"{which_python}{thearguments}")

            job = Job(name = jobname
                    ,executable = which_python
                    ,arguments = thearguments
                    ,submit=submit
                    ,error=error
                    ,output=output
                    ,log=log
                    ,getenv=True
                    ,dag=dagman
                    ,retry=5
                    ,requirements=" && ".join(config['condor_submit_requirements'])
                    ,extra_lines=["accounting_group_user="+accounting_group_user
                                    ,"accounting_group="+accounting_group
                                    ,f"transfer_input_files    = config.json{master_directory_input_files},{config['model1_path']},{config['model2_path']},{config['farfile']}/FARfile_interpolation_inverse.pkl,{config['farfile']}/FARfile_interpolation.pkl"
                                    ,f"transfer_output_files   = {output_file_name},trigger_directory_{i}"
                                    ,f"transfer_output_remaps = \"{output_file_name} = {config['output_directory']}/{output_file_name};trigger_directory_{i} = {config['trigger_directory']}/trigger_directory_{i}\""
                                    ,"should_transfer_files   = YES"
                                    ,"success_exit_code = 0"
                                    ,"when_to_transfer_output = ON_SUCCESS"] + config['condor_submit_extra_lines'])


        dagman.build_submit()
        with open('monitor.log', 'a') as file:
            # Write the line to the file
            line_to_add = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Offline search - Number of jobs submited: {len(segment_list)}\n"
            file.write(line_to_add)


    elif kwargs['mode']=='job':

        print(os.listdir('.'))

        i = int(kwargs['i'])
        
        os.mkdir(f"trigger_directory_{i}")

        np.random.seed(config['seed'] + i)

        segment = segment_list[i]

        # Loading models
        model1 = load_model(config['model1_path'].split('/')[-1]) # Load coincidence model
        model2 = load_model(config['model2_path'].split('/')[-1]) # Load coherence model

        # This parameter format is used in inference
        models = [
            [model1 , model2],
            [["strain"], ["strain","correlation"]]
            ]      
        
        # Mapping keeps consistent the categorical format
        mapping = 2 * [{
            "noise": [1, 0],
            "signal": [0, 1]
        }]


        # # # Main Loop

        # THE SEGMENTS GUARANTEE THAT THE TIMES ARE OF COINSIDECE

        background_data = []

        start_gps = int(segment[0])
        segment_size = int(segment[1] - segment[0])
        file_name_output = f"{start_gps + (config['required_buffer'] - config['duration'])/2 }-{start_gps + segment_size -(config['required_buffer'] - config['duration'])/2 }_{segment_size}"
        for det in detectors:
            
            if config['prefix']=='noprefix':

                print('seg',det,config['frames_directory'][det],segment[0],segment[1])
                conn=gwdatafind.connect()
                urls=conn.find_urls(det
                                , config['frames_directory'][det]
                                , segment[0]
                                , segment[1])
                                
                data = TimeSeries.read(urls
                                , config['channels'][det]
                                , start = segment[0]
                                , end = segment[1]
                                ).resample(config["fs"]).astype('float64').value

                print("background data ",det,data.shape)
                background_data.append(data)
                                       
            else:

            
                data = TimeSeries.read([frames_dir[det]+ file  for file in os.listdir(frames_dir[det]) if det+'-'+det+"1" in file]
                                        , channels[det]
                                        , start = segment_list[i][0]
                                        , end = segment_list[i][1])
                data = data.resample(config["fs"]).value
                print("background data ",det,data.shape)
                background_data.append(data)
            


        mly_output_list = []
        
        threshold = far("FARfile_interpolation_inverse.pkl"
                            ,config['far_config']['threshold'], inverse = True)
        
        for j in range(int(segment_size/config["duration"] - (config["required_buffer"] - config["duration"]) )):

            gps_time = start_gps + j

            strain_data_j = np.array(background_data)[: , j*config["fs"] : (j+config["required_buffer"])*config["fs"] ]
            
            zeros=len(np.where(strain_data_j==0.0)[0]) # weidly it returns array in a tuple
            if zeros>=0.10*config["required_buffer"]*config["fs"]:
                print(f"Error! Data has many zeros, skipped to the next.")
                continue

            
            buffer_pod = DataPod(np.array(background_data)[: , j*config["fs"] : (j+config["required_buffer"])*config["fs"] ],
                        detectors = config["detectors"], 
                        fs = config["fs"], 
                        gps = len(config["detectors"])*[float(gps_time)] 
                            )

            try:
                result, thepod = Validator.falseAlarmTest(
                                                models = models,
                                                duration = config["duration"],
                                                fs =  config["fs"],
                                                size = 1,
                                                detectors = config["detectors"],
                                                backgroundType = "real",
                                                noiseSourceFile = buffer_pod,
                                                windowSize = config["required_buffer"],          
                                                mapping = mapping,
                                                strides = None,
                                                plugins = ["correlation_30",'psd','uwstrain'],
                                                restriction = None,
                                                podreturn = True,
                                                **subconfig
                                            )
            except Exception as e:
                raise(e)
                continue
            # Change format of detector name to include 1 (ex. H->H1)
            ifos = ",".join([f"{detector}1" for detector in config["detectors"]])
            instance_start_time = result["GPSH"][0]
            # Create mly_output dictionary, GraceDB event file basis
            mly_output = {
                "gpstime": result["GPSH"][0],
                "far": far("FARfile_interpolation.pkl"
                                            ,result["total"][0], inverse = False),
                "ifos": ifos,
                "channels": list(config['channels'][det] for det in config['detectors']),

                "scores": {
                    "coincidence": result["scores1"][0],
                    "coherency": result["scores2"][0],
                    "combined": result["total"][0]
                },
                "instance_start_time": instance_start_time

            }


            # Internal latency, from GPS selection to scores.

            # # # Follow up

            # Create string of joined detector names
            detectors = "".join(config["detectors"])

            
            # If result us above threshold, do all even relate actions 

            # Perform time- and frequency-domain parameter estimation.
            # It adds parameter estimation to events.

            mly_output = runTimeFrequencyParameterEstimation(thepod,  mly_output)

            if mly_output["scores"]["combined"] >= threshold:
                
                mly_output['trigger']=True
                
                # Making the directory of the trigger
                eventDirectory = "T_"+str(mly_output['gpstime'])

                if os.path.exists(f"trigger_directory_{i}/{eventDirectory}"):
                    shutil.rmtree(f"trigger_directory_{i}/{eventDirectory}")
                
                os.mkdir(f"trigger_directory_{i}/{eventDirectory}")


                # Saving trigger into the trigger_directory
                with open(f"trigger_directory_{i}/{eventDirectory}/T_{mly_output['gpstime']}_{detectors}.json", "w") as mly_json:
                    json.dump(mly_output, mly_json,indent=4)
                    mly_json.close()

                # Saving trigger DataPod into the trigger_directory
                with open(f"trigger_directory_{i}/{eventDirectory}/T_{mly_output['gpstime']}_{detectors}.pkl", 'wb') as mly_pkl:
                    pickle.dump(thepod, mly_pkl, 4)
                    
                # Saving trigger background DataPod into the trigger_directory
                with open(f"trigger_directory_{i}/{eventDirectory}/T_{mly_output['gpstime']}_{detectors}_buffer.pkl", 'wb') as mly_pkl:
                    pickle.dump(buffer_pod, mly_pkl, 4)

                # Creating the strain plot
                thepod.plot(type_="strain")
                plt.savefig(f"trigger_directory_{i}/{eventDirectory}/T_{mly_output['gpstime']}_{detectors}_strain.png")
                plt.clf()
                # Creating the correlation plot
                thepod.plot(type_="correlation")
                plt.savefig(
                    f"trigger_directory_{i}/{eventDirectory}/T_{mly_output['gpstime']}_{detectors}_correlation.png")
                plt.clf()
                # Creating the tf_map plot
                thepod.plot('tf_map')
                plt.savefig(
                    f"trigger_directory_{i}/{eventDirectory}/T_{mly_output['gpstime']}_{detectors}_tfmap.png")

                if config['skymap']:

                    if ('V' in thepod.detectors) and ('V' not in config['detectors']):
                        thepod.strain = thepod.strain[:2]
                        thepod.detectors = thepod.detectors[:2]
                        thepod.gps = thepod.gps[:2]
                        thepod.psd = thepod.psd[:2]
                        thepod.uwstrain = thepod.uwstrain[:2]

                    # Create skymap plugin:
                    thepod.addPlugIn(skymap_plugin(alpha = config['skymap']['alpha']
                                  ,beta = config['skymap']['beta']
                                  ,sigma =config['skymap']['sigma']
                                  ,nside = config['skymap']['nside']
                                  ,window_parameter = (thepod.PE['start_time'], thepod.PE['end_time']
                                                     ,config['skymap']['ramp_duration'] 
                                                     ,config['skymap']['ramp_center']
                                                     ,config['skymap']['duration_limit']
                                                     ,thepod.PE['start_frequency'], thepod.PE['end_frequency'])))
                    
                    skymap_path = f"trigger_directory_{i}/{eventDirectory}/mly.multiorder.fits"
                    
                    skymap_prob = thepod.sky_map[0]

                    order = int(math.log2(config['skymap']['nside']))
                    npix = ah.nside_to_npix(config['skymap']['nside'])

                    uniq = nest2uniq(np.uint8(order), np.arange(npix))
                    probdensity = skymap_prob / hp.nside2pixarea(config['skymap']['nside'])

                    moc_data = np.rec.fromarrays(
                        [uniq, probdensity], names=['UNIQ', 'PROBDENSITY'])

                    with open(skymap_path, "w") as f:
                        fits.write_sky_map( skymap_path, moc_data)
                    
                    thepod.plot('sky_map')
                    plt.savefig(
                        f"trigger_directory_{i}/{eventDirectory}/T_{mly_output['gpstime']}_{detectors}_skymap.png")

                    summary_plot(thepod,config,save_path= f"trigger_directory_{i}/{eventDirectory}/T_{mly_output['gpstime']}_{detectors}_summary.png")

            else:

                mly_output['trigger']=False

            mly_output_list.append(mly_output)
            sys.stdout.flush()


        tempFrame = pd.DataFrame(columns = ['gpstime','far','ifos'
                                                    ,'coincidence','coherency'
                                                    ,'combined','central_time','duration','central_freq','bandwidth'
                                                    ,'trigger'])


        # A check value to make sure we add all the json files.
        frameSizeCheck = len(mly_output_list) 

        # Adding all the events in json format to the tempFrame
        for file in mly_output_list:

            p=file.copy()
                
            for k in list(p['scores'].keys()):
                p[k]=p['scores'][k]

            del(p['scores'])  

            for k in list(p.keys()):
                p[k]=[p[k]]


            tempFrame=pd.concat([tempFrame, pd.DataFrame.from_dict(p)]
                                    ,ignore_index=True)

                # Reseting index and sorting by GPS time
            tempFrame = tempFrame.sort_values(by="gpstime").reset_index(drop=True)
            tempFrame = tempFrame[['gpstime','far','ifos'
                                                    ,'coincidence','coherency'
                                                    ,'combined','central_time','duration','central_freq','bandwidth'
                                                    ,'trigger']]


        with open(f"{file_name_output}.pkl", 'wb') as output:
            pickle.dump(tempFrame, output, 4)


        print("f{file_name_output}.pkl saved")
        print("Size of file and interval ",frameSizeCheck, segment_size)

        print("Analysis complete ",str(1+i),"/",len(file_name_output))

    
    elif kwargs['mode']=='set_file_system':

        np.random.seed(config['seed'] - 1)

        createFileSysem(duration=config['duration']
                         ,fs=config['fs']
                         ,detectors=detectors
                         ,dates = segment_list
                         ,windowSize = 16
                         ,backgroundType='real'
                         ,masterDirectory=config['masterDirectory']
                         ,frames=config['frames_directory'] 
                         ,channels=config['channels']
                         ,observingFlags = config['active_flags']
                         ,accounting_group_user = config['accounting_group_user']
                         ,accounting_group = config['accounting_group']
                         ,dagman_name = f"{config['path'].split('/')[-1]}_createFileSystem"

        )




if __name__ == "__main__":

    # # # Managing arguments
    # 
    # List of arguments to pass:
    arguments = ['mode','i']

    #Construct argument parser:
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', default="condor")
    parser.add_argument('--i', default = None)
    # Pass arguments
    args = parser.parse_args()

    # Store arguments in dictionary:
    kwargs = {}
    for argument in arguments:
        kwargs[argument] = getattr(args, argument)

    kwargs["splitter"] = None
    kwargs["time_reference"] = 0

    main(**kwargs)
