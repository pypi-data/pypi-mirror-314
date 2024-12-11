
class CustomGenerator(g4.G4VUserPrimaryGeneratorAction):

    def __init__(self):
        print("Custom generator")
        super().__init__()
        
        n_particle = 1
        self.particle_gun = G4ParticleGun(n_particle)

        particle_table = G4ParticleTable.GetParticleTable()
        particle = particle_table.FindParticle("gamma")
        self.particle_gun.SetParticleDefinition(particle)
        self.particle_gun.SetParticleMomentumDirection(G4ThreeVector(0.,0.,1.))
        self.particle_gun.SetParticleEnergy(6.0 * MeV)

        self.envelope_box = None

    def GeneratePrimaries(self, event):
        env_sizeXY = 0
        env_sizeZ = 0

        if not self.envelope_box:
            env_lv = g4.G4LogicalVolumeStore.GetInstance().GetVolume("Envelope")
            self.envelope_box = env_lv.GetSolid()
        
        if self.envelope_box:
            env_sizeXY = self.envelope_box.GetXHalfLength() * 2.0
            env_sizeZ = self.envelope_box.GetZHalfLength() * 2.0
        else:
            raise RuntimeError("Could not find envelope box")
        
        size = 0.8
        x0 = size * env_sizeXY * (g4_uniform_rand() - 0.5)
        y0 = size * env_sizeXY * (g4_uniform_rand() - 0.5)
        z0 = -0.5 * env_sizeZ
        
        self.particle_gun.SetParticlePosition(G4ThreeVector(x0,y0,z0))

        self.particle_gun.GeneratePrimaryVertex(event)