The ``deltatwin drive`` is the command line dedicated to handle your data.


______________________________________________

===========
Resource
===========

.. click:: delta.cli.drive.resource.add:add_resource
   :prog: deltatwin drive resource add
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive resource add /path/to/resource Sentinel1.zip

Will add the resource given in argument, to the resources of the
working DeltaTwin® component.
If given the option *--download*, it will download the resource and
put it in the resources folder.
This command will add the entry to *manifest.json*.

---------------------------------

.. click:: delta.cli.drive.resource.delete:delete_resource
   :prog: deltatwin drive resource delete
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive resource delete Sentinel1.zip

This command will remove the entry from the *manifest.json*.

---------------------------------

.. click:: delta.cli.drive.resource.list:list_resource
   :prog: deltatwin drive resource list
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive resource list

List all the resources from the *manifest.json* of the
working DeltaTwin® component.

______________________________________________

.. click:: delta.cli.drive.resource.sync:sync
   :prog: deltatwin drive resource sync
   :nested: full

**Examples:**

.. code-block:: console

    deltatwin drive resource sync

This command will reload the *manifest.json*, to update all the resources
with the last manifest load.

.. code-block:: console

    INFO:Delta:Fetching https://catalogue.dataspace.copernicus.eu/odata/v1/Products(UUID)...
    INFO:Delta:https://catalogue.dataspace.copernicus.eu/odata/v1/Products(UUID) has been fetched.

______________________________________________

==========
Artifact
==========

DeltaTwin artifact stores output Data of DeltaTwin component executions.

______________________________________________

.. click:: delta.cli.drive.artifact.add:add_artifact
   :prog: deltatwin drive artifact add
   :nested: full

______________________________________________

.. click:: delta.cli.drive.artifact.list:list_artifact
   :prog: deltatwin drive artifact list
   :nested: full

______________________________________________

.. click:: delta.cli.drive.artifact.get:get_artifact
   :prog: deltatwin drive artifact get
   :nested: full

______________________________________________

.. click:: delta.cli.drive.artifact.delete:delete_artifact
   :prog: deltatwin drive artifact delete
   :nested: full

