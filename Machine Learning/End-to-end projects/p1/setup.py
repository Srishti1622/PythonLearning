# find_packages will automatically find out all the packages avaiable in the application
from setuptools import find_packages, setup
from typing import List

# it take filepath as string and returns a list of string having all the libraries name inside the list
def get_requirements(filepath:str)->List[str]:
    requirements=[]
    with open(filepath,'r') as file:
        requirements=file.readlines()
        requirements=[req.replace('\n','') for req in requirements]
        

# consider this as a metadata of entire application
setup(
    name='mlproject',
    version='0.0.1',
    author='Srishti',
    author_email='srishtia1622@gmail.com',
    packages=find_packages(),
    # install_requires=['pandas','numpy','seaborn']  # mention all the libraries which you want to install 
    install_requires=get_requirements('requirements.txt')
)