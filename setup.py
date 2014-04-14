from distutils.core import setup
import py2exe

setup(
  options = {
    'py2exe': {
        'dll_excludes': ['MSVCP90.dll', 'HID.DLL', 'w9xpopen.exe'],
        'includes': ['lxml.etree', 'lxml._elementpath', 'gzip'],
      }
    },
  windows = [
    {
      "script": 'racingleaguecharts.py',
      "icon_resources": [(1, "rlc.ico")],
      "name": "Racing League Charts Logger",
      "version": "0.9.2"
    }
  ],
  data_files = [ ( '', [ 'config.ini' ] ) ],
  zipfile = 'lib\\library.zip'
)
