   @echo off
   rem ***********************************************************************
   rem Removes existing virtual environment and creates new virtual environment,
   rem installing the required packages.
   rem 
   rem Usage:
   rem 		new_env
   rem
   rem ***********************************************************************
   
   :: Delete existing virtual environment (include, lib, scripts, tcl folders & pip-selfcheck.json)
   echo NEW ENV: Removing files...
   RMDIR /S /Q Lib
   RMDIR /S /Q Include
   RMDIR /S /Q Scripts
   RMDIR /S /Q tcl
   del pip-selfcheck.json
   
   :: Create new virtual environment
   echo NEW ENV: Creating new environment...
   virtualenv "%cd%"
   
   :: Install the required packages
   echo NEW ENV: Installing required packages...
   call Scripts\activate.bat
   pip install -r requirements.txt
   call Scripts\deactivate.bat
   
   :: Script finished
   echo NEW ENV: Done creating new environment.