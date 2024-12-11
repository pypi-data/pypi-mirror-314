import g4ppyy as g4
from g4ppyy import G4ParticleGun, G4ParticleTable, G4ThreeVector, MeV
from g4ppyy import new
from g4ppyy import G4Accumulable, G4double, G4AccumulableManager


g4.include("G4RunManagerFactory.hh")
g4.include("G4VUserActionInitialization.hh")

def g4_uniform_rand():
    return g4.CLHEP.HepRandom.getTheEngine().flat()


class CustomAccumulableManager(g4.G4AccumulableManager):
    
    def __init__(self):
        super().__init__()


class CustomRunAction(g4.G4UserRunAction):
    
    def __init__(self):
        super().__init__()
        self.edep = G4Accumulable[G4double](0)
        self.edep2 = G4Accumulable[G4double](0)
        self.accumulableManager = G4AccumulableManager.Instance()
        self.accumulableManager.RegisterAccumulable(self.edep)
        self.accumulableManager.RegisterAccumulable(self.edep2)
    
    def BeginOfRunAction(self, g4run):
        g4.G4RunManager.GetRunManager().SetRandomNumberStore(False)
        self.accumulableManager.Reset()
        pass
    
    def EndOfRunAction(self, g4run):
        self.accumulableManager.Merge()
        edep = self.edep.GetValue()
        edep2 = self.edep2.GetValue()
        print(f"edep: {edep}")
        print(f"edep2 {edep2}")
    
    def addEdep(self, edep):
        self.edep += edep
        self.edep2 += edep * edep
        
class CustomEventAction(g4.G4UserEventAction):
    
    def __init__(self, run_action):
        super().__init__()
        self.edep = 0
        self.run_action = run_action
    
    def BeginOfEventAction(self, event):
        self.edep = 0
    
    def EndOfEventAction(self, event):
        self.run_action.addEdep(self.edep)
        pass

    def addEdep(self, edep):
        self.edep += edep
        

class CustomSteppingAction(g4.G4UserSteppingAction):
    
    def __init__(self, event_action):
        super().__init__()
        self.event_action = event_action
        self.scoring_volume = None
    
    def UserSteppingAction(self, step):
        if not self.scoring_volume:
            det_con = g4.G4RunManager.GetRunManager().GetUserDetectorConstruction()
            self.scoring_volume = det_con.get_scoring_volume()
            
        volume = step.GetPreStepPoint().GetTouchableHandle().GetVolume().GetLogicalVolume()
        if volume != self.scoring_volume:
            return
        
        edep_step = step.GetTotalEnergyDeposit()
        self.event_action.addEdep(edep_step)

class CustomAction(g4.G4VUserActionInitialization):
    
    def __init__(self):
       super().__init__()
    
    def BuildForMaster(self):
        run_action = CustomRunAction()
        self.SetUserAction(run_action)
        # pass
    
    def Build(self):
        print("Custom action")
        self.gen = CustomGenerator()
        self.SetUserAction(self.gen)
        
        self.run_action = CustomRunAction()
        self.SetUserAction(self.run_action)
        
        self.event_action = CustomEventAction(self.run_action)
        self.SetUserAction(self.event_action)
        
        self.step_action = CustomSteppingAction(self.event_action)
        self.SetUserAction(self.step_action)