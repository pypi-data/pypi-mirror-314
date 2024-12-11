from . import lazy_loader as ll
from . import si_units as SI

ll.include('G4UImanager.hh')
ll.include('G4UIterminal.hh')
ll.include('G4VisExecutive.hh')
ll.include('G4VisExecutive.icc')
ll.include('G4UIExecutive.hh')
ll.include("G4ParticleTable.hh")

ll.include('Randomize.hh')
ll.include('globals.hh')

ll.include("G4String.hh")
G4String = ll.G4String

ll.include("G4ParticleGun.hh")
G4ParticleGun = ll.G4ParticleGun

ll.include('QGSP_BERT.hh')
QGSP_BERT = ll.QGSP_BERT

ll.include('QGSP_BERT_HP.hh')
QGSP_BERT_HP = ll.QGSP_BERT_HP

ll.include("G4VUserPrimaryGeneratorAction.hh")
G4VUserPrimaryGeneratorAction = ll.G4VUserPrimaryGeneratorAction

ll.include('G4RunManager.hh')
G4RunManager = ll.G4RunManager

ll.include('G4LogicalVolume.hh')
G4LogialVolume = ll.G4LogicalVolume

ll.include('G4Material.hh')
G4Material = ll.G4Material

ll.include('G4VPhysicalVolume.hh')
G4VPhysicalVolume = ll.G4VPhysicalVolume

ll.include('G4PVPlacement.hh')
G4PVPlacement = ll.G4PVPlacement

ll.include('G4NistManager.hh')
global gNistManager
gNistManager = ll.G4NistManager.Instance()

ll.include('G4VUserDetectorConstruction.hh')
G4VUserDetectorConstruction = ll.G4VUserDetectorConstruction

ll.include("G4ThreeVector.hh")
G4ThreeVector = ll.G4ThreeVector

ll.include("G4RotationMatrix.hh")
G4RotationMatrix = ll.G4RotationMatrix

ll.include("G4UserEventAction.hh")
G4UserEventAction = ll.G4UserEventAction

ll.include("G4UserSteppingAction.hh")
G4UserSteppingAction = ll.G4UserSteppingAction

ll.include("G4UserRunAction.hh")
G4UserRunAction = ll.G4UserRunAction

#ll.include("G4ParticleTable.hh")
#ll.G4ParticleTable.GetParticleTable()

ll.include("G4ParticleDefinition.hh")
G4ParticleDefinition = ll.G4ParticleDefinition

# ll.include("G4Neutron.hh")
# ll.include("G4Proton.hh")
# ll.include("G4Electron.hh")
# ll.include("G4MuonMinus.hh")
# ll.include("G4MuonPlus.hh")

# from ll.gbl import G4Neutron, G4Proton, G4Electron, G4MuonMinus, G4MuonPlus

NULL = ll.cppyy.nullptr

ll.include("G4RunManagerFactory.hh")
G4RunManagerFactory = ll.G4RunManagerFactory

ll.include("G4VSensitiveDetector.hh")
G4VSensitiveDetector = ll.G4VSensitiveDetector

ll.include("G4TrackStatus.hh")
G4TrackStatus = ll.G4TrackStatus
G4UImanager = ll.G4UImanager
G4VisExecutive = ll.G4VisExecutive
G4UIExecutive = ll.G4UIExecutive


ll.include("G4Box.hh")
ll.include("G4Sphere.hh")
ll.include("G4Tubs.hh")
ll.include("G4VSolid.hh")

G4VSolid = ll.G4VSolid

def G4Box(name,
          x : float = 1.0*SI.m,
          y : float = 1.0*SI.m,
          z : float = 1.0*SI.m):
    return ll.G4Box(name,
                           x,
                           y,
                           z)

def G4Sphere(name,
             rmin : float = 0.0,
             rmax : float = 1.0*SI.m,
             phimin : float = 0.0,
             phimax : float = SI.twopi,
             thetamin : float = 0.0,
             thetamax : float = SI.twopi):
    return ll.G4Sphere(name,
                              rmin,
                              rmax,
                              phimin,
                              phimax,
                              thetamin,
                              thetamax)

def G4Tubs(name,
           rmin : float = 0.0,
           rmax : float = 1.0*SI.m,
           zmax : float = 1.0*SI.m,
           phimin : float = 0.0,
           phimax : float = SI.twopi):
    return ll.G4Tubs(name,
                            rmin,
                            rmax,
                            zmax,
                            phimin,
                            phimax)



ll.include("G4Element.hh")
G4Element = ll.G4Element

ll.include("G4VSceneHandler.hh")


ll.include("G4VGraphicsSystem.hh")
ll.include("G4VSceneHandler.hh")
ll.include("globals.hh")
ll.include("G4Polyline.hh")
ll.include("G4Circle.hh")
ll.include("G4VMarker.hh")
ll.include("G4Visible.hh")

