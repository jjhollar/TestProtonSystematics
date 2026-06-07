import FWCore.ParameterSet.Config as cms

from Configuration.ProcessModifiers.Era_Run3_2023_CTPPS_directSim_cff import *
from Validation.CTPPS.base_cff import *
process = cms.Process('CTPPSTest', Run3_2023_CTPPS_directSim)

# Uncomment an option for only *one* of these variables below
ASYST = ""
OSYST = ""
RSYST = ""

# Alignment
#ASYST = "none"
#ASYST = "symx_mis"
ASYST = "asymx_mis"
#ASYST = "symy_mis"
#ASYST = "asymy_mis"

# Optics
#OSYST = "none"
#OSYST = "Lx"
#OSYST = "Lpx"
#OSYST = "Lpy"
#OSYST = "xd"

# Resolution
#RSYST = "Level1"
#RSYST = "Level2"
#RSYST = "Level3"
#RSYST = "Level4"


process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Validation.CTPPS.ctppsLHCInfoPlotter_cfi')
process.load('Configuration.Generator.randomXiThetaGunProducer_cfi')
process.load("CondCore.CondDB.CondDB_cfi")

# minimal logger settings
process.MessageLogger = cms.Service("MessageLogger",
    statistics = cms.untracked.vstring(),
    destinations = cms.untracked.vstring('cout'),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('WARNING')
    )
)

# particle generator
process.generator.xi_max = 0.25
process.generator.theta_x_sigma = 60.e-6
process.generator.theta_y_sigma = 60.e-6

# default source
process.source = cms.Source("EmptySource",
    firstRun = cms.untracked.uint32(1),
)

process.CondDB.connect = 'frontier://FrontierProd/CMS_CONDITIONS'
process.PoolDBESSource = cms.ESSource("PoolDBESSource",
    process.CondDB,
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('CTPPSPixelAnalysisMaskRcd'),
        tag = cms.string("CTPPSPixelAnalysisMask_Run3_v1_hlt"))
        ))

# random seeds
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    sourceSeed = cms.PSet(initialSeed = cms.untracked.uint32(98765)),
    generator = cms.PSet(initialSeed = cms.untracked.uint32(98766)),
    beamDivergenceVtxGenerator = cms.PSet(initialSeed = cms.untracked.uint32(3849)),
    ppsDirectProtonSimulation = cms.PSet(initialSeed = cms.untracked.uint32(4981))
)

# number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(int(1E4))
)

# systematics
process.ctppsProtonReconstructionSimulationValidator = cms.EDAnalyzer("CTPPSProtonReconstructionSimulationValidator",
  tagHepMCBeforeSmearing = cms.InputTag("generator", "unsmeared"),
  tagHepMCAfterSmearing = cms.InputTag("beamDivergenceVtxGenerator"),
  tagRecoProtonsSingleRP = cms.InputTag("ctppsProtons", "singleRP"),
  tagRecoProtonsMultiRP = cms.InputTag("ctppsProtons", "multiRP"),

  lhcInfoLabel = cms.string(""),

  outputFile = cms.string("")
)

# define (biased) optics for reconstruction
if OSYST != "":
    process.ctppsModifiedOpticalFunctionsESSource = cms.ESProducer("CTPPSModifiedOpticalFunctionsESSource",
                                                                inputOpticsLabel = cms.string(""),
                                                                outputOpticsLabel = cms.string("modified"),
                                                                   
                                                                scenario = cms.string(OSYST),
                                                                factor = cms.double(1),

                                                                rpId_45_N = cms.uint32(3),
                                                                rpId_45_F = cms.uint32(23),
                                                                rpId_56_N = cms.uint32(103),
                                                                rpId_56_F = cms.uint32(123)
                                                                )

process.generation = cms.Path(process.generator)

process.validation = cms.Path(
    process.ctppsProtonReconstructionSimulationValidator
)

# processing path
process.schedule = cms.Schedule(
    process.generation,
    process.validation
)

from SimPPS.Configuration.Utils import setupPPSDirectSim
setupPPSDirectSim(process)

process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetX45 = 0.
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetY45 = 0.
process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetZ45 = 0.
process.source.numberEventsInLuminosityBlock = process.ctppsCompositeESSource.generateEveryNEvents

if ASYST == "symx_mis":
    for p in process.ctppsCompositeESSource.periods:
        p.ctppsRPAlignmentCorrectionsDataXML.MisalignedFiles += cms.vstring("/tmp/jjhollar/TestProtonSystematics/misalignment_x_sym.xml")
    SetLargeTheta(process)
    SetLevel4(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_misalignment/misalignment_x_sym_validation.root"
if ASYST == "asymx_mis":
    for p in process.ctppsCompositeESSource.periods:
        p.ctppsRPAlignmentCorrectionsDataXML.MisalignedFiles += cms.vstring("/tmp/jjhollar/TestProtonSystematics/misalignment_x_asym.xml")
    SetLargeTheta(process)
    SetLevel4(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_misalignment/misalignment_x_asym_validation.root"
if ASYST == "symy_mis":
    for p in process.ctppsCompositeESSource.periods:
        p.ctppsRPAlignmentCorrectionsDataXML.MisalignedFiles += cms.vstring("/tmp/jjhollar/TestProtonSystematics/misalignment_y_sym.xml")
    SetLargeTheta(process)
    SetLevel4(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_misalignment/misalignment_y_sym_validation.root"
if ASYST == "asymy_mis":
    for p in process.ctppsCompositeESSource.periods:
        p.ctppsRPAlignmentCorrectionsDataXML.MisalignedFiles += cms.vstring("/tmp/jjhollar/TestProtonSystematics/misalignment_y_asym.xml")
    SetLargeTheta(process)
    SetLevel4(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_misalignment/misalignment_y_asym_validation.root"
if ASYST == "none":
    for p in process.ctppsCompositeESSource.periods:
        p.ctppsRPAlignmentCorrectionsDataXML.MisalignedFiles += cms.vstring("/tmp/jjhollar/TestProtonSystematics/misalignment_none.xml")
    SetLargeTheta(process)
    SetLevel4(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_misalignment/misalignment_none_validation.root"

if OSYST == "Lx":
    process.ctppsProtons.opticsLabel = "modified"
    SetLargeTheta(process)
    SetLevel4(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_optics/optics_Lx_1_validation.root"
if OSYST == "Lpx":
    process.ctppsProtons.opticsLabel = "modified"
    SetLargeTheta(process)
    SetLevel4(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_optics/optics_Lpx_1_validation.root"
if OSYST == "Lpy":
    process.ctppsProtons.opticsLabel = "modified"
    SetLargeTheta(process)
    SetLevel4(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_optics/optics_Lpy_1_validation.root"
if OSYST == "xd":
    process.ctppsProtons.opticsLabel = "modified"
    SetLargeTheta(process)
    SetLevel4(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_optics/optics_xd_1_validation.root"
if OSYST == "none":
    process.ctppsProtons.opticsLabel = "modified"
    SetLargeTheta(process)
    SetLevel4(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_optics/optics_none_1_validation.root"

if RSYST == "Level1":
    SetLargeTheta(process)
    SetLevel1(process)    
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_resolution/resolution_th_Large_level_1_validation.root"
if RSYST == "Level2":
    SetLargeTheta(process)
    SetLevel2(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_resolution/resolution_th_Large_level_2_validation.root"
if RSYST == "Level3":
    SetLargeTheta(process)
    SetLevel3(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_resolution/resolution_th_Large_level_3_validation.root"
if RSYST == "Level4":
    SetLargeTheta(process)
    SetLevel4(process)
    process.ctppsProtonReconstructionSimulationValidator.outputFile = "proton_reco_resolution/resolution_th_Large_level_4_validation.root"

#print(process.dumpPython())
