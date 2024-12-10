from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        print("Running systemd commands...")
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "lab-automation.service"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "lab-automation.timer"], check=True)
        subprocess.run(["sudo", "systemctl", "start", "lab-automation.timer"], check=True)
setup(
    name='automation_viavi',
    version='1.0',
    description='Fetches state of the lab units and updates the Confluence page with them',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pomparau Renato',
    author_email='renato.pomparau@viavisolutions.com',
    packages=find_packages(),  
    entry_points={
        'console_scripts':[
            'automation = lab_automation.automation:main' 
                          ]      
                 },
    install_requires=[
        'pyserial', 
        'requests',  
        'beautifulsoup4',  
    ],
        data_files=[
        ('/etc/systemd/system', [
            'systemd/lab-automation.service',
            'systemd/lab-automation.timer',
        ]),
    ],
        classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0', 
)
