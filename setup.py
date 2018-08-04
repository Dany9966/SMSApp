from setuptools import setup, find_packages

setup(
    name="SMS",
    version="0.0.1",
    author="Daniel Vincze",
    description="""
Supercalifragilisticexpialidocius Monitoring System (SMS) that monitors client
system resource usage (i.e. CPU percentage) and stores data on server app
""",
    packages=find_packages(),
    install_requires=['pika', 'sqlalchemy', 'psutil', 'flask'],
    entry_points={
        'console_scripts': [
            'SMS_client = SMS.cmd.client:main',
            'SMS_server = SMS.cmd.server:main',
        ],
    }
)
