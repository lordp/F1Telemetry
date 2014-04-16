F1Telemetry
===========

The code here is a basic live timing system for Codemasters F1 2013 racing game, used in conjunction with the Racing League Charts website - https://racingleaguecharts.com

## Run Time Requirements ##

You may need to install a C++ Redistributable from Microsoft. You can download this [here](https://www.microsoft.com/en-us/download/confirmation.aspx?id=29).

## How to use ##

1. Unzip to a convenient directory
2. Run racingleaguecharts.exe
3. This must be run, configured and started **before** F1 2013.
4. (Un)Checking the 'Enable' checkbox in the General section will change the game config on the fly.
5. The forwarding system is untested, use at your own risk (and it doesn't save entered values... sorry).

## Development Requirements ##

32 bit copy of Python 2.7.6 plus 32 bit versions of the following:

1. [wxPython](http://wxpython.org)
2. [python-requests](http://python-requests.org)
3. [lxml](http://lxml.de/)
4. [WMI](https://pypi.python.org/pypi/WMI/1.4.9)
5. [PyWin32](http://sourceforge.net/projects/pywin32/)