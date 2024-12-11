.. _Setting_up_a_search:

Setting up a search
###################


Setting up directories
======================

To run an MLy-Pipeline search we need a directory structure that will be used 
by the features of the pipeline. To make the creation of such directory 
structure easy we have a command automate the creation for us. With the installation of MLy-Pipeline there are soem commands that you can run from the terminal
to initialize a search. To create a search directory you should use ``mly-pipeline-init`` comand as shown below:

.. code-block:: bash
    
    mly-pipeline-init -p ./mysearch
    
Where instead of ``mysearch`` you can use a more apropriate name that fits your
need. The command above will create the directory ``./mysearch`` and also the subdirectories
below (these are their default names):

    - trigger_directory
    - output_directory
    - masterDirectory
    - bufferDirectory
    - falseAlarmRates
    - efficiencies
    - log
You can change the names of these directories by adding their new names as extra
parameters in the command. For example if we want to have a custom name for 
masterDirectory we can do:
    
.. code-block:: bash
    
    mly-pipeline-init -p ./mysearch --masterDirectory customName
    
This applies for all the other directories.

In addition to that, inside the search directory, it will also create a script to run the search called runall.sh
and the config.json file that has the parameters that are used by the search.
**It is up to the user to change those parameters to conduct the search the way they want.**

Running the search under different circumstances
------------------------------------------------

You might want to just run the search as it would be run in low latency (in real time).
In case you want to run the search on MDC data for example, which means you need a fixed background, then
there is a light version of the same command. When we run on MDC we do not need some of the 
directories, and also some configuration parameters will need to change to ignore specific
functionalities. The comand below will create a version of the search that does not do the
continuous FAR estimation and neither does efficiency tests. It also points the search to the 
MDC frames and channels.

.. code-block:: bash
    
    mly-pipeline-init -p ./mysearch --search_mode O3MDC_ONLINE --nofar

For the case of an MDC search or any search that the background is already tested and ready, you can
use the parameter `--nofar` to prevent the search from doing background analysis at the same time.

.. note:: You can use the same "search_mode" to initialize a search directory for a mock data challenge that
   has different frames and channels. The only thing you need to do is go to the config file 
   (see below) and edit the frame_directory and channels parameter.

Another example of similar special initialization is an offline search. For an offline --search_mode O3MDC_ONLINE
Bellow we show the example for a two detector search. Note that the default is three detector search (HLV).
There are no other options than HL and HLV.

.. code-block:: bash
    
    mly-pipeline-init -p ./mysearch -d HL 

Finally a way to test that the offline version of the pipeline works as expceted to intialise the following search:

.. code-block:: bash

  mly-pipeline-init -p firstdetection -d HL -s FIRSTDETECTION_OFFLINE

This is a testing example around the time of GW150914.


The runall.sh script
====================

Online search
-------------

The ``runall.sh`` is the only thing that you need to run from inside ``./mysearch`` 
(or however you named it) directory for the search to comence. Processing a second
during a search, doing inference and issiuing a possible alert takes more than a second. For that reason we split our 
search into many scripts to avoid queing delays. Hence is only one parameter that 
can be adjusted in the inside the runall script and that is the ``STEP`` parameter.
This paramater breaks the search into ``STEP`` in number, non overlaping scripts. 
The search as it is takes around 2 to maximum 3 seconds (rarely) to process a second.
To be sure we set the ``STEP=4`` in case there are any delays. We suggest that 
you keep that parameter fixed unless there is strong evidence that the latency 
of individual scripts is bigger than ``STEP``.

Inside the ``runall.sh`` script you will three main functions to be called, 
``search.py`` , ``manager.py`` and ``continuous_FAR.py``. 

* ``search.py`` runs the online search, saves the outputs and issues events when the output is bigger than the threshold where we define detections. The event creation is a paralell process that sends an alert to GraceDB and creates an event directory with the name of the GraceDB id. Inside this directory. it also creates plots of the data fed to the model and the skymap.

* ``manager.py`` runs every 5 minutes. It organises all outputs into pandas data frames (saved in pickle format) and in fixed intervals it runs efficiency tests. It also creates plots and clears files that no longer are needed.

* ``continuous_FAR.py`` is called with two different parameters does two things in parallel.
  
  * ``continuous_FAR.py --mode generation`` takes the data of the last hour saved in the masterDirectory and generates condor jobs. Each jobs greates a specific amount of timeshifted versions of these data and saves them in a temporary file in the scrach directory (falseAlarmRates/temp), ready to be used for background testing.
  
  * ``continuous_FAR.py --mode inference`` does inference on the data generated using available GPUs or the GPUs specified in ``selectedGPUs`` parameter. This script will load any time-lag data available and return a pandas data frame with the results. The asemble of those files is done by the managers script.

Offline search
--------------

For searches that run offline there is only one script that will be run through the runall.sh and that is:

* ``offline_search.py`` It runs the offline search by breaking the searh in jobs equivalent to the segments provided. It also does all the management of events.


Configuration File
==================

All the above functions get their parameters from the ``config.json`` file. Below we are going to give descriptions about each config parameter. By changing the 
config you change the way the search will run, so make sure that you check that
config is the way you want it after you create the search directory. 


File Names and Paths 
--------------------

The following are just the directory names of the directories created by with 
the ``initialization.py``. If the default names were used, this will look like:

* **output_directory**:"output_directory"
* **trigger_directory**:"trigger_directory"
* **masterDirectory**:"masterDirectory"
* **bufferDirectory**:"bufferDirectory"
* **falseAlarmRates**:"falseAlarmRates"
* **efficiencies**:"efficiencies"
* **log**:"log"

The log level that will be used for the log files.
* **log_level**:"INFO"


User and accounting group for condor jobs.

* **user_name**: This is automatically filled by the enviroment

* **accounting_group_user**: It defaults to be the same as user_name.

* **accounting_group**: "ligo.dev.o4.burst.allsky.mlyonline"

This is the name of the search directory, in our case it will look like:

* **path** :"./mysearch"

This is the name of a mirror directory that is used to make the results of the search visible if not by default.
For ligo cluster use, by default if you initialise the search within local directory,
the mirror will be in home/<albert.einstein/public_html>.

* **mirror_path** :"<another path>/mysearch" or "not-defined"
    
Generator Function Parameters
-----------------------------

The following parameters are passed to the generator function that processes
the data before inference. The values assigned are the default values.

* **fs**:1024 Sample frequency
* **duration**:1 Duration of processing window
* **detectors**:"HLV" Detectors used for the search

The prefix dictionary of the paths of directories where O3-replay and MDC data are. If the
source of the data you use is different, you need to edit this parameter, after
creating the search directory.

* **frames_directory**: A dictionary with entries for H, L and V for the detectors. For each detector it has a path to the directory of the frame files that are going to be used or a frame name recognised by gwdatafind. The default is empty but if you specified a mode of initialization then this will be filled with the respective paths.

* **channels**: Also a dictionary with entries for H, L and V for the detectors. For each detector it has the channel that is going to be used. The default is empty but if you specified a mode of initialization then this will be filled with the respective channels.

* **state_vectors**: Dictionary with the statevectors used only for the online search. For anything else, it is empty. 

* **segment_list**: This can be a path to a file that has segment intervals or it can be a list of two intervals corresponding to a start GPS time and an end GPS time. It is used only in offline searches. It defaults to an empty list.

* **active_flags**: Dictionary with the respective active flags for each detector. The default are the observing ones for each run.

* **segment_list**: A list or SegmentList of the segments to be used for an offline search. It is an empty list otherwize.

* **max_continuous_segment**: If the segments provided are too big we might want to break them in smaller runs. This parameter is the minimum segment size that will be used for one job. Also used only during offline searches. Defaults to 10000.


Requesting Data Parameters
--------------------------
* **parallel_scripts**: 4 This is the STEP parameter inside the runall.sh script (see above).
* **wait**:0.5 Time to wait before requesting a segment of data again
* **timeout**:20 How many times to try requesting a data segment before going to the next.
* **required_buffer**:16 How many seconds of data to request.
* **start_lag**:92 How many seconds before the current gps time to start the search from. We expect that given the reset time below this will be reseted in the first attempt.
* **gps_reset_time**:32 The amount of time difference in seconds where we reset the gps that we request to the current one. This is for cases where latency is running behind momenterily.
* **farfile**: "/home/vasileios.skliris/mly-hermes/outputs/FARfile" The path to an initial FAR directory. When the search starts there will be no background estimation yet. This will take sometime to be produced and until then we use another background. **The initial FAR estimation will be used until one year of background has been estimated. Then the manager will overight this path to the path of the search**: ``mysearch/falseAlarmRates/FARfile``

Models
------
* **model1_path**:"/home/mly/models/model1_32V_No5.h5" Coincidence model (model 1).
* **model2_path**:"/home/mly/models/model2_32V_No6.h5" Coherency model (model 2).

Skymap
------
* **skymap**: A dictionary of parameters related to the skymap generation after triggers.

  * **alpha**: The power of the contributin of the antena patern.

  * **beta**: 1.0. A power parameter that currently is not used.

  * **sigma**: The parameter inside the normalization exponential. 

  * **nside**:64 Parameter related to the resolution of the skymap.

Efficiecy Calculation Parameters
--------------------------------
    
* **eff_config** A dictionary of parameters that are related to the efficiency tests.

  * **injectionDirectoryPath**:"/home/mly/injections/" The path were all injection type directories are.
  * **injectionsWithHRSS**: ["SGE70Q3", "SGE153Q8d9", "SGL153Q8d9", "WNB250"] The list of the injection directories that use HRSS.
  * **injectionsWithSNR**: ["cbc_20_20", "wnb_03_train_pod", "cusp_00"] The list of the injection directories that use SNR.
  * **injectionHRSS**:"1e-22,1e-21,1e-22" Intervals for tests that use HRSS (first, last, step).
  * **injectionSNR**:"0,50,5" Intervals for tests that use SNR (first, last step).
  * **testSize**:"100" Number of tests on each value of HRSS or SNR respectively.
  * **howOften**: 3600 After how many successful inferences to run an efficiency test.


continuous FAR estimation Parameters
------------------------------------

* **far_config** A dictionary of parameters that are related to the continuous FAR tests.

  * **far_enabled**: true Option to opt out from false alarm rate calculation. Used by offline and online search at the initialisation of the search. If false make sure you provide a valid FARfile in the config entry **farfile**.
  * **batch_size**: 1024 Batch size of inference. Used by hermes client inference.
  * **threshold**: 2.3148e-05 Default for once per 2 days (Hz). **Used to define what is an event and what not.**
  * **restriction**: 0.0001 The minimum score of an inference to keep it in the history.
  * **max_lag**: 3600 The maximum time distance allowed, between two lagged segments.
  * **lags**: 1024 The number of timeshifts applied on the zero-lagged data to produced background tests.
  * **batches**: The amount of condor jobs to break the generation of background tests. **This can be adjusted if they do not finish within the hour.**
  * **visible_gpu_devices**: "local" GPU devices to use. Local will make all the local GPUs visible.
  * **selectedGPUs**: [0] An index list to choose which GPUs are to be used. Default is to use the first visible.
  * **parallelGenerations**: 3 How many dags ( each corresponding to an hour of data) are allowed to run at the same time. This is actually a condor_job number restriction. As the default values are, it will restrict the jobs to dags + jobs < parallelGenerations*batches.


Misc
----

* **maxDataFrameSize**:3600 The number of outputs grouped together in one data frame from the manager.
* **trigger_destination**:null Which domain of GraceDB to send the event (test,dev,playground). When left empty it it does not send an event but it creates follow-up and seves it in a file with made up ID. If not, it takes one of the following options, shown below with the corresponding destination.
    * `test` which sends the alerts to: "https://gracedb-test.ligo.org/api" (needs certificate to work)
    * `playground` which sends the alerts to: "https://gracedb-playground.ligo.org/api" (needs certificate to work)
    * `dev1` which sends the alerts to: "https://gracedb-dev1.ligo.org/api" (needs certificate to work)
    * `online` which sends the alerts to: "https://gracedb.ligo.org/api" (used only for realtime online search after pipeline is approved)
* **trigger_group**:null Which group of GraceDb triggers this will belong. This is used for online search only.
    * `Test` will create a test trigger and will not contaminate the list of the official triggers.
    * `Burst` will create a proper trigger.
* **seed**: 921101 Fixed to be able to reproduce the search. The birthday of Emily Voukelatu where the pipeline is named after.
    * There are also some other entries that might appear here when the config will be updated at somepoint within the search. They are to be ignored.

Now that the we went through the setting up of the search and the configuration parameters of it, we can see how to run such a search