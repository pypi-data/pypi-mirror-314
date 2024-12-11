import json, pickle, sys, time, os, argparse

# Scipy and numpy env parameters that limit the threads
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import numpy             as np
import matplotlib.pyplot as plt

from os                import path
from math              import ceil
from gwpy.timeseries   import TimeSeries, StateVector, TimeSeriesDict
from gwpy.segments     import SegmentList, Segment
from gwpy.time         import to_gps, from_gps, tconvert
from scipy.interpolate import interp1d
from scipy             import signal
from lal               import gpstime
from dqsegdb2.query    import query_segments

from ast               import literal_eval as make_tuple

from mly.datatools import DataPod
from mly.validators import Validator
from mly.plugins import *




def checkDetectorArguments(config):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary with error checked detector parameters.
        
       Parameters
       ----------
       
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------
    
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    """
    
    #Detector options: 
    allowed_detectors = "HLV"
    default_detectors = "HLV"
           
    # Check detector arguments:    
    if config["detectors"] == None: 
        # Output warning and set detectors to default if no detectors inputted.
        print(f"Warning! No detectors inputted. Using default detector values: \
 {default_detectors}")
        config["detectors"] = list(default_detectors)     
    elif not all((det in allowed_detectors) for det in config["detectors"] ):
        # Output warning and set detectors to default if no detectors inputted
        # not allowed.
        print(f"Warning! No invalid detectors inputted: {config['detectors']} \
        only {allowed_detectors} allowed. Using default detector values: \
        {default_detectors}")
        config["detectors"] = list(default_detectors)
    else:
        # Set config to list of inputted detectors if inputted and valid.
        config["detectors"] = list(config["detectors"])
    
    return config

def checkChannelArguments(config):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary with error checked channel parameters.
       
       Parameters
       ----------

       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------

       config: dict
           Dictionary containing program runtime variables
    """
    # Check if channels is a dictionary
    if not isinstance(config['channels'],dict):
        raise TypeError("Channel must be a dictionary, with keys the initials of the detectors.")
    # Check if channels has all the detectors
    # if not config["detectors"]==list(config['channels'].keys()):
    #     raise ValueError("Missmach of the length of detectors and the number of channels")

    return config

def checkThresholdArguments(config):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary with error checked threshold parameters.
       
       Parameters
       ----------

       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------

       config: dict
           Dictionary containing program runtime variables
    """
    
    # Check threshold arguments:    
    if config["far_config"]["threshold"] != None:
        threshold = float(config["far_config"]["threshold"])
        if threshold <= 0:
            # Raise error if threshold is not above 0.
            raise ValueError(f"Error! Inputted threshold {threshold} must be \
 greater than zero.");
        elif not isinstance(threshold,(int,float)):
            # Raise error if threshold is not float or integer.
            raise ValueError(f"Error! Inputted threshold {threshold} must be \
 float or integer.");
        else: 
            # Set config threshold to threshold if present, a valid type and
            # above 0.
            config["far_config"]["threshold"] = threshold
    else:
        # Raise error if no threshold inputted.
        raise ValueError(f"Error! No threshold inputted. Please input a threshold \
 value using the following syntax when running the command --threshold <value>.");
    
    return config

def checkOutputDirectoryArguments(config):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary with error checked output directory parameters.
       
       Parameters
       ----------

       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------

       config: dict
           Dictionary containing program runtime variables
    """
    
    # Check output directory:
    if config["output_directory"] != None:
        if not os.path.isdir(config["output_directory"]):
            # Raise error if directory does not exist:
            raise FileNotFoundError(f"{config['output_directory']} is not a valid path.")
    
        if config["output_directory"][-1] != "/":
            config["output_directory"] += "/"
    else:
        # If output directory does not exist set config output_directory to None:
        config["output_directory"] = None
    
    return config

def checkTriggerDirectoryArguments(config):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary with error checked trigger directory parameters.
       
       Parameters
       ----------

       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------

       config: dict
           Dictionary containing program runtime variables
    """
    
   #Check trigger directory:
    if config["trigger_directory"] != None:
        if os.path.isdir(config["trigger_directory"]):
            # Set config trigger directory if trigger directory argument present and directory
            # exists.
            config["trigger_directory"] = config["trigger_directory"]
        else:
            # Raise error if trigger directory does not exist:
            raise FileNotFoundError(f"{config['trigger_directory']} is not a valid path")
    else:
        # Raiser error if no trigger directory inputted:
        raise FileNotFoundError("You need to specify a directory where the triggers \
 will be saved using the following syntax when running the command --trigger_directory <value>.")
    
    return config


def checktriggerDestinationArguments(config):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary with error checked trigger_destination parameters.
       
       Parameters
       ----------

       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------

       config: dict
           Dictionary containing program runtime variables
    """

    if config['trigger_destination']!=None:

        if config['trigger_destination'] in ['test','playground','dev1']:
            url = "https://gracedb-"+config['trigger_destination']+".ligo.org/api"
            print("Current trigger_destination url is :"+url)
                
            config['trigger_destination'] = url

        elif config['trigger_destination'] == 'online':
            url = "https://gracedb.ligo.org/api"
            print("Current trigger_destination url is :"+url)
        else:
            url = config['trigger_destination']
            print("Current trigger_destination url is :"+url)
            print("WARNING, NO STANDAR PRESET OF URL HAS BEEN USED")

    else:
        
        config['trigger_destination'] = None
    
    return config

def checkSplitArguments(config):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary with error checked splitter parameters.
       
       Parameters
       ----------

       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------
           
       config: dict
           Dictionary containing program runtime variables
    """
    
    #Check split value:
    if config["splitter"]!=None:
        try:
            config["splitter"] = make_tuple(config["splitter"])
        except:
            #Raise exception if splitter cannot be made into tuple set splitter to None.
            raise ValueError(f"Error! splitter value {config['splitter']} cannot be \ made into tuple.")
        if not isinstance(config['splitter'],(list,tuple)):
            config["splitter"] = None
        elif config["splitter"][1]>=0:
            config["num_scripts"]  = config['splitter'][0]
            config["script_index"] = config['splitter'][1]
        else:
            raise ValueError("splitter must be a list or a tuple of two values. "
                             "The first is the number of scripts to split the search"
                             " and the second is the label (each for each script) of the individual scripts")                      
    else:
        config["num_scripts"]  = 1 
        config["script_index"] = 1    
    
    return config

def checkTimeReferenceArguments(config):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary with error checked output directory parameters.
       
       Parameters
       ----------
       
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------
    
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    """
    
    # Check output directory:
    if config['time_reference'] == None and "OFFLINE" not in config["search_mode"]:
        
        raise ValueError("You need a common reference of unix time for the splitter"
                        " otherwize you might have overlapin analysis")
    elif isinstance(config['time_reference'],(str,int)):
        
        config["time_reference"] = int(config['time_reference'])-315964782

    elif "OFFLINE" not in config["search_mode"]:

        raise ValueError("time_reference must be the current unix time in numerical or string format")

    return config


def checkSkymapArguments(config):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary with error checked output directory parameters.
       
       Parameters
       ----------
       
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------
    
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    """
    
    # Check output directory:
    if not isinstance(config['skymap'],dict):
        raise TypeError("skymap must be dictionary with the entries for (alpha, beta, sigma, nside) or an empty dictionary")
    
    if config['skymap']=={}:
        config['skymap']=False

    else:

        return config

    
def checkMasterDirectoryArguments(config):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary with error checked output directory parameters.
       
       Parameters
       ----------
       
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------
    
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    """
    # Check output directory:
    if config['masterDirectory']==None:
        pass
    elif isinstance(config['masterDirectory'],str) and os.path.isdir(config['masterDirectory']):
        if config['masterDirectory'][-1]!='/': config['masterDirectory']+='/'
    elif "OFFLINE" not in config["search_mode"]:
        raise ValueError("The masterDirectory is not properly defined: "+config['masterDirectory'])

    return config


def checkBufferDirectoryArguments(config):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary with error checked output directory parameters.
       
       Parameters
       ----------
       
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------
    
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    """
    # Check buffer directory:
    if config["bufferDirectory"] != None:
        if os.path.isdir(config["bufferDirectory"]):
            # Set config buffer directory if buffer directory argument present and directory
            # exists.
            if config["bufferDirectory"][-1]!='/':
                config["bufferDirectory"]+= "/"
            config["bufferDirectory"] = config["bufferDirectory"]
        elif "OFFLINE" not in config["search_mode"]:
            # Raise error if directory does not exist:
            raise FileNotFoundError(f"{config['bufferDirectory']} is not a valid path.")
    else:
        # If output directory does not exist set config output_directory to None:
        config["bufferDirectory"] = None
    
    return config
    


def check_segment_list(config):

    # If this is not an offline search, segment_list parameter is not used.
    if "OFFLINE" not in config["search_mode"]:
        return config

    segment_list = config['segment_list']
    # If there is a segment definer file in a txt format specified.
    if isinstance(segment_list,str):

        segment_list = list(Segment(el[0],el[1]) for el in np.loadtxt( segment_list , delimiter = ','))
        segment_list = SegmentList( segment_list).coalesce()

        config = find_default_segments(config, interval = [segment_list[0][0], segment_list[-1][1]])
    # If there is an interval defined to look for available segments.
    elif isinstance(segment_list,list) and all(isinstance(el,(int,float)) for el in segment_list ) and len(segment_list)==2:
        # Funtion that looks for coinsident segments.
        config = find_default_segments(config)
        print("looked for default segments")

        segment_list = config['segment_list']

    # If the segment list is already proccessed and it is a list of segments.
    # Usually this state is the product of the two previous checks.
    if isinstance(segment_list,list) and len(segment_list)!=0:
        segment_list = SegmentList( segment_list).coalesce()

        segment_list_cleared = []
        for i, seg in enumerate(segment_list):
            if (seg[1]-seg[0]) > config["required_buffer"]: 
                segment_list_cleared.append(seg)
        segment_list_cleared = SegmentList(segment_list_cleared).coalesce()

        config['segment_list'] = segment_list_cleared

    else:
        raise ValueError("No segment list provided", config['segment_list'])


    # Breaking up segments that are bigger than the max_continuous_segment
    segment_list_capped = []
    for segment in segment_list_cleared:
        segment_size = segment[1] - segment[0]

        if segment_size >  config['max_continuous_segment'] + config["required_buffer"] - config["duration"]:
            # Number of segments-1 to brake the original segment
            breaks = int(segment_size /  ( config['max_continuous_segment'] + config["required_buffer"] - config["duration"]) )
            for k in range(breaks):
                segment_list_capped.append(Segment(
                                     segment[0]+k* config['max_continuous_segment']
                                    ,segment[0]+(k+1)* config['max_continuous_segment'] + config["required_buffer"] - config["duration"]))
            # The remaining segment without window correction must also be

            remnant_size = segment[1]-(segment[0]+(k+1)* config['max_continuous_segment'] + config["required_buffer"] - config["duration"])
            
            if remnant_size >= config["required_buffer"]:
                segment_list_capped.append(Segment(segment[0]+(k+1)* config['max_continuous_segment']
                                                  ,segment[0]+(k+1)* config['max_continuous_segment']+remnant_size))
        elif config["required_buffer"] - config["duration"] <= segment_size < config['max_continuous_segment']:

            segment_list_capped.append(Segment(segment[0] ,segment[1]))
    
    # Replaces the segment_list parameter with the finalised and organised segments.
    config['segment_list'] = segment_list_capped 

    return config

        
        

    
def checkArguments(config):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary. Includes error checking.
       
       Parameters
       ----------
       
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------
    
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    """
    
    check_functions = [
        checkDetectorArguments, 
        checkChannelArguments, 
        checkThresholdArguments,
        checkOutputDirectoryArguments,
        checkTriggerDirectoryArguments,
        checktriggerDestinationArguments,
        checkSplitArguments,
        checkTimeReferenceArguments,
        checkSkymapArguments,
        checkMasterDirectoryArguments,
        checkBufferDirectoryArguments,
        
        check_segment_list,
        stackVirgo, 
        check_filename_prefix
    ]
    
    for function in check_functions:
        config = function(config)

    return config 

def stackVirgo(config): 
    
    """If virgo detector is not present adds new pure noise channel in its place.
       
       Parameters
       ----------
       
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    
       Returns
       -------
    
       config: dict 
           Dictionary containing comand line arguments
           
       config: dict
           Dictionary containing program runtime variables
    """
    
    #If in HL mode add white noise as virgo channel:
    if "V" not in config["detectors"]:
        
        # del config["frames_directory"]['V']
        # del config["channels"]['V']

        config["stackDetectorDict"] = { 
            "duration": config["duration"],
            "fs": config["fs"],
            "detectors" : "V",
            "backgroundType" :"optimal",
            "PSDm":{"V": 32}
        }
        
    return config 

def check_filename_prefix(config):
    # Issue to sort out for .read and .get methods
    if "/" not in list(config['frames_directory'].values())[0]:
        config['prefix'] = 'noprefix'
        return config
        
    prefix_name_list = []
    for k in list(config['frames_directory'].keys()):
        frame_files = os.listdir(config['frames_directory'][k])
        prefix_name_list.append(frame_files[0].split("-1")[0][5:]+"-")
    
    if all( name == prefix_name_list[0] for name in prefix_name_list):
        config['prefix'] = prefix_name_list[0]
        return config
    else:
        raise ValueError("Prefix names are not consistent in frames")


    
def readFrameFile(frames, channel, state_vector_channel , start_gps = None, end_gps = None, wait = 0.5, timeout = 5, count=0, logger = None):
    
    """A wrapper function for TimeSeries.read from gwpy. It reads the channels
    from the frames provided. If the reading fails for any reason it 
    waits <wait> time and tries again, up to <timeout> times.
    
    Parameters
    ----------
    
    frames : str/list of strings
        A the paths to all the frame files to be read. When reading more
        than one frame file, make sure they are continuous and they have
        not been through any prossessing beforhand.
        
    channel: str 
        The channel to read from the frame filies.
        
    wait : float (seconds)
        The amount of time to wait before retring.
        
    timeout: int 
        The amount of times the script will try to get the data.
        
    count: int
        This is used only for the recursive part of the function.
        It is the number of times it already tried.
        
        
    Returns
    -------
    
    timeseries data: gwpy.timeseries.TimeSeries 
        If data are fetched sucessfully it returns a gwpy TimeSeries
        
    None: 
        If data are not fetched after <timeout> attemts

    """
    
    if state_vector_channel is not None:
        channels = [channel, state_vector_channel]
    else:
        channels = [channel]
    
    try:
        
        try:
            data = TimeSeriesDict.read(frames, channels, start = start_gps, end = end_gps)

        except Exception as ex:
            if logger is not None and type(ex)!=RuntimeError:
                 logger.debug(f"Exception ({type(ex)} at TimeSeriesDict.read: {ex}") 
            raise(ex)
        
        if state_vector_channel is not None:
            logger.debug(f"State vector: {StateVector(data[state_vector_channel])}")
            state_vector_status = ( StateVector(data[state_vector_channel]).boolean[:,0:2].value.all()  # Observing 
                                  & StateVector(data[state_vector_channel]).boolean[:,5:9].value.all() )# Clear of injections

            if state_vector_status:
                if logger is not None:
                     logger.debug(f"Attempt to access the data {count+1}") 
                     logger.info(f"State vector [0,1,5,6,7,8] indeces are {state_vector_status}") 

                return data[channel]

            else:
                raise Exception(f"State vector [0,1,5,6,7,8] indeces are {state_vector_status}")
        else:
            if logger is not None: logger.info(f"Attempt to access the data {count+1}") 
            return data[channel]
            
    except Exception as e:

        time.sleep(wait)
        count += 1
        if count < timeout:
            return readFrameFile(frames, channel, state_vector_channel, start_gps, end_gps 
                                    , wait = wait, timeout=timeout, count = count,logger=logger)
            
        else:
            if logger is not None:
                logger.info(f"Could not find frames, Exception: {e}") 


        return None
    


def logarithmic_indices(length, n_points):
    """
    Generate indices of points to sample in logarithmic order.

    Args:
    - length: int, length of the array
    - n_points: int, number of points to sample

    Returns:
    - indices: list of int, indices of points to sample
    """
    # Generate logarithmically spaced indices that are unique
    log_indices = np.unique(np.append( np.logspace(0, np.log10(length - 1), num=n_points-1, base=10, dtype=int), length-1) )
    # Convert to list
    indices = list(log_indices)
    return indices    

    
def far_interpolation(testfile, testNumber, min_tail_points=24, inverse = False):

    if isinstance(testfile,str):
        with open(testfile,'rb') as obj:
            dataR = pickle.load(obj)
    else:
        dataR = testfile
                
    # dataR= dataR[dataR['score'] > 0.0001]

    try:
        scoreR=np.sort(np.array(dataR['score'])).tolist()[::-1]
    except Exception as e:
        scoreR=np.sort(np.array(dataR['scores1'])*np.array(dataR['scores2'])).tolist()[::-1]
    scoreFrequency=(np.arange(len(scoreR))+1)/testNumber

    
    # The number of points in the tail that belong 
    # to less than once per month FAR.
    month_tail = testNumber//(30*24*3600) 

    if month_tail >= min_tail_points:

        new_indeces = np.append(np.arange(month_tail)                               # The indeces of the significant events (all indeces)
                               ,logarithmic_indices(len(scoreR) - month_tail ,100)) # The indeces of all the rest (logarithmic)

        # Applying the indeces
        scoreR         = np.array(scoreR)[[new_indeces]][0]
        scoreFrequency = np.array(scoreFrequency)[[new_indeces]][0]

        print(scoreR[0],scoreR[-1])

        print(scoreFrequency[0],scoreFrequency[-1])

    if inverse==False:
    
        farInterpolation=interp1d(
            scoreR,
            scoreFrequency,
            bounds_error=False,
            fill_value=(scoreFrequency[-1],scoreFrequency[0])
        )
        
    elif inverse==True:
        
        farInterpolation=interp1d(
            scoreFrequency,
            scoreR,
            bounds_error=False,
            fill_value=(scoreR[0],scoreR[-1])
        )

    return farInterpolation
    


def far(far_interp, input , inverse=False):
    
    """Uses the interpolation function provided
    to provide the FAR of the input score provided (inverse=False)
    or the score corresponding to the input FAR provided
    (inverse=True). 
    
    Parameters
    ----------
    
    far_interp: str (path)
        The interpolation function to use
        
    input: float (score or FAR)
        The score value to evaluate on the interpolation
        function (inverse=False) which returns a FAR value,
        or the FAR value to evaluate on the interpolation
        function (inverse=True) which returns a score value.
    
    inverse: bool
        If false it will give FAR for a given score. If
        true it will give score for a given FAR.

    Returns
    -------

    event FAR or score: float
        The FAR coresponding value of <input> using the 
        interpolation. Or the score value of <input>.
    """
    
    if isinstance(far_interp,str):
        with open(far_interp,'rb') as obj:
            far_interp = pickle.load(obj)
    
    return float(far_interp(input))


def find_observing_run(config,interval =None):


    if all(config['frames_directory'][key]=="" for key in config['detectors']) or all(config['channels'][key]=="" for key in config['detectors']):

        if interval is None:

            start = config['segment_list'][0]
            end = config['segment_list'][1]
        
        else:

            start = interval[0]
            end = interval[1]

        if isinstance(start,str):
            start = to_gps(start)
        if isinstance(end,str):
            end = to_gps(end)


        run_dict = dict(o1 = Segment(1126051217,1137254417),
                            o2 = Segment(1164556817,1187733618),
                            o3a = Segment(1238166018, 1253977218),
                            o3b = Segment(1256655618, 1269363618),
                            o4a = Segment(1369180818, tconvert(gpsordate='now')))

        frame_dict = dict(o1 = {'H': 'H1_HOFT_C02'
                            ,'L': 'L1_HOFT_C02'
                            ,'V': 'V1Online'},
                    o2 = {'H': 'H1_HOFT_C02'
                            ,'L': 'L1_HOFT_C02'
                            ,'V': 'V1Online'},
                            
                    o3a = {'H': 'H1_HOFT_C01'
                            ,'L': 'L1_HOFT_C01'
                            ,'V': 'V1Online'},
                    o3b = {'H': 'H1_HOFT_C01'
                            ,'L': 'L1_HOFT_C01'
                            ,'V': 'V1Online'},
                    o4a = {'H': 'H1_HOFT_C00'
                            ,'L': 'L1_HOFT_C00'
                            ,'V': 'V1Online'})


        channel_dict = dict(o1 = {'H': 'H1:DCS-CALIB_STRAIN_C02'
                                    ,'L': 'L1:DCS-CALIB_STRAIN_C02'
                                    ,'V': 'V1:Hrec_hoft_16384Hz'},

                            o2 = {'H': 'H1:DCS-CALIB_STRAIN_C02'
                                    ,'L': 'L1:DCS-CALIB_STRAIN_C02'
                                    ,'V': 'V1:Hrec_hoft_16384Hz'},

                            o3a = {'H': 'H1:DCS-CALIB_STRAIN_C01'
                                    ,'L': 'L1:DCS-CALIB_STRAIN_C01'
                                    ,'V': 'V1:Hrec_hoft_16384Hz'},

                            o3b = {'H': 'H1:DCS-CALIB_STRAIN_C01'
                                    ,'L': 'L1:DCS-CALIB_STRAIN_C01'
                                    ,'V': 'V1:Hrec_hoft_16384Hz'},

                            o4a = {'H': 'H1:GDS-CALIB_STRAIN_CLEAN'
                                    ,'L': 'L1:GDS-CALIB_STRAIN_CLEAN'
                                    ,'V': 'V1:Hrec_hoft_16384Hz'})


        selected_run = None
        for run in run_dict.keys():
            if (start in run_dict[run]) and (end in run_dict[run]):
                selected_run = run
                break
        
        print('SELECTED RUN: ',selected_run)
        if selected_run is None:
            raise ValueError("start and end date do not belong in the same or any observing run\n", from_gps(start), from_gps(end))
            
        config['frames_directory']= frame_dict[selected_run]
        config['channels'] = channel_dict[selected_run]
        print(config['frames_directory'])
        with open("config.json", "w") as config_json:
            json.dump(config, config_json,indent=4)
            config_json.close()

        print("Config has been informed with the new frames and channels")

    return config

def find_default_segments(config, inclusion_flags=[] 
                                , exclusion_flags=[]):

    # # If there is an already defined segments.txt file it uses that.
    # if os.path.exists(config["path"]+"/segments.txt"):
    #     return config
    
    if os.path.isfile('used_segments.txt'):
        segments_ = []

        with open(config['path']+'/'+'used_segments.txt', 'r') as file:
            for line in file:
                start, end = map(float, line.strip().split(','))
                segments_.append((start, end))

        config['segment_list'] = segments_

    else:
        print("looking for default segments")
        detectors = config['detectors']
        start = config['segment_list'][0]
        end = config['segment_list'][1]

        config = find_observing_run(config,interval = [start,end])
        print("looked for observing run")

        detector_active_flag = config['active_flags']

        print('detector_active_flag: ',detector_active_flag)

        detector_segments = []

        for det in detectors:
            individual_detector_segment = query_segments(detector_active_flag[det], start, end)['active']
            print(det, individual_detector_segment)
            for flag in inclusion_flags:
                try: 
                    print("Flag(+)  ", flag[det])
                    individual_detector_segment = individual_detector_segment & query_segments(flag[det], start, end)['active']
                except KeyError:
                    print("Flag ", flag[det], " was not found, continuing to the next.")
                except:
                    raise

            for flag in exclusion_flags:
                try:
                    print("Flag(-)  ", flag[det])
                    individual_detector_segment = individual_detector_segment & ~query_segments(flag[det], start, end)['active']
                except KeyError:
                    print("Flag ", flag[det], " was not found, continuing to the next.")
                except:
                    raise
            detector_segments.append(individual_detector_segment)
            
        if 'V' in config['detectors'] and len(detector_segments[-1])==0:
            print("WARNING: VIRGO HAS NO SEGMENTS, WAS IT SUPPOSED TO BE IN THE DETECTORS?")

        coincident_segments = detector_segments[0]
        for segment in detector_segments[1:]:
            coincident_segments = coincident_segments & segment

        config['segment_list'] = coincident_segments

        segmentlist = list([seg[0],seg[1]] for seg in coincident_segments)
        np.savetxt('used_segments.txt', segmentlist, delimiter=',')

    return config

def calculateRequiredGPSTime(config, gps_index, initial_gps_time,logger=None):
    
    """Injests command line arguments dictionary and outputs runtime config
        dictionary. Includes error checking.
       
       Parameters
       ----------
           
       config: dict
           Dictionary containing program runtime variables
           
       gps_index: int
           How many gps times have been searched by this script alone.
           
       initial_gps_time: int
           First gps time searched by set of scripts.
    
       Returns
       -------
    
       gps_time: int 
           GPS time to search during this iteration.
           
       gps_index: int
           How many gps times have been searched by this script alone.
    """
    
    # Unpack variables for readability:
    num_scripts = config["num_scripts"]
    script_index = config["script_index"]
    gps_reset_time = config["gps_reset_time"]
    required_buffer = config["required_buffer"]
    
    #Find gps time for script
    gps_time = initial_gps_time + num_scripts*gps_index + script_index


    # If gps_time falls to far behind current time, reset gps time by  
    # making the index go appropriatly forward.
    if (gpstime.gps_time_now() - gps_time) > gps_reset_time:
        logger.info(f"S{config['script_index']} Before gps push - Requested / Difference from current GPS time: {gps_time} / {gpstime.gps_time_now() - gps_time}")

        if logger is not None:
            logger.info(f"Reseting GPS target time by skipping {num_scripts * int(gpstime.gps_time_now()-gps_time)//num_scripts + script_index } seconds")     
                    
        gps_index += int(gpstime.gps_time_now()-gps_time)//num_scripts  
        gps_time = initial_gps_time + num_scripts*gps_index + script_index

    else:
        # Iterate gps index
        gps_index += 1

    return gps_time, gps_index

def aquireData(config, gps_time,logger=None):
    
    """Aquires required data at inputted gps time.
       
       Parameters
       ----------
           
       config: dict
           Dictionary containing program runtime variables
           
       gps_time: int
           GPS time in which to search for data

       Returns
       -------
    
       buffers: list 
           List containing data streams from required detectors at requested time
    """
    
    buffers = []
    for detector, detector_initial in enumerate(config["detectors"]):

        #Combine path to frame file with prefix variable for readability:
        prefix = config['frames_directory'][detector_initial] + detector_initial+"-"+detector_initial+"1_"+config['prefix']

        #Generate names of fram files to be read:
        frames = [f"{prefix}{gps_time + i}-1.gwf" for i in range(config["required_buffer"] + 1)]
        #+1 is removed a few lines below, we keep it because resampling afects the edges of the timeseries
        state_vector = config["state_vectors"][detector_initial] if (config["state_vectors"] != {}) else None
        #Search for frame files, return None if not found
        strain = readFrameFile(
            frames, 
            config["channels"][detector_initial],
            state_vector,
            wait = config["wait"],
            timeout = int((config["num_scripts"]*1.5)/config["wait"]), # Using up to 1.5 times the time available in one loop of time. 
            logger = logger
        )

        if strain is not None:
            #Resample all strain data:
            strain = strain.resample(config["fs"]).value[int(config["fs"]*0.5):-int(config["fs"]*0.5)]
        else:
            #If no frame file is found return None
            return None

        #Raise error if erroneoud data detected
        zeros=len(np.where(strain==0.0)[0]) # weidly it returns array in a tuple
        if zeros>=0.10*len(strain):
            print(f"Error! Data in detector ",detector," has many zeros : {str(zeros/len(strain))}")
            return None
        else:
            buffers.append(strain.tolist()) # Why do we convert this to a list?
    


    return buffers


def runTimeFrequencyParameterEstimation(thepod,
                                        mly_output = None) -> dict:
    
    """Peforms time domain parameter estimation on inputted datapod.
       
       Parameters
       ----------
       
       thepod: datapod
           Data pod on which to perform time-
           and frequency-domain parameter estimation
       : dict

       Returns
       -------
    
       mly_output: dictionary
           Dictionary containing mly output values.
    """
    
    thepod.addPlugIn(tf_map_plugin)
    thepod.addPlugIn(tf_map_masked_plugin)
    thepod.addPlugIn(pe_plugin)

    if mly_output is not None:
        mly_output["SNR"] = thepod.PE['SNR']
        mly_output["central_time"] = mly_output['gpstime']+thepod.PE['peakTime']
        mly_output['gpstime'] = mly_output["central_time"]
        mly_output["duration"] = thepod.PE['duration']
        mly_output["central_freq"] = thepod.PE['peakFreq']
        mly_output["bandwidth"] = thepod.PE['bandwidth']

        mly_output["start_time"] = thepod.PE['start_time']
        mly_output["end_time"] = thepod.PE['end_time']
        mly_output["start_frequency"] = thepod.PE['start_frequency']
        mly_output["end_frequency"] = thepod.PE['end_frequency']


        return mly_output

   
def podToFileSystem(pod, masterDirectory):
    
    """This function takes a dataPod and splits it into seperate ones
    depending on the detectors included. It saves individual DataPods
    into a temporary file until the manager merges all the pods into a
    DataSet.
    
    Parameters
    ----------
        
    pod : mly.datatools.DataPod
        The DataPod object to be included in the fileSystem
    
    masterDirectory: str (path)
        A path to a valid file system directory. A valid file system
        directory needs to have subfolders with the initials of all
        detectors used and a 'temp' file that also includes subfolders
        with initials of all detectors.
    
    Note
    ----
    
    We don't use checking functions to save time in low latency searces.
    """
    
    detectors = pod.detectors
    for det in detectors:
        _gps = pod.gps[pod.detectors.index(det)]
        if _gps==0.0: continue # Correction to avoid saving virgo
        _pod = DataPod(pod.strain[pod.detectors.index(det)]
                       ,detectors = [det]
                       ,fs = pod.fs
                       ,gps = [_gps])
        
        _pod.save(masterDirectory+'temp/'+det+'/'+str(_gps)+'_1')
    
def create_tf_map(data,fs, Tfft = 1/16, wind=None, verbose = True):

    # % --------------------------------------------------------------------------
    # %    Create the time-frequency map of the data.
    # % --------------------------------------------------------------------------

    # % ---- THE PE FUNCTION WILL START HERE.

    # % ---- We will FFT using a window with 50% overlap. The FFT duration chosen 
    # %      above should be large compared to the light travel time between detectors.
    # %      Then we can ignore time delays and simply add the TF maps from all 
    # %      detectors together.

    # % ---- FFT Window: We will NOT use one of the standard window functions.
    # %      Instead we will use 
    # %          window = sin(n*pi/Nfft)
    # %      (i.e., the square-root of the hann window). This unusual choice has
    # %      the property that sum(wx^2) = sum(x^2) where x is the original data
    # %      and wx is the windowed overlapping segments. This choice should 
    # %      therefore keep the total energy or squared SNR in the data the same
    # %      before and after windowing.

    if verbose: print(f"Shape of data: {data.shape}")

    T = max(data.shape)/fs
    Ndet = min(data.shape)
    N = int(T*fs)          # %-- timeseries length
    Nfft = int(Tfft*fs)    # %-- FFT length

    if wind == None:
        wind = np.sin(np.arange(1,Nfft+1)*np.pi/Nfft)[np.newaxis]

    # % ---- Number of columns in the segmented overlapping data.
    Ncol = 2*N//Nfft-1
    # % ---- Number of non-negative frequency bins ([0,...,Nyquist]).
    Nrow = Nfft//2+1
    
    # % ---- Prepare temporary storage for the segmented overlapping data (we work 
    # %      with one detector at a time).
    sdata= np.zeros((Nfft,Ncol))

    # % ---- Prepare storage for the time-frequency map.
    tf_map   = np.zeros((Nrow,Ncol))

    # % ---- Create the time-frequency map by looping over detectors and adding the
    # %      map for each.

    for iDet in np.arange(0,Ndet):
        # % ---- Segment and window the data.
        for icol in np.arange(0,Ncol):
            shiftIdx = int(icol*Nfft/2)
            #sdata[: ,icol] = np.fft.fft(data[shiftIdx : shiftIdx+Nfft,iDet] * wind)
            sdata[: ,icol] = data[shiftIdx : shiftIdx+Nfft,iDet] * wind
            
        if verbose:
            # % ---- Sanity check: have we preserved power? Note that the first and last
            # %      half bins don't have an overlapping segment so don't include those
            # %      in power comparison.
            powerIn = np.sum(data[Nfft//2: -Nfft//2,iDet]**2)
            powerOut = sdata.flatten(order = 'F')
            powerOut = np.sum(powerOut[Nfft//2: -Nfft//2]**2)
            print('Power conservation test for detector ' + str(iDet) + ':')
            print('  Power in  = ' + str(powerIn))
            print('  Power out = ' + str(powerOut))
            
        # % ---- FFT and retain non-negative frequencies only ([0,...,Nyquist]).
        sdata= np.fft.fft(sdata,axis=0)
        #print(tf_map.shape, sdata[np.arange(0,Nfft//2+1),:].shape)
        #tf_map = tf_map + abs(sdata)[np.arange(0,Nfft//2+1),:]**2
        tf_map = tf_map + abs(sdata[np.arange(0,Nfft//2+1),:])**2

    if verbose:
        plt.figure()
        plt.imshow(tf_map)

    return(tf_map)


def summary_plot(mly_pod,config,save_path = None):
    from mly.skymap_utils import skymap_plot_function, mask_window_tf
    from mly.plugins import plotcorrerlaion
    from mly_pipeline.search_functions import tf_map_masked_plot_function

    duration = config['duration']
    fs = config['fs']
    detectors = config['detectors']

    # Recreating the mask as it is not retrievable
    mask = mask_window_tf(duration, fs,mly_pod.PE['start_time']
                                      ,mly_pod.PE['end_time'] 
                                      ,config['skymap']['ramp_duration'] 
                                      ,config['skymap']['ramp_center']
                                      ,config['skymap']['duration_limit']).numpy()
 
    plt.figure(figsize=(18, 9))

    # Correlation plot
    ax1 = plt.subplot(2,4,5)
    ax1 = plotcorrerlaion(mly_pod.strain,detectors,fs,data=mly_pod.correlation,ax=ax1)

    # Masked tf-map plot
    ax2 = plt.subplot(2,4,6)
    ax2 = tf_map_masked_plot_function( mly_pod.strain,tf_map = mly_pod.tf_map ,data = mly_pod.tf_map_masked, ax = ax2)

    # Skymap
    ax3 = plt.subplot(2,2,4,projection='astro hours mollweide')
    ax3 = skymap_plot_function(mly_pod.strain,data=mly_pod.sky_map,ax = ax3)

    # The filtered time-series plot
    ax4 = plt.subplot(2,1,1)
    ax4.set_title("Whitened Time-series")
    ax4.plot(np.arange(0,duration,1/fs),mly_pod.sky_map[-1][0]*mask  ,label='H1 Filtered',color='#ee0000')
    ax4.plot(np.arange(0,duration,1/fs),mly_pod.sky_map[-1][1]*mask  +5 ,label='L1 Filtered',color='#4ba6ff')

    ax4.plot(np.arange(0,duration,1/fs),mly_pod.strain[0] ,label='H1',color='#ee0000',alpha = 0.5)
    ax4.plot(np.arange(0,duration,1/fs),mly_pod.strain[1] +5 ,label='L1',color='#4ba6ff',alpha = 0.5)

    ax4.plot(np.arange(0,duration,1/fs),mask ,color='k',label = 'Mask')
    ax4.plot(np.arange(0,duration,1/fs),mask +5 ,color='k')

    ax4.legend()
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path)

def masked_tf_map(tf_map
                , bpp = 0.05   # %-- fraction of loudest pixels in the map to keep for PE
                , verbose = True
                , searchRadius = 2):  # %-- radius in pixels to search for neighbors
    # % --------------------------------------------------------------------------
    # %    Threshold and cluster the time-frequency map.
    # % --------------------------------------------------------------------------

    # Keep everything except the two first and two last rows that are corupted
    tf_map[:2, :] = 0
    tf_map[-2:, :] = 0
    
    # % ---- Number of pixels retained.
    Nbp = int(bpp*tf_map.size) #matlab would have ceil for index being +1
    
    # N = int(T*fs)          # %-- timeseries length
    # Nfft = int(Tfft*fs)    # %-- FFT length
    # # % ---- Number of columns in the segmented overlapping data.
    # Ncol = 2*N//Nfft-1
    # # % ---- Number of non-negative frequency bins ([0,...,Nyquist]).
    # Nrow = Nfft//2+1
    

    
    # % ---- Find the map threshold corresponding to the Nbp'th highest value.
    sortedmap = np.sort(tf_map.flatten(order = 'F'))[::-1] # %-- (:) reshapes into a vector in descending order
    if verbose: print("sortedmap",sortedmap.shape)
    mapMedian = np.median(sortedmap)
    if verbose: print("mapMedian",mapMedian)
    threshold = sortedmap[Nbp]
    if verbose: print("thresold", threshold)
    # # % ---- Zero out unwanted pixels.
    maksed_map = np.where(tf_map >= threshold, tf_map, 0)


    # # % ---- I will define my signal as the loudest pixel, all other pixels that are 
    # # %      above threshold and share an edge or corner with the loudest pixel, and 
    # # %      all other pixels that share an edge or corner with another pixel in the
    # # %      event, working out recursively until there are no remaining pixels above
    # # %      threshold bordering the event. Matlab has the bwlabel function for this;
    # # %      I will avoid using it or any other special matlab commands and just rely 
    # # %      on simple commands.

    # # % ---- Find maximum value of map.
    Nrow, Ncol = tf_map.shape
    maxMap = 0
    for icol in np.arange(0,Ncol):
        for irow in np.arange(0,Nrow):
            if tf_map[irow,icol] > maxMap:
                maxMap = tf_map[irow,icol]
                maxRow = irow
                maxCol = icol

    # % ---- Initialise mask marking pixels that are part of our event cluster.
    mask = np.zeros(tf_map.shape)
    # % ---- Add loudest pixel.
    mask[maxRow,maxCol] = 1


    # % ---- Search outward from loudest to find other loud neighboring pixels.
    # %      otherPixels* list the pixels to be checked for neighbors. Add to this
    # %      as we find new neighbors and keep searching until we have checked all
    # %      of them.
    otherPixelsRow = [maxRow]
    otherPixelsCol = [maxCol]
    while len(otherPixelsRow)!=0:
        # % ---- Pixel we are searching around.
        irow = otherPixelsRow[0];
        icol = otherPixelsCol[0];
        for ii in np.arange(-searchRadius,searchRadius+1):
            for jj in np.arange(-searchRadius,searchRadius+1):
                if ii !=0 & jj !=0: # % ---- Skip 0,0 - this is the pixel we are searching around.
                    pass
                elif (irow+ii < 0 or irow+ii >= Nrow or icol+jj < 0 or icol+jj >= Ncol): # % ---- Target "pixel" is off the edge of the map - skip.
                    pass
                elif tf_map[irow+ii,icol+jj]>threshold and mask[irow+ii,icol+jj]==0:
                    # % ---- Add this pixel to the mask and the list of pixels to be checked.
                    mask[irow+ii,icol+jj] = 1
                    otherPixelsRow.append(irow+ii)
                    otherPixelsCol.append(icol+jj)
        # % ---- Remove this pixel from the list to be checked.
        _ = otherPixelsRow.pop(0)
        _ = otherPixelsCol.pop(0)
        
    if verbose:
        
        fig, ax = plt.subplots(1,2)
        ax[0].imshow(mask)
        ax[0].set_title("Mask")
        ax[1].imshow(maksed_map)
        ax[1].set_title("Masked map")
        
    return mask , maksed_map, mapMedian


def compute_PE(mask, masked_map, map_median, fs, Tfft = 1/16, verbose = True):
    # --------------------------------------------------------------------------
    #    Compute properties of the pixel cluster.
    # --------------------------------------------------------------------------

    Nrow, Ncol = masked_map.shape

    # ---- Initialise values of cluster properties.
    # ---- Number of pixels.
    nPixels = 0
    # ---- Start time.
    startTime = Ncol #-- [bin] dummy value larger than any in map
    # ---- End time.
    endTime = 0        #%-- [bin] dummy value smaller than any in map
    # ---- Weighted peak time.
    peakTime = 0
    # ---- Minimum frequency.
    startFreq = Nrow #%-- [bin] dummy value larger than any in map
    # ---- Maximum frequency.
    endFreq = 0        #%-- [bin] dummy value smaller than any in map
    # ---- Weighted peak frequency.
    peakFreq = 0
    # ---- SNR.
    snrSquared = 0

    # ---- Loop over all pixels and add to the output properties.
    for irow in np.arange(0,Nrow):
        for icol in np.arange(0,Ncol):
            if mask[irow,icol]==1:
                nPixels = nPixels + 1
                snrSquared = snrSquared + masked_map[irow,icol] 
                if icol < startTime:
                    startTime = icol
                
                if icol > endTime:
                    endTime = icol
                
                peakTime = peakTime + icol*masked_map[irow,icol]
                if irow < startFreq:
                    startFreq = irow
                
                if irow > endFreq:
                    endFreq = irow
                
                peakFreq = peakFreq + irow*masked_map[irow,icol]
                
    # ---- Normalise peakTime, peakFreq.
    peakTime = peakTime / snrSquared
    peakFreq = peakFreq / snrSquared
    # ---- Convert all times from bins to seconds.
    T0 = Tfft/2  # %-- central time of first bin
    dT = Tfft/2  # %-- hard-coded for 50% overlap
    startTime = T0 + (startTime)*dT - dT  # %-- start of bin (bin width = 2*dT)
    endTime   = T0 + (  endTime)*dT + dT # %-- end of bin (bin width = 2*dT)
    peakTime  = T0 + ( peakTime)*dT
    # % ---- Convert all frequencues from bins to Hz.
    F0 = 0       # %-- central freq of first bin
    dF = 1/Tfft # %-- spacing of frequency bins
    startFreq = F0 + (startFreq)*dF - 0.5*dF # %-- start of bin
    endFreq   = F0 + (  endFreq)*dF + 0.5*dF # %-- end of bin
    peakFreq  = F0 + ( peakFreq)*dF
    # % ---- Duration.
    duration = endTime - startTime
    # % ---- Bandwidth.
    bandwidth = endFreq - startFreq
    # ---- Estimate SNR.
    SNR = max(2*(snrSquared-nPixels*map_median)/(Tfft*fs),0)**0.5

    if verbose:
        print("PE results:")
        print("peakTime ",peakTime)
        print("duration ",duration)
        print("bandwidth ",bandwidth)
        print("peakFreq ",peakFreq)
        print("start_time", startTime)
        print("end_time", endTime)
        print("SNR ", SNR)

        print(Nrow,Ncol,dT,dF)
        fig, ax = plt.subplots()
        ax.imshow(masked_map, origin='lower',extent=[T0,Nrow*dT,F0,Ncol*dF],aspect = 1/(Ncol*dF))

        ax.set_title("Masked map")
    
    pe_dict = dict( peakTime = peakTime
                   ,duration = duration
                   ,bandwidth = bandwidth
                   ,peakFreq = peakFreq
                   ,start_frequency = startFreq
                   ,end_frequency = endFreq
                   ,start_time = startTime
                   ,end_time = endTime
                   ,SNR = SNR)


    return pe_dict


# PLUGIN FUNCTIONS (tf_map)

def tf_map_gen_function(strain,fs,detectors,gps):


    # Making a specific exception when search is run in two detectors.
    if 'V' in detectors and gps[detectors.index('V')]==0.0:

        detectors_ = detectors.copy()
        detectors_.remove('V')

        if all( list( gps[detectors_.index(det)] != 0.0 for det in detectors_)):
            strain = np.delete(strain, detectors.index('V'),axis=0)

    tf_map = create_tf_map(data = np.transpose(strain),fs = fs, Tfft = 1/16, verbose = False)

    return tf_map

def tf_map_plot_function( strain,data = None, ax = None):

    T0 = (1/16)/2  # Tfft/2 %-- central time of first bin
    dT = (1/16)/2  # Tfft/2 %-- hard-coded for 50% overlap
    # % ---- Convert all frequencues from bins to Hz.
    F0 = 0       # %-- central freq of first bin
    dF = 1/(1/16) # 1/Tfft%-- spacing of frequency bins

    Nrow , Ncol = data.shape
    
    if ax is None:
        fig, ax = plt.subplots()
    im = ax.imshow(data, origin='lower',extent=[T0,Nrow*dT,F0,Ncol*dF],aspect = 1/(Ncol*dF))
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title("Time-Frequency map")
    ax.figure.colorbar(im)

    return ax

# PLUGIN FUNCTIONS (tf_map_masked)

def tf_map_masked_gen_function(strain,fs,tf_map):

    mask , masked_map , map_median = masked_tf_map(tf_map = tf_map , bpp = 0.05, verbose = False)

    return [mask , masked_map , map_median]

def tf_map_masked_plot_function( strain,tf_map,data = None, ax = None):

    T0 = (1/16)/2  # Tfft/2 %-- central time of first bin
    dT = (1/16)/2  # Tfft/2 %-- hard-coded for 50% overlap
    # % ---- Convert all frequencues from bins to Hz.
    F0 = 0       # %-- central freq of first bin
    dF = 1/(1/16) # 1/Tfft%-- spacing of frequency bins

    mask , masked_map , map_median = data

    Nrow , Ncol = tf_map.shape

    if ax is None:    
        fig, ax = plt.subplots()
    im = ax.imshow(tf_map, origin='lower',extent=[T0,Nrow*dT,F0,Ncol*dF],aspect = 1/(Ncol*dF))
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title("Time-Frequency map")
    ax.figure.colorbar(im,shrink = 0.5)

    # Masking plot
    f = lambda x,y: mask[int(y),int(x) ]
    g = np.vectorize(f)
    
    x = np.linspace(0,mask.shape[1], mask.shape[1]*100)
    y = np.linspace(0,mask.shape[0], mask.shape[0]*100)
    X, Y= np.meshgrid(x[:-1],y[:-1])
    Z = g(X[:-1],Y[:-1])

    ax.contour(Z, [0.5], colors='r', linewidths=1
                ,extent=[T0,Nrow*dT,F0,Ncol*dF])

    return ax


# PLUGIN FUNCTIONS (PE)

def pe_gen_function(fs, tf_map_masked):

    mask, masked_map, map_median = tf_map_masked

    return compute_PE(mask, masked_map, map_median, fs , verbose = False)



tf_map_plugin = PlugIn('tf_map',genFunction=tf_map_gen_function,attributes=['strain','fs','detectors','gps']
                               ,plotFunction=tf_map_plot_function, plotAttributes=['strain'])

tf_map_masked_plugin = PlugIn('tf_map_masked',genFunction=tf_map_masked_gen_function,attributes=['strain','fs','tf_map']
                                             ,plotFunction=tf_map_masked_plot_function, plotAttributes=['strain','tf_map'])


pe_plugin = PlugIn('PE', genFunction = pe_gen_function,attributes=['fs','tf_map_masked'])




