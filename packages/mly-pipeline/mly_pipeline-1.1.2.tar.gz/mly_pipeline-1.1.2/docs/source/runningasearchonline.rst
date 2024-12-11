.. _Online_search_timeline:


Online Search Timeline
######################

By the moment the pipeline starts running and from now on there is a constant production of processed data instances and inference results. Both of which are saved and organised for post processing.

* The script requests at least 16 seconds of data for each inference. These 16 seconds are usually the most recent 16 seconds. We call these data the buffer or **buffer instance**.
* The buffer is whitened, bandpassed (20,512 Hz) and then the central second (7.5,8.5) is cropped. This is a **timeseries data instance**.
* The **timeseries data instance** is used to create the pearson **correlation data instance**, which is used in coherency model (model2).
* The timseries and correlation data instances are fed to the models to produce an **inference result**.

With every inference  
--------------------

If the **inference result** is above the detection threshold:

* The **inference** result is saved in json format inside ``output_directory`` and in labeled as a **trigger**.
* A series of actions related to :ref:`trigger handling<Trigger handling>` take place.

If the **inference result** is below the detection threshold:

* The **inference** result is saved in json format inside ``output_directory``.
* The timeseries data are split to individual detector timeseries in mly.DataPod objects. Then they are saved in ``masterDirectory/temp/H,L,V`` directories in pickle (.pkl) format for later background estimation tests.
* The buffer which is also a mly.DataPod is saved  inside ``bufferDirectory/temp`` again in pickle format. It is going to be used later for efficiency testing.

How manager.py manages the search part 1
----------------------------------------

The manager script runs around every five minutes to organise all the products of the search.

* Collates all the **inference result** in ``output_directory`` together. The parameter **maxDataFrameSize** is defining the size of the collation the manager will do, the default is 3600. When the json files exceed that number it creates pandas.DataFrame with all of them and saves it in pickle (.pkl) format. **Note here that 3600 is not necessarily mean every hour**. The collation file created has the GPS of the first and the GPS of the last inference that includes in its name (STARTGPS-ENDGPS_3600.pkl). 
* Every hour it collates the **timeseries data instances** inside ``masterDirectory/temp/H, L, V`` for each detector respectively and save them as an mly.DataSet object in pickle (.pkl) format at ``masterDirectory/H, L, V`` for each detector respectively. All those files will have the same name but they will be in different directories. Note the difference with the previous point here. This happens every hour, so the new files created will have as many data were used within the hour and not necessarily 3600.
* Collates all the **buffer instances** in ``bufferDirectory/temp`` into one **buffer dataset**. The parameter **howOften** in the ``eff_config`` of the configuration file determine how many buffers are needed to do this collation. The **buffer dataset** is saved in pickle (.pkl) format with a standard name ``bufferDirectory/BUFFER_SET.pkl``. Every time the collation takes place the **buffer set** is replaced.
* After the creation of a new **buffer set**, it is used to issue an :ref:`efficiency test script<Efficiency Test>` that will provide us with the estimated efficiencies of selected waveforms the last hour.

There are some other tasks the manager does but the need some extra context.


Continuous False Alarm Rate estimation
--------------------------------------

The continuous FAR estimation is a mandatory tool to make sure we constantly know the rate of false events our model trigger on and accordingly correct our event thresholds.
There are two **modes** of this functionality, hence two different scripts running at the same time. Those two script are working on the same directories and files inside ``falseAlarmRates`` directory.
The parameters mentioned here are all inside **far_config** section in the configuration file of the search.

**continuesFAR --mode generation**

* The generation mode looks for new unused dataset files inside ``masterDirectory/H, L, V``. 
* For each one of these datasets it will organize the generation of time-lagged background combinations of the detector data.
* The total lags it will attempt to create are specified in **lags** parameter. 
* The number of jobs between which it will distribute this generation is specified by **batches** parameter.
* It will create a dagman with all these jobs and submit it. 
* Each of these jobs will create a dataset with time-lagged data along with their correlation data and save them in ``falseAlarmRates/temp`` directory.
* Then the script will go to the next unused file inside ``masterDirectory/H, L, V``, **or wait until this is possible**.

.. note:: The script will not produce condor jobs indefinitely. Before it continuous to a new unused file, it checks to see how many condor jobs are already running and how many "generations" of files have been already produced. The parameters used to determine that are **parallelGenerations** and **batches**. It will wait until this statement is no longer true: ``condor_jobs_running >= batches*(parallelGenerations-1)) or files_in_temp >= parallelGenerations*batches``


**continuesFAR --mode inference**


* The inference mode looks for dataset produced by the --mode generation script and puts them in the queue for inference.
* After it loads a time-lagged file from ``falseAlarmRates/temp``, it produces its inference results and it saves the inference result inside ``falseAlarmRates`` directory. 
* Then it deletes the time-lagged file it used. 

.. note:: The specific script has some known issues that originate the the subpackages it uses. This is taken into account within runall.sh, and there are special loops that check and restart it.


Efficiency Tests
----------------

The efficiency tests script is called once a **buffer set** has been created through the manager script. All the parameters related to the efficiency tests are in the **eff_config** section of the configuration file.

* There are two metrics used in the efficiency tests, **SNR** and **hrss**. Each metric has its own corresponding waveforms **injectionsWithSNR** and **injectionsWithHRSS** respectively. 
* The waveforms are located inside **injectionDirectoryPath** which is in mly user directory in CIT.
* Each metric has also its corresponding intervals to test on, **injectionSNR** and **injectionHRSS** respectively. Both of them have default values with big steps and to be practical they need to be changed by hand when needed. 
* **If you do not want an efficiency test, you can empty those parameter list.**
* For each of one of these intervals specified there will be **testSize** amount of different waveforms being tested. The bigger the **testSize** the smoother the efficiency curve produced.
* All those tests on different waveforms are done through condor, and their result is a dictionary with scores saved in pickle (.pkl) format inside ``efficiencies``.
* One of these jobs is the final job where it creates the plot with the efficiencies of different waveforms.
* When a new efficiency test starts, the files of the old one are moved inside ``efficiencies/history`` directory for future reference.
* A new efficiency test will not start if the previous one has not finished yet. To make sure this suits your need of testing, change **howOften** or/and **testSize** or/and the intervals you test accordingly.


Trigger handling
----------------

As the search runs, when there is an inference that provides a FAR abobe the threshold defined in config, a subscript is issued tp generate all the extra information needed for this new event.

* Parameter estimation (duration, central time, frequency bandwidth and central frequency).
* Creating a GraceDB event (if a ``trigger_destination`` has been specified in the config).
* Generation of the skymap.
* Updating the GraceDB event with the skymap info.
* Creating an event directory with the GraceDB id and the GPS of the event in the directory name. This directory will be located in **triggerplot_directory**.
* Creating plots and saving them inside that directory.
* Putting the trigger ``.json`` file inside **trigger_directory**.

How manager.py manages the search part 2
----------------------------------------

Now that we have described how continuous FAR works, we will add some more things that the manager script does that are, important.

* Every time the manager runs, it checks the new background tests that have been produced by the continuous FAR inference script.
* It collates them according to their "generation" or hour of production, or more technically according to the dagman they came from.
* Those groups we call them hourly groups. The collations of hourly groups are saved in ``falseAlarmRates/hourly`` directory.
* If there are any inference files that do not have a group created yet, it creates one for them.
* At the end it deletes the files used for the production of the hourly files.
* Then it collates all the hourly files ever produced to create the current most updated FAR estimation of the background.
* This estimation is saved in ``falseAlarmRates/FARfile/`` an its name is ``FARfile_#######`` where the hashes represent the total test number. This is a number that changes every time an update is made.
* Along with the main FARfile, there are two interpolation files created.
* One interpolates score values into FAR values. It is used to decide the FAR of each inference.
* The second does the opposite, interpolates FAR values into score values. It is used to identify the scores of current thresholds.
* Both of these interpolations, have also a copy of themselves as a reserve, in case the file is getting updated at the point where an interpolation is requested.
* Finally, the manager does a big change once per search. When the estimation of the background has enough tests, the ``farfile`` parameter changes to point on the FARfile of the current search, instead of the initial. Currently we use 1 year of tests as minimum for this change to take place. 
* The manager then quits to force runall.sh to restart all the scripts with the new configuration file.




Monitoring the search
---------------------

The status page
---------------

If you are running the search in one of the LIGO clusters, the pipeline will create a soft link of the search directory in the ``~/publick_html`` directory. There you will find a ``status.html`` file and if you click it, you will see the status page of the search. It includes a false alarm rate plot, a series of efficiency tests and a table with the events and all their links.

To monitor that the search is running normally you can open the ``.out`` files that correspond to each subscript. Although there are many other things that you can check as the time passes, noted below. Additionally you can check the log files created inside log directory which will have usefull info about the latest actions that took place.

After the first two minutes
---------------------------

After you run the runall.sh script, the search scripts will already have some output. Use your favourite editor to open the ``search_step_#.out`` files 
and see if there is any output in them. As the inference on the processed data takes place, you should start seeing ``.json`` files appearing inside the output_directory.

You can also check in bufferDirectory and see that there are some pickle files (mly.DataPod(s)) saved there too. 

The processed timeseries data instances that were used for the inference are also saved inside masterDirectory/temp/ in individual detector directories (H, L, V). These will be used later to produce time-lagged background test instances later.

After the first ten minutes 
---------------------------

Five minutes after you start the search, the manager script will run for the first time and will take all the ``.json`` files in output_directory and put them together in one pandas.Dataframe file, saved in pickle format. 
The first pickle frame file to appear is called ``tempFrame.pkl``. 
If you look in the output_directory, you will see that file along with some json files too. 

After roughly an hour
---------------------
After an hour, or at least after 3600 inferences have been done, you will see that inside the output_directory there is the first collated output file as described before.

Now that at least one hourly dataset has been saved in the masterDirectory we can generate our first time-lagged data to do a background estimation. Inside ``continuesFAR_generation.out`` you will see the first condor dagmans to be submitted.
When the first jobs have finished they will save the time-lagged data in ``falseAlarmRates/temp`` directory. Each job will save an individual file. 

The inference script is constantly checking to see if there are any files created for inference. When it sees them you will star seeing the inference information inside ``continuous_FAR_inference_#######``.
**The continuous FAR inference mode output has a number attached to it. That number is the unix time it was created and it can help us troubleshooting the script. So do not worry if you see many of them appearing over time.**

After two hours you will also be able to see the first efficiency results and plots inside ``efficiencies``.


