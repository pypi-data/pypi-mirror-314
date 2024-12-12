Change log of DeltaTwin® CLI
#############################



.. list-table:: Change summary
   :widths: 30, 70
   :header-rows: 1

   * - Version
     - Change notice
   * - 1.5.0
     - :ref:`Version 1.5.0`
   * - 1.4.0
     - :ref:`Version 1.4.0`
   * - 1.3.3
     - :ref:`Version 1.3.3`
   * - 1.3.2
     - :ref:`Version 1.3.2`
   * - 1.3.0
     - :ref:`Version 1.3.0`
   * - 1.2.0
     - :ref:`Version 1.2.0`
   * - 1.1.0
     - :ref:`Version 1.1.0`
   * - 1.0.1
     - :ref:`Version 1.0.1`
   * - 1.0.0
     - :ref:`Version 1.0.0`


Version 1.5.0
==================
.. _Version 1.5.0:


* The metric command for the artifacts has been moved to a generic command named "deltatwin metrics"
* the commands for managing DeltaTwin components have been grouped under the "deltatwin component" section
* Add a new group of commands to schedule runs and manage these scheduling
* Add a command to delete a DeltaTwin component or only a specific version of a DeltaTwin component


Version 1.4.0
==================
.. _Version 1.4.0:


* Add metric feature for artifact
* Fix author name when displaying the list of DeltaTwin®


Version 1.3.3
==================
.. _Version 1.3.3:


* Correct command run_local to start_local


Version 1.3.2
==================
.. _Version 1.3.1:


* Update Readme
* Publish on PyPi


Version 1.3.0
==================
.. _Version 1.3.0:


* Remove all commands marked as deprecated
* Get deltatwin component description and versioning
* Improve management of DeltaTwin® resources (add/delete/list)
* Improve management of DeltaTwin® dependencies (add/delete/list)
* Add return code, and documentation.


Version 1.2.0
==================
.. _Version 1.2.0:


* Mark git wrapping command as deprecated
* Add artifact generation and listing
* Improve token management when log
* Start remote run execution
* Get information on run execution


Version 1.1.0
==================
.. _Version 1.1.0:


* Improve documentation and its pdf generation
* Add deltatwin login option to list DeltaTwin®
* Remove pull, fetch, push command


Version 1.0.1
==================
.. _Version 1.0.1:


* Add release notes in documentation
* Improve CLI documentation
* No more Error raise when the command is not implemented
* Fix documentation.
* Add the deltatwin list command, to list open access DeltaTwins or to list them by group.

Version 1.0.0
================
.. _Version 1.0.0:


* Add version command.
* Raise NotImplementedError for all not implemented commands.
* Organize, and clean the doc generation to PDF
* Remove all click.echo() from run commands.

