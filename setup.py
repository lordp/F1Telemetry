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
      "icon_resources": [(1, "rlc.ico")]
    }
  ],
  data_files = [ ( '', [ 'config.ini' ] ) ],
  zipfile = 'lib\\library.zip'
)
