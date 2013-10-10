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


# install met recipe
os.system("addpkg DataFormats/PatCandidates V06-05-06-12")
os.system("addpkg PhysicsTools/PatAlgos V08-09-62")
os.system("addpkg PhysicsTools/PatUtils V03-09-28")
os.system("addpkg RecoMET/METAnalyzers V00-00-08")  
os.system("addpkg DataFormats/METReco V03-03-11-01")
os.system("addpkg JetMETCorrections/Type1MET V04-06-09-02")

# met cleaning
os.system("cvs co -r V00-00-13-01 RecoMET/METFilters")
os.system("cvs co -r V01-00-11-01 DPGAnalysis/Skims")
os.system("cvs co -r V00-11-17 DPGAnalysis/SiStripTools")
os.system("cvs co -r V00-00-08 DataFormats/TrackerCommon")
os.system("cvs co -r V01-09-05 RecoLocalTracker/SubCollectionProducers")



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
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/unvalidated/MSTW2008lo68cl.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/unvalidated/MSTW2008nlo68cl_asmz+68cl.tar.gz',\
        'http://www.hepforge.org/archive/lhapdf/pdfsets/6.0/unvalidated/MSTW2008nlo68cl_asmz-68cl.tar.gz',\
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

