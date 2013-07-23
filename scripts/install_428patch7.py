#!/usr/bin/env python
from IPHCcommon import *
installer = IPHCcommon(__file__)

# Display a beautiful header
# The name is oompletely irrelevant
installer.DisplayHeader("CMSSW_4_2_8_patch7")

# System configuration
installer.CheckConfiguration()
installer.AskNCores()

# Move to the $CMSSW_BASE/src folder for installation
installer.GoTo_CMSSWBASE_SRC()

# Installing module
print YELLOW+"Installing PAT recipe for 428_patch7 ..."+NORMAL
print ""
os.system("addpkg DataFormats/PatCandidates V06-04-19-02")
os.system("addpkg PhysicsTools/PatAlgos V08-06-50")
os.system("addpkg PhysicsTools/PatUtils V03-09-18")
os.system("addpkg PhysicsTools/PatExamples V00-05-24")
os.system("addpkg CommonTools/ParticleFlow B4_2_X_V00-03-00")
os.system("addpkg PhysicsTools/SelectorUtils V00-03-24")
os.system("addpkg PhysicsTools/UtilAlgos V08-02-14")

print YELLOW+"Installing new recipe Type1/1p2 MET correction ..."+NORMAL
print ""
os.system("cvs co -r V04-05-07 JetMETCorrections/Type1MET")
os.system("cvs co -r V03-03-07 DataFormats/METReco")
os.system("cvs co -r V02-03-00 JetMETCorrections/Algorithms")
os.system("rm -f JetMETCorrections/Algorithms/interface/L1JPTOffsetCorrector.h")
os.system("rm -f JetMETCorrections/Algorithms/src/L1JPTOffsetCorrector.cc")
os.system("cvs co -r V03-01-00 JetMETCorrections/Objects")
os.system("addpkg JetMETCorrections/Modules")
os.system("cvs up -r 1.4 JetMETCorrections/Modules/plugins/JetCorrectorOnTheFly.cc")
os.system("cvs up -r 1.6 JetMETCorrections/Modules/interface/JetCorrectionProducer.h")

print YELLOW+"Installing eID with likelihood ..."+NORMAL
print ""
os.system("cvs co -r V00-03-31 RecoEgamma/ElectronIdentification")

# Compiling all CMSSW modules (scram b)
installer.CompileCMSSWmodules()

# Builing dictionnary related to IPHCDataFormat
installer.BuildIPHCDataFormat()

# Systematics on jet energy
if installer.IPHCAnalysis:
    os.system("cp /afs/cern.ch/user/s/speer/public/JR_Standalone.tgz .")
    os.system("tar -xzvf JR_Standalone.tgz")
    os.system("rm -rf JR_Standalone.tgz")
    os.system("cd JR_Standalone/JetMETObjects/ && make")
    os.system("mv JR_Standalone/lib/libJetMETObjects.so IPHCAnalysis/.")

# Compiling IPHCAnalysis
installer.CompileIPHCAnalysis()

# Move to the initial current folder
installer.GoBackTo_CurrentFolder()

# The end
print ""
print YELLOW+"The end"+NORMAL

