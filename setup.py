from distutils.core import setup

setup(
    name = 'Atha',
    version = '0.0.2',
    
    author = 'Alan Thiessen',
    description = 'A Python UPnP Control Point with a mobile web front end geared towards home automation',
    license = 'GNU GPL',
    
    packages = ['atha', 'atha/ControlPoint', 'atha/core', 'atha/LightController']
)
