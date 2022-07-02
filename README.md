# AlphaFold-Multimer-Prediction-Automator
This script compiles protein sequence pairs from Google Sheets and runs AlphaFold Multimer predictions on them through the ChimeraX command line.

# How to Use
Install the gspread, watchdog.observers, watchdog.events, os, bottle, threading, webbrowser, wsgiref.simple_server, and boxsdk modules to both your virtual environment and the ChimeraX application's bin.

Then, import each required module manually through ChimeraX's built-in command line.

Input the required information as directed in the script.

The chimerax.core.commands module only activates when there is an active ChimeraX session. Therefore, the script must be ran through the ChimeraX command line instead of PowerShell.

# Planned Updates
* Enable compiling three proteins for AlphaFold Multimer prediction
* Minimize path dependency in the script
* Automate name and directory change for videos
* Troubleshoot ChimeraX crashing issue
