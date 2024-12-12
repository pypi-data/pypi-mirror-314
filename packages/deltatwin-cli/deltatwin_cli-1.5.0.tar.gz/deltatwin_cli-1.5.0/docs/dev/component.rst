The ``deltatwin component`` is the command line dedicated to handle DeltaTwin® project.
It stores the ``manifest`` and ``workflow`` files and all the models and source code that enable to build your DeltaTwin® component.

The DeltaTwin® component anatomy can be described with the following empty local representation:
::

    my_project
    ├─── manifest.json
    ├─── artifacts/
    ├─── models/
    ├─── resources/
    ├─── sources/
    └─── workflow.yml

______________________________________________


.. click:: delta.cli.components.list:list_deltatwins
   :prog: deltatwin component list
   :nested: full

.. code-block:: console

    deltatwin component list

This command will list the DeltaTwin® components visible to the user,
it includes, the user's DeltaTwin® components, all the DeltaTwin® components of the
Starter Kit and all the published DeltaTwins
with public visibility.
By default the information's will be displayed as an array, these information can also
be retrieved as a json.

.. code-block:: console

    deltatwin component list --format-output json

This command will list the DeltaTwin® components of the user.
Before using this command the user must be logged in,
using the *deltatwin* *login* command. For example, it returns:

.. code-block:: console

    [
        {
            "name": "Deltatwin1",
            "description": "Description of the Deltatwin1",
            "creation_date": "2024-02-21T13:16:47.548Z",
            "license": "LGPLv3",
            "topics": [
                "starter-kit",
                "sentinel-2",
                "optical",
                "color-composition"
            ],
            "author": "delta-user"
            "visibility": "public"
        },
        {
            "name": "Deltatwin2",
            "description": "Description of the Deltatwin2",
            "creation_date": "2024-02-21T13:16:47.548Z",
            "license": "LGPLv3",
            "topics": [
                "starter-kit",
                "sentinel-2",
                "optical",
                "color-composition"
            ],
            "author": "delta-user"
            "visibility": "public"
        }
    ]

______________________________________________


.. click:: delta.cli.components.get:get_deltatwin_info
   :prog: deltatwin component get
   :nested: full

.. code-block:: console

    deltatwin component get dt_name -f json

This command will show the information of a DeltaTwin® component,
before using this command the user must be logged in,
using the *deltatwin* *login* command. As example, it returns:

.. code-block:: console

    {
        "name": "Deltatwin2",
        "description": "Description of the Deltatwin2",
        "publication_date": "2024-03-07T12:50:55.055721Z",
        "topics": [
            "starter-kit",
            "sentinel-2",
            "optical",
            "color-composition"
        ],
        "version": "1.1.0",
        "available_version": [
            "1.1.0",
            "1.0.1",
            "1.0.0"
        ],
        "author": "delta-user",
        "inputs": [],
        "outputs": []
    }



______________________________________________


.. click:: delta.cli.components.init:init
   :prog: deltatwin component init
   :nested: full

**Examples**:
For example, you can create a new DeltaTwin® called *ndvi* with the following command:

.. code-block:: console

    deltatwin component init /home/user/desktop/ndvi

This command will create the basic files of a DeltaTwin® component, in a folder called *ndvi* and returns the following data

.. code-block:: console

    INFO:Delta:New commit : 076f911d678a97038bf83d873c8d94797341ef65 master
    INFO:Delta:Twin has been initialized at /home/user/desktop/ndvi
    INFO: DeltaTwin® ndvi created

______________________________________________


.. click:: delta.cli.components.build:build
   :prog: deltatwin component build
   :nested: full

**Examples:**

.. code-block:: console

    delta component build -t <tag name>

This command will build a (Docker) image of your DeltaTwin® component.

______________________________________________


.. click:: delta.cli.components.publish:publish_dt
   :prog: deltatwin component publish
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin component publish  <version name>

The first command will publish your DeltaTwin® component to the DeltaTwin® platform.

If you have already pushed your DeltaTwin®, please use the second command to 
publish a new version of your DeltaTwin® component.

**Example 1:**
To publish a new DeltaTwin component, execute:

.. code-block:: console

    deltatwin component publish 1.0.0 --change-log "First version"


**Example 2:**

To publish a new version of an existing DeltaTwin name 'my_deltatwin',
execute:

.. code-block:: console

    deltatwin component publish 1.1.0 --change-log "New version of my DeltaTwin"


______________________________________________


.. click:: delta.cli.components.delete:delete_deltatwin_info
   :prog: deltatwin component delete
   :nested: full


**Examples:**

.. code-block:: console

    delta component delete -v 1.2.0 MyDeltaTwin

This command will remove the version 1.2.0 of the Deltatwin component named 
MyDeltaTwin.

