from distutils.core import setup
import sys


VERSION_MAJOR = 0
VERSION_MINOR = 4
VERSION_PATCH = 4



versionstr  = '%s.%s.%s' % (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)


if sys.version_info[0] == 2:
    base_dir = 'python2'
elif sys.version_info[0] == 3:
    base_dir = 'python3'

setup(
    name='WeatherAlerts',
    version=versionstr,
    author='Zeb Palmer',
    author_email='zeb@zebpalmer.com',
    packages=['weatheralerts', 'weatheralerts.test'],
    package_dir={
        'weatheralerts': base_dir + "/weatheralerts"},
    scripts=[ base_dir + "/bin/NagiosWeatherAlerts.py", 
              base_dir + "/bin/MonitorAlertsByCounty.py"],
    url='http://github.com/zebpalmer/WeatherAlerts',
    license='GPLv3',
    description='Parse the National Weather Service Emergency Alerts Feed, do useful stuff with it',  
    long_description=open('README.rst').read(),
    classifiers=[
              'Development Status :: 3 - Alpha',
              'Environment :: Console',
              'Environment :: Plugins',
              'Intended Audience :: Developers',
              'Intended Audience :: Education',
              'Intended Audience :: End Users/Desktop',
              'Intended Audience :: Science/Research',
              'Intended Audience :: System Administrators',
              'Intended Audience :: Telecommunications Industry',
              'License :: OSI Approved :: GNU General Public License (GPL)',
              'Natural Language :: English',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.2',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Utilities'
              ],    
)

