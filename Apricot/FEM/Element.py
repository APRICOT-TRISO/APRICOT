# Import dataclass library
from dataclasses import dataclass

# Import numpy library
import numpy as np

# Import inverse library
from numpy.linalg import inv

# Import functions
from Material import Material
from Node import Node

#################
# ELEMENT CLASS #
#################

# Element class initialization
@dataclass
class Element:
    
    ######
    # ID #
    ######
    
    # Element ID
    ID: int
    
    #################
    # NODE 1 STRUCT #
    #################
    
    # Node 1 struct
    node1: Node
    
    #################
    # NODE 2 STRUCT #
    #################
    
    # Node 2 struct
    node2: Node
    
    ##########
    # REGION #
    ##########
    
    # Region name
    region: str
    
    ###################
    # MATERIAL STRUCT #
    ###################
    
    # Material struct
    material: Material
    
    #######################
    # CONSTITUTIVE MATRIX #
    #######################
    
    # Constitutive matrix
    C: np.ndarray
    
    ######################
    # IRRIDIATION MATRIX #
    ######################
    
    # Irridiation matrix
    A: np.ndarray
    
    ############
    # G MATRIX #
    ############
    
    # G matrix
    G: np.ndarray
    
    ################
    # D PARAMETERS #
    ################
    
    # D parameters
    d11: float = 0.0
    d12: float = 0.0
    
    ##########################################
    # RADIAL IRRIDIATION INDUCED CHANGE RATE #
    ##########################################
    
    # Radial irridiation induced change rate ( - )
    er: float = 0.0
    
    ##############################################
    # TANGENTIAL IRRIDIATION INDUCED CHANGE RATE #
    ##############################################
    
    # Tangential irridiation induced change rate ( - )
    et: float = 0.0
    
    ####################
    # STIFFNESS MATRIX #
    ####################
    
    # Stiffness matrix
    Ke: np.ndarray = np.zeros( ( 2 , 2 ) )
    
    #########################
    # INTERNAL FORCE VECTOR #
    #########################
    
    # Internal force vector
    Fei: np.ndarray = np.zeros( ( 2 , 1 ) )
    
    #########################
    # EXTERNAL FORCE VECTOR #
    #########################
    
    # External force vector
    Fee: np.ndarray = np.zeros( ( 2 , 1 ) )
    
    #######################
    # DISPLACEMENT VECTOR #
    #######################
    
    # Displacement vector
    ue: np.ndarray = np.zeros( ( 2 , 1 ) )
    
    ##################
    # INITIALIZATION #
    ##################
    
    # Initialization
    def __init__ ( self, ID: int, node1: Node, node2: Node, region:str, material:Material ):
        
        # ID allocation
        self.ID = ID
        
        # Node 1 struct allocation
        self.node1 = node1
        
        # Node 2 struct allocation
        self.node2 = node2
        
        # Region allocation
        self.region = region
        
        # Material struct allocation
        self.material = material
        
    #############################
    # SET # CONSTITUTIVE MATRIX #
    #############################
        
    # Set consitutive matrix - According to equation (2)
    def setC( self ):
        
        ##################
        # INITIALIZATION #
        ##################
        
        # Initialize constitutive matrix
        self.C = np.zeros( ( 2 , 2 ) )
        
        ##############
        # ALLOCATION #
        ##############
        
        # Allocate constitutive matrix
        self.C[ 0 , 0 ] = ( + 1.0 / self.material.E );
        self.C[ 0 , 1 ] = ( - 2.0 * self.material.v / self.material.E )
        self.C[ 1 , 0 ] = ( - 1.0 * self.material.v / self.material.E )
        self.C[ 1 , 1 ] = ( + ( 1.0 - self.material.v ) / self.material.E )
    
    ############################
    # SET # IRRIDIATION MATRIX #
    ############################
        
    # Set irridiation matrix - According to equation (4)
    def setA( self ):
        
        ##################
        # INITIALIZATION #
        ##################
        
        # Initialize irridiation matrix
        self.A = np.zeros( ( 2 , 2 ) )
        
        ##############
        # ALLOCATION #
        ##############
        
        # Allocate irridiation matrix
        self.A[ 0 , 0 ] = ( + 1.0 * self.material.K );
        self.A[ 0 , 1 ] = ( - 2.0 * self.material.vc * self.material.K )
        self.A[ 1 , 0 ] = ( - 1.0 * self.material.vc * self.material.K )
        self.A[ 1 , 1 ] = ( + ( 1.0 - self.material.vc ) * self.material.K )
        
    ##################
    # SET # G MATRIX #
    ##################
        
    # Set G matrix - According to equation (8)
    def setG( self, beta:float ):
        
        ###############
        # CALCULATION #
        ###############
        
        # Calculate G matrix
        self.G = inv( self.C + ( beta * self.material.phi * self.A ) )
        
    ############################
    # SET # INITIAL CONDITIONS #
    ############################
        
    # Set initial conditions
    def setInitialConditions( self ):
         
        ################
        # D PARAMETERS #
        ################
        
        # Set D parameters on element
        self.d11 = self.material.E * ( 1.0 - self.material.v ) / ( ( 1.0 + self.material.v ) + ( 1.0 - ( 2.0 * self.material.v ) ) )
        self.d12 = self.material.E * ( 2.0 * self.material.v ) / ( ( 1.0 + self.material.v ) + ( 1.0 - ( 2.0 * self.material.v ) ) )
        
        # Set irridiation on element
        self.er = self.material.er
        self.et = self.material.et
        
        ###############
        # SET # NODES #
        ###############
        
        # Set D parameters on node 1
        self.node1.setd11( self.d11 )
        self.node1.setd12( self.d12 )
        
        # Set D parameters on node 2
        self.node2.setd11( self.d11 )
        self.node2.setd12( self.d12 )
        
        # Set irridiation on node 1
        self.node1.seter( self.material.er )
        self.node1.setet( self.material.et )
        
        # Set irridiation on node 2
        self.node2.seter( self.material.er )
        self.node2.setet( self.material.et )
        
    #######################
    # SET # ELEMENT MODEL #
    #######################
        
    # Set element parameters
    # Element stiffness matrix - Ke
    # Element internal force vector - Fei
    # Element external force vector - Fee
    # Element model matrix - Ve
    def setElementParameters( self ):
        
        ##################
        # INITIALIZATION #
        ##################
    
        # Stiffness matrix initialization
        self.Ke = np.zeros( ( 2 , 2 ) )    
   
        # Internal force vector
        self.Fei = np.zeros( ( 2 , 1 ) )
        
        # External force vector
        self.Fee = np.zeros( ( 2 , 1 ) )
        
        # Displacement vector
        self.ue = np.zeros( ( 2 , 1 ) ) 
            
        #######################################
        # NUMBER OF POINTS # GAUSS QUADRATURE #
        #######################################
        
        # Number of gauss points
        Ngauss = 2
        
        ###########################
        # GAUSS QUADRATURE POINTS #
        ###########################
        
        # Guass quadrature points initialization
        pointsGauss = np.zeros( ( Ngauss , 1 ) )
        
        # Gauss quadrature points definition
        pointsGauss[ 0 , 0 ] = + np.sqrt( 1.0 / 3.0 )
        pointsGauss[ 1 , 0 ] = - np.sqrt( 1.0 / 3.0 )
        
        ############################
        # GAUSS QUADRATURE WEIGHTS #
        ############################
        
        # Guass quadrature weights initialization
        weightsGauss = np.zeros( ( Ngauss , 1 ) )
        
        # Gauss quadrature weights definition
        weightsGauss[ 0 , 0 ] = 1.0
        weightsGauss[ 1 , 0 ] = 1.0        
                    
        ############
        # JACOBIAN #
        ############
        
        # Element length definition
        L = self.node2.x - self.node1.x
        
        # Jacobian definition
        J = L / 2.0
        
        ####################### 
        # LOOP # GAUSS POINTS #
        #######################
        
        # Loop over gauss
        for i in range( Ngauss ):
            
            #######################
            # GET GAUSS CONDITION #
            #######################
            
            # Natural coordinate point inside element
            r = pointsGauss[ i , 0 ]
            
            # Weight
            w = weightsGauss[ i , 0 ]
            
            ###################
            # SHAPE FUNCTIONS #
            ###################
            
            # Shape functions definition
            N1r = ( 1.0 - r ) / 2.0
            N2r = ( 1.0 + r ) / 2.0
            
            ##############################
            # SHAPE FUNCTIONS DERIVATIVE #
            ##############################
            
            # Shape functions derivative in relation to r
            DN1r = ( - 1.0 ) / 2.0
            DN2r = ( + 1.0 ) / 2.0
            
            ########
            # ZETA #
            ########
            
            # Get derivative from d11 and d12
            Dd11 = ( self.node2.d11 - self.node1.d11 ) / 2.0
            Dd12 = ( self.node2.d12 - self.node1.d12 ) / 2.0
            
            # Get d11 on gauss point
            d11 = ( N1r * self.node1.d11 ) + ( N2r * self.node2.d11 )
            
            # Zeta definitions - Initial conditions
            zeta1 = + 2.0 + ( ( r / d11 ) * Dd11 )
            zeta2 = - 2.0 + ( ( r / d11 ) * Dd12 )
                        
            ##########
            # LAMBDA #
            ##########
            
            # Get derivative from radial and tangent irridiation
            Deret = ( ( self.node2.er - self.node2.et ) - ( self.node1.er - self.node1.et ) ) / 2.0

            # Get derivative from tangent irridiation
            Det = ( self.node2.et - self.node1.et ) / 2.0
            
            # Get er and et on gauss point
            er = ( N1r * self.node1.er ) + ( N2r * self.node2.er )
            et = ( N1r * self.node1.et ) + ( N2r * self.node2.et )
            
            # Lambda definitions
            lambda1 = Deret + ( ( ( 1.0 + self.material.v ) / ( 1.0 - self.material.v ) ) * Det )
            lambda2 = ( 2.0 * ( ( ( 1.0 - ( 2.0 * self.material.v ) ) / ( 1.0 - self.material.v ) ) * ( er - et ) ) ) + ( ( r / d11 ) * Dd11 * er ) + ( ( r / d11 ) * Dd12 * et )
                   
            ###################
            # STIFFNESS TERMS #
            ###################
            
            # Stiffness terms
            self.Ke[ 0 , 0 ] += ( 4.0 * w * np.pi * ( ( ( ( r * r ) / J ) * DN1r * DN1r ) + ( ( 2.0 - zeta1 ) * r * N1r * DN1r ) - ( zeta2 * J * N1r * N1r ) ) )
            self.Ke[ 0 , 1 ] += ( 4.0 * w * np.pi * ( ( ( ( r * r ) / J ) * DN1r * DN2r ) + ( ( 2.0 - zeta1 ) * r * N1r * DN2r ) - ( zeta2 * J * N1r * N2r ) ) )
            self.Ke[ 1 , 0 ] += ( 4.0 * w * np.pi * ( ( ( ( r * r ) / J ) * DN2r * DN1r ) + ( ( 2.0 - zeta1 ) * r * N2r * DN1r ) - ( zeta2 * J * N2r * N1r ) ) )
            self.Ke[ 1 , 1 ] += ( 4.0 * w * np.pi * ( ( ( ( r * r ) / J ) * DN2r * DN2r ) + ( ( 2.0 - zeta1 ) * r * N2r * DN2r ) - ( zeta2 * J * N2r * N2r ) ) )
                                    
            #########################
            # INTERNAL FORCES TERMS #
            #########################
            
            # External coordinate points
            rminus = - 1.0
            rplus = + 1.0
            
            # Derivative of r in relation to u - Initial conditions
            dudr = 0.0
                        
            # Internal forces terms
            self.Fei[ 0 , 0 ] += 0.5 * ( - 4.0 * np.pi * ( rminus ) * ( rminus ) * dudr )
            self.Fei[ 1 , 0 ] += 0.5 * ( + 4.0 * np.pi * ( rplus ) * ( rplus ) * dudr )    
                        
            #########################
            # EXTERNAL FORCES TERMS #
            #########################
            
            # External forces terms
            self.Fee[ 0 , 0 ] += - 4.0 * w * np.pi * r * J * ( ( r * lambda1 ) + lambda2 ) * N1r
            self.Fee[ 1 , 0 ] += - 4.0 * w * np.pi * r * J * ( ( r * lambda1 ) + lambda2 ) * N2r
                
    #########
    # PRINT #
    #########
        
    # Print
    def print( self ):
        
        # Print header
        print( '--------------------------------------------------------------------' )
        
        # Print ID
        print( 'Element %d' % self.ID )
        
        # Print initial coordinate
        print( 'Initial coordinate [ um ]     = %.2f' % self.node1.x )
        
        # Print end coordinate
        print( 'End coordinate [ um ]         = %.2f' % self.node2.x )        
                
        # Print d11 parameter for node 1
        print( 'd11 parameter - Node %d       = %.2f' % ( self.node1.ID, self.node1.d11 ) )
        
        # Print d11 parameter for node 2
        print( 'd11 parameter - Node %d       = %.2f' % ( self.node2.ID, self.node2.d11 ) )        
        
        # Print d11 parameter for element ( constant )
        print( 'd11 parameter on element      = %.2f' % self.d11 )
        
        # Print d12 parameter for node 1
        print( 'd12 parameter - Node %d       = %.2f' % ( self.node1.ID, self.node1.d12 ) )
                
        # Print d12 parameter for node 2
        print( 'd12 parameter - Node %d       = %.2f' % ( self.node2.ID, self.node2.d12 ) )
                
        # Print d12 parameter for element ( constant )
        print( 'd12 parameter on element      = %.2f' % self.d12 )
        
        # Print radial irridiation induced change rate for node 1
        print( 'Radial irridiation - Node %d  = %.2e' % ( self.node1.ID, self.node1.er ) )
        
        # Print radial irridiation induced change rate for node 2
        print( 'Radial irridiation - Node %d  = %.2e' % ( self.node2.ID, self.node2.er ) )
        
        # Print radial irridiation induced change rate for element ( constant )
        print( 'Radial irridiation on element = %.2e' % self.er )
        
        # Print tangential irridiation induced change rate for node 1
        print( 'Tangent irridiation - Node %d = %.2e' % ( self.node1.ID, self.node1.et ) )
        
        # Print tangential irridiation induced change rate for node 2
        print( 'Tangent irridiation - Node %d = %.2e' % ( self.node2.ID, self.node2.et ) )
        
        # Print tangential irridiation induced change rate for element ( constant )
        print( 'Tangent irridiation on element= %.2e' % self.et )
        
        # Print tangential irridiation induced change rate
        print( 'Tangent irridiation ind. rate = %.2e' % self.et )
        
        # Print region name
        print( 'Region Name                   = %s' % self.region )
                
        # Print material struct
        self.material.printShort()
        
        # Print constitutive matrix
        print( 'Constitutive matrix - C - Equation 2' )
        print( self.C )
        
        # Print irridiation matrix
        print( 'Irridiation matrix - A - Equation 4' )
        print( self.A )
        
        # Print G matrix
        print( 'G matrix - G - Equation 8' )
        print( self.G )
        
        # Print stiffness matrix
        print( 'K matrix - K - Equation 13' )
        print( self.Ke )
        
        # Print internal force vector
        print( 'Internal force vector - Fei - Equation 12' )
        print( self.Fei )
        
        # Print external force vector
        print( 'External force vector - Fee - Equation 14' )
        print( self.Fee )
        
        # Print displacement vector
        print( 'Displacement vector - ue - Equation 12' )
        print( self.ue )

        # Print footer
        print( '--------------------------------------------------------------------' )  