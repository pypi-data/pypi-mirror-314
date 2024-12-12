# Cognitive Modeling Course UOS Python Package

## Purpose of this repo
This repo comprises the cm-course-uos python package intended to supplement the Cognitive Modeling Assignments for Students at the University of Osnabrueck. The repository is private to prevent solution leaks. The changes you create here will be available on google colab or wherever else you install the package "cm-course-uos"


## Colaborating on GitHub

### Example Workflow
(first time working with it: `git clone https://github.com/denizmgun/cm-course-uos.git`)

0. `git pull`
1. Edit <yourproblemset.py>
2. `pylint .\cm_course_uos\<yourproblemset>.py` (back to 1. if pylint complains, `pip install pylint` if you don't have it)
3. increase version number in "setup.py"
4. `git add .`
5. `git commit -m "<your changes>"`
6. `git push origin master`
7. Check whether there is a green check mark on github


### Installation
The package can be installed in colab or other environments via
```
pip install cm-course-uos
```

### Package Updates
With every push to master, a github workflow automatically builds the python package and uploads the package binaries to PyPi. Make sure to increase the version number in `setup.py` before every push to master. Otherwise the package release on PyPi will be rejected because of duplicate version numbers. 


### Note on Cheating
Cheating is still possible by decompiling the package in an IDE such as pycharm. This can be circumvented by adding a check in `setup.py` for  environment variables like "COLAB_GPU" and preventing installations if they're not found. This seems to be excessive for now ( may create other problems) but can be easily implemented if needed.