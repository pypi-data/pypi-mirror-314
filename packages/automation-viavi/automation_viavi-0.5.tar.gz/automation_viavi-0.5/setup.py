from setuptools import setup, find_packages

setup(
    name='automation_viavi',
    version='0.5',
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
        classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0', 
)
