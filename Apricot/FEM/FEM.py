# Import dataclass library
from dataclasses import dataclass

# Import list library
import typing

# Import numpy library
import numpy as np

# Import functions
from ModelInput import ModelInput
from Material import Material
from Node import Node
from Element import Element

########################
# FINITE ELEMENT CLASS #
########################

# Finite element class initialization
@dataclass
class FEM:
    
    ##################
    # INITIAL LENGTH #
    ##################
    
    # Initial length [ um ]
    Li: float
    
    ################
    # FINAL LENGTH #
    ################
    
    # Final length [ um ]
    Lf: float
    
    ################
    # TOTAL LENGTH #
    ################
    
    # Total length [ um ]
    L: float
    
    ###################
    # NUMBER OF NODES #
    ###################
    
    # Number of nodes
    Nnodes: int
    
    ######################
    # NUMBER OF ELEMENTS #
    ######################
    
    # Number of elements
    Nelements: int 
    
    ###############################
    # NUMBER OF DEGREE OF FREEDOM #
    ###############################
    
    # Number of degree of freedom
    Ndofs: int
    
    ################
    # NODES STRUCT #
    ################
    
    # Nodes struct initialization
    nodes: 'typing.Any'
    
    ###################
    # ELEMENTS STRUCT #
    ###################
    
    # Elements struct initialization
    elements: 'typing.Any'
    
    #####################
    # METHOD MULTIPLIER #
    #####################
    
    # Method multiplier ( 0 = explicit / 0.5 = Crank Nicholson / 1.0 = implicit )
    beta: float
    
    ###########################
    # GLOBAL STIFFNESS MATRIX #
    ###########################
    
    # Global stiffness matrix
    K: np.ndarray
    
    ################################
    # GLOBAL INTERNAL FORCE VECTOR #
    ################################
    
    # Global internal force vector
    Fi: np.ndarray
    
    ################################
    # GLOBAL EXTERNAL FORCE VECTOR #
    ################################
    
    # Global external force vector
    Fe: np.ndarray
    
    #######################
    # GLOBAL FORCE VECTOR #
    #######################
    
    # Global force vector
    F: np.ndarray
    
    ##############################
    # GLOBAL DISPLACEMENT VECTOR #
    ##############################
    
    # Global displacement vector
    u: np.ndarray
   
    ##################
    # INITIALIZATION #
    ##################
    
    # Initialization
    def __init__ ( self, model: ModelInput, PyC: Material, SiC:Material ):
        
        # Initial length ( Kernel radius )
        self.Li = ( model.kernelDiameter / 2.0 )
        
        # Final length
        self.Lf = self.Li + model.bufferThickness + model.IPyCThickness + model.SiCThickness + model.OPyCThickness
        
        # Total length
        self.L = self.Lf - self.Li
        
        # Number of elements
        self.Nelements = 4 * model.Nelements
        
        # Number of nodes
        self.Nnodes = self.Nelements + 1
        
        # Number of degree of freedom
        self.Ndofs = self.Nnodes
        
        # Method multiplier
        self.beta = model.beta
        
        ################
        # LOOP # NODES #
        ################
        
        # Nodes structure initialization
        self.nodes = [ ]
        
        # Loop over nodes
        for i in range( self.Nnodes.astype( int ) ):
            
            ##############
            # COORDINATE #
            ##############
            
            # Coordinate definition
            r = self.Li + ( ( self.L / self.Nelements ) * i )
            
            ########
            # NODE #
            ########
            
            # Node struct
            node = Node( i + 1 , r )
            
            ##############
            # ALLOCATION #
            ##############
            
            # Allocation on nodes structure
            self.nodes.append( node )
            
        ###################
        # LOOP # ELEMENTS #
        ###################
        
        # Elements structure initialization
        self.elements = [ ]
        
        # Loop over elements
        for i in range( self.Nelements.astype( int ) ):
            
            ##########
            # NODE 1 #
            ##########
            
            # Node 1 struct definition
            node1 = self.nodes[ i ]
            
            ##########
            # NODE 2 #
            ##########
            
            # Node 2 struct definition
            node2 = self.nodes[ i + 1 ]
            
            ##########
            # BUFFER #
            ##########
            
            # Buffer region definition
            if ( 0 * model.Nelements ) <= i < ( 1 * model.Nelements ):
                
                ####################
                # ELEMENT # BUFFER #
                ####################
                
                # Element struct
                element = Element( i + 1 , node1, node2, 'Buffer', PyC )
            
                ##############
                # ALLOCATION #
                ##############
                
                # Allocation on elements structure
                self.elements.append( element )
                
            ########
            # IPyC #
            ########
            
            # IPyC region definition
            if ( 1 * model.Nelements ) <= i < ( 2 * model.Nelements ):
                
                ##################
                # ELEMENT # IPyC #
                ##################
                
                # Element struct
                element = Element( i + 1 , node1, node2, 'IPyC', PyC )
            
                ##############
                # ALLOCATION #
                ##############
                
                # Allocation on elements structure
                self.elements.append( element )
            
            #######
            # SiC #
            #######
            
            # SiC region definition
            if ( 2 * model.Nelements ) <= i < ( 3 * model.Nelements ):
                
                #################
                # ELEMENT # SiC #
                #################
                
                # Element struct
                element = Element( i + 1 , node1, node2, 'SiC', SiC )
            
                ##############
                # ALLOCATION #
                ##############
                
                # Allocation on elements structure
                self.elements.append( element )
            
            ########
            # OPyC #
            ########
            
            # OPyC region definition
            if ( 3 * model.Nelements ) <= i < ( 4 * model.Nelements ):
                
                ##################
                # ELEMENT # OPyC #
                ##################
                
                # Element struct
                element = Element( i + 1 , node1, node2, 'OPyC', PyC )
            
                ##############
                # ALLOCATION #
                ##############
                
                # Allocation on elements structure
                self.elements.append( element )
                
            ###########################
            # SET CONSTITUTIVE MATRIX #
            ###########################
                    
            # Set constitutive matrix
            self.elements[ i ].setC()
            
            ##########################
            # SET IRRIDIATION MATRIX #
            ##########################
                    
            # Set irridiation matrix
            self.elements[ i ].setA()   
            
            ################
            # SET G MATRIX #
            ################
            
            # Set G matrix
            self.elements[ i ].setG( self.beta )
            
            ##########################
            # SET INITIAL CONDITIONS #
            ##########################
            
            # Set initial conditions
            self.elements[ i ].setInitialConditions()

    ############
    # ASSEMBLY #
    ############
    
    # Assembly finite element problem
    def assembly( self ):
        
        ##################
        # INITIALIZATION #
        ##################
        
        # Global stiffness initialization
        self.K = np.zeros( ( self.Ndofs.astype( int ), self.Ndofs.astype( int ) ) )
        
        # Global internal forces initialization
        self.Fi = np.zeros( ( self.Ndofs.astype( int ) , 1 ) )
        
        # Global external forces initialization
        self.Fe = np.zeros( ( self.Ndofs.astype( int ) , 1 ) )
        
        ###################
        # LOOP # ELEMENTS #
        ###################
        
        # Loop over elements
        for i in range( self.Nelements.astype( int ) ):
            
            ##########################
            # SET ELEMENT PARAMETERS #
            ##########################
            
            # Set element parameters
            self.elements[ i ].setElementParameters()
            
            #################################
            # ALLOCATION # GLOBAL STIFFNESS #
            #################################
            
            # Allocation on global stiffness
            self.K[ i + 0 , i + 0 ] += self.elements[ i ].Ke[ 0 , 0 ]
            self.K[ i + 0 , i + 1 ] += self.elements[ i ].Ke[ 0 , 1 ]
            self.K[ i + 1 , i + 0 ] += self.elements[ i ].Ke[ 1 , 0 ]
            self.K[ i + 1 , i + 1 ] += self.elements[ i ].Ke[ 1 , 1 ]
            
            #######################################
            # ALLOCATION # GLOBAL INTERNAL FORCES #
            #######################################
            
            # Allocation global internal forces
            self.Fi[ i + 0 , 0 ] = self.elements[ i ].Fei[ 0 , 0 ]
            self.Fi[ i + 1 , 0 ] = self.elements[ i ].Fei[ 1 , 0 ]
            
            #######################################
            # ALLOCATION # GLOBAL EXTERNAL FORCES #
            #######################################
            
            # Allocation global external forces
            self.Fe[ i + 0 , 0 ] += self.elements[ i ].Fee[ 0 , 0 ]
            self.Fe[ i + 1 , 0 ] += self.elements[ i ].Fee[ 1 , 0 ]

    #########
    # SOLVE #
    #########
    
    # Solve element problem
    def solve( self ):
        
        ###############
        # FEM PROBLEM #
        ###############
        
        # Sum the internal and external forces
        self.F = self.Fi + self.Fe
        
        ###################
        # SOLVE # K.u = F #
        ###################
        
        # Solve FEM problem
        self.u = np.linalg.solve( self.K , self.F )
        
        ###################
        # LOOP # ELEMENTS #
        ###################
        
        # Loop over elements
        for i in range( self.Nelements.astype( int ) ):
        
            ###############################
            # ALLOCATE RESULTS # ELEMENTS #
            ###############################
            
            # Allocation results
            self.elements[ i ].ue[ 0 , 0 ] = self.u[ i + 0 , 0 ]
            self.elements[ i ].ue[ 1 , 0 ] = self.u[ i + 1 , 0 ]

    #########
    # PRINT #
    #########
        
    # Print
    def print( self ):
        
        # Print header
        print( '--------------------------------------------------------------------' )
        print( 'Finite element parameters' )
        
        # Print initial length [ um ]
        print( 'Initial length [ um ]         = %.2f' % self.Li )
        
        # Print final length [ um ]
        print( 'Final length [ um ]           = %.2f' % self.Lf )
        
        # Print total length [ um ]
        print( 'Total length [ um ]           = %.2f' % self.L ) 
        
        # Print number of elements
        print( 'Number of elements            = %d' % self.Nelements ) 
        
        # Print number of nodes
        print( 'Number of nodes               = %d' % self.Nnodes ) 
        
        # Print number of degree of freedom
        print( 'Number of degree of freedom   = %d' % self.Ndofs ) 
            
        # Print elements struct
        print( 'Elements' )
        
        # Loop over elements
        for i in range( self.Nelements.astype( int ) ):        
                    
            #########
            # PRINT #
            #########
            
            # Print element struct
            self.elements[ i ].print()        
         
        # Print global stiffness
        print( 'Global stiffness: ' )
        print( self.K )
        
        # Print global internal force vector
        print( 'Global internal force vector: ' )
        print( self.Fi )
        
        # Print global external force vector
        print( 'Global external force vector: ' )
        print( self.Fe )
        
        # Print global force vector
        print( 'Global force vector: ' )
        print( self.F )
        
        # Print global displacement vector
        print( 'Global displacement vector: ' )
        print( self.u )
            
        # Print footer
        print( '--------------------------------------------------------------------' )      
  