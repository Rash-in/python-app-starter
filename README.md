# python-app-starter
Python scripts used to start a new python-based development project. I found myself re-writing a lot of code everytime I started a new project. This allows me to not have to do that and keep the individualized code inside the repo. It is a one-time use script per repo that gets stored after use for the next project. I don't really have any plans for this script aside from some minor compatibility bugfixes to harden it and make it compatable with Windows.

Windows OS Compatibility will be coming soon. Until then, this script will work on Linux and MacOS.

## Use Case Warning
These scripts are used as-is described in section #7 under the Apache License.

That being said the intention behind this script is that it is used inside of someone's "home" directory. ie.(linux: `~/Documents/Projects/Repos/` Windows: `C:\Users\IAMME\Documents\Projects\Repos`)

So if you are planning on using this script, please be aware that if you put it someplace weird like `/var/lib` or `C:\windows\system32` you will run into inconsistencies such as permission writing issues, and general clutter in places this script doesn't need to be running in.

## Requirements
- Operating System: Linux / MacOS
- Internet connection: Installing packages
- Git installed on host.
  - Test in terminal
  - `git --version`
- GitHub Account
  - If you don't have an account, get it [here](https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F&source=header-home)
  - Personal Access Token: If you don't have one, instructions are [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- Python 3 installed on host and is in PATH.
  - Test in terminal (For on PATH)
    - `which python3`
  - Test in terminal (For access)
    - `python3`
    - Command by itself should open up a shell.


## Getting Started
Download the latest release from this repo. It is a single file that uses python to create folders and files associated to a new project.

1) Create a new [GitHub](https://github.com) repository and note the name of the repository

2) Find a path that you want to work out of on your local system.
   - i.e. i like to use: `~/.GitRepos` or `/home/rashin/.GitRepos`  

Running the file (terminal):
- `python3 -B path/to/install_script.py`
- Follow the on-screen instructions.
- There are no arguments for the script as the data that needs be obtained is asked for in-application.


## What this does (Detailed)
1. Upon starting the script, it will ask to input an application name and an installation path (that Python can write to). 
    - If that path that was entered doesn't exist, it will create it. 
    - inside of that folder will be another called what was entered for the application name. i.e.
      - `~/Documents/YOUR_INSTALL_PATH/YOUR_APP_NAME`

2. Once those folders are created and validated, the script will install a Python Virtual Environment (VENV) if it doesn't already exist.

3. Next, the runtime folders will be created inside of it. I like keeping these here as I don't generally delete my virtual environments so inside of the venv is out of the way enough to not be annoying. 

    The following folder structure is created inside of `.env/`:
    - `.runtime`
      - base folder for the runtime of the application.
    - `.runtime/logs`
      - folder for logs.
    - `.runtime/certs`
      - folder for SSL certificates
    - `.runtime/pids`
      - folder for application service PIDs.
    - `.runtime/envs`
      - folder for dotenv files to be injected into the application.
    - `.runtime/envs/local.env`
      - dotenv file the the install_script parses into. It contains variables that the application will use to identify its own path and configuration.
    - `.runtime/envs/app.env`
      - dotenv file that you as a developer will use to inject environment variables into your application. Script will create the file, but not write to it.


4. After the runtime folders are created, the base folder structure of the application is created
- `src`
  - folder used to house all source files
- `src/bin`
  - folder used to house the runtime executable for the python app.
- `src/{app_name}`
  - folder for src material for the supplied application name.
- `src/{app_name}/bin`
  - folder for the application executables to be placed.
- `src/main.py`
  - file for the main application itself.
- `src/requirements.txt`
  - application requirements file. Script will run several pip install commands and freeze them into this file.

5. Install script will take the install_template.py and copy it over to the `src/bin` directory renaming it to the application name chosen.

- The sole purpose of install_template.py script is to get a step back from the actual application, and load the dotenv files if local development. 
- It takes two arguments, `local` and `remote`. local will load the dotenv files associated in step 3, where as remote will just load the application.
- The idea is that `remote` is for an acutal deployment that uses secrets being injected as environment variables and not a dotenv file so they are not needed.
- Assertion: Dockerfile CMD line would look like this:
  - `[ 'python3', '/app/bin/app_name.py', 'remote' ]`

6. Install some application dependencies required for use in the application setup.
   - python-dotenv: so that we can load dotenv files.
   - pipdeptree: so that we can list and verify that the virtual environment is working with loaded packages. (verifies pip installs were successful.)

7. Save dependencies using pip-freeze command and overwrite `src/requirements.txt`

End of Script