# DeltaTwin® service

GAEL Systems is developing a dedicated service, named "DeltaTwin® Service" to 
facilitate modelling activities of digital twins. 

It aims to offer a collaborative environment for building and running 
multi-scale and composable workflow, leveraging the numerous 
available data sources, sharing results, and easing interoperability 
with other digital twin standards and system dynamics models.

The DeltaTwin® is the central element for the management of workflows, 
resources and their results. They follow a precise structure folder to ensure 
they are handled by the DeltaTwin® service.

The service includes the “drive” element in charge of handling DeltaTwin® 
storage, their configuration and versionning.   
The “run“ element is in charge of the models executions and their monitoring. 

The DeltaTwin® command line allows user to control the management of the 
later modules. It allows user to either work online and perform all actions
in a cloud environment or locally using your computer's resources. 

DeltaTwin® service also provides a web application to graphically manages your
Deltatwins and their execution.

# DeltaTwin® Command-line

The command line interface allows the user to configure a DeltaTwin and manage its run
operation either from the a shell command prompt or with a script. 

The commands are divided into five main groups:
- those that allow user to configure and manage the DeltaTwin’s composition 
(``deltatwin drive``)
- those dedicated to the to the run concept (``deltatwin run``)
- those which help to get information on DeltaTwin® (``deltatwin get`` 
``deltatwin list``)
- those which give general information on service ( ``deltatwin version``)
- those which allow connexion (``deltatwin login``)


## Installation

DeltaTwin® command-line can be installed using pip:
```
pip install deltatwin-cli
```



# *DeltaTwin* API

Commands are described below. 
These descriptions are also available by using the ``--help`` option on each 
individual command.


| *deltatwin* command |                parameters                 |                                                                                                                                 description |
|-----------------|:-----------------------------------------:|--------------------------------------------------------------------------------------------------------------------------------------------:|
| drive         |  |                                                                                DeltaTwin drive is dedicated to manage  DeltaTwin project repository. |
| run    |  |                                                                                DeltaTwin run uses models stored into Delta component repository |
| get         |  |                                                                                Get the information of a DeltaTwin component. |
| version         | -all: show all deltatwin components versions. |                                                                                Show DeltaTwin version and check if deltatwin is properly installed. |
| list            |                                       |                                                                                                        	List the DeltaTwin from marketplace |
| login           |  -a api.url -c conf.ini path                                   |   logs the user to the service, and allows the use of commands, such as ``deltatwin list`` command,that require online registration                                                                                                                                          |

Configured deltatwin information will be stored into $HOME/.delta/config.json 

# *DeltaTwin drive* API

The ``deltatwin drive`` is the command line dedicated to handle DeltaTwin project repository. 
It stores all the configuration, resources, models and sources to run a DeltaTwin and retrieve data.
For more details, use the parameter ``--help``.



# *DeltaTwin run* API

DeltaTwin run module uses models stored into DeltaTwin repository. The command is ``deltatwin run``
The objective of this service is to allow edition and run of the models stored into the DeltaTwin.
The run can be done remotely and locally when possible.
Run results shall be stored into the artifact folder of the deltatwin drive environment.
For more details, use the parameter ``--help``.



# *DeltaTwin get* API

Get information about a DeltaTwin component by specifying its name. By default, the command 
returns information for the latest version of the Delta component. To get information 
about a previous version, you must specify it with the --version option 
`deltatwin get [deltatwin_name] --version x.y.z`. To get the list of all available versions you 
can either use `deltatwin list --version` or `deltatwin get [deltatwin_name] --version`.
DT_NAME : DeltaTwin component name [MANDATORY]


# *DeltaTwin version* API

Command ``deltatwin version`` shows DeltaTwin version and check if deltatwin is properly installed.
For more details, use the parameter ``--help``.


# *DeltaTwin list* API

``deltatwin list`` Lists the DeltaTwin from marketplace
For more details, use the parameter ``--help``.


# *DeltaTwin login* API

The command ``deltatwin login`` logs the user to the service. We use it in the form:

```
deltatwin login <username> <password> [options]
```
For more details, use the parameter ``--help``.