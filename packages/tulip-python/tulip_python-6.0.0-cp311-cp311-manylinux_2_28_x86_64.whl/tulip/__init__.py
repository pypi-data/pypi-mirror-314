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
