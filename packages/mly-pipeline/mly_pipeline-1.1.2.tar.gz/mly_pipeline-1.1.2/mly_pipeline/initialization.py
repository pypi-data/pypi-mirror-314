#! /usr/bin/env python3

import os, sys, json, argparse, subprocess, shutil

def _parser():

    arguments = ["search_mode"
                 ,"path"
                 ,"output_directory"
                 ,"trigger_directory"
                 ,"masterDirectory"
                 ,"bufferDirectory"
                 ,"falseAlarmRates"
                 ,"efficiencies"
                 ,"detectors"
                 ,"reset"
                 ,"nofar"]

    
    #Construct argument parser:
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--search_mode', type=str
                        , default = "DEFAULT_OFFLINE"
                        , help = "For automatically setting the pipeline for different uses"
                        , required = False)

    parser.add_argument('-p', '--path', type=str
                        , default = "./mlyPipelineOrigin"
                        , help = "The path and name of the"
                        +" directory to be used by mlyPipeline."
                        , required = False)

    parser.add_argument('-o', '--output_directory', type=str
                        , default = 'output_directory'
                        , help = "The name of the"
                        +" directory to be used by mlyPipeline for the storage"
                        +" of the results from every inference."
                        , required = False)

    parser.add_argument('-t', '--trigger_directory', type=str
                        , default = 'trigger_directory'
                        , help = "The name of the"
                        +" directory to be used by mlyPipeline for the storage"
                        +" of the triggers."
                        , required = False)

    parser.add_argument('-m', '--masterDirectory', type=str
                        , default = 'masterDirectory'
                        , help = "The name of the"
                        +" directory to be used by mlyPipeline for the storage"
                        +" of the plots from the triggers."
                        , required = False)

    parser.add_argument('-b', '--bufferDirectory', type=str
                        , default = 'bufferDirectory'
                        , help = "The name of the"
                        +" directory to be used by mlyPipeline for the storage"
                        +" of the data around every instance (buffer) to be used"
                        +" for the efficiecy tests"
                        , required = False)

    parser.add_argument('-f', '--falseAlarmRates', type=str
                        , default = 'falseAlarmRates'
                        , help = "The name of the"
                        +" directory to be used by mlyPipeline for the storage"
                        +" of the false alarm rate data."
                        , required = False)

    parser.add_argument('-e', '--efficiencies', type=str
                        , default = 'efficiencies'
                        , help = "The name of the"
                        +" directory to be used by mlyPipeline for the storage"
                        +" of the false alarm rate data."
                        , required = False)

    parser.add_argument('-d', '--detectors', type=str
                        , default = 'HLV'
                        , help = "The initials of the detectors used"
                        , required = False)
    
    parser.add_argument('-R', '--reset'
                        , action = 'store_true'
                        , default = False
                        , help = "If passed it will ovewright the target path"
                        + " with a clean new filesystem."
                        , required = False)

    parser.add_argument('-nofar', '--nofar'
                        , action = 'store_true'
                        , default = False
                        , help = "If passed it will exclude the FAR scripts used for background estimation. This is only for OFFLINE searches"
                        , required = False)




    
    # Pass arguments:
    args = parser.parse_args()
    
    # Store arguments in dictionary:
    kwargs = {}
    for argument in arguments:
        kwargs[argument] = getattr(args, argument)

    print('nofar: ',kwargs['nofar'])

    return kwargs
   
def connect_path_relatively_to(path_to_change,path_to_connect):
    common_part = []
    for dir in path_to_change.split('/'):
        if dir in path_to_connect.split('/'):
            common_part.append(dir)
        else:
            break

    common_part = '/'.join(common_part)

    new_path_to_change = path_to_change.split(common_part)
    
    return '..'+new_path_to_change[-1]

def createRunAllScript(**kwargs):
    
    """ Creating a script called runall.sh that withing the search director will
    run and manage all the scripts needed for the search.
    """
    search_directory = kwargs['path'].split('/')[-1]
    with open(kwargs['path'] + '/' + 'runall.sh','w') as f:
        
        # Sourcing mlyPipeline module
        #f.write("source=" + kwargs['mlyPipelineSource'] + "\n")
        
        # Things to write only if OFFLINE mode is active 
        # (OFFLINE is not complete)
        f.write("echo $(date +'%Y-%m-%d %T') SEARCH HAS STARTED > monitor.log" + "\n")
        f.write("echo $(date +'%Y-%m-%d %T') Version of mly: $(python -m pip show mly 2>/dev/null | grep Version | awk '{print $2}') >> monitor.log" + "\n")
        f.write("echo $(date +'%Y-%m-%d %T') Version of mly-pipeline: $(python -m pip show mly_pipeline 2>/dev/null | grep Version | awk '{print $2}') >> monitor.log" + "\n")     

        if "ONLINE" in kwargs['search_mode']:
            
            # Loop that checks the state of the jobs and doesn't stop
            f.write("while true" + "\n")
            f.write("do" + "\n")
            
            # Collection of the process ids of the scripts
            f.write("    processID=()"+ "\n")
            # Used to sinchronise the independent scripts of the search
            f.write("    unixtime=$(date +%s)" + "\n")
            # The number of paralel schripts to run 
            # !Note: If you change this from the config, you will have to 
            #        edit in the runall.sh script by hand.CD ..
            f.write("    STEP="+"$(jq -r '.parallel_scripts' config.json)"+ "\n\n")
            
            # Lopp to run the scripts for the search
            f.write("    for INITIAL in `seq 0 $(($STEP-1))`" + "\n")
            f.write("    do" + "\n\n")
            f.write("        nohup python -m mly_pipeline.search"
                             +" --splitter [$STEP,$INITIAL]"
                             +" --time_reference $unixtime" 
                             +" &> search_step_$INITIAL.out & processID+=($(echo $!)) ; echo $!>>.jobids.txt" + "\n\n")
            f.write("    echo $(date +'%Y-%m-%d %T') Search file with initial $INITIAL started >> monitor.log" + "\n")     
            f.write("    done" + "\n\n\n")
        
            # Script that runs the manager script
            f.write("    nohup python -m mly_pipeline.manager &> manager.out & managerID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
            f.write("    echo $(date +'%Y-%m-%d %T') Manager script started >> monitor.log" + "\n")     

            # If the search runs as expected by default, it will also run scripts
            # for generating timelags and running FAR tests.
            if kwargs['far_config']['far_enabled']:
                f.write("    nohup python -m mly_pipeline.continuous_FAR --mode generation &> continuous_FAR_generation.out & generationID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
                f.write("    echo $(date +'%Y-%m-%d %T') Continuous FAR generation script started >> monitor.log" + "\n")     

                f.write("    nohup python -m mly_pipeline.continuous_FAR --mode inference &> continuous_FAR_inference.out & inferenceID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
                f.write("    echo $(date +'%Y-%m-%d %T') Continuous FAR inference script started >> monitor.log" + "\n")     
            # # # Maintenance of jobs 
            
            # If total_failure becomes 1, the script runs everything from scratch
            f.write("    total_failure=0" + "\n")
            
            # Sometimes the FAR script might stal indefinetly for unknow reasons
            # related to triton package, so if it does we restart it.
            if kwargs['far_config']['far_enabled']:

                f.write("    stalling_points=0" + "\n")
            
            # We add the number of timelag files present to see if our rate of 
            # doing FAR inference is efficient. Check the monitor.txt present in
            # the search directory, if there are too many zeros we can increase
            # our timelag production - "lags", always along with "batches". If
            # there are no zeros, we need to decrease the "lags" or inference 
            # does not work properly.
                    
            # Loop that checks if the main (not inference) scripts are running
            # every minute.
            f.write("    while [ $total_failure -ne 1 ]" + "\n")
            f.write("    do" + "\n")
            f.write("        sleep 60" + "\n\n")
                    
            # Updating the number of lag files for monitoring
            if kwargs['far_config']['far_enabled']:
                f.write("        echo $(date +'%Y-%m-%d %T') Continuous FAR status: $(ls falseAlarmRates/temp | wc -l) files in inference queue >> monitor.log" + "\n")     

            # Checking all scripts (not inference), if one fails total_failure=1
            f.write("        for pid in \"${processID[@]}\"" + "\n")
            f.write("        do" + "\n")
                    
            f.write("            if ! ps $pid > /dev/null" + "\n")
            f.write("            then" + "\n")
            f.write("                total_failure=1" + "\n")
            f.write("                echo -e $(date +'%Y-%m-%d %T') Main search script with pid $pid exited unexpectedly. Restarting search sequence ... >> monitor.log" + "\n")     
            f.write("                break" + "\n")
            f.write("            fi" + "\n") 
            f.write("        done" + "\n\n")

            f.write("        if ! ps $managerID > /dev/null"+ "\n")
            f.write("        then" + "\n")
            f.write("            nohup python -m mly_pipeline.manager &>"
                                +" manager.out & managerID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
            f.write("            echo $(date +'%Y-%m-%d %T') Manager script status: Manager script restarted due to unexpected exit >> monitor.log" + "\n")     
            f.write("        fi" + "\n\n")  
            # Specifically for inference script we check seperatelly, if it
            # doesn't look properly we rerun only the inference script. 
            if kwargs['far_config']['far_enabled']:

            
                # Checking if the number of inference files stays 0 for a long time.
                # If lag files increase without any new inference files, that means
                # stalling, and we add a stalling point. If not we reset it to 0.
                f.write("        if [ $(ls falseAlarmRates | wc -l) -eq 4 ] && [ $(ls falseAlarmRates/temp | wc -l) -ne 0 ]" + "\n")
                f.write("        then" + "\n")
                f.write("            echo $(date +'%Y-%m-%d %T') Continuous FAR status: Stalling points increase to $stalling_points >> monitor.log" + "\n")     
                f.write("            ((stalling_points=stalling_points+1))" + "\n")
                f.write("        else" + "\n")
                f.write("            stalling_points=0" + "\n")
                f.write("        fi" + "\n\n")

                # In case inference script gets killed or we have at least 5 minutes
                # of stalling, we restart inference script. Although, we keep the 
                # corresponding unix time it got killed in the name of the  output
                # file.
                f.write("        if ! ps $inferenceID > /dev/null || [ $stalling_points -ge 5 ]"+ "\n")
                f.write("        then" + "\n")
                f.write("            singularity instance stop --all" + "\n")
                f.write("            nohup python -m mly_pipeline.continuous_FAR --mode inference &>"
                                    +" continuous_FAR_inference_$(date +%s).out"
                                    +" & inferenceID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
                f.write("            echo $(date +'%Y-%m-%d %T') Continuous FAR status: Continuous FAR inference script restarted - Stalling points $stalling_points/5 >> monitor.log" + "\n")     
                f.write("            stalling_points=0" + "\n")
                f.write("        fi" + "\n\n")

                f.write("        if ! ps $generationID > /dev/null"+ "\n")
                f.write("        then" + "\n")
                f.write("            nohup python -m mly_pipeline.continuous_FAR --mode generation &> "
                                    +"continuous_FAR_generation_$(date +%s).out"
                                    +" & generationID=($(echo $!)) ; echo $!>>.jobids.txt"+ "\n")
                f.write("            echo $(date +'%Y-%m-%d %T') Continuous FAR status: Continuous FAR generation script restarted due to unexpected exit >> monitor.log" + "\n")     
                f.write("        fi" + "\n\n")  
                    
            f.write("    done" + "\n")
                    
            # If the previous loop exits, it means there was a total_failure=1
            # So we will have to rerun everything. But first we kill the python
            # scripts (inference included).
            # !Note: We are not remove any condor jobs from the lag generation
            #        script because they do not interfere with the scripts.
            f.write("    for pid in \"${processID[@]}\"" + "\n")
            f.write("    do" + "\n")
            f.write("        kill $pid" + "\n")
            f.write("    done" + "\n")
            
            if kwargs['far_config']['far_enabled']:

                f.write("    kill $managerID" + "\n")
                f.write("    kill $inferenceID" + "\n")
                f.write("    kill $generationID" + "\n")
                f.write("    singularity instance stop --all" + "\n")

            f.write("    echo $(date +'%Y-%m-%d %T') SEARCH HAS RESTARTED  >> monitor.log" + "\n")     
            f.write("done" + "\n")
        
        # Currently the offline script is very simple (under developement)
        else:
            
            if kwargs['far_config']['far_enabled']:

                f.write("echo $(date +'%Y-%m-%d %T') Setting file system - Creating condor jobs >> monitor.log" + "\n")
                f.write("python -m mly_pipeline.offline_search --mode set_file_system" + "\n\n")
                f.write("echo $(date +'%Y-%m-%d %T') Setting file system - Condor jobs submited >> monitor.log" + "\n\n")

                f.write("dagman_out_file=$(find masterDirectory/condor/submit -type f -name '*dagman.out' -exec ls -t {} + | head -n 1)" + "\n")
                f.write(f"total_jobs_number=$(grep -oP 'Dag contains \K\d+' $dagman_out_file)" + "\n")

                f.write("while ! grep -q 'EXITING WITH STATUS' \"$dagman_out_file\"; do" + "\n")
                f.write(f"   sleep 300" + "\n")
                f.write(f"   count=$(grep -c 'completed successfully' $dagman_out_file)" + "\n") 
                f.write("    echo $(date +'%Y-%m-%d %T') Setting file system - Completed jobs: $count/$total_jobs_number>> monitor.log" + "\n")
                f.write(f"done" + "\n")
                f.write(f"exiting_status=$(grep -oP 'EXITING WITH STATUS \K\d+' \"$dagman_out_file\")" + "\n")

                f.write(f"created_background_files=$(python -c 'from mly_pipeline.initialization import get_file_counts_after_createFileSystem; get_file_counts_after_createFileSystem()') "+ "\n")
                
                f.write("echo $(date +'%Y-%m-%d %T') Setting file system - $created_background_files/$total_jobs_number, with EXITING WITH STATUS $exiting_status>> monitor.log" + "\n")
                f.write("echo $(date +'%Y-%m-%d %T') Setting file system - Completed >> monitor.log" + "\n")
                
                f.write("nohup python -m mly_pipeline.continuous_FAR --mode generation &> continuous_FAR_generation.out & generationID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
                f.write("nohup python -m mly_pipeline.continuous_FAR --mode inference &> continuous_FAR_inference.out & inferenceID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
                f.write("echo $(date +'%Y-%m-%d %T') Background estimation initiated >> monitor.log" + "\n")

                # Checking if the number of inference files stays 0 for a long time.
                # If lag files increase without any new inference files, that means
                # stalling, and we add a stalling point. If not we reset it to 0.
                
                f.write("stalling_points=0" + "\n")
                f.write("premature_ending_points=0" + "\n")

                f.write("# The batches of generation times the dagmans" + "\n")
                f.write("background_scripts=$(ls masterDirectory/*.py | wc -l)" + "\n")


                f.write("# While the number of far files generated is not equal to background_scripts" + "\n")
                f.write("while [ $(ls falseAlarmRates/hourly/*.pkl | wc -l) -lt $background_scripts ] || [ $(ls falseAlarmRates/temp | wc -l) -ne 0 ] || (condor_q -af JobBatchName | grep -q \""+search_directory+"\") " + "\n")
                f.write("do" + "\n")
                

                f.write("    echo $(date +'%Y-%m-%d %T') Background estimation - completion: $(ls falseAlarmRates/hourly/*.pkl | wc -l) / $background_scripts >> monitor.log" + "\n")
                f.write("    sleep 300" + "\n\n")

                f.write("    if [ $(ls falseAlarmRates | wc -l) -eq 4 ] && [ $(ls falseAlarmRates/temp | wc -l) -ne 0 ]" + "\n")
                f.write("    then" + "\n")
                f.write("        echo stalling points increase to $stalling_points" + "\n")   
                f.write("        ((stalling_points=stalling_points+1))" + "\n")
                f.write("        echo $(date +'%Y-%m-%d %T') Background estimation - completion: $(ls falseAlarmRates/hourly/*.pkl | wc -l) / $background_scripts, inference stalling points increased to $stalling_points/5 >> monitor.log" + "\n")
                f.write("    else" + "\n")
                f.write("        stalling_points=0" + "\n")
                f.write("    fi" + "\n\n")

                # In case inference script gets killed or we have at least 5 minutes
                # of stalling, we restart inference script. Although, we keep the 
                # corresponding unix time it got killed in the name of the  output
                # file.

                f.write("    if [ $stalling_points -ge 5 ]"+ "\n")
                f.write("    then"+ "\n")
                f.write("        kill $inferenceID"+ "\n")
                f.write("        singularity instance stop --all"+ "\n")
                f.write("    fi"+ "\n\n")

                f.write("    if ! ps $inferenceID > /dev/null"+ "\n")
                f.write("    then" + "\n")
                f.write("        nohup python -m mly_pipeline.continuous_FAR --mode inference &> continuous_FAR_inference.out & inferenceID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
                f.write("        stalling_points=0" + "\n")
                f.write("    fi" + "\n\n")       

                f.write("    if ! ps $generationID > /dev/null"+ "\n")
                f.write("    then" + "\n")
                f.write("        nohup python -m mly_pipeline.continuous_FAR --mode generation &> "
                                +"continuous_FAR_generation.out & generationID=($(echo $!)) ; echo $!>>.jobids.txt"+ "\n")
                f.write("    fi" + "\n\n")                    
                        
                f.write("    if ! (condor_q -af JobBatchName | grep -q \""+search_directory+"\")  "
                            +"&& [ $(($(ls falseAlarmRates | wc -l) - 4)) -eq 0 ] "
                            +"&& [ $(ls falseAlarmRates/temp | wc -l) -eq 0 ]" + "\n")
                f.write("    then" + "\n")
                f.write("        ((premature_ending_points=premature_ending_points+1))" + "\n")
                f.write("        echo $(date +'%Y-%m-%d %T') Background estimation - completion: $(ls falseAlarmRates/hourly/*.pkl | wc -l) / $background_scripts, premature ending points increased: $premature_ending_points/3 >> monitor.log" + "\n")
                f.write("    fi" + "\n\n")

                f.write("    if [ $premature_ending_points -ge 3 ]" + "\n")
                f.write("    then " + "\n")
                f.write("        echo $(date +'%Y-%m-%d %T') Background estimation - PREMATURE COMPLETION: $(ls falseAlarmRates/hourly/*.pkl | wc -l) / $background_scripts  >> monitor.log" + "\n")

                f.write("        break" + "\n")
                f.write("    fi" + "\n\n")

                f.write("    python -c \"from mly_pipeline.manager import manage_FAR_inefernce_files; manage_FAR_inefernce_files()\" "+ "\n")


                f.write("done" + "\n")

                f.write("failed_groups=$(comm -23 <(ls falseAlarmRates/condor | awk -F'_' '{print $1}' | sort) <(ls falseAlarmRates/hourly/*.pkl | awk -F'_' '{print $1}' | sort))"+ "\n")
                f.write("failed_groups_n=$(echo $failed_groups | wc -w)"+ "\n")

                f.write("echo $(date +'%Y-%m-%d %T') Background estimation - COMPLETED: $(ls falseAlarmRates/hourly/*.pkl | wc -l)/$(( background_scripts - failed_groups_n )) with $failed_groups_n FAILED groups>> monitor.log" + "\n")
                f.write("[ -n \"$failed_groups\" ] && echo $(date +'%Y-%m-%d %T') Background estimation - The following groups did not generate timelags: $failed_groups"+ "\n")

                f.write("kill $inferenceID $generationID" + "\n")
                f.write("singularity instance stop --all" + "\n")

                # Making the FAR plot for the status page
                f.write("echo $(date +'%Y-%m-%d %T') Generating FAR and Segment plots >> monitor.log" + "\n")
                f.write("python -c \"from mly_pipeline.manager import far_plot; far_plot();\" "+ "\n")

                f.write("python -c \"from mly_pipeline.manager import manage_FAR_inefernce_files; manage_FAR_inefernce_files()\" "+ "\n")
        
            f.write("python -c \"from mly_pipeline.manager import segments_plot; segments_plot();\" "+ "\n")

            # If FAR is already calculated we only need this to run
            f.write("echo $(date +'%Y-%m-%d %T') Offline search - Initialised >> monitor.log" + "\n")
            f.write("python -m mly_pipeline.offline_search \n\n")
            f.write("search_jobs=$(awk -F 'Offline search - Number of jobs submited: ' '/Offline search - Number of jobs submited:/ {jobs=$2} END {print jobs}' monitor.log)" + "\n\n")
            f.write("while [ $(ls output_directory | wc -l) -lt $search_jobs ] " + "\n")
            f.write("do" + "\n")
            f.write("    echo $(date +'%Y-%m-%d %T') Offline search - Search jobs completed: $(ls output_directory | wc -l)/$search_jobs >> monitor.log" + "\n")
            f.write("    sleep 300" + "\n")
            f.write("    if ! condor_q -af JobBatchName | grep -q \""+search_directory+"_offline_search\"" + "\n")
            f.write("    then " + "\n")
            f.write("        echo $(date +'%Y-%m-%d %T') Offline search - WARNING: Condor jobs have finished before all the search output files have been produced - $(ls output_directory | wc -l)/$search_jobs"+ "\n")
            f.write("        break" + "\n\n")            
            f.write("    fi" + "\n\n")            
            f.write("done" + "\n")            
            f.write("echo $(date +'%Y-%m-%d %T') Offline search - Search jobs completed: $(ls output_directory | wc -l)/$search_jobs >> monitor.log" + "\n")

            f.write("if [ $(ls output_directory | wc -l) -ne $search_jobs ]" + "\n")
            f.write("    then " + "\n")
            f.write("    dagman_out_file=$(find condor/submit -type f -name '*dagman.out' -exec ls -t {} + | head -n 1)" + "\n")
            f.write("    error_line=$(grep -n \"ERROR: the following job(s) failed:\" \"$dagman_file\" | cut -d \":\" -f 1)" + "\n")
            f.write("    lines=$(awk -v error_line=\"$error_line\" 'NR > error_line && /Job Submit File:/ { sub(/.*Job Submit File:/, \"\"); print }' \"$dagman_file\")" + "\n")
            f.write("    echo $(date +'%Y-%m-%d %T') The following scripts failed:" + "\n")
            f.write("    while IFS= read -r submit_line; do error_file=$(echo \"$submit_line\" | sed 's/submit/error/g' | tr -d '[:space:]'); echo \"    $error_file - ERROR: $(tail -n 1 \"$error_file\")\" >> monitor.log; done <<< \"$lines\"" + "\n")
            f.write("fi" + "\n\n")    

            f.write("python -c \"from mly_pipeline.manager import manage_offline_trigger_directory; manage_offline_trigger_directory();\" "+ "\n")

            f.write("echo $(date +'%Y-%m-%d %T') Creating status page >> monitor.log" + "\n")
            f.write("python -c \"from mly_pipeline.manager import segments_plot; segments_plot();\" "+ "\n")
            f.write("mly-pipeline-statuspage" + "\n")
            f.write("python -c \"from mly_pipeline.manager import copy_files_to_mirror; copy_files_to_mirror();\" "+ "\n")

            f.write("echo $(date +'%Y-%m-%d %T') SEARCH HAS FINISHED >> monitor.log" + "\n")
            f.write("echo SEARCH PAGE:  https://ldas-jobs.ligo.caltech.edu/~$USER/$(jq -r '.path' config.json | awk -F'/' '{print $NF}')/status.html >> monitor.log" + "\n")



def main():
    
    kwargs = _parser()

    if kwargs['path'][-1]=="/" : 
        kwargs['path'] = kwargs['path'][:-1]
    
    # Setting the mirror directory if needed for the visualization of the search page
    main_path = os.path.abspath(kwargs['path'])
    main_user = os.environ['HOME'].split("/")[-1]

    if "local" in main_path:
        mirror_path = main_path.replace(f"/local/{main_user}"
                                        ,f"/home/{main_user}/public_html")
    else:
        mirror_path = 'not_defined'

    # Remove the search directory and its contents if it exists
    if os.path.exists(main_path):
        if kwargs['reset']:
            print(kwargs['path']," is going to be reset")
            print("Are you sure you want to delete the contents of that directory?")
            answer = input()
            
            if answer in ['yes','y','YES','Yes','Y']:

                shutil.rmtree(main_path)
                try:
                    shutil.rmtree(mirror_path)
                except:
                    pass
            else:
                raise ValueError("Initialization stoped from user")
        
        else:
            raise ValueError("The directory you try to create already exist"
                                    +". Run the same command but with `-R or --reset` to "
                                    +"ovewright the directory.")
    
    
    # Create the directory
    print(f"Search mode selected: {kwargs['search_mode']}")

    os.makedirs(main_path, exist_ok=True)
    print(f"Search path: {main_path}")

    os.makedirs(mirror_path, exist_ok=True)
    print(f"Mirror search path: {mirror_path}")

    frames_dict = dict(  DEFAULT_ONLINE = {"H":"" ,"L":"" ,"V":""}

                        ,DEFAULT_OFFLINE = {"H":"" ,"L":"" ,"V":""}

                        , FIRSTDETECTION_OFFLINE = {"H":"" ,"L":"" ,"V":""}

                        , O4_ONLINE = {"H":"/dev/shm/kafka/H1/"
                                      ,"L":"/dev/shm/kafka/L1/"
                                      ,"V":"/dev/shm/kafka/V1/"}

                        , O3MDC_ONLINE = {"H":"/dev/shm/kafka/H1_O3ReplayMDC/"
                                  ,"L":"/dev/shm/kafka/L1_O3ReplayMDC/"
                                  ,"V":"/dev/shm/kafka/V1_O3ReplayMDC/"}

                        , O3REPLAY_ONLINE = {"H":"/dev/shm/kafka/H1_O3ReplayMDC/"
                                     ,"L":"/dev/shm/kafka/L1_O3ReplayMDC/"
                                     ,"V":"/dev/shm/kafka/V1_O3ReplayMDC/"}

                        , BENCHMARK_MDC_OFFLINE = {"H":"/scratch/florent.robinet/BurstBenchmark/"
                                              ,"L":"/scratch/florent.robinet/BurstBenchmark/"
                                              ,"V":"/scratch/florent.robinet/BurstBenchmark/"}
                    )

    channels_dict = dict( DEFAULT_ONLINE = {"H":"" ,"L":"" ,"V":""}
    
                        , DEFAULT_OFFLINE = {"H":"" ,"L":"" ,"V":""}

                        , FIRSTDETECTION_OFFLINE = {"H":"" ,"L":"" ,"V":""}

                        , O4_ONLINE = {"H":"H1:GDS-CALIB_STRAIN_CLEAN"
                                      ,"L":"L1:GDS-CALIB_STRAIN_CLEAN"
                                      ,"V":"V1:Hrec_hoft_16384Hz_Gated"}

                        , O3MDC_ONLINE = {"H":"H1:GDS-CALIB_STRAIN_INJ1_O3Replay"
                                  ,"L":"L1:GDS-CALIB_STRAIN_INJ1_O3Replay"
                                  ,"V":"V1:Hrec_hoft_16384Hz_INJ1_O3Replay"}

                        , O3REPLAY_ONLINE = {"H":"H1:GDS-CALIB_STRAIN_O3Replay"
                                     ,"L":"L1:GDS-CALIB_STRAIN_O3Replay"
                                     ,"V":"V1:Hrec_hoft_16384Hz_INJ1_O3Replay"}

                        , BENCHMARK_MDC_OFFLINE = {"H":"H1:STRAIN_BURST_0"
                                                  ,"L":"L1:STRAIN_BURST_0"
                                                  ,"V":"V1:STRAIN_BURST_0"}
                                )
    
    state_vector_dict = dict( 
                          DEFAULT_ONLINE = {}

                        , DEFAULT_OFFLINE = {}

                        , FIRSTDETECTION_OFFLINE = {}

                        , O4_ONLINE = {"H":"H1:GDS-CALIB_STATE_VECTOR"
                                      ,"L":"L1:GDS-CALIB_STATE_VECTOR"
                                      ,"V":"V1:DQ_ANALYSIS_STATE_VECTOR"}
                        , O3MDC_ONLINE = {"H":"H1:GDS-CALIB_STATE_VECTOR"
                                      ,"L":"L1:GDS-CALIB_STATE_VECTOR"
                                      ,"V":"V1:DQ_ANALYSIS_STATE_VECTOR"}
                        , O3REPLAY_ONLINE = {}
                        )

    active_flags_dict = dict( 
                          DEFAULT_ONLINE = {"H":"" ,"L":"" ,"V":""}

                        , DEFAULT_OFFLINE = {"H": "H1:DMT-ANALYSIS_READY:1"
                                            ,"L": "L1:DMT-ANALYSIS_READY:1"
                                            ,"V": "V1:ITF_SCIENCE:1"}

                        , FIRSTDETECTION_OFFLINE = {"H": "H1:DMT-ANALYSIS_READY:1"
                                            ,"L": "L1:DMT-ANALYSIS_READY:1"
                                            ,"V": "V1:ITF_SCIENCE:1"}

                        , O4_ONLINE = {"H": "H1:DMT-ANALYSIS_READY:1"
                                        ,"L": "L1:DMT-ANALYSIS_READY:1"
                                        ,"V": "V1:ITF_SCIENCE:1"}

                        , O3MDC_ONLINE = {"H": "H1:DMT-ANALYSIS_READY:1"
                                        ,"L": "L1:DMT-ANALYSIS_READY:1"
                                        ,"V": "V1:ITF_SCIENCE:1"}

                        , O3REPLAY_ONLINE = {"H": "H1:DMT-ANALYSIS_READY:1"
                                            ,"L": "L1:DMT-ANALYSIS_READY:1"
                                            ,"V": "V1:ITF_SCIENCE:1"}

                        , BENCHMARK_MDC_OFFLINE = {"H":"" ,"L":"" ,"V":""}
                                    )


    

                                

    if kwargs['search_mode'] == "BENCHMARK_MDC_OFFLINE":
        segment_list_default = "/home/vasileios.skliris/public_html/benchmark_segments.txt"
    
    elif kwargs['search_mode'] == "FIRSTDETECTION_OFFLINE":
        
        segment_list_default = [1126249462, 1126269462]

    else:
        segment_list_default = []

    if len(kwargs['detectors'])==3: # Needs to be reevaluated
        skymap_config = dict(alpha = 2.2
                           , beta = 1.0
                           , sigma = 161.1 
                           , nside =64
                           , ramp_duration = 1/16
                           , ramp_center = 0
                           , duration_limit = 1/32)
                           
    elif len(kwargs['detectors'])==2: 
        if 'O3' in kwargs['search_mode']:
            skymap_config = dict(alpha = 2.0
                            , beta = 1.0
                            , sigma = 25.0 
                            , nside =64
                            , ramp_duration = 1/16
                            , ramp_center = 0
                            , duration_limit = 1/32)

        else:
            skymap_config = dict(alpha = 3.7
                                , beta = 1.0
                                , sigma = 20.5 
                                , nside =64
                                , ramp_duration = 1/16
                                , ramp_center = 0
                                , duration_limit = 1/32)


    # # # # # # # CONFIG FILE # # # # # # #

    configuration = dict(
        

    # Mode that creates some presets if used
    search_mode  = kwargs["search_mode"],
    # # # Directory organisation 
    
    output_directory = kwargs["output_directory"],
    trigger_directory = kwargs["trigger_directory"],
    masterDirectory = kwargs["masterDirectory"],
    bufferDirectory = kwargs["bufferDirectory"],
    falseAlarmRates = kwargs["falseAlarmRates"],
    efficiencies = kwargs["efficiencies"],
    log = "log",
    # Logging level
    log_level = "INFO",
        
    # User name
    
    user_name = os.environ['HOME'].split("/")[-1],


    accounting_group_user = os.environ['HOME'].split("/")[-1],
    # Acounting Group
    accounting_group = "ligo.dev.o4.burst.allsky.mlyonline",

    # Search directory path
    path = os.path.abspath(kwargs['path']),
    # Mirrored path directory to be used for the status page
    mirror_path = mirror_path,
    # # # Generator Parameters    
    
    # Num samples per second to feed into models.
    fs=1024,           
        
    # Time duration of segments to analyse (analysis window).
    duration=1,         
        
    # Number of segments to analyse, keep to 1 for real-time analysis.
    size=1,
    
    # Detectors used for this search
    detectors = kwargs['detectors'],
    
    # Frame file prefixes to use
    frames_directory= frames_dict[kwargs['search_mode']],
    
    # The channels to use, INJ is the MDC and NOISE is O3-replay
    channels = channels_dict[kwargs['search_mode']],

    # The state vector used, used only in online searces
    state_vectors = state_vector_dict[kwargs['search_mode']],

    # The active flag used
    active_flags= active_flags_dict[kwargs['search_mode']],

    segment_list = segment_list_default,

    max_continuous_segment = 5120 if "FIRSTDETECTION_OFFLINE" != kwargs['search_mode'] else 512,
    # # # Fetching data related parameters 

    # The number of search script running. (The number of scripts must be more than 
    # the time it takes to process one instance (second) of data.)
    parallel_scripts=4,

    # Number of seconds to wait between each read attempt.
    wait=0.5,
        
    # Number of seconds required for PSD calculation.
    required_buffer=16,  
        
    # Number of seconds before current GPS time to begin search.
    start_lag=64,
        
    # If search time is left behind by that amount of seconds it skips ahead.
    gps_reset_time=128,
        
    # FAR file that is used to calculate FAR. It is used only at
    # the beggining of the search, until there is enough background estimation.
    
    farfile= ("/home/vasileios.skliris/mly-hermes/outputs/FARfile" if ('ONLINE' in kwargs['search_mode']) else kwargs["falseAlarmRates"]+"/FARfile" ),
    
    # # # Models 
        
    # Model1 path, conincidence model.
    model1_path=("/home/mly/models/model1_32V_No5.h5"), 
        
    # Model2 path, coherence model.
    model2_path=("/home/mly/models/model2_32V_No6.h5"),  

    # # # Skymap parameters
    
    # Skymap parameters
    skymap = skymap_config,
        
    # # # Efficiency calculation parametersp

    # Testing configuration
    eff_config = dict( injectionDirectoryPath="/home/mly/injections/" # Injection directories
                      ,injectionsWithHRSS = ['SGE70Q3'
                                            ,'SGE153Q8d9'
                                            ,'SGL153Q8d9'
                                            ,'WNB250'] if "OFFLINE" not in kwargs['search_mode'] else []
                      ,injectionsWithSNR = ['cbc_20_20'
                                             ,'wnb_03_train_pod'
                                             ,'cusp_00'] if "OFFLINE" not in kwargs['search_mode'] else []
                      ,injectionHRSS = "1e-22,1e-21,1e-22"
                      ,injectionSNR =  "0,50,5"
                      ,testSize = "100"
                      ,howOften = 3600),

    far_config = dict( 
                    # Enabling or not the calculation of FAR.
                    far_enabled = not kwargs['nofar']
                    # Number of timelags used.
                    ,batch_size=1024
                    # It is used only at the beggining of a search until a FAR is estimated.
                    ,threshold = 2.3148e-05 if "OFFLINE" in kwargs['search_mode'] else 1/3600
                    # The score from which we keep FAR statistics.
                    ,restriction = 0.0001
                    # The maximum lag to be used. Determines the DataSet size of the saved instances.
                    ,max_lag = 3600
                    # The amount of lags to use for each file. Depends on the capasity to produce them.
                    ,lags = 1024 if "FIRSTDETECTION_OFFLINE" != kwargs['search_mode'] else 16
                    # Then number of condor jobs per file to be used for timelags. With a file of
                    # size 3600 (max_lag) this will create jobs that will produce files
                    # of ~3600*lags/batches. Change with caution.
                    ,batches = 64 if "FIRSTDETECTION_OFFLINE" != kwargs['search_mode'] else 8
                    # GPU devices to use. If not defined it will just load the local visible ones.
                    ,visible_gpu_devices = "local"
                    # The GPU number(s)) (run nvidia-smi to see the numbers), to use for the tests.
                    ,selectedGPUs = [0]
                    # Maximum amount of dags to run at the same time in condor for the generation of data.
                    ,parallelGenerations = 3
                    ),
                         
    # # # MISC
    # Extra condor attributes to be added to jobs
    condor_submit_requirements = ["Has_sse4_1 == True",
                                  "TARGET.Online_MLy == True"] if "ONLINE" in kwargs['search_mode'] else ["Has_sse4_1 == True"],
    condor_submit_extra_lines = ["my.Online_MLy = True",
                                 "request_memory = 4G",
                                 "request_disk   = 4G"] if "ONLINE" in kwargs['search_mode'] else ["request_memory = 4G",
                                                                                                   "request_disk   = 4G"],
    # The group size of the files that used to save the outputs    
    maxDataFrameSize = 3600,
    # The destination of the triggers, None means testing mode with FAKEIDs.
    trigger_destination = "playground" if kwargs['search_mode'] in ["O3MDC_ONLINE"] else None,
    # For the online search only
    trigger_group = "Burst" if 'ONLINE' in kwargs['search_mode'] else None,
    # Random number generator seed
    seed = 921101

    

    )


    os.system("mkdir " + configuration['path'] +"/"+ configuration['output_directory'])
    os.system("mkdir " + configuration['path'] +"/"+ configuration['trigger_directory'])
    os.system("mkdir " + configuration['path'] +"/"+ configuration['log'])

    os.system("mkdir " + configuration['path'] +"/"+ configuration['masterDirectory'])
    os.system("mkdir " + configuration['path'] +"/"+ configuration['masterDirectory'] +"/temp")
    for det in configuration['detectors']:
        os.system("mkdir " + configuration['path'] +"/"+ configuration['masterDirectory'] +"/"+ det)
        os.system("mkdir " + configuration['path'] +"/"+ configuration['masterDirectory'] +"/temp/"+ det)

    os.system("mkdir " + configuration['path'] +"/"+ configuration['bufferDirectory'])
    os.system("mkdir " + configuration['path'] +"/"+ configuration['bufferDirectory'] +"/temp")

    os.system("mkdir " + configuration['path'] +"/"+ configuration['efficiencies'])
    os.system("mkdir " + configuration['path'] +"/"+ configuration['efficiencies'] +"/history")

    if not kwargs['nofar']:

        os.system("mkdir " + configuration['path'] +"/"+ configuration['falseAlarmRates'])
        os.system("mkdir " + configuration['path'] +"/"+ configuration['falseAlarmRates']+"/hourly")
        os.system("mkdir " + configuration['path'] +"/"+ configuration['falseAlarmRates']+"/FARfile")
        os.system("mkdir " + configuration['path'] +"/"+ configuration['falseAlarmRates']+"/condor")
        os.system("mkdir " + configuration['path'] +"/"+ configuration['falseAlarmRates']+"/temp")
        
    # Saving config file to json format
    with open(configuration['path'] +"/"+"config.json", "w") as config_json:
        json.dump(configuration, config_json,indent=4)
        config_json.close()

    
    createRunAllScript(**configuration)

def _start_search():

    #Construct argument parser:
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--search_path', type=str
                        , default = "./"
                        , help = "The path to the search to start"
                        , required = False)

    # Pass arguments:
    args = parser.parse_args()
    

    search_path = getattr(args, "search_path")      

    if os.path.isfile(search_path+"runall.sh"):

        os.system(f"cd {search_path} ; nohup bash runall.sh &> runall.out & echo $!>>.jobids.txt")
        print("Search has started!")

    else:

        raise FileNotFoundError(f"The path provided {search_path} does not have a runall.sh file to start the search.")

      
def _end_search():

    #Construct argument parser:
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--search_path', type=str
                        , default = "./"
                        , help = "The path to the search to start"
                        , required = False)

    # Pass arguments:
    args = parser.parse_args()
    

    search_path = getattr(args, "search_path")      
    if os.path.isfile(search_path+".jobids.txt"):

        with open(f"{search_path}/.jobids.txt", "r") as idfile:
            idfile_ = idfile.read()
  
        # replacing end of line('/n') with ' ' and
        # splidfile.read()
    
        # replacing end of line('/n') with ' ' and
        # splitting the text it further when '.' is seen.
        job_id_list = idfile_.replace('\n', ' ').split(" ")
    
        for id_ in job_id_list:
            try:
                os.system(f"kill {str(id_)} >/dev/null 2>&1")#,stderr=subprocess.STDOUT)
            except Exception as e:
                pass

        try:
            os.system(f"singularity instance stop --all >/dev/null 2>&1")
        except Exception as e:
            pass

        os.system(f">{search_path}/.jobids.txt")

        print("Search stopped")
    else:

        raise FileNotFoundError(f"The path provided {search_path} does not have a .jobids.txt file to start the search.")


def _status_page():

    from .manager import manage_status_page
    manage_status_page()

def _search_status():

    #Construct argument parser:
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--n', type=int
                        , default = "3"
                        , help = "The number of lines to show from the file."
                        , required = False)
    
    parser.add_argument('-p', '--search_path', type=str
                        , default = "./"
                        , help = "The path to the search to start"
                        , required = False)

    # Pass arguments:
    args = parser.parse_args()
    

    search_path = getattr(args, "search_path") 
    n = getattr(args, "n") 
    with open('monitor.log', 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines[-n:], start=1):
        if i == n:
            print("\033[1m" + line.strip() + "\033[0m")  # Use ANSI escape codes for bold text
        else:
            print(line.strip())
    


def get_file_counts_after_createFileSystem():

    with open('config.json') as json_file:
        config = json.load(json_file)
    
    master_directory = config['masterDirectory']
    detectors = config['detectors']
    # Counting files after the createFileSystem
    file_counts = {}
    for detector in detectors:
        path = os.path.join(master_directory, detector)
        file_counts[detector] = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])

    common_files = set.intersection(*(set(os.listdir(os.path.join(master_directory, detector))) for detector in detectors))

    if len(set(file_counts.values())) == 1:
        print("All detectors have the same number of files. Successful jobs: ")
    else:
        # Deleting files that are not in all detectors.
        for detector in detectors:
            path = os.path.join(master_directory, detector)
            non_common_files = set(os.listdir(path)) - common_files
            for file_name in non_common_files:
                #print(os.path.join(path, file_name))
                os.remove(os.path.join(path, file_name))
        
        print("Some files not present in all directories, were removed. Successful jobs: ")

    final_file_counts = min([file_counts[detector] for detector in detectors])
    print(final_file_counts)


if __name__ == "__main__":
    
     main()

