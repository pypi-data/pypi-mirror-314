
import os
# Scipy and numpy env parameters that limit the threads
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import json
import pickle
import argparse
import sys ,time
import pandas as pd
import os
import logging
import subprocess
import random
import shutil

from mly.tools import dirlist
from mly.datatools import *
from .search_functions import *
from dqsegdb2.query import query_segments
from gwpy.segments import Segment, SegmentList, DataQualityFlag
from gwpy.time import from_gps, to_gps, tconvert
from datetime import datetime


# # # Managing arguments
# 
# List of arguments to pass:
arguments = [

    "restriction",
    "timeUnit"
]

#Construct argument parser:
parser = argparse.ArgumentParser()

parser.add_argument('--restriction')
parser.add_argument('--timeUnit')


# Pass arguments
args = parser.parse_args()

# Store arguments in dictionary:
kwdict = {}
for argument in arguments:
    kwdict[argument] = getattr(args, argument)
    
with open('config.json') as json_file:
    config = json.load(json_file)
    
config={ **kwdict , **config}


# # # Initialising logging
log_level = logging.getLevelName(config["log_level"])

# create logger
logger = logging.getLogger("logger_for_manager")
logger.setLevel(log_level)



# create console handler and set level to debug
ch = logging.handlers.TimedRotatingFileHandler('log/manager.log', when='H',interval=12, backupCount=1,)
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)



def manage_output_directory(config=None):

    output_directory = config['output_directory']
    maxDataFrameSize = config['maxDataFrameSize']

    frame_size_check=0
    fileList = dirlist(output_directory)
    dFramesList  = []
    jsonList = []
    # Listing the files in the directory
    # Separating the json from pkl
    for file in fileList:

        if ".json" in file:
            jsonList.append(file)
        elif ".pkl" in file:
            dFramesList.append(file)

    # if there are no new outputs we skip that step
    if len(jsonList)!=0: 

        # We expect that every time the manager runs, there is a temp_frame
        # file that might have events but it is not of the size we group
        # them (maxDataFrameSize). 
        try:

            with open(output_directory+'tempFrame.pkl','rb') as obj:
                temp_frame = pickle.load(obj)
        # The first time manager is running this file is created instead.
        except FileNotFoundError:
            temp_frame = pd.DataFrame(columns = ['gpstime','far','ifos'
                                                ,'coincidence','coherency'
                                                ,'combined','trigger'])

            temp_frame["trigger"]=temp_frame["trigger"].astype(bool)

            logger.info(f"Creating tempfile for the first time.")

        # The size of the frame
        initial_temp_frame_size=len(temp_frame)
        json_list_size = len(jsonList)

        #logger.info(f"Check that all files used, initial temp frame file {initial_temp_frame_size}")
        #logger.info(f"Check that all files used, json list size {json_list_size}")

        # A check value to make sure we add all the json files.
        frame_size_check = json_list_size + initial_temp_frame_size

        # Adding all the events in json format to the temp_frame
        for file in jsonList:

            try:
                with open(output_directory+file,"r") as jf:
                    p=json.load(jf)
                    jf.close()
            # Need to explain why this try point
            except Exception as e:
                frame_size_check = -1
                logger.warning(f"Exception in loading json file {file}, {e}")
                continue

            # Reformating the score parameters to the desired format.
            for k in list(p['scores'].keys()):
                p[k]=p['scores'][k]
            # Making a string of ifos list to avoid line breaking into two
            p['ifos'] = [str(p['ifos'])]

            if file[0]=='N':
                p['trigger']=False
            elif file[0]=='T':
                p['trigger']=True
            else:
                p['trigger']=False


            del(p['scores'])  
            del(p['channels'])  

            p = pd.DataFrame(p)
            p["trigger"]=p["trigger"].astype(bool) # Avoiding a future warning

            temp_frame=pd.concat([temp_frame,p],ignore_index=True)

        # Reseting index and sorting by GPS time
        temp_frame=temp_frame.sort_values(by="gpstime").reset_index(drop=True)
        # Rearanging the columns
        temp_frame = temp_frame[['gpstime','far','ifos','coincidence','coherency'
                            ,'combined','trigger']]
        # Chopping the temp_frame to chuncs of maxDataFrameSize outputs
        # IMPORTANT: We don't separate them by hour, we just collect 
        # maxDataFrameSize of them together

        while len(temp_frame) > maxDataFrameSize:

            # Creating a newframe to include the maxDataFrameSize instances
            newFrame=temp_frame[:maxDataFrameSize]
            with open(output_directory+str(newFrame['gpstime'][0])+"-"
                    +str(newFrame['gpstime'][maxDataFrameSize-1])
                    +"_"+str(maxDataFrameSize)+'.pkl', 'wb') as output:
                pickle.dump(newFrame, output, 4)

            # Removing the newframe from temp_frame
            temp_frame=temp_frame[maxDataFrameSize:].reset_index(drop=True)

            frame_size_check=-maxDataFrameSize

        # What is left in temp_frame, overights the temp_frame.pkl
        with open(output_directory+'tempFrame.pkl', 'wb') as output:
            pickle.dump(temp_frame, output, 4)
            logger.info(f"Saving the incomplete group of outputs: {output_directory}tempFrame.pkl")

        frame_size_check-=len(temp_frame)
        # We remove all json files already included in a dataFrame
        for file in jsonList:
            os.remove( output_directory + file )
        
        logger.info(f"Check that all files used, must be zero {frame_size_check}")




def manage_master_directory(config=None):


    maxDataFrameSize = config['maxDataFrameSize']
    # Listing all files saved in the temp file (files to be managed)
    detectors= list( det for det in config['detectors'])
    

    number_of_files={}
    file_numbers={}
    dataSet_dict={}
    
    # For each detector we count how many files have been saved in all
    # detectors and we sort them.
    for det in detectors:
        number_of_files[det] = len(dirlist(config['masterDirectory']+'/temp/'+det))
        file_numbers[det] = sorted(list(file.split('_')[0] for file in dirlist(
            config['masterDirectory']+'/temp/'+det)))
        dataSet_dict[det] = []

    # If there are no files we skip this step
    if len(file_numbers[detectors[0]])==0:
        logger.info(f"Empty temp directory")
        
    # If the files included in temp are less than maxDataFrameSize, we skip
    # this step.
    elif (int(float(file_numbers[detectors[0]][-1]))
        -int(float(file_numbers[detectors[0]][0]))) < maxDataFrameSize:
        logger.info(f"Not enough data \
                    {maxDataFrameSize - (int(float(file_numbers[detectors[0]][-1])) -  int(float(file_numbers[detectors[0]][0])))}\
                    to run the FAR test yet")
        
    # If the files included in temp are enough we group them
    elif (int(float(file_numbers[detectors[0]][-1]))
        -int(float(file_numbers[detectors[0]][0]))) >= maxDataFrameSize:
        
        c=0
        
        # We keep track of the files used to delete them later
        file_to_delete=[]
        
        # Checking that all detectors have the same number of files
        logger.debug(f"Number of files for each detector: {list(len(file_numbers[det]) for det in detectors)}")
        
        last_file_number=None
        
        for filenumber in file_numbers[detectors[0]][:int(maxDataFrameSize)]:

            # For each file we in first detector we check that it exists in the
            # other detectors too. 
            if all( list( os.path.isfile(config['masterDirectory']
                                        +'/temp/'+det+'/'+file_numbers[detectors[0]][c]
                                        +'_1.pkl') for det in detectors)):
                _temp_dataSet_dict = {}

                try:
                    for det in detectors:
                            _temp_dataSet_dict[det] = DataPod.load(config['masterDirectory']
                                                    +'/temp/'+det+'/'+str(filenumber)+'_1.pkl')
                    for det in detectors:

                        dataSet_dict[det].append(_temp_dataSet_dict[det])

                except Exception as e:

                    logger.warning(f"Exception {type(e)}:{e} was raised at fille {config['masterDirectory']}/temp/{det}/{filenumber}_1.pkl")

                        
                    
                last_file_number=int(float(filenumber))
                file_to_delete.append(str(filenumber)+'_1.pkl')
                
            # Othewise we delete it and it can't be used
            else:
                file_to_delete.append(str(filenumber)+'_1.pkl')
            
            c+=1

        # We use those two for name creation
        first = str(int(float(file_numbers[detectors[0]][0])))
        last = str(last_file_number)
        # print('first,last: ',first,last)
        
        # Saving the instances in dataSets
        for det in detectors:
            _set = DataSet(dataSet_dict[det])
            name = first+'-'+last+'_'+str(len(_set))
            _set.save(config['masterDirectory']+'/' + det + '/' + name)

            # # Deleting files that already passed.
            for file in file_to_delete:
                try:
                    os.remove(config['masterDirectory']+'/temp/'+det+'/'+file)
                except FileNotFoundError as e:
                    logger.warning(f"Exception {type(e)}:{e} was raised at while trying to delete file {config['masterDirectory']}/temp/{det}/{file}")
                    pass
                except Exception as e:
                    logger.warning(f"Exception {type(e)}:{e} was raised at while trying to delete file {config['masterDirectory']}/temp/{det}/{file}")
                    raise(e)
    
    return None




def manage_efficiency_test(config = None):

    if config is None:
        with open('config.json') as json_file:
            config = json.load(json_file)

    np.random.seed(config['seed'])
    random.seed(config['seed'])

    # # # Efficiency test buffer management
    
    
    # How many inferences to wait to run the test, roughly how often in seconds

    efficiencyTestBuffer = config["eff_config"]["howOften"]

    # We load all the buffer pods that live in temp
    buffer_set = []
    pod_list = dirlist(config['bufferDirectory']+"/temp")
    # Shuffling the pods so that the ones used are randomly distributed along the time.
    random.shuffle(pod_list)
    
    num_pods = len(pod_list)
    
    # If number of the buffer pods are more than maxDataFrameSize, we 
    # putting them in a dataSet to be used.
    logger.info(f"Buffer size accumulated: {num_pods}/{efficiencyTestBuffer} .Start efficiency test: {num_pods >= efficiencyTestBuffer}")
    # I there are enough buffer pods we can save them to be used in an efficiency test.
    if num_pods >= efficiencyTestBuffer:
        
        for each_pod in pod_list[:efficiencyTestBuffer]:
            pod = DataPod.load(config['bufferDirectory']+"/temp/"+each_pod) 
            buffer_set.append(pod)
        # Keeping only the number of pods needed for the efficiency test
        random.shuffle(buffer_set)
        buffer_dataset = DataSet(buffer_set[: int(config['eff_config']['testSize'])])

        buffer_dataset.save(config['bufferDirectory']+"/BUFFER_SET")

        # Deleting the files in temp
        for each_pod in pod_list:    
            os.remove(config['bufferDirectory']+"/temp/"+each_pod)
        
        issue_efficiency_test()
        logger.info(f"Efficiency test initiated")

def issue_efficiency_test():
    os.system("nohup python -m mly_pipeline.make_eff_estimation --mode condor &> efficiencyTest.out &")

def manage_FAR_inefernce_files(config = None):

    if config is None:
        with open('config.json') as json_file:
            config = json.load(json_file)
    # # # FAR test management 
    #

    # The list of all temporary inference files
    if os.path.isdir(config['falseAlarmRates']):
        if config['far_config']['restriction']==None: 
            config['far_config']['restriction']=0.0
        
        restriction=float(config['far_config']['restriction'])
        
        inference_temp_files = dirlist(config['falseAlarmRates'])

        for directory in ['hourly', 'condor', 'FARfile','temp']:
            if directory in inference_temp_files: inference_temp_files.remove(directory)


        # The list of all the files in hourly (grouped by hour/DAG of generation)
        hourly_files = [file_ for file_ in os.listdir(f"{config['falseAlarmRates']}/hourly") if file_.endswith(".pkl")]

        # The group names inside hourly
        hourly_files_groups = list(file.split("_")[0] for file in hourly_files)

        # The group names (start-end gps) in inference_temp_files
        inference_temp_files_groups = list(file.split("_")[0] for file in inference_temp_files)
        inference_temp_files_groups = list(dict.fromkeys(inference_temp_files_groups))

        logger.debug(f"HOURLY GROUPS: {len(hourly_files_groups)}")
        logger.debug(f"TEMP GROUPS: {len(inference_temp_files_groups)}")

        # First we will go through the files that already have a group inside hourly
        # We will add them in their corresponding hourly group file and remove them 
        # from inference_temp_files

        for hgroup, hfile_name in zip(hourly_files_groups, hourly_files):

            if hgroup in inference_temp_files_groups:

                # with open(config['falseAlarmRates']+"/hourly/"+hfile_name,'rb') as obj:
                #     hfile = pickle.load(obj)
                
                # hfile_size = int(hfile_name.split("_")[-1][:-4])

                to_remove_from_inference_temp_files = []

                for file_name in inference_temp_files:
                    
                    if hgroup in file_name:
                        
                        # Moving the inference files to their coresponding group safe
                        os.rename( f"{config['falseAlarmRates']}/{file_name}" , f"{config['falseAlarmRates']}/hourly/{hgroup}/{file_name}")
                        
                        to_remove_from_inference_temp_files.append(file_name)


                for f_num, file_name in enumerate(os.listdir(f"{config['falseAlarmRates']}/hourly/{hgroup}")):

                    with open(f"{config['falseAlarmRates']}/hourly/{hgroup}/{file_name}",'rb') as obj:
                        file = pickle.load(obj)

                    file = file[file['score'] >= restriction]

                    if f_num==0:
                        hfile = file.copy()
                        # Initiating the file size 
                        hfile_size = int(file_name.split("_")[-1][:-4])

                    else:

                        hfile = pd.concat([hfile, file], ignore_index=True)
                        # Adding the size of the file to the hourly file
                        hfile_size += int(file_name.split("_")[-1][:-4])
                
                # Deleting the previous combined hourly file of this group
                os.remove(config['falseAlarmRates']+"/hourly/"+hfile_name)

                # Saving the new combined hourly group file
                new_hfile_name = "_".join(hfile_name.split("_")[:-1])+"_"+str(hfile_size)
                with open(config['falseAlarmRates']+"/hourly/"+new_hfile_name+'.pkl', 'wb') as output:
                    pickle.dump(hfile, output, 4)


                for file_name in to_remove_from_inference_temp_files:
                    inference_temp_files.remove(file_name)

        # Now we can create new hourly files for the new groups that appeared
        # First we reset the inference_temp_files. There will be no already existing froup
        # for those files

        # Reseting temp_file_groups 
        inference_temp_files_groups = list(file.split("_")[0] for file in inference_temp_files)
        inference_temp_files_groups = list(dict.fromkeys(inference_temp_files_groups))

        # A check to make sure all files left do not belong in an existing group.
        check = all( [ all([hgroup not in file for file in inference_temp_files]) for hgroup in hourly_files_groups] )
        logger.debug(f"All groups left are new: {check}")


        for tgroup in inference_temp_files_groups:

            to_remove_from_inference_temp_files = []
            
            # Making the new group directory inside hourly
            os.makedirs(f"{config['falseAlarmRates']}/hourly/{tgroup}")

            for file_name in inference_temp_files:

                if tgroup in file_name:

                    if len(to_remove_from_inference_temp_files)==0:

                        with open(config['falseAlarmRates']+"/"+file_name,'rb') as obj:
                            new_hfile = pickle.load(obj)

                        new_hfile_size = int(file_name.split("_")[-1][:-4])
                    
                    else:

                        with open(config['falseAlarmRates']+"/"+file_name,'rb') as obj:
                            file = pickle.load(obj)

                        new_hfile = pd.concat([new_hfile, file], ignore_index=True)

                        new_hfile_size += int(file_name.split("_")[-1][:-4])

                    to_remove_from_inference_temp_files.append(file_name)
                    
                    # Moving the inference files to their coresponding group safe
                    os.rename( f"{config['falseAlarmRates']}/{file_name}" , f"{config['falseAlarmRates']}/hourly/{tgroup}/{file_name}")

            new_hfile_name = tgroup+"_"+str(new_hfile_size)
            with open(config['falseAlarmRates']+"/hourly/"+new_hfile_name+'.pkl', 'wb') as output:
                pickle.dump(new_hfile, output, 4)

            logger.info(f"Informing / Saving FAR file : {config['falseAlarmRates']}/hourly/{new_hfile_name}.pkl")

            for file_name in to_remove_from_inference_temp_files:
                inference_temp_files.remove(file_name)

        logger.debug(f"This should be zero, inference_temp_files: {len(inference_temp_files)}")
        
        # Loading the background tests (hourly files) into one, to update the final interpolation.

        hourly_files = [file_ for file_ in os.listdir(f"{config['falseAlarmRates']}/hourly") if file_.endswith(".pkl")]

        for i, hfile_name in enumerate(hourly_files):

            if i==0: 
                with open(config['falseAlarmRates']+"/hourly/"+hfile_name,'rb') as obj:
                    farfile = pickle.load(obj)

                farfile_size = int(hfile_name.split("_")[-1][:-4])
            else:
                
                with open(config['falseAlarmRates']+"/hourly/"+hfile_name,'rb') as obj:
                    farfile_part = pickle.load(obj)

                farfile = pd.concat([farfile, farfile_part], ignore_index=True)

                farfile_size += int(hfile_name.split("_")[-1][:-4])

        # Deleting the old FARfile before creating the new one (they have the size of tests on their name).
        farfile_to_delete = None
        old_far_files = dirlist(config['falseAlarmRates']+"/FARfile")
        for file in old_far_files:
            if 'FARfile_interpolation' not in file:
                farfile_to_delete = file
                logger.info(f"FARfile to be replaced: {farfile_to_delete}")
                break 

        if len(hourly_files)!=0:
            with open(config['falseAlarmRates']+"/FARfile/FARfile_"+str(farfile_size)+".pkl", 'wb') as output:
                pickle.dump(farfile, output, 4)

                logger.info(f"New FARfile saved: {config['falseAlarmRates']}/FARfile/FARfile_{farfile_size}.pkl")

            far_interpolation_output = far_interpolation(farfile, farfile_size, inverse = False)
            far_interpolation_output_inverse = far_interpolation(farfile, farfile_size, inverse = True)

            with open(config['falseAlarmRates']+"/FARfile/FARfile_interpolation.pkl", 'wb') as output:
                pickle.dump( far_interpolation_output , output, 4)
            with open(config['falseAlarmRates']+"/FARfile/FARfile_interpolation_reserve.pkl", 'wb') as output:
                pickle.dump( far_interpolation_output , output, 4)
                
            with open(config['falseAlarmRates']+"/FARfile/FARfile_interpolation_inverse.pkl", 'wb') as output:
                pickle.dump(far_interpolation_output_inverse , output, 4)
            with open(config['falseAlarmRates']+"/FARfile/FARfile_interpolation_inverse_reserve.pkl", 'wb') as output:
                pickle.dump(far_interpolation_output_inverse , output, 4)
            
            logger.info(f"New FARfile interpolations saced")

            if (farfile_to_delete is not None 
                    and farfile_to_delete!="FARfile_"+str(farfile_size)+".pkl"):
                os.remove(config['falseAlarmRates']+"/FARfile/"+farfile_to_delete)
            
        # Overwriting config farfile when enough files
        if len(hourly_files)!=0 and (farfile_size) >=4*365*24*3600 and (config['farfile'] != config['falseAlarmRates']+"/FARfile"):

            with open('config.json') as json_file:
                _config = json.load(json_file)
                _config['farfile'] = config['falseAlarmRates']+"/FARfile"
            with open("config.json", "w") as config_json:
                json.dump(_config, config_json,indent=4)
                config_json.close()

            logger.info(f"FARFILE UPDATED FROM THE TEMPORARY TO THE SEARCH LOCAL!")
            raise SystemError("This is just an interuption to load the new FAR sourse.")


# add here the page function
def manage_status_page():
    os.system("nohup python -m mly_pipeline.create_status_page --mode condor > status_page.out &")

def far_plot():

    farfile_path = config['farfile']


    for file in os.listdir(farfile_path):
        if 'interpolation' not in file:
            main_file = file
            break


    interpolation= farfile_path + '/FARfile_interpolation.pkl'
    inverse_interpolation= farfile_path + '/FARfile_interpolation_inverse.pkl'

    testnums=int(main_file.split('_')[-1][:-4])
    years_of_background = "{:0.2f}".format(testnums/365/24/3600)

    with open(interpolation,'rb') as handle:
        interp= pickle.load(handle)

    with open(inverse_interpolation,'rb') as handle:
        inverse= pickle.load(handle)

    s = np.arange(1e-2,1,1e-4)

    halfday_score = inverse(1/(12*3600))
    month_score = inverse(1/(30*24*3600))
    year_score = inverse(1/(365*24*3600))
    fouryear_score = inverse(1/(4*365*24*3600))

    # print(month_score,year_score,fouryear_score)

    data = 1/(interp(s)*24*3600*365)
    # print(data[-1])
    fig, ax  = plt.subplots()

    ax.axis([s[0], 1, data[-1], data[0]])

    ax.loglog(s,data) # IFAR months
    ax.axvline(x=halfday_score,ls='--',color='black',label ='2/day')#,color=colours[i])
    ax.axvline(x=month_score,ls='--',color='green',label ='1/month')#,color=colours[i])
    ax.axvline(x=year_score,ls='--',color='orange',label = '1/year')#,color=colours[i])
    ax.axvline(x=fouryear_score,ls='--',color='red', label = '1/4years')#,color=colours[i])

    ax.set_title(f"Background score distribution of {years_of_background} years")
    ax.set_ylabel("IFAR (years)")
    ax.set_xlabel("Scores")

    ax.text(halfday_score, 1/1e3, "{:6.3f}".format(halfday_score), color ='black',fontweight ='bold',horizontalalignment = 'right',verticalalignment ='top')
    ax.text(month_score, 1/1e2, "{:6.3f}".format(month_score), color ='green',fontweight ='bold',horizontalalignment = 'right',verticalalignment ='top')
    ax.text(year_score, 1/1e1, "{:6.3f}".format(year_score), color ='orange',fontweight ='bold',horizontalalignment = 'right',verticalalignment ='top')
    ax.text(fouryear_score, 1/1e0, "{:6.3f}".format(fouryear_score), color ='red',fontweight ='bold',horizontalalignment = 'right',verticalalignment ='top')


    ax.legend()

    plt.savefig('far.png')


def segments_plot():


    detectors = config['detectors']

    if 'ONLINE' in config['search_mode']:

        end = float(tconvert(gpsordate = 'now'))
        start = end-3600*24*3+3600

    elif 'OFFLINE' in config['search_mode'] and isinstance(config['segment_list'],(list,tuple)):

        start = config['segment_list'][0]
        end = config['segment_list'][-1]

    else:

        print('NO VALID SEGMENT INPUT WAS PROVIDED')

    detector_active_flag =  config['active_flags']
    detector_segments =[]

    for det in detectors:
        individual_detector_segment = query_segments(detector_active_flag[det], start, end)['active']
        detector_segments.append(individual_detector_segment)

    coincident_segments = SegmentList(detector_segments[0])
    for segment in detector_segments[1:]:
        coincident_segments = coincident_segments & segment

    slist = get_segments_out_of_outputs(gps_start = start
                                        , gps_end = None
                                        , target_directory = config['output_directory'])

    flag = DataQualityFlag(name=' '
                    , active=slist
                    , known=coincident_segments)

    plot = flag.plot(color='gwpy:ligo-hanford',alpha =0.6)
    #plt.title('Processed Segments the last 3 days')
    plot.savefig('segment_plot.png')


def get_segments_out_of_outputs(gps_start
                                ,gps_end=None
                                ,target_directory='output_directory/'
                                ,include_tempFile=False
                                ,similarity_radius = 1):

    if gps_end is None:
        include_tempFile = True
        gps_end = float(tconvert(gpsordate = 'now'))



    files = list(file for file in sorted(os.listdir(target_directory)) 
                if (file[-4:]=='.pkl' and 'tempFrame' not in file 
                and float(file.split('-')[1].split('_')[0]) > gps_start 
                and float(file.split('-')[0]) < gps_end)
                )
    # Initial value to check 
    df = None

    # Loading all output files
    for i, file in enumerate(files):

        if i == 0: 
            with open(f"{target_directory}/{file}",'rb') as out:
                df = pickle.load(out)
        else:
            with open(f"{target_directory}/{file}",'rb') as out:
                df_ = pickle.load(out)

            df = pd.concat([df,df_],ignore_index = True)

    # Including tempFile if requested
    if include_tempFile and df is not None:
        try:
            with open(f"{target_directory}/tempFrame.pkl",'rb') as out:
                df_ = pickle.load(out)

            df = pd.concat([df,df_],ignore_index = True)
        except Exception as e:
            pass
    if len(files)==0:
        print('empty')
        return []

    # Sort the DataFrame based on gpstime column
    df_sorted = df.sort_values(by='gpstime')
    
    df_sorted = df_sorted[(df_sorted['gpstime']>=gps_start) & (gps_end>df_sorted['gpstime'])]
    # Initialize variables for segment creation
    start_time = None
    end_time = None
    segments = []

    # Iterate through sorted DataFrame to identify continuous segments
    for idx, row in df_sorted.iterrows():
        if start_time is None:
            start_time = int(row['gpstime'])
            end_time = int(row['gpstime'])+1
        elif int(row['gpstime']) - end_time > similarity_radius:  # If the difference is more than 2 seconds
            # Create a segment and start a new one
            segments.append(Segment(start_time, end_time))
            start_time = int(row['gpstime'])
            end_time = int(row['gpstime'])+1
        else:
            # Extend the segment
            end_time = int(row['gpstime'])+1

    # Create a segment for the last continuous segment
    if start_time is not None:
        segments.append(Segment(start_time, end_time))

    # Return a segment list
    return segments


def copy_files_to_mirror():
    """
    Copies important files to a mirror directory if requested.

    """
    # Check if the source file exists
    
    if config['mirror_path'] == 'not_defined':
        return 
    
    mirror_path = config['mirror_path']

    if not os.path.exists(mirror_path):
        os.makedirs(mirror_path)

    shutil.copy2(f"{config['path']}/config.json", f"{mirror_path}/config.json")
    try:
        shutil.copy2(f"{config['path']}/Efficiencies.png", f"{mirror_path}/Efficiencies.png")
    except:
        pass
    shutil.copy2(f"{config['path']}/far.png", f"{mirror_path}/far.png")
    shutil.copy2(f"{config['path']}/segment_plot.png", f"{mirror_path}/segment_plot.png")
    shutil.copy2(f"{config['path']}/status.html", f"{mirror_path}/status.html")

    # Iterate over the files and subdirectories in the trigger_directory
    for root, dirs, files in os.walk(f"{config['path']}/trigger_directory"):
        # Compute the corresponding destination directory
        rel_path = os.path.relpath(root, f"{config['path']}/trigger_directory")
        dst_dir = os.path.join(f"{mirror_path}/trigger_directory", rel_path)
        
        # Ensure the destination directory exists
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        # Copy files that do not exist in the destination directory
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_dir, file)
            if not os.path.exists(dst_file):
                shutil.copy2(src_file, dst_file)
                logger.info(f"Copied: {src_file} to {dst_file}")

    return
        

def manage_offline_trigger_directory():

    for temp_dir in os.listdir(config['trigger_directory']):
        
        if len(os.listdir(f"{config['trigger_directory']}/{temp_dir}")) == 0:
            shutil.rmtree(f"{config['trigger_directory']}/{temp_dir}")
            continue

        else:

            for event_dir in os.listdir((f"{config['trigger_directory']}/{temp_dir}")):

                shutil.move(f"{config['trigger_directory']}/{temp_dir}/{event_dir}"
                        , f"{config['trigger_directory']}/{event_dir}")

                shutil.rmtree(f"{config['trigger_directory']}/{temp_dir}")

    return


def main(config):

    config = checkOutputDirectoryArguments(config)

    # The size in which we group the outputs
    if config['maxDataFrameSize']==None: 
        config['maxDataFrameSize']=3600

    maxDataFrameSize = int(config['maxDataFrameSize'])


    # This is the time scale to use for the plots
    timeUnitDict={1:'s', 60:'m', 3600:'h', 24*3600:'days',30*24*3600:'months', 365*24*3600:'years'}

    if config['timeUnit']==None: 
        config['timeUnit']=3600
    else:
        config['timeUnit']=int(config['timeUnit'])
        

    sys.stdout.flush()


    lastdatetimehour = -1 # Hour index so that some processes run every hour only

    while (1):

        loopT0=time.time()

        # # # Managing the output directory files
        #
        #        
        logger.debug(f"PROCESSES before output management: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")
        
        manage_output_directory(config)

        # # # FileSystem for FAR management
        #
        logger.debug(f"PROCESSES before FAR management: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

        manage_master_directory(config)

        # # # Efficiency test buffer management
        #
        logger.debug(f"PROCESSES before efficiency and buffers management: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

        if os.path.isdir(config['efficiencies']):
            manage_efficiency_test(config)

        # # # FAR test management 
        #
        manage_FAR_inefernce_files(config)
        
        # # # Updating page plots
        # 
        
        if datetime.now().hour != lastdatetimehour:

            segments_plot()
        
        lastdatetimehour = datetime.now().hour

        far_plot()

        # # # Update status page
        #
        manage_status_page()  
        logger.info(f"Status page updated")
        
        copy_files_to_mirror()
        
        # Timing
        logger.info(f"Manager loop time:{(time.time()-loopT0)/60} minutes, waiting 5 minutes ... ")
        sys.stdout.flush()

        time.sleep(5*60)
        
        
if __name__ == "__main__":
        
    main(config)
    


