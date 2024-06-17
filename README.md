# WESTPA Workshop 2024 Tutorial Files
https://www.github.com/westpa/westpa-workshop2024-tutorials

A repository with WESTPA Workshop 2024 Tutorial Files


# Quick Start Guide
* Video Guide: https://youtu.be/iU_cUbZDvfU

## Logging in
1.	Go to https://jupyter.crc.pitt.edu
* Login with your Pitt ID/Password
* Click "Start Server"
* Select the "WESTPA 12-core 6 hours"

## Setting up files and stuff
2.	Run the following:
*	``git clone https://github.com/jeremyleung521/h2p-quickstart``
*	``source h2p-quickstart/run_bash.sh``
*	Refresh your browser page 
*	If Firefox, make sure Enhanced Tracking Protection is off (little shield icon next to URL)

## Activating environment
3.	After everything is done, you should be in ``$TMPDIR/westpa-workshop2024-tutorials``
* A virtual environment called ``westpa-workshop2024`` is made in ``~/``
* To use venv, select the correct kernel (Top right of Notebook) or run ``source ~/h2p-quickstart/activate_env.sh`` (Terminal)

Notes:
* Everything in ``$TMPDIR`` will be deleted when your session terminates (TIMEOUT, SLURM job deleted/canceled and/or by clicking “Stop my server” on the CRC website)
* You can reconnect even when your browser disconnects (nothing deleted)
* Your environment (built in ``~/``) will be preserved. Run ``source ~/h2p-quickstart/activate_env.sh`` (Sets environment variables and activates environment: westpa-workshop2024/bin/activate, clones this repository into $TMPDIR if doesn't exist).
* If the kernel is acting weird (can't import things even after kernel restart), just stop your server and restart. (File --> Hub Control Panel --> Stop My Server). Run ``source ~/h2p-quickstart/activate_env.sh`` to reclone the repository + activate environment.

•	https://pitt.zoom.us/j/94041061817
•	Meeting ID: 940 4106 1817
•	Passcode: 12345
 
•	Backup: 
* Run on Google Colab: https://colab.research.google.com/
* File -> Open Notebook, paste GitHub Link. Select Notebook.
* Notebooks: 
https://github.com/jeremyleung521/westpa-workshop2024-colab
