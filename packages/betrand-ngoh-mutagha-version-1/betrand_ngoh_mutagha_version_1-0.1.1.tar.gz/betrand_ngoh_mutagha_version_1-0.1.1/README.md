# cicd
####
Go to steup.py edit the version
Go to setup edit the user name
######

Step 1: Clean the Workspace 
run:     rm -rf dist build *.egg-info
run:     rm -rf target
run:     rm -rf dist build *.egg-info target
run:      ls dist
####


####
Step 2: Build the Project
run:     python setup.py sdist bdist_wheel   
#####


###
upload to pypi
run:   twine upload dist/*
####


 ####
 It downloads and installs the package from PyPI into your local Python environment.
 pip install <setup_project_name> same name in pypi
#####

#####
to run it locally
python -m <the_root_directory_name_that_contain_your_application_with.app> 
example python -m hello_world_app.app
explain:
Python treats the app.py file inside the hello_world_app directory as a module. When you run
python -m hello_world_app.app .app refers to the app.py file inside that directory.
####


####
cloud
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m hello_world_app.app
