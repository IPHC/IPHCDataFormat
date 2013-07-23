import os
import sys
import commands
import glob
import multiprocessing

YELLOW = '\x1b[33m'
RED    = '\x1b[31m'
PINK   = '\x1b[35m'
NORMAL = '\x1b[0m'
CYAN   = '\x1b[36m'
class IPHCcommon:

    def __init__(self,script):
        self.script = script
        self.CMSSW_DIR   = ""
        self.SCRIPT_FILE = ""
        self.CURRENT_DIR = ""
        self.IPHCAnalysis         = False
        self.IPHCDataFormat       = False
        self.IPHCProducer         = False
        self.IPHCMinitreeAnalysis = False
        self.ncores = 1

    def DisplayHeader(self,release):

        # Script header
        print " "
        print YELLOW+"##############################################"+NORMAL
        print YELLOW+"#                  Warning                   #"+NORMAL
        print YELLOW+"#   this script assume that you're using     #"+NORMAL
        print YELLOW+"#"+self.Center("[ "+release+" ]",44)+"#"+NORMAL
        print YELLOW+"##############################################"+NORMAL
        print " "
        print CYAN+"Hello, "+os.getlogin()+"."+NORMAL
        print CYAN+"You're looking well today."+NORMAL
        print ""

    def CleanFolderName(self,name):
        newname=os.path.expandvars(name)
        newname=os.path.expanduser(newname)
        newname=os.path.normpath(newname)
        newname=os.path.realpath(newname)
        return newname
        
    def AskNCores(self):
        nmaxcores=multiprocessing.cpu_count()
        print YELLOW+"How many cores for the compiling? default = max = " +\
                     str(nmaxcores)+NORMAL
        
        test=False
        while(not test):
            answer=raw_input("Answer: ")
            if answer=="":
                test=True
                ncores=nmaxcores
                break
            try:
                ncores=int(answer)
            except:    
                test=False
                continue
            if ncores<=nmaxcores and ncores>0:
                test=True
                    
        self.ncores=ncores
        

    def CheckConfiguration(self):

        # Getting CMSSW folder by using the CMSSW_BASE variable
        try:
            self.CMSSW_DIR=os.environ["CMSSW_BASE"]
        except:
            print RED+"ERROR: environment variable $CMSSW_BASE is not defined"+NORMAL
            print RED+"       have you typed 'cmsenv' ?"+NORMAL
            sys.exit()
        self.CMSSW_DIR=self.CleanFolderName(self.CMSSW_DIR+'/src')

        # Getting folder of the present script
        self.SCRIPT_FILE=os.path.realpath(self.script)
        self.SCRIPT_FILE=self.CleanFolderName(self.SCRIPT_FILE)

        # Getting current folder
        self.CURRENT_DIR=os.getcwd()
        self.CURRENT_DIR=self.CleanFolderName(self.CURRENT_DIR)

        # Looking for IPHC packages
        self.IPHCDataFormat       = os.path.isdir(self.CMSSW_DIR+'/IPHCDataFormat')
        self.IPHCProducer         = os.path.isdir(self.CMSSW_DIR+'/IPHCProducer')
        self.IPHCAnalysis         = os.path.isdir(self.CMSSW_DIR+'/IPHCAnalysis')
        self.IPHCMinitreeAnalysis = os.path.isdir(self.CMSSW_DIR+'/IPHCMinitreeAnalysis')
        
        # Displaying CMSSW folder
        print YELLOW+"Your configuration:"+NORMAL
        print YELLOW+" - Current folder = "+NORMAL+self.CURRENT_DIR
        print YELLOW+" - CMSSW folder   = "+NORMAL+self.CMSSW_DIR
        print YELLOW+" - Script file    = "+NORMAL+self.SCRIPT_FILE
        package_string = ""
        if self.IPHCDataFormat:
            package_string+="IPHCDataFormat, "
        if self.IPHCProducer:
            package_string+="IPHCProducer, "
        if self.IPHCAnalysis:
            package_string+="IPHCAnalysis, "
        if self.IPHCMinitreeAnalysis:
            package_string+="IPHCMinitreeAnalysis, "
        if package_string.endswith(", "):
            package_string=package_string[:-2]
        print YELLOW+" - IPHC packages found = "+NORMAL+package_string
        print ""

    def GoTo_CMSSWBASE_SRC(self):

        # Entering the CMSSW_BASE folder
        print YELLOW+"Entering "+self.CMSSW_DIR+" folder ..."+NORMAL
        print ""
        try:
            os.chdir(self.CMSSW_DIR)
        except:
            print RED+"ERROR: impossible to enter the folder "+self.CMSSW_DIR+NORMAL
            sys.exit()


    def GoBackTo_CurrentFolder(self):

        # Go back to the initial current folder
        print YELLOW+"Go back to "+self.CURRENT_DIR+" folder ..."+NORMAL
        print ""
        try:
            os.chdir(self.CURRENT_DIR)
        except:
            print RED+"ERROR: impossible to enter the folder "+self.CURRENT_DIR+NORMAL
            sys.exit()

    def CompileCMSSWmodules(self):
        print YELLOW+"Compiling CMSSW modules ..."+NORMAL
        print ""
        os.system("scramv1 b -j"+str(self.ncores))
        print ""

    def BuildIPHCDataFormat(self):
        print YELLOW+"Building IPHCDataFormat ..."+NORMAL
        print ""
        os.system("cd IPHCDataFormat/NTFormat/src && make -j"+str(self.ncores))
        print ""

    def CompileIPHCAnalysis(self):
        print YELLOW+"Compling IPHCAnalysis ..."+NORMAL
        os.system("mkdir IPHCAnalysis/NTuple/.lib")
        os.system("cd IPHCAnalysis/NTuple && make -j"+str(self.ncores)+" all")
        print ""

    def Center(self,pattern,width):

        # Check width
        if width<=0:
            return ''

        # Size difference between pattern and line
        space = width - len(pattern)

        # Trivial case
        if space<=0:
            return pattern

        # Normal case
        else:

            space1 = int(space/2)
            space2 = space - space1
            return self.Fill(' ',space1) +\
                   pattern +\
                   self.Fill(' ',space2)

    def Fill(self,pattern,ntimes):

        # Check ntimes
        if ntimes<=0:
            return ''

        str=''
        for i in range(ntimes):
            str+=pattern
        return str

