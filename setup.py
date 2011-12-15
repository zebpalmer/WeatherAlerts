from distutils.core import setup

setup(
    name='WeatherAlerts',
    version='0.4.1build3',
    author='Zeb Palmer',
    author_email='zeb@zebpalmer.com',
    packages=['weatheralerts', 'weatheralerts.test'],
    scripts=['bin/NagiosWeatherAlerts.py'],
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
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.2',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Utilities'
              ],    
)


