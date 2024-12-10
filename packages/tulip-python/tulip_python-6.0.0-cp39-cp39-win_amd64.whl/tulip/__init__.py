# This file is part of Tulip (https://tulip.labri.fr)
#
# Authors: David Auber and the Tulip development Team
# from LaBRI, University of Bordeaux
#
# Tulip is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# Tulip is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.


# start delvewheel patch
def _delvewheel_patch_1_9_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'tulip_python.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-tulip_python-6.0.0')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-tulip_python-6.0.0')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_9_0()
del _delvewheel_patch_1_9_0
# end delvewheel patch

__all__ = ['tlp']
__author__ = 'David Auber and the Tulip development Team'
__license__ = 'LGPLv3'
__version__ = "6.0.0"
__email__ = 'tulipdev@labri.fr'
__status__ = 'Production'

import os
import os.path
import platform
import sys
import traceback
import importlib

_tulipNativeLibsPath = os.path.join(os.path.dirname(__file__), 'native')
sys.path.append(_tulipNativeLibsPath)

if platform.system() == 'Windows':
    os.environ['PATH'] = '%s;%s;%s' % (
        _tulipNativeLibsPath,
        os.path.join(_tulipNativeLibsPath, '../../..'),
        os.environ['PATH'])
    paths = os.environ['PATH'].split(";")
    for p in paths:
        if os.path.isdir(p):
            os.add_dll_directory(p)

import _tulip # noqa

# cleanup
sys.path.pop()

class tlpType(_tulip.tlp.__class__):

    def __getattr__(cls, name):
        if hasattr(_tulip.tlp, name):
            return _tulip.tlp.getTulipGlobalVar(name)
        else:
            raise AttributeError(name)

    def __setattr__(cls, name, value):
        if hasattr(_tulip.tlp, name):
            _tulip.tlp.setTulipGlobalVar(name, value)
        else:
            super(tlpType, cls).__setattr__(name, value)


# utility function from the 'six' module
def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(metaclass, 'temporary_class', (), {})


class tlp(with_metaclass(tlpType, _tulip.tlp)):

    @staticmethod
    def loadTulipPythonPlugin(pluginFilePath):
        if not os.path.isfile(pluginFilePath):
            print('[tulip] Error: Path %s is not a valid file' %
                  pluginFilePath, file=sys.stderr)
            return False


        with open(pluginFilePath) as pluginFile:
            pluginFileContent = pluginFile.read()

            if 'tulipplugins.register' not in pluginFileContent:
                return False

            modulePath = os.path.dirname(pluginFilePath)
            moduleName = os.path.basename(pluginFilePath)[:-3]

            if modulePath not in sys.path:
                sys.path.append(modulePath)

            try:
                importlib.import_module(moduleName)
            except ImportError:
                print('There was an error when trying to load the tulip Python plugin from '+pluginFilePath, file=sys.stderr)
                traceback.print_exc()
                return False
            return True
        print("Error: Cannot open "+pluginFilePath, file=sys.stderr)
        traceback.print_exc()
        return False

    @staticmethod
    def loadTulipPluginsFromDir(pluginsDirPath, loadCppPlugin=True,
                                pluginLoader=None):
        if not os.path.exists(pluginsDirPath):
            return False

        if loadCppPlugin:
            tlp.loadPluginsFromDir(pluginsDirPath, pluginLoader, False)

        files = os.listdir(pluginsDirPath)

        for file in files:
            filePath = os.path.join(pluginsDirPath, file)
            if not os.path.isdir(filePath) and filePath.endswith('.py'):
                tlp.loadTulipPythonPlugin(filePath)

        for file in files:
            filePath = os.path.join(pluginsDirPath, file)
            if os.path.isdir(filePath):
                tlp.loadTulipPluginsFromDir(filePath, loadCppPlugin,
                                            pluginLoader)

        return True


tulipVersion = tlp.getTulipRelease()
tulipVersion = tulipVersion[:tulipVersion.rfind('.')]

startupScriptsPath = os.path.join(
    tlp.TulipLibDir, 'tulip/python/startup')
startupScriptsHomePath = os.path.join(
    os.path.expanduser('~'), '.Tulip-%s/python/startup' % tulipVersion)


def runStartupScripts(scriptsPath):
    if not os.path.exists(scriptsPath):
        return

    files = os.listdir(scriptsPath)

    for file in files:
        filePath = os.path.join(scriptsPath, file)
        if os.path.isfile(filePath) and filePath.endswith('.py'):
            with  open(filePath) as fd:
                exec(compile(fd.read(), filePath, 'exec'),
                 globals(), locals())


runStartupScripts(startupScriptsPath)
runStartupScripts(startupScriptsHomePath)

tlpPythonPluginsPath = os.path.join(
    tlp.TulipLibDir, 'tulip/python/tulip/plugins')
tlpPythonPluginsHomePath = os.path.join(
    os.path.expanduser('~'), '.Tulip-%s/plugins/python' % tulipVersion)

tlp.loadTulipPluginsFromDir(tlpPythonPluginsPath, False)
tlp.loadTulipPluginsFromDir(tlpPythonPluginsHomePath, False)

_tulipNativePluginsPath = os.path.join(_tulipNativeLibsPath, 'plugins')

# fix loading of Tulip plugins when the tulip module has been
# installed with the pip tool
if platform.system() == 'Linux' and os.path.exists(_tulipNativePluginsPath):
    dlOpenFlagsBackup = sys.getdlopenflags()
    dlOpenFlags = os.RTLD_NOW | os.RTLD_GLOBAL
    sys.setdlopenflags(dlOpenFlags)

tlp.loadTulipPluginsFromDir(_tulipNativePluginsPath)

# load bundled Tulip Python plugins when the tulip module has been
# installed with the pip tool
if not sys.argv[0] == 'tulip':
    tlp.loadTulipPluginsFromDir(
        os.path.join(os.path.dirname(__file__), 'plugins'))

if platform.system() == 'Linux' and os.path.exists(_tulipNativePluginsPath):
    sys.setdlopenflags(dlOpenFlagsBackup)
