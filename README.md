# cozmo-touch-2018

## Building Package for Windows
In order to build a package for Windows, the following requirements must be met:
1. You are using a machine running Windows
2. You have installed `pipenv` ([installation instructions](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv))

If you've met the above requirements, then simply run the following two commands in PowerShell (within this project's directory):
```bash
$ pipenv install
$ ./package.py
```

This will create a new file in the project's directory called `cozmos_night_at_the_museum.zip`. This ZIP file contains all the necessary files to run the code on Windows with an Android device, and requires no extra setup. To run the code on Windows with an iOS device, the only extra setup required is an iTunes installation.

## Running the Package on Windows with an Android Device
1. Unzip `cozmos_night_at_the_museum.zip`
2. Run the `cozmos_night_at_the_museum/windows_and_android.ps1` PowerShell script

## Running the Package on Windows with an iOS Device
1. [Install iTunes](https://www.apple.com/itunes/download/)
2. Unzip `cozmos_night_at_the_museum.zip`
3. Run the `cozmos_night_at_the_museum/windows_and_ios.ps1` PowerShell script

### Summary of Required Steps to Install without Package:
On Windows, requires at least 9 steps and usage of the command line.
```
# Install git (multiple steps)
# Install python3 (multiple steps)
pip3 install --user 'cozmo[camera]'
# Install iTunes or ADB (multiple steps)
git clone git@github.com:Rac535/cozmo-touch-2018.git
cd cozmo-touch-2018
python main.py
```
