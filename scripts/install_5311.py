#!/usr/bin/env python
from IPHCcommon import *
installer = IPHCcommon(__file__)

# Display a beautiful header
# The name is oompletely irrelevant
installer.DisplayHeader("CMSSW_5_3_11")
# System configuration
installer.CheckConfiguration()
installer.AskNCores()

# Move to the $CMSSW_BASE/src folder for installation
installer.GoTo_CMSSWBASE_SRC()

# Installing module
print YELLOW+"Installing CMSSW packages ..."+NORMAL
print ""


os.system("cvs co -r V00-00-09 EgammaAnalysis/ElectronTools")
os.system("cvs co -r V09-00-01 RecoEgamma/EgammaTools")

# Compiling all CMSSW modules (scram b)
installer.CompileCMSSWmodules()


os.system("cd EgammaAnalysis/ElectronTools/data && cat download.url | xargs wget")



# Builing dictionnary related to IPHCDataFormat
installer.BuildIPHCDataFormat()

# Systematics on jet energy
if installer.IPHCAnalysis:
    os.system("cp IPHCDataFormat/scripts/JR_Standalone.tgz .")
    os.system("tar -xzf JR_Standalone.tgz")
    os.system("rm -f JR_Standalone.tgz")
    os.system("cd JR_Standalone/JetMETObjects/ && make -j"+str(installer.ncores))
    os.system("mv JR_Standalone/lib/libJetMETObjects.so IPHCAnalysis/NTuple/")



# Compiling LHAPDF
installer.CompileLHAPDF()

# Downloading PDF sets
print YELLOW+"Download PDF sets ..."+NORMAL
pdf = [ 'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/cteq6l1.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/unvalidated/cteq66.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/MSTW2008lo68cl.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/unvalidated/MSTW2008nlo68cl_asmz+68cl.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/unvalidated/MSTW2008nlo68cl_asmz-68cl.tar.gz']
installer.InstallPDF(pdf)


# Compiling IPHCAnalysis
installer.CompileIPHCAnalysis()

# Move to the initial current folder
installer.GoBackTo_CurrentFolder()

# The end
print ""
print YELLOW+"The end"+NORMAL

