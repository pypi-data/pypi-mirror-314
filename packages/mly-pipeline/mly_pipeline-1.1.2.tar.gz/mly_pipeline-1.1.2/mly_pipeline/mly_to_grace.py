#! /usr/bin/env python3

import os, json, math, time

# Scipy and numpy env parameters that limit the threads
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import argparse
import numpy as np
import matplotlib.pyplot as plt

from lal import gpstime
from ligo.gracedb.rest import GraceDb

# # # Managing arguments
# 
# List of arguments to pass:
arguments = [
    "trigger_destination",
    "triggerfile",
]

#Construct argument parser
parser = argparse.ArgumentParser()
[parser.add_argument(f"--{argument}") for argument in arguments]

# Pass arguments
args = parser.parse_args()

# Store arguments in dictionary
kwargs = {}
for argument in arguments:
    kwargs[argument] = getattr(args, argument)

# Config file is inherited by the search script updated
with open('config.json') as json_file:
    config = json.load(json_file)


"""This function issues a GraceDB event provided with a json file.

Parameters
----------


trigger_destination: {'test, 'playground', 'dev1', None}
    The GraceDB domain for the triggers to be uploaded. Each option represent
    a corresponding url. If equals to None, it will not issue an GraceDB event.

triggerfile : 'str'
    The path to the json file to use for the event.

"""

# print("Main beggining: ",gpstime.gps_time_now()- float(kwargs['triggerfile'].split('_')[-2]))
# Argument checks

if kwargs['triggerfile']!=None:

    if os.path.isfile(kwargs['triggerfile']):
        triggerfile = kwargs['triggerfile']
    else:
        raise FileNotFoundError(
            kwargs['triggerfile'] +
            " is not a valid file path")
else:
    raise FileNotFoundError("You need to specify the trigger file path.")




# # # Push to GraceDb

# Checking latencies
gpsbefore = gpstime.gps_time_now()

# If the authentication is correct and we can send events, trigger_destination
# can be defined.


if kwargs['trigger_destination'] != 'None':

    url=kwargs['trigger_destination']

    client = GraceDb(service_url=url)

    graceEventOutput = client.create_event(group=config["trigger_group"], 
                                           pipeline="MLy",
                                           filename=triggerfile,
                                           search="AllSky",
                                           labels = ['PE_READY'])
    
    graceEventDict = graceEventOutput.json()
    
    print(triggerfile+" uploaded to "+url)

# Otherwise for just testing we can create a fake id to use.
else:
    
    graceEventDict = {'graceid':'FAKEID'+str(np.random.randint(999999))}

# Checking latency from the GPS time involved    
print("Latency before opening client: ",gpsbefore- float(kwargs['triggerfile'].split('_')[-2]))
timeafterclient = time.time()

# # # Extra features to be added
#
# To this point an event is created. The following is to be added after the
# event creation in the future. Some arguments are checked here so that 
# they don't contribute to the event latency until their feature is used



from mly.datatools import DataPod

# Loading the pod that has all the data that produced the trigger
thepod = DataPod.load(triggerfile[:-4]+'pkl')

gpsstring=triggerfile.split('_')[-2]
detectors=triggerfile.split('.')[-2].split('_')[-1]

# Renaming the already created tempEventDirectory to one with the gracedb id in the name

temp_eventDirectory = 'tempEventDirectory_'+gpsstring
# Creating a directory for each event using the graceid from the event creation.
# Not always works.
try:
    eventDirectory = graceEventDict['graceid']+'-'+gpsstring+'-'+detectors
except Exception as e:
    print(e)
    eventDirectory = 'NoGraceID'+'-'+gpsstring+'-'+detectors

# Renaming the event directory
os.rename(  f"{config['trigger_directory']}/{temp_eventDirectory}"
          , f"{config['trigger_directory']}/{eventDirectory}")

# Creating the strain plot
thepod.plot(type_="strain")
plt.savefig(f"{config['trigger_directory']}/{eventDirectory}/T_{gpsstring}_{detectors}_strain.png")

# Creating the correlation plot
thepod.plot(type_="correlation")
plt.savefig(f"{config['trigger_directory']}/{eventDirectory}/T_{gpsstring}_{detectors}_correlation.png")

thepod.plot('tf_map')
plt.savefig(f"{config['trigger_directory']}/{eventDirectory}/T_{gpsstring}_{detectors}_tfmap.png")

if config['skymap']:

    from .search_functions import summary_plot
    from mly.skymap_utils import skymap_plugin, containment_region
    from mly.plugins import PlugIn
    from ligo.skymap.io import fits
    from ligo.skymap.moc import nest2uniq 
    import astropy_healpix as ah
    import healpy as hp
    from tensorflow.config import threading

    threading.set_inter_op_parallelism_threads(1)
    threading.set_intra_op_parallelism_threads(1)

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

    skymap_path = f"{config['trigger_directory']}/{eventDirectory}/mly.multiorder.fits"
    
    skymap_prob = thepod.sky_map[0]

    order = int(math.log2(config['skymap']['nside']))
    npix = ah.nside_to_npix(config['skymap']['nside'])

    uniq = nest2uniq(np.uint8(order), np.arange(npix))
    probdensity = skymap_prob / hp.nside2pixarea(config['skymap']['nside'])

    moc_data = np.rec.fromarrays(
        [uniq, probdensity], names=['UNIQ', 'PROBDENSITY'])

    # Standard metadata needed for the headers
    skymap_metadata = {'objid' : graceEventDict['graceid'],
                    'instruments': set(d+'1' for d in detectors),
                    'gps_time' : float(gpsstring),
                    'origin' : 'LIGO/Virgo/KAGRA'
                    }

    with open(skymap_path, "w") as f:
        fits.write_sky_map( skymap_path, moc_data, **skymap_metadata)
    
    # Upload skymap to grace db:
    if kwargs['trigger_destination'] != 'None':

        client.write_log(graceEventDict['graceid'], 'Sky Localization',  filename=skymap_path, tag_name='sky_loc')
        client.write_label(graceEventDict['graceid'], 'SKYMAP_READY')
    
    print("Latency after skymap log: ",time.time()-timeafterclient)

    thepod.plot('sky_map')
    plt.savefig(f"{config['trigger_directory']}/{eventDirectory}/T_{gpsstring}_{detectors}_skymap.png")
    
    summary_plot(thepod,config,save_path= f"{config['trigger_directory']}/{eventDirectory}/T_{gpsstring}_{detectors}_summary.png")

    if kwargs['trigger_destination'] != 'None':

        plot_string = f"{config['trigger_directory']}/{eventDirectory}/T_{gpsstring}_{detectors}"

        #client.write_log(graceEventDict['graceid'], 'TimeSeries Plot',  filename=f"{plot_string}_strain.png", tag_name='strain')
        #client.write_log(graceEventDict['graceid'], 'Correlation Plot',  filename=f"{plot_string}_correlation.png", tag_name='strain')
        client.write_log(graceEventDict['graceid'], 'Time-Frequency Map',  filename=f"{plot_string}_tfmap.png", tag_name='tfplots')
        client.write_log(graceEventDict['graceid'], 'Skymap Probability',  filename=f"{plot_string}_skymap.png", tag_name='sky_loc')
        client.write_log(graceEventDict['graceid'], 'Summary Plot',  filename=f"{plot_string}_summary.png", tag_name='em_follow')


raise SystemExit()

# if __name__ == "__main__":


#     main(**kwargs)

#     quit()
