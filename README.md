# capstone-project-3900-h18b-codechefs

## Installation
* The installation instructions contained within this section describe the installation in an Ubuntu 20.04.1 LTS system. If installing on a different Linux distribution or a different operating system please refer to the user guide and/or package manager for that system.
* If you’re running a Unix/Unix-like operating system you can get the kernel version using “uname -a”. To verify the operating system is Ubuntu 20.04 LTS issue the command “cat /etc/os-release”, which should contain the line VERSION=”20.04.1 LTS (Focal Fossa)”.

### Backend Installation
* The backend requires the installation of the python3 interpreter, python3-pip package manager and various python modules (packages).
* Run “sudo apt update” to fetch a list of packages from ubuntu’s repository.
* Run “sudo apt install python3 python3-pip” to install the python3 and python3-pip, selecting “Y” to confirm installation.
* Clone the project repository from github.com using the command git@github.com:unsw-cse-comp3900-9900-22T3/capstone-project-3900-h18b-codechefs.git
* Change into directory “~/capstone-project-3900-h18b-codechefs/backend” then run “pip install -r requirements.txt”. If this should fail for any reason at all such as not being able to find a certain package, as an alternative run “cat requirements.txt | xargs -n 1 pip install”.
* A successful install of the modules in requirements.txt is confirmed by changing into  “~/capstone-project-3900-h18b-codechefs/backend/src” and running “python3 server.py”


### Database Installation
* To install PostgreSQL server, run “sudo apt install postgresql postgresql-contrib”, then select “Y”.
* Start PostgreSQL server by running “sudo service postgresql start” and confirm the server is operational by running “sudo service postgresql status”.
* An account with your username will need to be created in PostgreSQL (Your username can be determined by running the command “whoami”). If your username is “lubuntu” then create an account by running the command “sudo -u postgres createuser lubuntu”. That’s followed by creating the database “code_chefs_db” by running the command “sudo -u postgres createdb code_chefs_db”.
* The postgres user now needs to grant all privileges to lubuntu in order to be able to execute DML (i.e. create, alter, drop, etc) and DDL (i.e. select, insert, delete, update, etc) statements. That is achieved by running the command “grant all privileges on database code_chefs_db to lubuntu”.
* If the above was successful, you should be able to get into the code_chefs_db database by running the command “psql code_chefs_db”.
* “/etc/postgresql/12/main/pg_hba.conf” will need to be modified such that it allows password-less login via an application. This is achieved by changing the line “local  all  all peer” to “local  all all trust”. Note: this is not advisable for a live system as it severely compromises the security of the database. However this option should be used in this case as it avoid having to modify configuration files in the backend.
* Ideally a live system should have a password for the database user, achieved by running the command “alter user lubuntu with encrypted password ‘<your-chosen-password>’;”. Note that this option means python config files will need to be updated to use a different configuration. For simplicity this step is therefore not required.
* If the installation of all python modules (packages) and PostgreSQL was successful, on opening “localhost:5000/reset” in a browser should produce the JSON output “Database schema.sql was successfully reset”.


### Frontend Installation
* Run “sudo apt update” to update the list of packages then “sudo apt install nodejs npm” to install nodejs and npm.
* Select “y” to install nodejs and npm
* Nodejs and npm are old versions but the python3 version is ok for our purposes.
* Run “sudo npm install -g n” then “sudo n stable” to install the current stable version of nodejs.
* Run “sudo npm install -g npm” to install the current stable version of npm and “sudo npm install -g yarn” to install the current stable version of yarn.
* Nodejs and npm should be the newer versions, yarn should now be installed and python3 should still be the same.
* If the frontend software and packages installed successfully and you’ve cloned the github project repository (see backend), change into “~/capstone-project-3900-h18b-codechefs/frontend”. Then run the command “yarn install”.
* Installation of the project needs to download many packages from node/yarn repositories, therefore installation might take a while.
* Once installation is complete run the command “yarn start”.
* The frontend should should start. If you get any error messages ensure the backend and database are running.

## Loading Sample Data
* This is a completely optional step, used to demonstrate the capabilities of the system with sample data.
* Change into directory “~/capstone-project-3900-h18b-codechefs/backend/src” then run the command “psql code_chefs_db < dbdump.sql”.
* The script should run to completion, and shouldn’t output any errors.
* Run “python3 server.py” in one tab or terminal window, and “yarn start” in another terminal window. The website with demo data should now be completely usable.
