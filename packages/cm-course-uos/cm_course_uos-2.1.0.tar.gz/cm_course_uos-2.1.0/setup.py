from setuptools import setup
import fnmatch
import os

PACKAGE_NAME = "cm_course_uos"
VERSION = "2.1.0"

def find_pyc_files():
    matches = []
    for root, dirnames, filenames in os.walk(PACKAGE_NAME):
        for filename in fnmatch.filter(filenames, '*.pyc'):
            # Append the path from root to filename
            matches.append(os.path.join(root[len(PACKAGE_NAME)+1:], filename))
    return matches


setup(
    name=PACKAGE_NAME,
    version=VERSION, #always increase this number before pushing to master -- x.y.z. : small edits, change "z", big edits & new files, change "y"
    description='This package hosts code required to run the colab notebooks which host the course assignemnts.',
    long_description='The package is separated into submodules "ps1","ps2".. which respectively host the code for each problem set. The main reasons this package was created were hiding unnecessary complexity from the students and enabling us to perform automating testing, grading and task aids while discouraging cheating. Cheating is still possible by installing the package and reverse engineering the functions but the effort would be better spent on solving the task.',
    author='smusslick,denizmgun,melisaaltinyelek,pelinito,rbastian',
    author_email='dguen@uos.de',
    url='https://github.com/denizmgun/cm-course-uos',
    install_requires=[
        # List any dependencies your package requires
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    package_data={'':find_pyc_files()},
    include_package_data=True,
    zip_safe=False
)