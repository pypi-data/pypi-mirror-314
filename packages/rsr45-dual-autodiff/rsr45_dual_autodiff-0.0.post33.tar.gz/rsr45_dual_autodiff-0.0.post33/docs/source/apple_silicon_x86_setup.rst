Apple Silicon x86_64 Setup
==========================

This document outlines the steps to configure an Apple Silicon machine to work in **x86_64** mode for compatibility with x86_64 tools and environments.

.. contents::
   :local:

Setting Up for x86_64
---------------------
Use the `arch -x86_64` prefix to explicitly run commands in x86_64 mode. This ensures tools, packages, and environments are compatible with the x86_64 architecture.

Example:
.. code-block:: bash

   arch -x86_64 /bin/bash

Installing Conda for x86_64
---------------------------
Download and install an x86_64 version of **Miniconda** or **Anaconda**. Run the installer in x86_64 mode:

.. code-block:: bash

   arch -x86_64 bash Miniconda3-latest-MacOSX-x86_64.sh

Creating a Conda Environment
----------------------------
Create the Conda environment for x86_64 with the desired Python version:

.. code-block:: bash

   arch -x86_64 conda create -n x86_env python=3.9

Activating and Installing Dependencies
--------------------------------------
Activate the environment and install required packages:

.. code-block:: bash

   conda activate x86_env
   conda install numpy pandas matplotlib
   pip install additional-package

Configuring Jupyter Notebook
----------------------------
Set up Jupyter Notebook to use the x86_64 environment:

1. Install the `ipykernel` package:
   .. code-block:: bash

      conda install ipykernel

2. Register the environment as a Jupyter kernel:
   .. code-block:: bash

      python -m ipykernel install --user --name=x86_env --display-name "Python (x86_64)"

Launch Jupyter in x86_64 mode:
.. code-block:: bash

   arch -x86_64 jupyter notebook

Verifying Architecture
----------------------
Ensure the environment is running in x86_64 mode:

- **Check Python Architecture**:
  .. code-block:: bash

     python -c "import platform; print(platform.architecture())"

- **Verify Installed Packages**:
  .. code-block:: bash

     python -m pip list

