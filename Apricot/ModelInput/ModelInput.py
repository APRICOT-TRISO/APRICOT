# Import dataclass library
from dataclasses import dataclass

# Import pandas library
import pandas as pd

###############
# MODEL CLASS #
###############

# Model class initialization
@dataclass
class ModelInput:
    
    ###################
    # KERNEL DIAMETER #
    ###################
    
    # Kernel diameter [ um ]
    kernelDiameter: float
    
    ####################
    # BUFFER THICKNESS #
    ####################
    
    # Buffer thickness [ um ]
    bufferThickness: float
        
    ##################
    # IPYC THICKNESS #
    ##################
    
    # IPyC thickness [ um ]
    IPyCThickness: float
    
    #################
    # SIC THICKNESS #
    #################
    
    # SiC thickness [ um ]
    SiCThickness: float
    
    ##################
    # OPYC THICKNESS #
    ##################
    
    # OPyC thickness [ um ]
    OPyCThickness: float
    
    ##################
    # KERNEL DENSITY #
    ##################
    
    # Kernel density [ g / cm³ ]
    kernelDensity: float
    
    ##################
    # BUFFER DENSITY #
    ##################
    
    # Buffer density [ g / cm³ ]
    bufferDensity: float
        
    ################
    # IPYC DENSITY #
    ################
    
    # IPyC density [ g / cm³ ]
    IPyCDensity: float
    
    ###############
    # SIC DENSITY #
    ###############
    
    # SiC density [ g / cm³ ]
    SiCDensity: float
    
    ################
    # OPYC DENSITY #
    ################
    
    # OPyC density [ g / cm³ ]
    OPyCDensity: float
    
    ############
    # IPYC BAF #
    ############
    
    # IPyC BAF [ - ]
    IPyCBAF: float
    
    ############
    # OPYC BAF #
    ############
    
    # OPyC BAF [ - ]
    OPyCBAF: float
    
    ########################
    # IRRIDIATION DURATION #
    ########################
    
    # Irridiation duration [ - ]
    EFDP: float
    
    #####################
    # END OF LIFE BUMUP #
    #####################
    
    # End of life bumup [ % ]
    endLifeBumup: float
    
    #######################
    # END OF LIFE FLUENCE #
    #######################
    
    # End of life fluence [ MeV ]
    endLifeFluence: float
    
    ###########################
    # IRRIDIATION TEMPERATURE #
    ###########################
    
    # Irridation temperature [ ºC ]
    irridiationTemperature: float
    
    ########################
    # END OF LIFE PRESSURE #
    ########################
    
    # End of life internal pressure [ MPa ]
    endLifeInternalPressure: float
    
    ####################
    # AMBIENT PRESSURE #
    ####################
    
    # Ambient pressure [ MPa ]
    ambientPressure: float    
    
    ######################
    # NUMBER OF ELEMENTS #
    ######################
    
    # Number of elements
    Nelements: int 
    
    #####################
    # METHOD MULTIPLIER #
    #####################
    
    # Method multiplier
    beta: float 
    
    ##################
    # INITIALIZATION #
    ##################
    
    # Initialization
    def __init__ ( self ):
        
        #############
        # READ FILE #
        #############
        
        # Read excel file
        excel = pd.read_excel( 'InputData.xlsx' )
        
        ############
        # ALLOCATE #
        ############
        
        # Kernel diameter [ um ]
        self.kernelDiameter = excel.iloc[ 0 ][ 1 ]
        
        # Buffer thickness [ um ]
        self.bufferThickness = excel.iloc[ 1 ][ 1 ]
        
        # IPyC thickness [ um ]
        self.IPyCThickness = excel.iloc[ 2 ][ 1 ]
        
        # SiC thickness [ um ]
        self.SiCThickness = excel.iloc[ 3 ][ 1 ]
        
        # OPyC thickness [ um ]
        self.OPyCThickness = excel.iloc[ 4 ][ 1 ]
        
        # Kernel density [ g / cm³ ]
        self.kernelDensity = excel.iloc[ 5 ][ 1 ]
        
        # Buffer density [ g / cm³ ]
        self.bufferDensity = excel.iloc[ 6 ][ 1 ]
        
        # IPyC density [ g / cm³ ]
        self.IPyCDensity = excel.iloc[ 7 ][ 1 ]
        
        # SiC density [ g / cm³ ]
        self.SiCDensity = excel.iloc[ 8 ][ 1 ]
        
        # OPyC density [ g / cm³ ]
        self.OPyCDensity = excel.iloc[ 9 ][ 1 ]
        
        # IPyC BAF [ - ]
        self.IPyCBAF = excel.iloc[ 10 ][ 1 ]
        
        # OPyC BAF [ - ]
        self.OPyCBAF = excel.iloc[ 11 ][ 1 ]
        
        # Irridiation duration [ - ]
        self.EFDP = excel.iloc[ 12 ][ 1 ]
        
        # End of life bumup [ % ]
        self.endLifeBumup = excel.iloc[ 13 ][ 1 ]
        
        # End of life fluence [ MeV ]
        self.endLifeFluence = excel.iloc[ 14 ][ 1 ]
        
        # Irridiation temperature [ ºC ]
        self.irridiationTemperature = excel.iloc[ 15 ][ 1 ]

        # End of life internal pressure [ MPa ]
        self.endLifeInternalPressure = excel.iloc[ 16 ][ 1 ]
        
        # Ambient pressure [ MPa ]
        self.ambientPressure = excel.iloc[ 17 ][ 1 ]
        
        # Number of elements
        self.Nelements = excel.iloc[ 18 ][ 1 ]
        
        # Method multiplier
        self.beta = excel.iloc[ 19 ][ 1 ]
   
    #########
    # PRINT #
    #########
        
    # Print
    def print( self ):
        
        # Print header
        print('---------------------------------------------------------')
        print("       #  ####   ####  #   ####  ####  #####  ")
        print("      ##  #  #   #  #  #   #     #  #    #    ")    
        print("     #_#  ####   ###   #   #     #  #    #    ")    
        print("    #  #  #      #  #  #   ####  ####    #    ") 
        print('---------------------------------------------------------')

        # Print kernel diameter [ um ]
        print( 'Kernel diameter [ um ]        = %.2f' % self.kernelDiameter )
        
        # Print buffer thickness [ um ]
        print( 'Buffer thickness [ um ]       = %.2f' % self.bufferThickness )
        
        # Print IPyC thickness [ um ]
        print( 'IPyC thickness [ um ]         = %.2f' % self.IPyCThickness )
        
        # Print SiC thickness [ um ]
        print( 'SiC thickness [ um ]          = %.2f' % self.SiCThickness )
        
        # Print OPyC thickness [ um ]
        print( 'OPyC thickness [ um ]         = %.2f' % self.OPyCThickness )
        
        # Print kernel density [ g / cm³ ]
        print( 'Kernel density [ g / cm³ ]    = %.2f' % self.kernelDensity )
        
        # Print buffer density [ g / cm³ ]
        print( 'Buffer density [ g / cm³ ]    = %.2f' % self.bufferDensity )
        
        # Print IPyC density [ g / cm³ ]
        print( 'IPyC density [ g / cm³ ]      = %.2f' % self.IPyCDensity )
        
        # Print SiC density [ g / cm³ ]
        print( 'SiC density [ g / cm³ ]       = %.2f' % self.SiCDensity )
        
        # Print OPyC density [ g / cm³ ]
        print( 'OPyC density [ g / cm³ ]      = %.2f' % self.OPyCDensity )
        
        # Print IPyC BAF [ - ]
        print( 'IPyC BAF [ - ]                = %.2f' % self.IPyCBAF )
        
        # Print OPyC BAF [ - ]
        print( 'OPyC BAF [ - ]                = %.2f' % self.OPyCBAF )
        
        # Print irridiation duration [ - ]
        print( 'Irridiation duration [ - ]    = %.2f' % self.EFDP )
        
        # Print end of life bumup [ - ]
        print( 'End of life bumup [ %% ]       = %.2f' % self.endLifeBumup )
        
        # Print end of life fluence [ MeV ]
        print( 'End of life fluence [ MeV ]   = %.2f' % self.endLifeFluence )
        
        # Print irridiation temperature [ ºC ]
        print( 'Irridiation temperature [ºC]  = %.2f' % self.irridiationTemperature )
        
        # Print end of life internal pressure [ MPa ]
        print( 'End of life pressure [ MPa ]  = %.2f' % self.endLifeInternalPressure )
        
        # Print ambient pressure [ MPa ]
        print( 'Ambient pressure [ MPa ]      = %.2f' % self.ambientPressure )
        
        # Print number of elements
        print( 'Number of elements per region = %d' % self.Nelements )
        
        # Print method multipliers
        print( 'Method multiplier - beta      = %.2f' % self.beta )
         
        # Print footer
        print( '--------------------------------------------------------------------' )