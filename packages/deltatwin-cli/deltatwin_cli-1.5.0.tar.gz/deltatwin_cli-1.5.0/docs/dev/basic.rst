.. click:: delta.cli:delta_login
   :prog: deltatwin login
   :nested: full


.. code-block:: console

    deltatwin login username password -a https://api.deltatwin.destine.eu/

This command will log in to the service with the api given in argument.
To set the service you want to query, you can either use *--api*,
or set the path to your configuration file *--conf*. If no path is
given, the *conf.ini* is saved in the *.deltatwin* folder in your
home directory.

.. code-block:: console

    INFO: Login to the service token saved in /home/jiloop/.deltatwin/conf.ini

When log, all the connection information will be stored into a configuration file (conf.ini),
it will contain the token, and the api url, all the information mandatory to interact with,
the deltatwin services.

Once this file is created, you can simply log again using this command.

.. code-block:: console

    deltatwin login

It will find all the connection information into the configuration file.

---------------------------------

.. click:: delta.cli:version
   :prog: deltatwin version
   :nested: full

.. code-block:: console

    deltatwin version

Prints the DeltaTwin® command line version currently used.

.. code-block:: console

    DeltaTwin® CLI version : 1.2.0

.. code-block:: console

    deltatwin version --all

Prints the DeltaTwin® command line version and the core version installed.

.. code-block:: console

    DeltaTwin® CLI version : 1.3.0
    DeltaTwin® CORE version : 1.1.0


---------------------------------

.. click:: delta.cli.metrics:metrics_deltatwins
   :prog: deltatwin metrics
   :nested: full

.. code-block:: console

    deltatwin metrics

Show to the user the storage consumption (Bytes) of is Artifacts.

.. code-block:: console

    {
        "category": "artifacts",
        "storage_used": 91579,
        "total_objects": 22227972,
        "last_metric_update": "Oct 29, 2024, 10:46:24 AM"
    }
