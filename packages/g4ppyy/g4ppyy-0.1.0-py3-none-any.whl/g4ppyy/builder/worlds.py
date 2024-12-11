
class BasicWorld(g4.G4VUserDetectorConstruction):
    
    def __init__(self, dimensions):
       super().__init__()
    
    def Construct(self):
        env_sizeXY = 20 * g4.cm
        env_sizeZ = 30 * g4.cm
        env_mat = new(g4.gNistManager.FindOrBuildMaterial("G4_WATER"))

        check_overlaps = True

        world_sizeXY = 1.2 * env_sizeXY
        world_sizeZ = 1.2 * env_sizeZ
        world_mat = new( g4.gNistManager.FindOrBuildMaterial("G4_AIR") )

        solid_world = new(g4.G4Box("World",
                               0.5*world_sizeXY,
                               0.5*world_sizeXY,
                               0.5*world_sizeZ))
        logic_world = new(g4.G4LogicalVolume(solid_world,
                                         world_mat,
                                         "World"))
        self.phys_world = new(g4.G4PVPlacement(g4.cppyy.nullptr,
                                      g4.G4ThreeVector(),
                                      logic_world,
                                      "World",
                                      g4.cppyy.nullptr,
                                      False,
                                      0,
                                      check_overlaps))

        
        return self.phys_world
    