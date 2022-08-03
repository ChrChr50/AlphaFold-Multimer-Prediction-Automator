# AlphaFold-Multimer-Prediction-Automator
The Python script in this repository compiles protein sequence pairs from Google Sheets and runs AlphaFold Multimer predictions on them through the ChimeraX command line. It was created within the specific context of the repository owner's undergraduate research laboratory and thus is not applicable to everyone.

# Import:
* gspread - Google Sheets Python API library
* time - Python module for representing time
* datetime - Python module for representing dates
* os - Python module for interacting with the operating system
* watchdog.observers - Python library for monitoring files
* watchdog.events - Python library for handling OS events
* bottle - Web microframework
* threading - Python library for multithreaded processing
* webbrowser - Python module for displaying web-based documents
* wsgiref.simple_server - Python module for implementing simple HTTP servers
* boxsdk - Software development kit for Box

How to import:
* Open the command line for your device and type "pip install [package name]" where [package name] is verbatim one of the names listed above.
* Close and open the command line as administrator, then change directory by running "cd C:\Program Files\ChimeraX 1.4.dev202202131839\bin."
* Run ".\python.exe -m pip install [package name]" for every required package in order to install them in the ChimeraX bin.
* If necessary, manually run "import [package name]" for every required package on ChimeraX's built-in command line.
* chimerax.core.commands is a module that does not need to be installed and only activates when there is an active ChimeraX session.

# How to Use:
The Python script provided has a section where you will need to input the following information:
* Google_Sheet - The name of the Google Sheet being used for AlphaFold predictions
* AlphaFold_Directory - The path for the directory that all AlphaFold predictions are stored in will need to be provided
* Client_ID - The ID of the Box application being used
* CLIENT_SECRET - The secret key of the Box application being used
* Box_VideoFolder_ID - The folder ID of the Box folder that contains the 3D protein animations
* Box_ModelFolder_ID - The folder ID of the Box folder that contains the predicted model folders (the main folder)
* VideoFile_Path - The desired path that 3D protein animations should go to

The Box application and the Google Sheets bot have already been set up.

To run the script, run "python [path of Python script]" on the ChimeraX command line. This will automatically extract amino acid sequences for unpredicted protein pairs from the Google Sheet, input them into AlphaFold 2, generate animations, organize the predicted models in the file system, mark the completion date for each pair on the Google Sheet, and upload the predicted models and animations to Box.

# Planned Updates:
* Automate name and directory change for videos
* Troubleshoot ChimeraX crashing issue
