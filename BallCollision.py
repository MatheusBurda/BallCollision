# This code was created by Matheus A. Burda - April/2020
# Email: matheusburda@alunos.utfpr.edu.br
#
# This code simulates elastic collision between balls inside a closed box conserving the kinetic energy.
#
# Made using Python/PyOpenGL

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
import random
import argparse

# Size of the screen 
WIDTH = 800
HEIGHT = 600

# Number of balls inside the cube, RADIUS and MAX_VELOCITY of the balls
NUM_BALLS = 15
RADIUS = 0.45
MAX_VELOCITY = 0.005
COLOR_ON = True # Toggle the color of the balls to on/off

# Cube Vertices coordinates and its size
CUBE_SIZE = 2 # Half the size of the cube


# Edges of the cube
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

def argumentParser():
    global WIDTH
    global HEIGHT
    global NUM_BALLS
    global RADIUS
    global MAX_VELOCITY
    global COLOR_ON
    global CUBE_SIZE

    parser = argparse.ArgumentParser(description='This program simulates a 3D elastic collision between balls inside a closed cube conserving the kinetic energy.')
    parser.add_argument('--width', type=int, help='screen width. Defaults to {}'.format(WIDTH))
    parser.add_argument('--height', type=int, help='screen height. Defaults to {}'.format(HEIGHT))

    parser.add_argument('-n', '--num-balls', type=int, help='amount of balls used in the simulation. Defaults to {}'.format(NUM_BALLS))
    parser.add_argument('-r', '--radius', type=float, help='radius of balls. Defaults to {}'.format(RADIUS))
    parser.add_argument('-v', '--max-velocity', type=float, help='max velocity allowed. Defaults to {}'.format(MAX_VELOCITY))
    parser.add_argument('--no-color', action='store_false', help='toggle colored balls off')

    parser.add_argument('-s', '--size', type=int, help='size of the cube that contains the balls. Defaults to {}'.format(CUBE_SIZE))

    args = parser.parse_args()

    if args.width is not None:
        WIDTH = args.width
    if args.height is not None:
        HEIGHT = args.height
    if args.num_balls is not None:
        NUM_BALLS = args.num_balls
    if args.radius is not None:
        RADIUS = args.radius
    if args.max_velocity is not None:
        MAX_VELOCITY = args.max_velocity
    if args.no_color is not None:
        COLOR_ON = args.no_color
    if args.size is not None:
        CUBE_SIZE = args.size

# Function to draw the Cube
def Cube():
    vertices = (
        ( CUBE_SIZE,-CUBE_SIZE,-CUBE_SIZE),
        ( CUBE_SIZE, CUBE_SIZE,-CUBE_SIZE),
        (-CUBE_SIZE, CUBE_SIZE,-CUBE_SIZE),
        (-CUBE_SIZE,-CUBE_SIZE,-CUBE_SIZE),
        ( CUBE_SIZE,-CUBE_SIZE, CUBE_SIZE),
        ( CUBE_SIZE, CUBE_SIZE, CUBE_SIZE),
        (-CUBE_SIZE,-CUBE_SIZE, CUBE_SIZE),
        (-CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        )
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Class Ball (for each ball)
class Ball:
    center = []
    velocity = [] 
    color = [1.0,1.0,1.0,1.0]
    lastCollision = -1
    def __init__(self, center, velocity, color, RADIUS):        
        self.center = center
        self.velocity = velocity
        self.color = color
        self.RADIUS = RADIUS
    
    def changePosition(self):
        for i in range(3):
            self.center[i] = self.center[i] + self.velocity[i]
    
    def setLastCollision(self, lastCollision):
        self.lastCollision = lastCollision
    def getLastCollision(self):
        return self.lastCollision

#ballList 
ballList = []

# Function to determinate the Dot (Scalar) Product between 2 vectors (x,y,z)
# Arguments: 2 vectors (x,y,z)
def dotProduct(vec1, vec2):
    return (vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2])

# Function to calculate the Norm/Magnitude of a vector
# Arguments: 1 vector (x,y,z)
def sizeVector(vec1):
    return (math.sqrt( vec1[0] ** 2 + vec1[1] ** 2 + vec1[2] ** 2 ))

# Function to calculate the distance between two points
# Arguments: 2 vectors (x,y,z)
def distPoints(vec1, vec2):
    return (math.sqrt((vec1[0] - vec2[0]) ** 2 + (vec1[1] - vec2[1]) **2 + (vec1[2] - vec2[2]) ** 2 ))

# Function to determine the orthogonal projection of a vector1(vec1) onto vector2(vec2)
# Arguments: the two vectors
def orthogonalProjection(vec1, vec2):
    alfa = dotProduct(vec1, vec2) / sizeVector(vec2) ** 2
    vector = []
    for i in range(len(vec2)): 
        vector.append(vec2[i] * alfa)
    return vector

# Function to determine the subtraction between two vectors (vec1 - vec2)
# Argumetns: Vector1 (vec1) and Vector2(vec2)
def subVector(vec1, vec2):
    vector = []
    if len(vec1) == len(vec2):
        for i in range(len(vec1)):
            vector.append(vec1[i] - vec2[i])
        return vector
    else:
        print("Impossible to subtract vectors of different sizes")


# Function to handdle collision with balls
# Arguments: the number of the balls in the list
def ballCollision(i, j):
    global ballList
    collisionDirection = []
    for x in range(3):
        collisionDirection.append( ballList[j].center[x] - ballList[i].center[x] )
    
    w1 = orthogonalProjection(ballList[i].velocity, collisionDirection)
    w2 = orthogonalProjection(ballList[j].velocity, collisionDirection)
    u1 = subVector(ballList[i].velocity , w1)
    u2 = subVector(ballList[j].velocity, w2)

    for x in range(3):
        ballList[i].velocity[x] = u1[x] + w2[x]
        ballList[j].velocity[x] = u2[x] + w1[x]

# Function to initialize OpenGL, called after the window is created
def initializeGl():
    glClearColor(0.,0.,0.,1.)                               
    glShadeModel(GL_SMOOTH)                                 
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [10.,4.,10.,1.]                     # Position of the light    
    lightZeroColor = [1.0,1.0,1.0,1.0]                      # White light
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)        
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)        
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)       
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)

# Function to handle if the screen is resized
def screenResize(WIDTH, HEIGHT):
    if HEIGHT == 0:						# Prevent A Divide By Zero If The Window Is Too Small
        HEIGHT = 1
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(WIDTH)/float(HEIGHT), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# Function to check collisions and update the position of the balls
def update():
    global ballList
    # Update the position of the balls
    for i in range(len(ballList)):
        ballList[i].changePosition()
    
    # Test if each ball is colliding with other balls
    # The 'x' thing is to not check collision with the same balls two times in a row
    x = 1
    for i in range(len(ballList)):
        for j in range(len(ballList) - x):
            if((distPoints(ballList[i].center, ballList[j + x].center)) <= ballList[i].RADIUS + ballList[j+x].RADIUS) and ((ballList[i].getLastCollision() != (j+x)) or (ballList[j+x].getLastCollision() != i)):
                ballCollision(i, j+x)
                ballList[i].setLastCollision(j+x)
                ballList[j+x].setLastCollision(i)
        x +=1
        
    # Test the collision of the balls with the walls of the cube
    for i in range(len(ballList)):
        if (ballList[i].center[0] - ballList[i].RADIUS < -CUBE_SIZE or ballList[i].center[0] + ballList[i].RADIUS > CUBE_SIZE):   # x
            ballList[i].velocity[0] *= -1
            ballList[i].setLastCollision(-1)
        if (ballList[i].center[1] - ballList[i].RADIUS < -CUBE_SIZE or ballList[i].center[1] + ballList[i].RADIUS > CUBE_SIZE):   # y
            ballList[i].velocity[1] *= -1
            ballList[i].setLastCollision(-1)
        if (ballList[i].center[2] - ballList[i].RADIUS < -CUBE_SIZE or ballList[i].center[2] + ballList[i].RADIUS > CUBE_SIZE):   # z
            ballList[i].velocity[2] *= -1
            ballList[i].setLastCollision(-1)

# Function to print text on the screen
def printText( x,  y, z, text):

    glColor3f(1,1,1)
    glWindowPos3f(x,y,z)
    for ch in text :
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15 , ctypes.c_int(ord(ch)))



# GLUT Display function
def display():
    global ballList
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    # Update ball position and check collisions
    update()

    # Draw the Cube
    glPushMatrix()
    color = [1.0,1.,1.,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    Cube()
    glPopMatrix()   

    # Draw Balls
    for i in range(len(ballList)):
        glPushMatrix()
        glMaterialfv(GL_FRONT,GL_DIFFUSE,ballList[i].color)
        glTranslatef(ballList[i].center[0],ballList[i].center[1],ballList[i].center[2])
        glutSolidSphere(ballList[i].RADIUS, 20, 20)
        glPopMatrix()

    # Info about the balls, uncomment each line to show different info about the balls
    # Meant to be used one at a time
    """ glPushMatrix()
    for i in range(len(ballList)):
        #printText( 1 , (i+3)*16 , -1 ,  str(i) + " last collided with " + str(ballList[i].getLastCollision())) # Shows the last ball each ball collided with
        #printText( 1 , (i+3)*16 , -1 ,  "V" + str(i) + " = " + str(sizeVector(ballList[i].velocity))) # Shows the velocity of each ball
        #printText( 1 , (i+3)*16 , -1 ,  "Center " + str(i) + " = " + str(ballList[i].center)) # Shows the center position of each ball
    glPopMatrix() """

    cineticEnergy = 0.00
    for i in range(len(ballList)):
        cineticEnergy += float((sizeVector(ballList[i].velocity) ** 2) / 2.0)
    
    glPushMatrix()
    printText( 1 , 1 , -1 , "K = " + str(round(cineticEnergy, 12)))
    printText(1, 17, -1, "Balls: " + str(NUM_BALLS) + "  RADIUS: " + str(RADIUS))
    printText(1, 33, -1, "Size of the Cube: " + str(2*CUBE_SIZE))
    glPopMatrix()

    glutSwapBuffers()
    return

# Function to create the balls in different positions, with different velocities and different collors
def inicializeBalls():

    centerList = randomCenter(NUM_BALLS)
    for i in range(NUM_BALLS):
        ballList.append(Ball(centerList[i], randomVelocity(), randomColor(), RADIUS))

# Function to give the balls the start center position
# Returns a list of vectors [x,y,z]
def randomCenter(NUM_BALLS):
    vector = []

    qBall = int((CUBE_SIZE / RADIUS))
    qBall3 = qBall ** 3

    if(qBall3 >= NUM_BALLS):

        for j in range (NUM_BALLS):  # For all the balls
            pos = newPos(qBall)

            while (checkBallInside(vector, pos)):
                pos = newPos(qBall)

            vector.append(pos)

    else: 
        print("ERROR: not possible to fit the balls into the cube. \nTry reducing the quantity of balls, make the balls smaller or increase the CUBE_SIZE")
        quit()
    
    return vector

# Function to generate a new position for the list in randomCenter() Function
# Returns the position [x,y,z]
def newPos(qBall):
    pos = []
    if (qBall == 2):
        for i in range(3):  # X, Y, Z ( 3 times )
            randomNumber = random.choice( [-1,1] )
            pos.append(randomNumber * RADIUS)

    elif not (qBall % 2):    # Even number
        for i in range(3):  # X, Y, Z ( 3 times )
            randomNumber = random.randint( -qBall / 2 , qBall / 2 )

            if (randomNumber > 0): 
                pos.append(randomNumber * 2 * RADIUS - RADIUS)
            elif (randomNumber < 0):
                pos.append(randomNumber * 2 * RADIUS + RADIUS)
            else:   # randomNumber == 0
                randomNumber = random.choice( [-1,1] )
                pos.append(randomNumber * RADIUS)
    
    else:                   # Odd number
        for i in range(3):  # X, Y, Z ( 3 times )
            randomNumber = random.randint( int(-qBall / 2) , int(qBall / 2 ))
            pos.append(randomNumber * 2 *RADIUS)
    
    return pos

# Function to determine how many balls in the vector created on the randomCenter() function 
# are inside each other 
# Returns the number of balls "Colliding"
def checkBallInside(vector, pos):
    # The 'x' thing is to not check the same balls two times in a row
    for i in range(len(vector)):
        if(vector[i][0] == pos[0]) and (vector[i][1] == pos[1]) and (vector[i][2] == pos[2]):
            return True
    return False

# Function to give a ball the start velocity
# Returns a vector [x,y,z]
def randomVelocity():
    vector = [] 
    for i in range(3):
        vector.append( round(random.uniform( -MAX_VELOCITY , MAX_VELOCITY  ), 4) )
    return vector

# Function to give a ball a random color
# Returns a color [r,g,b,alfa]
def randomColor():
    if(COLOR_ON):
        color = [random.choice( [0.0,1.0] ), random.choice( [0.0,1.0] ), random.choice( [0.0,1.0] ), 1.0]
        while (color[0] == 0.0) and (color[1] == 0.0) and (color[2] == 0.0):
            color = [random.choice( [0.0,1.0] ), random.choice( [0.0,1.0] ), random.choice( [0.0,1.0] ), 1.0]
    else:
        color = [1.0,1.0,1.0,1.0]
    return color
    



def main():

    argumentParser()

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # Determine the size of the screen
    glutInitWindowSize(WIDTH, HEIGHT)

    # The window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)

    # Create a window with the name choosen
    glutCreateWindow('Ball Collision')

    # To register the main display function
    glutDisplayFunc(display)

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(display)

    # Register the function called when our window is resized.
    glutReshapeFunc(screenResize)

    # Initialize balls on different positions, with different velocities and different collors 
    inicializeBalls()

    # Initialize the window.
    initializeGl()

    gluLookAt(0,0,10,
              0,0,0,
              0,1,0)
    #glRotatef(8, 1.0, 1.0, 0.0)
    glTranslatef(1.0, 0.0, -CUBE_SIZE/2)

    glPushMatrix()
    # Start Event Processing Engine
    glutMainLoop()


if __name__ == "__main__":
    main()
