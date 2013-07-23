#!/usr/bin/env python
from IPHCcommon import *
installer = IPHCcommon(__file__)

# Display a beautiful header
# The name is oompletely irrelevant
installer.DisplayHeader("CMSSW_5_3_2_patch4")

# System configuration
installer.CheckConfiguration()
installer.AskNCores()

# Move to the $CMSSW_BASE/src folder for installation
installer.GoTo_CMSSWBASE_SRC()

# Installing module
print YELLOW+"Installing CMSSW packages ..."+NORMAL
print ""
os.system("addpkg CommonTools/ParticleFlow V00-03-15")
os.system("addpkg CommonTools/RecoAlgos    V00-03-23")
os.system("addpkg CommonTools/RecoUtils    V00-00-12")

os.system("addpkg CondFormats/EgammaObjects  	V00-04-00")

os.system("addpkg DataFormats/METReco  		V03-03-11")
os.system("addpkg DataFormats/PatCandidates  	V06-05-01")

os.system("addpkg JetMETCorrections/Algorithms  V02-03-00")
os.system("addpkg JetMETCorrections/Modules  	V05-01-06")
os.system("addpkg JetMETCorrections/Objects  	V03-01-00")
os.system("addpkg JetMETCorrections/Type1MET  	V04-06-09")

os.system("addpkg PhysicsTools/Configuration  	V00-12-07")
os.system("addpkg PhysicsTools/IsolationAlgos   V01-05-07")
os.system("addpkg PhysicsTools/IsolationUtils   V00-03-01-01")
os.system("addpkg PhysicsTools/PatAlgos  	V08-09-21")
os.system("addpkg PhysicsTools/PatExamples 	V00-05-24")
os.system("addpkg PhysicsTools/PatUtils  	V03-09-23")
os.system("addpkg PhysicsTools/SelectorUtils  	V00-03-24")
os.system("addpkg PhysicsTools/UtilAlgos  	V08-02-14")

os.system("addpkg RecoEgamma/ElectronIdentification  V00-03-31")
os.system("addpkg RecoJets/JetAnalyzers  	     V00-07-02-03")
os.system("addpkg RecoJets/JetProducers  	     V05-10-02")
os.system("addpkg RecoMET/METAnalyzers  	     V00-00-08")
os.system("addpkg RecoMET/METFilters  		     V00-00-10")
os.system("addpkg RecoParticleFlow/PFProducer        V15-01-11")

#os.system("cvs co -r V00-00-30 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools/")
os.system("cvs co -r HEAD EgammaAnalysis/ElectronTools/interface/ElectronEffectiveArea.h")

print YELLOW+"Installing tau id ..."+NORMAL
print ""
os.system("cvs up -r 1.31.6.4 PhysicsTools/PatAlgos/python/producersLayer1/tauProducer_cfi.py")
os.system("cvs up -r 1.52.10.4 PhysicsTools/PatAlgos/python/tools/tauTools.py")
os.system("cvs co -r V01-04-23 RecoTauTag/RecoTau")
os.system("cvs co -r V01-04-10 RecoTauTag/Configuration")

# Compiling all CMSSW modules (scram b)
installer.CompileCMSSWmodules()

# Builing dictionnary related to IPHCDataFormat
installer.BuildIPHCDataFormat()

# Compiling IPHCAnalysis
installer.CompileIPHCAnalysis()

# Move to the initial current folder
installer.GoBackTo_CurrentFolder()

# The end
print ""
print YELLOW+"The end"+NORMAL

