.. _Running_a_search:

Running a search
################


To run the search you only have to get inside the search directory (we assume here that this is ``./mysearch``) and run ``mly-pipeline-start``


.. code-block:: bash
    
    cd ./mysearch
    mly-pipeline-start    

This will run the ``runall.sh`` script on the background and it will not terminate when you close your terminal. The output and error messages will all go into ``runall.out``.

.. note:: Before you start any type of search, check the config file to make sure the parameters that are there are the ones you want.  


Ending a search
===============

Online search runs a series of scripts that would be usefull to be able to stop easily. For that reason when you want to end or pause a search, you can run the following command inside the search directory.

.. code-block:: bash
    
    mly-pipeline-stop

If you want to resume the online search you run again the ``mly-pipeline-start`` command. The stop command is only for the online search. For offline searches is not yet implement given that they do not run indefinetly.

**For online and offline search there are sometimes condor jobs running. The mly-pipeline-stop command will not end those. To end them you will have to use condor_rm**

Monitoring the search
=====================

As the runall.sh script is active there is a monitor.log file that is been updated as the search is active. To access the monitor you can either open the file or use the following command to access tha last N lines:

.. code-block:: bash
    
    mly-pipeline-status -n N

The default is N=3.

Pickle format
=============

Many files that are saved during a search will be of pickle format. This format preserves the python object to be saved. The types of objects saved are python dictionary, mly.DataPod, mly.DataSet and pandas.DataFrame. We save them in such format to be able to change them for different purposes.

Timelines
=========

For both online and offline search there are pages with their descriptions.

* :ref:`Online_search_timeline`

* :ref:`Offline_search_timeline`

