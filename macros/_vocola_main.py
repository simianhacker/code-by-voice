# _vocola_main.py - NatLink support for Vocola
# -*- coding: latin-1 -*-
#
# Contains:
#    - "Built-in" voice commands
#    - Autoloading of changed command files
#
#
# Copyright (c) 2002-2012 by Rick Mohr.
# 
# Portions Copyright (c) 2012-2013 by Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


#
# WARNING: This version of _vocola_main.py has been modified to work
#          with Quintijn's installer/version of NatLink and has a
#          number of unofficial changes/improvements.  The code has
#          been organized to minimize the diff's with the official
#          version.
#

import string
import sys
import os               # access to file information
import os.path          # to parse filenames
import time             # print time in messages
from   stat import *    # file statistics
import re
import natlink
from   natlinkutils import *



###########################################################################
#                                                                         #
# Configuration                                                           #
#                                                                         #
###########################################################################

# The Vocola translator is a perl program. By default we use the precompiled
# executable vcl2py.exe, which doesn't require installing perl.
# To instead use perl and vcl2py.pl, set the following variable to 1:
usePerl = 0


try:
    import natlinkstatus
    Quintijn_installer = True
    status             = natlinkstatus.NatlinkStatus()
    VocolaEnabled      = not not status.getVocolaUserDirectory()
    language           = status.getLanguage()
except ImportError:
    Quintijn_installer = False
    VocolaEnabled      = True
    language           = 'enx'


# get location of MacroSystem folder:
NatLinkFolder = os.path.split(
    sys.modules['natlinkmain'].__dict__['__file__'])[0]
# (originally, natlinkmain lived in MacroSystem, not MacroSystem\core)
NatLinkFolder = re.sub(r'\core$', "", NatLinkFolder)


VocolaFolder     = os.path.normpath(os.path.join(NatLinkFolder, '..', 'Vocola'))
ExecFolder       = os.path.normpath(os.path.join(NatLinkFolder, '..', 'Vocola', 'exec'))
# C module "simpscrp" defines Exec(), which runs a program in a minimized
# window and waits for completion. Since such modules need to be compiled
# separately for each python version we need this careful import:
pydFolder        = os.path.normpath(os.path.join(NatLinkFolder, '..', 'Vocola', 'exec', sys.version[0:3]))
ExtensionsFolder = os.path.normpath(os.path.join(NatLinkFolder, '..', 'Vocola', 'extensions'))

NatLinkFolder    = os.path.abspath(NatLinkFolder)

if VocolaEnabled:
    sys.path.append(pydFolder)
    sys.path.append(ExecFolder)
    sys.path.append(ExtensionsFolder)


def get_command_folder():
    configured = None
    try:
        import natlinkstatus
        # Quintijn's's installer:
        configured = natlinkstatus.NatlinkStatus().getVocolaUserDirectory()
    except ImportError:
        try:
            import RegistryDict
            import win32con
            # Scott's installer:
            r = RegistryDict.RegistryDict(win32con.HKEY_CURRENT_USER,
                                          "Software\NatLink")             
            if r:                                                         
                configured = r["VocolaUserDirectory"]              
        except ImportError:
            pass
    if os.path.isdir(configured):                      
        return configured

    systemCommandFolder = os.path.join(VocolaFolder, 'Commands')
    if os.path.isdir(systemCommandFolder):
        return systemCommandFolder

    return None
    
commandFolder = get_command_folder()
if VocolaEnabled and not commandFolder:
    print >> sys.stderr, "Warning: no Vocola command folder found!"


## 
## Quintijn's unofficial multiple language kludge:
## 

def copyVclFileLanguageVersion(Input, Output):
    """copy to another location, keeping the include files one directory above
    """
    # let include lines to relative paths point to the folder above ..\
    # so you can take the same include file for the alternate language.
    reInclude = re.compile(r'(include\s+)\w')
    Input     = os.path.normpath(Input)
    Output    = os.path.normpath(Output)
    input     = open(Input, 'r').read()
    output    = open(Output, 'w')
    output.write("# vocola file for alternate language: %s\n"% language)
    lines = map(string.strip, str(input).split('\n'))
    for line in lines:
        if reInclude.match(line):
            line = 'include ..\\' + line[8:]
        output.write(line + '\n')
    output.close()                

def copyToNewSubDirectory(trunk, subdirectory):
    for f in os.listdir(trunk):
        if f.endswith('.vcl'):
            copyVclFileLanguageVersion(os.path.join(trunk, f),
                                       os.path.join(subdirectory, f))

if VocolaEnabled and status.getVocolaTakesLanguages():
    print '_vocola_main started with language: %s' % language
    if language != 'enx' and commandFolder:
        uDir  = commandFolder
        uDir2 = os.path.join(uDir, language)
        if not os.path.isdir(uDir2):
            print 'creating userCommandFolder for language %s' % language
            os.mkdir(uDir2)
            copyToNewSubDirectory(uDir, uDir2)
        commandFolder = uDir2



###########################################################################
#                                                                         #
# The built-in commands                                                   #
#                                                                         #
###########################################################################

class ThisGrammar(GrammarBase):

    gramSpec = """
        <NatLinkWindow>     exported = [Show] (NatLink|Vocola) Window;
        <edit>              exported = Edit [Voice] Commands;
        <editGlobal>        exported = Edit Global [Voice] Commands;
        <editMachine>       exported = Edit Machine [Voice] Commands;
        <editGlobalMachine> exported = Edit Global Machine [Voice] Commands;
        <loadAll>           exported = Load All [Voice] Commands;
        <loadCurrent>       exported = Load [Voice] Commands;
        <loadGlobal>        exported = Load Global [Voice] Commands;
        <loadExtensions>    exported = Load [Voice] Extensions;
        <discardOld>        exported = Discard Old [Voice] Commands;
    """

    if language == 'nld':
        gramSpec = """
<NatLinkWindow>     exported = Toon (NatLink|Vocola) venster;
<edit>              exported = (Eddit|Bewerk|Sjoo|Toon)(Commandoos|Commands) |
                               (Eddit|Bewerk|Sjoo|Toon)(stem|vojs)(Commandoos|Commands);
<editGlobal>        exported = (Eddit|Bewerk|Sjoo|Toon) (Global|globale) [stem|vojs] (Commandoos|Commands);
<editMachine>       exported = (Eddit|Bewerk|Sjoo|Toon) Machine [stem|vojs] (Commandoos|Commands);
<editGlobalMachine> exported = (Eddit|Bewerk|Sjoo|Toon) (Global|globale) Machine [stem|vojs] (Commandoos|Commands);
<loadAll>           exported = (Laad|Lood) alle [stem|vojs] (Commandoos|Commands);
<loadCurrent>       exported = (Laad|Lood) [stem|vojs] (Commandoos|Commands);
<loadGlobal>        exported = (Laad|Lood) globale [stem|vojs] (Commandoos|Commands);
<loadExtensions>    exported = Laad [stem] extensies;
<discardOld>        exported = (Discard|Verwijder) (oude|oold) [stem|vojs] (Commandoos|Commands);
    """
    elif language == 'fra':
        gramSpec = """
<NatLinkWindow>     exported = [Afficher] Fenetre (NatLink|Vocola);
<edit>              exported = Editer Commandes [Vocales];
<editGlobal>        exported = Editer Commandes [Vocales] Globales;
<editMachine>       exported = Editer Commandes [Vocales] Machine;
<editGlobalMachine> exported = Editer Commandes [Vocales] Globales Machine;
<loadAll>           exported = Charger Toutes Les Commandes [Vocales];
<loadCurrent>       exported = Charger Commandes [Vocales];
<loadGlobal>        exported = Charger Commandes [Vocales] Globales;
<loadExtensions>    exported = Charger Extensions [Vocales];
<discardOld>        exported = Effacer Commandes [Vocales] Precedentes;
    """
    elif language == 'deu':
        gramSpec = """
<NatLinkWindow>     exported = [Zeige] (NatLink|Vocola) Fenster;
<edit>              exported = Bearbeite [Sprach] Befehle;
<editGlobal>        exported = Bearbeite globale [Sprach] Befehle;
<editMachine>       exported = Bearbeite Maschinen [Sprach] Befehle;
<editGlobalMachine> exported = Bearbeite globale Maschinen [Sprach] Befehle;
<loadAll>           exported = Lade alle [Sprach] Befehle;
<loadCurrent>       exported = Lade [Sprach] Befehle;
<loadGlobal>        exported = Lade globale [Sprach] Befehle;
<loadExtensions>    exported = Lade [Sprach] Extensions;
<discardOld>        exported = Verwerfe alte [Sprach] Befehle;
    """   
    elif language == 'ita':
        gramSpec = """
<NatLinkWindow>     exported = [Mostra] Finestra Di (NatLink|Vocola);
<edit>              exported = Modifica Comandi [Vocali];
<editGlobal>        exported = Modifica Comandi [Vocali] Globali;
<editMachine>       exported = Modifica Comandi [Vocali] [del] Computer;
<editGlobalMachine> exported = Modifica Comandi [Vocali] Globali [del] Computer;
<loadAll>           exported = Carica Tutti I Comandi [Vocali];
<loadCurrent>       exported = Carica I Comandi [Vocali];
<loadGlobal>        exported = Carica Comandi [Vocali] Gliobali;
<loadExtensions>    exported = Carica Estensioni [Vocali];
<discardOld>        exported = Annulla Vecchi Comandi [Vocali];
    """
    elif language == 'esp':
        gramSpec = """
<NatLinkWindow>     exported = [Mostrar] Ventana de (NatLink|Vocola) ;
<edit>              exported = (Modificar|Editar) Comandos [de voz];
<editGlobal>        exported = (Modificar|Editar) Comandos [de voz] Globales ;
<editMachine>       exported = (Modificar|Editar) Comandos [de voz] de (este ordenador|la Computadora);
<editGlobalMachine> exported = (Modificar|Editar) Comandos [de voz] Globales de (este ordenador|la Computadora);
<loadAll>           exported = (Recargar|Cargar) Todos Los Comandos [de voz];
<loadCurrent>       exported = (Recargar|Cargar) Comandos [de voz];
<loadGlobal>        exported = (Recargar|Cargar) Comandos [de voz] Globales;
<loadExtensions>    exported = (Recargar|Cargar) Extensiones [de voz];
<discardOld>        exported = Descartar Comandos [de voz] Viejos;
    """
    elif language != 'enx':
        print >> sys.stderr,  """\n\n
Vocola Warning: no language "%s" translations for the built-in Vocola
commands (e.g., commands to load voice commands) are currently
available; consider helping translate them -- inquire on
http://www.speechcomputing.com.  For now the English versions, like "Edit
Commands" and "Edit Global Commands" are activated.
""" % language
        

    def initialize(self):
        self.updateUnimacroHeaderIfNeeded()

        if os.environ.has_key('COMPUTERNAME'):
            self.machine = string.lower(os.environ['COMPUTERNAME'])
        else: self.machine = 'local'

        self.load_extensions()
        self.loadAllFiles(False)

        self.load(self.gramSpec)
        self.activateAll()

    def gotBegin(self,moduleInfo):
        self.currentModule = moduleInfo
        # delay enabling until now to avoid NatLink clobbering our callback:
        enable_callback() 

                                      
    # Get app name by stripping folder and extension from currentModule name
    def getCurrentApplicationName(self):
        return string.lower(os.path.splitext(os.path.split(self.currentModule[0]) [1]) [0])


### Miscellaneous commands

    # "Show NatLink Window" -- print to output window so it appears
    def gotResults_NatLinkWindow(self, words, fullResults):
        print "This is the NatLink/Vocola output window"

    # "Load Extensions" -- scan for new/changed extensions:
    def gotResults_loadExtensions(self, words, fullResults):
        self.load_extensions(True)
        for module in sys.modules.keys():
            if module.startswith("vocola_ext_"):
                del sys.modules[module]

    def load_extensions(self, verbose=False):
        #if sys.modules.has_key("scan_extensions"):
        #    del sys.modules["scan_extensions"]
        import scan_extensions
        arguments = ["scan_extensions", ExtensionsFolder]
        if verbose:
            arguments.insert(1, "-v")
        scan_extensions.main(arguments)


### Loading Vocola Commands

    # "Load All Commands" -- translate all Vocola files
    def gotResults_loadAll(self, words, fullResults):
        self.loadAllFiles(True)

    # "Load Commands" -- translate Vocola files for current application
    def gotResults_loadCurrent(self, words, fullResults):
        self.loadSpecificFiles(self.getCurrentApplicationName())

    # "Load Global Commands" -- translate global Vocola files
    def gotResults_loadGlobal(self, words, fullResults):
        self.loadSpecificFiles('')

    # "Discard Old [Voice] Commands" -- purge output then translate all files
    def gotResults_discardOld(self, words, fullResults):
        purgeOutput()
        self.loadAllFiles(True)

    # Load all command files
    def loadAllFiles(self, force):
        if commandFolder:
            compile_Vocola(commandFolder, force)

    # Load command files for specific application
    def loadSpecificFiles(self, module):
        special = re.compile(r'([][()^$.+*?{\\])')
        pattern = "^" + special.sub(r'\\\1', module)
        pattern += "(_[^@]*)?(@" + special.sub(r'\\\1', self.machine)
        pattern += ")?\.vcl$"
        p = re.compile(pattern)

        targets = []
        if commandFolder:
            targets += [os.path.join(commandFolder,f)
                        for f in os.listdir(commandFolder) if p.search(f)]
        if len(targets) > 0:
            for target in targets:
                self.loadFile(target)
        else:
            print >> sys.stderr
            if module == "":
                print >> sys.stderr, "Found no Vocola global command files [for machine '" + self.machine + "']"
            else:
                print >> sys.stderr, "Found no Vocola command files for application '" + module + "' [for machine '" + self.machine + "']"

    # Load a specific command file, returning false if not present
    def loadFile(self, file):
        try:
            os.stat(file)
            compile_Vocola(file, False)
            return True
        except OSError:
            return False   # file not found


### Editing Vocola Command Files

    # "Edit Commands" -- open command file for current application
    def gotResults_edit(self, words, fullResults):
        app = self.getCurrentApplicationName()
        file = app + '.vcl'
        comment = 'Voice commands for ' + app
        self.openCommandFile(file, comment)

    # "Edit Machine Commands" -- open command file for current app & machine
    def gotResults_editMachine(self, words, fullResults):
        app = self.getCurrentApplicationName()
        file = app + '@' + self.machine + '.vcl'
        comment = 'Voice commands for ' + app + ' on ' + self.machine
        self.openCommandFile(file, comment)

    # "Edit Global Commands" -- open global command file
    def gotResults_editGlobal(self, words, fullResults):
        file = '_vocola.vcl'
        comment = 'Global voice commands'
        self.openCommandFile(file, comment)

    # "Edit Global Machine Commands" -- open global command file for machine
    def gotResults_editGlobalMachine(self, words, fullResults):
        file = '_vocola@' + self.machine + '.vcl'
        comment = 'Global voice commands on ' + self.machine
        self.openCommandFile(file, comment)


    def FindExistingCommandFile(self, file):
        if commandFolder:
            f = commandFolder + '\\' + file
            if os.path.isfile(f): return f

        return ""
    
    # Open a Vocola command file (using the application associated with ".vcl")
    def openCommandFile(self, file, comment):
        if not commandFolder:
            print >> sys.stderr, "Error: Unable to create command file because no Vocola command folder found."
            return

        path = self.FindExistingCommandFile(file)
        if not path:
            path = commandFolder + '\\' + file

            new = open(path, 'w')
            new.write('# ' + comment + '\n\n')
            # insert include line to Unimacro.vch:
            if status.getVocolaTakesUnimacroActions():
                if language == 'enx' or not status.getVocolaTakesLanguages():
                    includeLine = 'include Unimacro.vch;\n\n'
                else:
                    includeLine = 'include ..\\Unimacro.vch;\n\n'
                new.write(includeLine)                    
            new.close()

        wantedPath = os.path.join(commandFolder, file)
        if path and path != wantedPath:
            # copy from other location
            if wantedPath.startswith(path) and len(wantedPath) - len(path) == 3:
                print 'copying enx version to language version %s'% language
                copyVclFileLanguageVersion(path, wantedPath)
            else:
                print 'copying from other location'
                self.copyVclFile(path, wantedPath)
            path = wantedPath   

        #
        # NatLink/DNS bug causes os.startfile or wpi32api.ShellExecute
        # to crash DNS if allResults is on in *any* grammer (e.g., Unimacro)
        #
        # Accordingly, use AppBringUp instead:
        #

        #try:
        #    os.startfile(path)
        #except WindowsError, e: 
        #    print
        #    print "Unable to open voice command file with associated editor: " + str(e)
        #    print "Trying to open it with notepad instead."
        #    prog = os.path.join(os.getenv('WINDIR'), 'notepad.exe')
        #    os.spawnv(os.P_NOWAIT, prog, [prog, path])
        natlink.execScript("AppBringUp \"" + path + "\", \"" + path + "\"")

    def copyVclFile(self, Input, Output):
        """copy to another location
        """
        # QH, febr, 5, 2008
        Input  = os.path.normpath(Input)
        Output = os.path.normpath(Output)

        input  = open(Input, 'r').read()
        output = open(Output, 'w')
        output.write("# vocola file from a sample directory %s\n"% Input)
        lines = map(string.strip, str(input).split('\n'))
        for line in lines:
            output.write(line + '\n')
        output.close()                

    def updateUnimacroHeaderIfNeeded(self):
        import shutil
        if not status.getVocolaTakesUnimacroActions(): 
            return
        
        destDir              = status.getVocolaUserDirectory()
        sourceDir            = os.path.join(status.getUserDirectory(), 'vocola_compatibility')
        destPath             = os.path.join(destDir,   'Unimacro.vch')
        sourcePath           = os.path.join(sourceDir, 'Unimacro.vch')
        sourceTime, destTime = vocolaGetModTime(sourcePath), vocolaGetModTime(destPath)

        if not (sourceTime or destTime):
            print >> sys.stderr, """\n
Error: The option "Vocola Takes Unimacro Actions" is switched on, but
no file "Unimacro.vch" is found.

Please fix the configuration of NatLink/Vocola/Unimacro and restart
Dragon.  Either ensure the source file is at:
    "%s",
or switch off the option "Vocola Takes Unimacro Actions".
"""% sourceDir
            return
        
        if destTime < sourceTime:
            try:
                shutil.copyfile(sourcePath, destPath)
            except IOError:
                print >> sys.stderr, """\n
Warning: Could not copy example "Unimacro.vch" to:
    "%s".

There is a valid "Unimacro.vch" available, but a newer file is
available at: "%s".

Please fix the configuration of NatLink/Vocola/Unimacro and restart
Dragon, if you want to use the updated version of this file."""% (destDir, sourceDir)
            else:
                print 'Succesfully copied "Unimacro.vch" from\n\t"%s" to\n\t"%s".'% (sourceDir, destDir)




###########################################################################
#                                                                         #
# Compiling Vocola files                                                  #
#                                                                         #
###########################################################################

may_have_compiled = False  # has the compiler been called?
compile_error     = False  # has a compiler error occurred?

# Run Vocola compiler, converting command files from "inputFileOrFolder"
# and writing output to NatLink/MacroSystem
def compile_Vocola(inputFileOrFolder, force):
    global may_have_compiled, compiler_error

    may_have_compiled = True

    # below line currently needed because kludge changes the the folder:
    VocolaFolder = os.path.normpath(os.path.join(NatLinkFolder, '..', 'Vocola'))
    if usePerl:
        executable = "perl"
        arguments  = [VocolaFolder + r'\exec\vcl2py.pl']
    else:
        executable = VocolaFolder + r'\exec\vcl2py.exe'
        arguments  = []
    executable = sys.prefix + r'\python.exe'
    arguments  = [VocolaFolder + r'\exec\vcl2py.py']

    arguments += ['-extensions', ExtensionsFolder + r'\extensions.csv']
    if language == "enx":
        arguments += ['-numbers', 
                      'zero,one,two,three,four,five,six,seven,eight,nine']

    arguments += ["-suffix", "_vcl" ]
    if force: arguments += ["-f"]

    arguments += [inputFileOrFolder, NatLinkFolder]
    hidden_call(executable, arguments)

    logName = commandFolder + r'\vcl2py_log.txt'
    if os.path.isfile(logName):
        try:
            log = open(logName, 'r')
            compiler_error = True
            print  >> sys.stderr, log.read()
            log.close()
            os.remove(logName)
        except IOError:  # no log file means no Vocola errors
            pass

# Unload all commands, including those of files no longer existing
def purgeOutput():
    pattern = re.compile("_vcl\d*\.pyc?$")
    [os.remove(os.path.join(NatLinkFolder,f)) for f 
     in os.listdir(NatLinkFolder) if pattern.search(f)]

# 
# Run program with path executable and arguments arguments.  Waits for
# the program to finish.  Runs the program in a hidden window.
# 
def hidden_call(executable, arguments):
    args = [executable] + arguments
    try:
        # Using simpscrp is depreciated; remove '_disabled' below to use:
        import simpscrp_disabled
        args = ['"' + str(x) + '"' for x in args]
        call = ' '.join(args)
        simpscrp.Exec(call, 1)
    except ImportError:
        try:
            import subprocess
            si             = subprocess.STARTUPINFO()
            # Location of below constants seems to vary from Python
            # version to version so hardcode them:
            si.dwFlags     = 1 # subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = 0 # subprocess.SW_HIDE
            return subprocess.call(args, startupinfo=si)
        except ImportError:
            pid = os.spawnv(os.P_NOWAIT, executable, args)
            pid, exit_code = os.waitpid(pid, 0)
            exit_code = exit_code >> 8
            return exit_code


lastVocolaFileTime    = 0
lastCommandFolderTime = 0

def compile_changed():
    global lastVocolaFileTime, lastCommandFolderTime
    global compiler_error

    current = getLastVocolaFileModTime()
    if current > lastVocolaFileTime:
        compiler_error = False
        thisGrammar.loadAllFiles(False)
        if not compiler_error:
            lastVocolaFileTime =  current

    #source_changed = False
    #if commandFolder:
    #    if vocolaGetModTime(commandFolder) > lastCommandFolderTime:
    #        lastCommandFolderTime = vocolaGetModTime(commandFolder)
    #        source_changed = True
    #if source_changed:
    #    deleteOrphanFiles()

# Returns the newest modified time of any Vocola command folder file or
# 0 if none:
def getLastVocolaFileModTime():
    last = 0
    if commandFolder:
        last = max([last] +
                   [vocolaGetModTime(os.path.join(commandFolder,f))
                    for f in os.listdir(commandFolder)])
    return last

# Returns the modification time of a file or 0 if the file does not exist:
def vocolaGetModTime(file):
    try: return os.stat(file)[ST_MTIME]
    except OSError: return 0        # file not found


def deleteOrphanFiles():
    print "checking for orphans..."
    for f in os.listdir(NatLinkFolder):
        if not re.search("_vcl.pyc?$", f): continue

        s = getSourceFilename(f)
        if s:
            if vocolaGetModTime(s)>0: continue

        f = os.path.join(NatLinkFolder, f)
        print "Deleting: " + f
        os.remove(f)

def getSourceFilename(output_filename):
    m = re.match("^(.*)_vcl.pyc?$", output_filename)
    if not m: return None                    # Not a Vocola file
    name = m.group(1)
    if not commandFolder: return None

    marker = "e_s_c_a_p_e_d__"
    m = re.match("^(.*)" + marker + "(.*)$", name)  # rightmost marker!
    if m:
        name = m.group(1)
        tail = m.group(2)
        tail = re.sub("__a_t__", "@", tail)
        tail = re.sub("___", "_", tail)
        name += tail

    name = re.sub("_@", "@", name)
    return commandFolder + "\\" + name + ".vcl"


lastNatLinkModTime = 0

# Check for changes to our output .py files and report status relative
# to last time this routine was called; return code means:
#   0: no changes
#   1: 1 or more existing .py files were modified, but no new .py files created
#   2: one or more new .py files may have been created, plus maybe existing changed
def output_changes():
    global lastNatLinkModTime, may_have_compiled

    old_may_have_compiled = may_have_compiled
    may_have_compiled = False

    current = vocolaGetModTime(NatLinkFolder)
    if current > lastNatLinkModTime:
        lastNatLinkModTime = current
        return 2

    if old_may_have_compiled:
        return 1
    else:
        return 0


# When speech is heard this function will be called before any others.
#
# Must return result of output_changes() so we can tell NatLink when
# files need to be loaded.
def utterance_start_callback(moduleInfo):
    compile_changed()
    return output_changes()



###########################################################################
#                                                                         #
# Callback handling                                                       #
#                                                                         #
###########################################################################

# 
# With Quintijn's installer as of February 4, 2008:
# 
#   _vocola_main is loaded before any other NatLink modules
#   vocolaBeginCallback is called directly by natlinkmain before any
#     other grammer's gotBegin method
#   natlinkmain now guarantees we are not called with CallbackDepth>1
#   we return the result of output_changes() directly rather than
#     massaging NatLink to deal with new .py files
#


callback_enabled = False

def enable_callback():
    global callback_enabled
    if not callback_enabled:
        callback_enabled = True
        if not Quintijn_installer:
            # Replace NatLink's "begin" callback function with ours:
            natlink.setBeginCallback(vocolaBeginCallback)

def disable_callback():
    global callback_enabled
    callback_enabled = False
    if not Quintijn_installer:
        natlink.setBeginCallback(beginCallback)


def vocolaBeginCallback(moduleInfo):
    if not callback_enabled:
        return 0

    changes = 0
    if Quintijn_installer or getCallbackDepth()<2:
        changes = utterance_start_callback(moduleInfo)

    if Quintijn_installer:
        return changes
    else:
        if changes > 1:
            # make sure NatLink sees any new .py files:
            natlinkmain.findAndLoadFiles()
            natlinkmain.loadModSpecific(moduleInfo)
        natlinkmain.beginCallback(moduleInfo)



###########################################################################
#                                                                         #
# Startup/shutdown                                                        #
#                                                                         #
###########################################################################

thisGrammar = None

# remove previous Vocola/Python compilation output as it may be out of
# date (e.g., new compiler, source file deleted, partially written due
# to crash, new machine name, etc.):
purgeOutput()

if not VocolaEnabled:
    print "Vocola not active"
else:
    print "Vocola version 2.8I starting..."
    thisGrammar = ThisGrammar()
    thisGrammar.initialize()


def unload():
    global thisGrammar
    disable_callback()
    if thisGrammar: thisGrammar.unload()
    thisGrammar = None
