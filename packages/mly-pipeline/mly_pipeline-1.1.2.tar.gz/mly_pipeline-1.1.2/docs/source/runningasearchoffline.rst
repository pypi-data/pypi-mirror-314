.. _Offline_search_timeline:

Offline search timeline
#######################

For the offline search the timeline is more linear. Remember that you have to specify the **segments** entry in the config file ([start , stop] or path to segments file), for this search to run.

How to check the status of the search
=====================================
To check the status of the search you should run ``mly-pipeline-status -n <lines>`` from within the search directory. 
This will show in your terminal the last three (or however many lines you pass to the -n argument) entries of the ``monitor.log`` with a time stamp. 
You can investigate ``monitor.log`` file yourself that is located in the search directory. The parts of the search that are documented in the monitor.log are the ones below.

Setting file system
===================

The first step is to get coinsident available segments of the detectors specified. 
The available segments are processed second by second and saved in hourly groups in dataset objects inside masterdirector/<detector> directories.

Background estimation
=====================

Before we do the search we first create a background estimation using the segments that are downloaded. 
Note that this part of the search will start when the first data file from the previous step is completed.
The process of doing that is the same with the online search with the only difference that the time-lagged files generated are finite.
Both continues_FAR -generation and continuous_FAR -inference scripts are running in paralell until all timelagged files have been passed through the models 
and have produced the corresponding inference files. 

Every five minutes there is a check that the scripts run correctly and a managing function is used to create the FAR_file and the interpolations of the background curve function. 
From them we can calculate the FAR for each event and also the score corresponding to the **threshold** parameter used to separate events.


Offline search
==============

This is just running all the processed data segments through the models.
When an instance has bigger FAR that the threshold it is saved inside the trigger_directory with its own event directory.
All the rest of the instances results are saved in pandas dataframes (.pkl) in chunks (default is 10000) in output_directory.

.. Efficiency test (not working yet)
.. =================================
.. At the same time as the search, efficiency test script is lunched to produce plots of efficiency tests.

The status page
===============

When the search is complete, the status page will be created automatically. To access it you can find the link to it at the end of the monitor.log page (``mly-pipeline-status``)