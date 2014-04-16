#!/usr/bin/env python
from IPHCcommon_sl6 import *
installer = IPHCcommon_sl6(__file__)

# Display a beautiful header
# The name is oompletely irrelevant
installer.DisplayHeader("CMSSW_5_3_16_patch1")
# System configuration
installer.CheckConfiguration()
installer.AskNCores()

# Move to the $CMSSW_BASE/src folder for installation
installer.GoTo_CMSSWBASE_SRC()

# Installing module
print YELLOW+"Installing CMSSW packages ..."+NORMAL
print ""

os.system("git cms-init")
os.system("git cms-addpkg PhysicsTools/PatAlgos")
os.system("git cms-merge-topic cms-analysis-tools:5_3_16_patch1-testNewTau")
os.system("git cms-merge-topic -u TaiSakuma:53X-met-140217-01")
os.system("git cms-addpkg EgammaAnalysis/ElectronTools")
os.system("cd EgammaAnalysis/ElectronTools/data && cat download.url | xargs wget")
os.system("cd -")
os.system("git cms-addpkg RecoEgamma/EgammaTools")
os.system("git cms-merge-topic cms-analysis-tools:5_3_16_patch1-updateTopRefSel")

# Compiling all CMSSW modules (scram b)
installer.CompileCMSSWmodules()

# Builing dictionnary related to IPHCDataFormat
installer.BuildIPHCDataFormat()

# Compiling LHAPDF
installer.CompileLHAPDF()

# Downloading PDF sets
print YELLOW+"Download PDF sets ..."+NORMAL
pdf = [ 'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/cteq6l1.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/unvalidated/cteq66.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/MSTW2008lo68cl.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/MSTW2008nlo68cl_asmz+68cl.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/MSTW2008nlo68cl_asmz-68cl.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/NNPDF23_nlo_as_0119.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/NNPDF23_nlo_as_0118.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/NNPDF23_nlo_as_0120.tar.gz']
installer.InstallPDF(pdf)

# Compiling IPHCAnalysis
installer.CompileIPHCAnalysis()

# Move to the initial current folder
installer.GoBackTo_CurrentFolder()

# The end
print ""
print YELLOW+"The end"+NORMAL

