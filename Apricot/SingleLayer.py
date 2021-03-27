# Import system
import sys

# Append path of the functions
sys.path.append( 'Material' )
sys.path.append( 'ModelInput' )
sys.path.append( 'FEM' )

# Import functions
from ModelInput import ModelInput
from Material import Material
from FEM import FEM

####################
# MODEL PARAMETERS #
####################

# Model initialization
model = ModelInput()

#####################
# PRINT MODEL INPUT #
#####################

# Print model input
model.print()

######################
# INITIAL PARAMETERS #
######################

# Fast fluence
phi = 10

# Irridiation temperature ( ºC )
Ti  = 1000 

###########################
# MATERIAL INITIALIZATION #
###########################

# PyC material initaliazation
PyC = Material ( 1 , 'PyC', Ti, phi, 3.96e4 , 0.33 , 1.90, 5.50e-6, 200, 5.00 )

# Sic material initaliazation
SiC = Material ( 2 , 'SiC', Ti, phi, 3.70e5 , 0.13 , 3.20, 4.90e-6, 873, 8.02 )

##########################
# CREEP PARAMETERS # PYC #
##########################

# Set if the creep parameter is temperature dependent
PyC.setCreepDependent( True )

# Set irridiation creep coefficient - If the above is true, this line will be disregarded
PyC.setIrridiationCreepCoefficient( 2.7e-4 )

# Set poisson ration in creep
PyC.setCreepPoissonRatio( 0.50 )

################################
# IRRIDIATION PARAMETERS # PYC #
################################

# Set irradiation case
PyC.setIrridiationCase( 'b' )

###########################
# PRINT MATERIAL DATABASE #
###########################

# Print material database
PyC.print()
SiC.print()

#################################
# FINITE ELEMENT INITIALIZATION #
#################################

# Finite element initialization
FEM = FEM( model, PyC, SiC )

############
# ASSEMBLY #
############

# Assembly finite element problem
FEM.assembly()

#########
# SOLVE #
#########

# Solve finite element problem
FEM.solve()

###################
# POST PROCESSING #
###################

# Finite element post processing
#FEM.postProcessing()

###################################
# PRINT FINITE ELEMENT PARAMETERS #
###################################

# Print finite element parameters
FEM.print()