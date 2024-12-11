import os
import glob
import subprocess 
import cppyy

global G4PREFIX
G4PREFIX = "WARNING_NOT_SET"

# -----------------------
# HELPERS
# -----------------------

# Simple external command call
def ext_cmd(cmd):
    process = subprocess.Popen(cmd.split(" "), 
                    stdout=subprocess.PIPE)
    (lib_output, err) = process.communicate()
    exit_code = process.wait()

    return str(lib_output.decode()).strip()

# -----------------------
# GEANT4 IMPORTS
# -----------------------
print("[G4PPYY] : Loading G4 Modules.")

# Get GEANT4 PREFIX
G4PREFIX = ext_cmd("geant4-config --prefix")
print(f"[G4PPYY] : G4PREFIX : {G4PREFIX}")

# Add include + lib DIRS
try:
    cppyy.add_include_path(os.path.abspath(f'{G4PREFIX}/include/Geant4/'))
except:
    pass

try:
    cppyy.add_library_path(os.path.abspath(f"{G4PREFIX}/lib64/"))
except:
    pass

try:
    cppyy.add_library_path(os.path.abspath(f"{G4PREFIX}/lib/"))
except:
    pass

os.environ["LD_LIBRARY_PATH"] = os.environ["LD_LIBRARY_PATH"] + ":" + f'{G4PREFIX}/lib64/'
os.environ["LD_LIBRARY_PATH"] = os.environ["LD_LIBRARY_PATH"] + ":" + f'{G4PREFIX}/lib64/'

# Load Libraries (recursively if required)
lib_output = ext_cmd("geant4-config --libs")

vals = lib_output.split()
lib_dir = vals[0].replace("-L","")

libraries = []
for x in vals[1:]:
    libraries.append( x.replace("-l","") )

count = 0
while len(libraries) > 0 and count < 5:
    remaining = []
    for val in libraries:
        try:
            cppyy.load_library(val)        
        except:
            remaining.append(val)

    if (len(remaining) > 0):
        print("[G4PPYY] : Failed to load : ", remaining, len(remaining))
        
    libraries = remaining
    count += 1

# -----------------------
# LAZY LOADER DEFINITIONS
# -----------------------

# Module level lazy loader, intercepts attr calls
# for the module allowing for access of G4 variables through this
# e.g. g4ppyy.G4VisAttributes,
def __getattr__(name):
    
    try:
        return globals()[name]
    except:
        pass   

    # Run slightly dodgy eval, needs to be replaced
    # with a scopped attribute check
    try:
        globals()[name] = eval('cppyy.gbl.' + name)
        return cppyy.gbl.hasattr(name)
    except AttributeError:
        pass

    try:
        cppyy.include(name + '.hh')
    except:
        pass

    try:
        globals()[name] = eval('cppyy.gbl.' + name)
        return globals()[name]
    except AttributeError:
        pass
    
    # If the attribute is not found, raise AttributeError as usual
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Adds headers to CPPYY for access
def lazy_include(name):
    try:
        cppyy.gbl.include(name)
    except:
        pass

# Attempts to find the corresponding GEANT4 Header File
def lazy_load(name, g4dir="{G4PREFIX}/include/Geant4/"):

    if not isinstance(name, list):
        name = [name]
        
    for n in name:
        for file in glob.glob(g4dir + "/" + n):
            file = (file.replace(g4dir,""))
            classname = file.replace(".hh","")
            try:
                cppyy.gbl.include(file)
            except:
                pass

            try:
                __getattr__(classname)
            except:
                pass
    

# Add wrappers around cppyy just to make g4ppyy functions easier.
gbl = cppyy.gbl
include = cppyy.include

print("[G4PPYY] : Module loading complete.")
