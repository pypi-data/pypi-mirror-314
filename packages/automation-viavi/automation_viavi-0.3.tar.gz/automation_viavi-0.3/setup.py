from setuptools import setup, find_packages

setup(
    name='automation_viavi',  # Numele pachetului
    version='0.3',
    description='Fetches state of the lab units and updates the Confluence page with them',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pomparau Renato',
    author_email='renato.pomparau@viavisolutions.com',
    packages=find_packages(),  # Găsește și include toate pachetele Python
    install_requires=[
        'pyserial',  # Pentru importul serial
        'requests',  # Pentru importul requests
        'beautifulsoup4',  # Pentru importul BeautifulSoup
    ],
        classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',  # Poți seta versiunea minimă de Python
)
