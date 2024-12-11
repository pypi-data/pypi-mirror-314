#!/usr/bin/env python

import os
import time ,json, argparse, subprocess

import numpy as np
import pickle
import matplotlib.pyplot as plt

from gwpy.time import from_gps
from pycondor import Job, Dagman
from mly.datatools import DataSet
from mly.validators import Validator
from mly.tools import *


from .search_functions import far, stackVirgo

with open('config.json') as json_file:
    config = json.load(json_file)

config = stackVirgo(config)

np.random.seed(config['seed'])

#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

which_python = str(subprocess.check_output(['which','python']))[2:-3]
print(which_python)

# # # Managing arguments
# 
# List of arguments to pass:
arguments = ['mode','injectionPath','injectionSNR','injectionHRSS','group_directory']

#Construct argument parser:
parser = argparse.ArgumentParser()

parser.add_argument('--mode')
parser.add_argument('--injectionPath')
parser.add_argument('--injectionSNR' , default = None)
parser.add_argument('--injectionHRSS', default = None)
parser.add_argument('--group_directory', default = None)

# Pass arguments
args = parser.parse_args()

# Store arguments in dictionary:
kwdict = {}
for argument in arguments:
    kwdict[argument] = getattr(args, argument)


def moving_average(x, w):
    ma=[]
    for i in range(len(x)):
        if i<int(w/2)+1:
            ma.append(np.mean(x[:i+1]))
        elif i>=len(x)-(w/2+1):
            ma.append(np.mean(x[i:]))
        else:
            ma.append(np.mean(x[i-int(w/2):i+int(w/2)]))

    return np.array(ma)


def main():
    
    mode = kwdict['mode']
    
    if mode=='test':

        size = int(float(config["eff_config"]["testSize"]))
        injection_path = kwdict['injectionPath']
        noiseSource = "BUFFER_SET.pkl"#config["bufferDirectory"]+"/BUFFER_SET.pkl"
        injectionSNR = kwdict["injectionSNR"]
        injectionHRSS = kwdict["injectionHRSS"]
        group_directory = kwdict["group_directory"]


        print("INJSNR",injectionSNR, type(injectionSNR))
        print("INJHRSS",injectionHRSS, type(injectionHRSS))
        if injectionSNR != None:

            injectionSNR = np.array(list(float(_) for _ in injectionSNR.split(',')))
            injectionSNR = np.arange(injectionSNR[0], injectionSNR[1], injectionSNR[2]).tolist()

        if injectionHRSS != None:
            injectionHRSS = np.array(list(float(_) for _ in injectionHRSS.split(',')))
            injectionHRSS = np.arange(injectionHRSS[0], injectionHRSS[1], injectionHRSS[2]).tolist()


        print("INJSNR",injectionSNR)
        print("INJHRSS",injectionHRSS)
        noiseSource = DataSet.load(noiseSource)
        gps_time_start = int(noiseSource[0].gps[0])
        gps_time_end = int(noiseSource[-1].gps[0])

        models = [[config['model1_path'],config['model2_path']]
                  ,[["strain"], ["strain", "correlation"]]]

        # print(models)
        # print(injectionSNR)
        # print(injectionHRSS)
        print('injection_path: ',injection_path)
        t0=time.time()
        print("savefile",group_directory+f"{injection_path.split('/')[-1]}_{gps_time_start}-{gps_time_end}")

        if 'V' not in config['detectors']:
            efficiencies = Validator.accuracy(models=models, 
                                        duration=1, 
                                        size=size,
                                        fs=1024,
                                        detectors=config['detectors'], 
                                        labels={"type": "signal"},
                                        backgroundType="real",
                                        injection_source=injection_path,
                                        injectionSNR = injectionSNR,
                                        noiseSourceFile = noiseSource,
                                        windowSize = 16, 
                                        plugins=["correlation_30"], 
                                        mapping=2 * [{"noise":[ 1, 0], "signal":[0, 1]}],
                                        name=f"{injection_path.split('/')[-1]}_{gps_time_start}-{gps_time_end}",
                                        savePath = "./",
                                        injectionHRSS = injectionHRSS, #list(np.arange(0, 100) * 1e-23)
                                        stackDetectorDict = config['stackDetectorDict']
            )   


        else:
            efficiencies = Validator.accuracy(models=models, 
                                duration=1, 
                                size=size,
                                fs=1024,
                                detectors=config['detectors'], 
                                labels={"type": "signal"},
                                backgroundType="real",
                                injection_source=injection_path,
                                injectionSNR = injectionSNR,
                                noiseSourceFile = noiseSource,
                                windowSize = 16, 
                                plugins=["correlation_30"], 
                                mapping=2 * [{"noise":[ 1, 0], "signal":[0, 1]}],
                                name=f"{injection_path.split('/')[-1]}_{gps_time_start}-{gps_time_end}",
                                savePath = "./",
                                injectionHRSS = injectionHRSS
                                )#list(np.arange(0, 100) * 1e-23))]]

        print(time.time()-t0)
        #return efficiencies
    
    elif mode=='plot':
        
        farfile_inverse_interpolation = "FARfile_interpolation_inverse.pkl"

        thresholds = {#'10year': far(farfile_inverse_interpolation, 1/(10*365*24*3600) , inverse = True)
                      '4years': far(farfile_inverse_interpolation, 1/(4*365*24*3600) , inverse = True)
                      ,'1year': far(farfile_inverse_interpolation, 1/(1*365*24*3600) , inverse = True)
                      ,'12hours': far(farfile_inverse_interpolation, 1/(12*3600) , inverse = True)

                     }

        print(thresholds)
        
        tkeys=list(thresholds.keys())  

        files_in_directory = os.listdir("./")
        tests= [file for file in files_in_directory if file.endswith('.pkl') and "FARfile" not in file]
        
        buffer_start_time = from_gps(int(tests[0].split("_")[-1][:-4].split('-')[0]))
        buffer_extention = f"{(config['eff_config']['howOften']/3600):.1f}"

        colours=['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']

        fig,ax=plt.subplots(2,3,figsize=(15,10))

        ACC50={}

        for t in range(len(tkeys)):
            ACC50[tkeys[t]]={}

            for l in range(len(tests)):
                label = tests[l].split('_')[0]

                with open(tests[l],'rb') as handle: data= pickle.load(handle)

                print(tests[l])
                acc=[]
                
                if 'hrss' in data.keys():
                    looper = data['hrss']
                    xlabel = 'hrss'
                    
                    for hrss in range(len(looper)):
                        count=0
                        for sc in np.array(data['scores1'][hrss])*np.array(data['scores2'][hrss]):
                            if sc>=thresholds[tkeys[t]]: count+=1
                        acc.append(100*count/len(np.array(data['scores1'][hrss])*np.array(data['scores2'][hrss])))
                    
                    #ax[0,t].plot(looper,moving_average(acc,10),label=label,color=colours[l])
                    ax[0,t].plot(looper,acc,label=label,color=colours[l])

                    mvave=moving_average(acc,10)
                    for snr in range(1,len(looper)):

                        if mvave[snr]>50 and mvave[hrss-1]<=50:
                            ACC50[tkeys[t]][label]=looper[snr]


                    ax[0,t].set_title(f"IFAR {tkeys[t]}")

                    ax[0,t].set_xlabel(xlabel)
                    ax[0,t].set_ylim(0,100)
                    ax[0,t].grid(True,which='both')



                elif 'snrs' in data.keys():
                    looper = data['snrs']
                    xlabel = 'SNR'
                    
                    
                    for snr in range(len(looper)):
                        count=0
                        for sc in np.array(data['scores1'][snr])*np.array(data['scores2'][snr]):
                            if sc>=thresholds[tkeys[t]]: count+=1
                        acc.append(100*count/len(np.array(data['scores1'][snr])*np.array(data['scores2'][snr])))
                        
                    #ax[1,t].plot(looper,moving_average(acc,10),label=label,color=colours[l])
                    ax[1,t].plot(looper,acc,label=label,color=colours[l])

                    mvave=moving_average(acc,10)
                    for snr in range(1,len(looper)):

                        if mvave[snr]>50 and mvave[snr-1]<=50:
                            ACC50[tkeys[t]][label]=looper[snr]

                    ax[1,t].set_xlabel(xlabel)
                    ax[1,t].set_ylim(0,100)
                    ax[1,t].grid(True,which='both')

                
        ax[0,0].set_ylabel("% of signals detected")
        ax[1,0].set_ylabel("% of signals detected")

        ax[0,2].legend()
        ax[1,2].legend()
        fig.suptitle(f"Efficiencies at {buffer_start_time} + {buffer_extention}h", fontsize=25)

        fig.savefig('./Efficiencies.png')
        fig.savefig('./Efficiencies_copy.png')


            
    elif mode=='condor':
        
        
        noiseSource_path = f"./{config['bufferDirectory']}/BUFFER_SET.pkl"
        noiseSource = DataSet.load(noiseSource_path)
        gps_time_start = int(noiseSource[0].gps[0])
        gps_time_end = int(noiseSource[-1].gps[0])
        group_directory = f"{config['efficiencies']}/history/{gps_time_start}-{gps_time_end}/"

        os.mkdir(group_directory)


        accounting_group_user=config['accounting_group_user']
        accounting_group=config['accounting_group']

        injSourceDir = config["eff_config"]["injectionDirectoryPath"]
        
        # These are writen on the condor node so the need a path that works
        # on the condor node independently from the submition node.
        error = f"./{group_directory}condor/error"
        output = f"./{group_directory}condor/output"
        # These two are not writen from the condor node so relative path is fine.
        log = f"{group_directory}condor/log"
        submit = f"{group_directory}condor/submit"
        dagman = Dagman(name='efficiencyTestDagman',submit=submit)


        injection_paths_HRSS =  config["eff_config"]["injectionsWithHRSS"]
        
        injection_paths_SNR = config["eff_config"]["injectionsWithSNR"]

        
        job_list=[]
        output_files = "" # Will be used for the plot job
        for injection_path in injection_paths_HRSS:
            
            output_file = f"{injection_path.split('/')[-1]}_{gps_time_start}-{gps_time_end}.pkl"
            print('output_file:',output_file)

            print(injSourceDir+injection_path)
            output_files += f"{group_directory}{output_file},"
            jobname = injection_path.split('/')[-1]
            thearguments = ( "-m mly_pipeline.make_eff_estimation"
                             +" --mode=test" 
                             +" --injectionPath="+injSourceDir+injection_path
                             +" --injectionHRSS="+config['eff_config']['injectionHRSS']
                             +" --group_directory="+group_directory)




            job = Job(name = jobname
                       ,executable = which_python
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
                                    ,f"transfer_input_files    = {noiseSource_path},config.json"
                                    ,f"transfer_output_files   = {output_file}"
                                    ,f"transfer_output_remaps = \"{output_file} = {group_directory}{output_file}\""
                                    ,"should_transfer_files   = YES"
                                    ,"when_to_transfer_output = ON_EXIT"] + config['condor_submit_extra_lines'])

            job_list.append(job)
            
            
            
            
            
        for injection_path in injection_paths_SNR:

            output_file = f"{injection_path.split('/')[-1]}_{gps_time_start}-{gps_time_end}.pkl"
            print('output_file:',output_file)

            print(injSourceDir+injection_path)
            output_files += f"{group_directory}{output_file},"
            jobname = injection_path.split('/')[-1]
            thearguments = ( "-m mly_pipeline.make_eff_estimation"
                             +" --mode=test" 
                             +" --injectionPath="+injSourceDir+injection_path
                             +" --injectionSNR="+config['eff_config']['injectionSNR']
                             +" --group_directory="+group_directory)





            job = Job(name = jobname
                       ,executable = which_python
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
                                    ,f"transfer_input_files    = {noiseSource_path},config.json"
                                    ,f"transfer_output_files   = {output_file}"
                                    ,f"transfer_output_remaps = \"{output_file} = {group_directory}{output_file}\""
                                    ,"should_transfer_files   = YES"
                                    ,"when_to_transfer_output = ON_EXIT"] + config['condor_submit_extra_lines'])

            job_list.append(job)


        plot_job = Job(name = 'plotJob'
                   ,executable = which_python
                   ,arguments = ( " -m mly_pipeline.make_eff_estimation"
                                 +" --mode=plot"
                                 +f" --group_directory={gps_time_start}-{gps_time_end}")
                   ,submit=submit
                   ,error=error
                   ,output=output
                   ,log=log
                   ,getenv=True
                   ,dag=dagman
                   ,requirements=" && ".join(config['condor_submit_requirements'])
                   ,extra_lines=["accounting_group_user="+accounting_group_user
                                ,"accounting_group="+accounting_group
                                ,f"transfer_input_files    = {output_files}{config['farfile']}/FARfile_interpolation_inverse.pkl,config.json"
                                ,f"transfer_output_files   = Efficiencies.png,Efficiencies_copy.png"
                                ,f"transfer_output_remaps = \"Efficiencies_copy.png={group_directory}Efficiencies.png\""
                                ,"should_transfer_files   = YES"
                                ,"when_to_transfer_output = ON_EXIT"] + config['condor_submit_extra_lines'])

        plot_job.add_parents(job_list)


        dagman.build_submit()

if __name__ == "__main__":
    main()
