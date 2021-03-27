# Import dataclass library
from dataclasses import dataclass

##################
# MATERIAL CLASS #
##################

# Material class initialization
@dataclass
class Material:
    
    ######
    # ID #
    ######
    
    # Material ID
    ID: int
    
    ########
    # NAME #
    ########
    
    # Name
    name: str    
     
    ###############
    # TEMPERATURE #
    ###############
    
    # Temperature ( ºC )
    T: float
    
    ################
    # FAST FLUENCE #
    ################
    
    # Fast fluence ()
    phi: float
    
    ###################
    # ELASTIC MODULUS #
    ###################
    
    # Elastic modulus ( MPa )
    E: float
    
    #################
    # POISSON RATIO #
    #################
    
    # Poisson ratio ( - )
    v: float
    
    ###########
    # DENSITY #
    ###########
    
    # Density ( ton / mm³ )
    p: float
       
    #################################
    # THERMAL EXPANSION COEFFICIENT #
    #################################
    
    # Thermal expansion coefficient ( / K )
    a: float
    
    #################
    # MEAN STRENGTH #
    #################
    
    # Mean strength ( MPa )
    S: float
    
    ###################
    # WEIBULL MODULUS #
    ###################
    
    # Weibull modulus ( - )
    k: float
    
    #################################
    # IRRIDIATION CREEP COEFFICIENT #
    #################################
    
    # Irridiation creep coefficient ( MPa^-1 )
    K: float
    
    # Irridiation creep coefficient dependent of temperature
    K_temp: bool
    
    #######################
    # POISSON RATIO CREEP #
    #######################
    
    # Poisson ratio in creep ( - )
    vc: float
    
    ################################
    # IRRIDIATION CORRELATION CASE #
    ################################
    
    # Irridiation correlation case ( - )
    irrCase: str
    
    ##########################################
    # RADIAL IRRIDIATION INDUCED CHANGE RATE #
    ##########################################
    
    # Radial irridiation induced change rate ( - )
    er: float
    
    ##############################################
    # TANGENTIAL IRRIDIATION INDUCED CHANGE RATE #
    ##############################################
    
    # Tangential irridiation induced change rate ( - )
    et: float
    
    ##################
    # INITIALIZATION #
    ##################
    
    # Initialization
    def __init__ ( self , ID: int , name: str , T: float , phi: float, E: float , v: float , p: float, a: float, S: float, k: float ):
        
        ##############
        # ALLOCATION #
        ##############
        
        # ID allocation
        self.ID = ID
        
        # Name allocation
        self.name = name
        
        # Temperature allocation
        self.T  = T
        
        # Fast fluence allocation
        self.phi = phi
        
        # Elastic modulus allocation
        self.E  = E
        
        # Poisson ratio allocation
        self.v  = v
        
        # Density transformation and allocation in ton/mm³
        self.p  = p * 1e-9
               
        
        # Thermal expansion coefficient allocation
        self.a  = a
        
        # Mean strength allocation
        self.S  = S
        
        # Weibull modulus allocation
        self.k  = k
        
        # Irridiation coefficient initialization
        self.K  = 0.0
        
        # Irridiation coefficient dependable of temperature
        self.K_temp = False
        
        # Poisson ratio in creep initialization
        self.vc = 0.0
        
        # Irridiation correlation case initialization
        self.irrCase = ''
        
        # Radial irridiation induced change rate initialization
        self.er = 0.0
        
        # Tangential irridiation induced change rate initialization
        self.et = 0.0
        
    ####################
    # CREEP PARAMETERS #
    ####################
        
    # Set if the irridiation creep coefficient is dependent of temperature
    def setCreepDependent( self, K_temp: bool ):
        
        # Irridiation creep coefficient is dependent of temperature
        self.K_temp = K_temp
        
        # Check if the irridiation creep coefficient is dependent of temperature
        if( self.K_temp == True ):
            
            # Calculate irridiation creep coefficient
            self.K = 4.386e-4 - ( 9.70e-7 * self.T ) + ( 8.0294e-10 * self.T * self.T )
    
    # Set irridiation creep coefficient
    def setIrridiationCreepCoefficient( self, K: float ):
        
        # Only update if the irridiation creep coefficient is not temperature dependent
        if( self.K_temp == False ):
        
            # Irridiation creep coefficient
            self.K = K
    
    # Set creep parameters
    def setCreepPoissonRatio( self, vc:float ):
        
        # Poisson's ration in creep allocation
        self.vc = vc
        
    ##########################
    # IRRIDIATION PARAMETERS #
    ##########################
        
    # Set irridiation correlation case
    def setIrridiationCase( self, irrCase: str ):
        
        # Correlation case allocation
        self.irrCase = irrCase

        # Correlation case B
        if( self.irrCase == 'b' ):
            
            # Radial irridiation induced change calculation
            self.er = + ( 1.36334e-3 * ( self.phi**3.0 ) ) - ( 7.77024e-3 * ( self.phi**2.0 ) ) + ( 2.00861e-2 * ( self.phi**1.0 ) ) - 2.22642e-2
            
            # Tangent irridiation induced change calculation
            self.et = - ( 3.53804e-4 * ( self.phi**3.0 ) ) + ( 1.67251e-3 * ( self.phi**2.0 ) ) + ( 2.63307e-3 * ( self.phi**1.0 ) ) - 1.91253e-2
            
        # Correlation case C
        if ( self.irrCase == 'c' ):
            
            # Radial irridiation induced change calculation
            self.er = + ( 4.03266e-4 * ( self.phi**3.0 ) ) - ( 2.25937e-3 * ( self.phi**2.0 ) ) + ( 9.82884e-3 * ( self.phi**1.0 ) ) - 1.80613e-2
            
            # Tangent irridiation induced change calculation
            self.et = - ( 4.91648e-4 * ( self.phi**3.0 ) ) + ( 2.32979e-3 * ( self.phi**2.0 ) ) + ( 1.71315e-3 * ( self.phi**1.0 ) ) - 1.78392e-2
            
        # Correlation case C
        if ( self.irrCase == 'd' ):
            
            # Check phi condition
            if( self.phi <= 6.08 ):
                
                # Radial irridiation induced change calculation
                self.er = + ( 4.52013e-4 * ( self.phi**5.0 ) ) - ( 8.36313e-3 * ( self.phi**4.0 ) ) + ( 5.67549e-2 * ( self.phi**3.0 ) ) - ( 1.74247e-1 * ( self.phi**2.0 ) ) + ( 2.62692e-1 * ( self.phi**1.0 ) ) - 1.43234e-1
            
                # Tangent irridiation induced change calculation
                self.et = + ( 1.30457e-4 * ( self.phi**3.0 ) ) - ( 2.10029e-3 * ( self.phi**2.0 ) ) + ( 9.07826e-3 * ( self.phi**1.0 ) ) - 3.24737e-2
                
            else:
                
                # Radial irridiation induced change calculation
                self.er = + 0.0954
            
                # Tangent irridiation induced change calculation
                self.et = - 0.0249                
        
    #########
    # PRINT #
    #########
        
    # Print
    def print( self ):
        
        # Print header
        print( '--------------------------------------------------------------------' )
        
        # Print name
        print( 'Material Name                 = %s' % self.name )
        
        # Print ID
        print( 'Material ID                   = %d' % self.ID )
                
        # Print temperature
        print( 'Temperature                   = %.2f ºC' % self.T )
        
        # Print fast fluence
        print( 'Fast fluence                  = %.2f' % self.phi )
        
        # Print elastic modulus
        print( 'Elastic modulus               = %.2e MPa' % self.E )
        
        # Print poisson ratio
        print( 'Poisson ratio                 = %.2f' % self.v )
                
        # Print density
        print( 'Density                       = %.2e ton/mm³' % self.p )
        
        # Print thermal expansion coefficient
        print( 'Thermal exp. coefficient      = %.2e K^-1' % self.a )
        
        # Print mean strength
        print( 'Mean strength                 = %d MPa' % self.S )
        
        # Print Weibull modulus
        print( 'Weibull modulus               = %.2f' % self.k )
        
        # Print if the irridiation creep coefficient is dependent of temperature
        print( 'Creep temperature dependent   = %s' % self.K_temp )
        
        # Print irridiation creep coefficient
        print( 'Irridiation creep coefficient = %.2e MPa^-1' % self.K )
        
        # Print poisson ratio in crep
        print( 'Poisson ratio in creep        = %.2f' % self.vc )
        
        # Print irridiation correlation case
        print( 'Irridiation correlation case  = %s' % self.irrCase )
        
        # Print radial irridiation induced change rate
        print( 'Radial irridiation ind. rate  = %.2e' % self.er )
        
        # Print tangential irridiation induced change rate
        print( 'Tangent irridiation ind. rate = %.2e' % self.et )
        
        # Print footer
        print( '--------------------------------------------------------------------' )
        
    ###############
    # PRINT SHORT #
    ###############
        
    # Print
    def printShort( self ):
        
        # Print name
        print( 'Material Name                 = %s' % self.name )      