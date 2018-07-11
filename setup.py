from setuptools import setup

setup(
    name="SMS",
    version="0.0.1",
    author="Daniel Vincze",
    description="""
Supercalifragilisticexpialidocius Monitoring System (SMS) that monitors client
system resource usage (i.e. CPU percentage) and stores data on server app
""",
    packages=['SMS'],
    install_requires=['pika', 'sqlalchemy'],
    entry_points={
        'console_scripts': [
            'SMS_client = SMS.cmd.client:main',
            'SMS_server = SMS.cmd.server:main',
        ],
    }
)
