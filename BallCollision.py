# This code was created by Matheus A. Burda - April/2020
# Email: matheusburda@alunos.utfpr.edu.br
#
# This code simulates elastic collision between balls inside a closed box
# conservating the cinetic energy.
#
# Made using Python/PyOpenGL

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
import random

# Name of the screen
screenName = 'Ball Collision'

# Size of the screen 
width = 800
height = 600

# Number of balls inside the cube, radius and maxvelocity of the balls
numBalls = 15
radius = 0.45
maxVelocity = 0.005
colorOn = True # Toggle the color of the balls to on/off

# Cube Vertices coordinates and its size
cubeSize = 2 # Half the size of the cube


vertices = (
    ( cubeSize,-cubeSize,-cubeSize),
    ( cubeSize, cubeSize,-cubeSize),
    (-cubeSize, cubeSize,-cubeSize),
    (-cubeSize,-cubeSize,-cubeSize),
    ( cubeSize,-cubeSize, cubeSize),
    ( cubeSize, cubeSize, cubeSize),
    (-cubeSize,-cubeSize, cubeSize),
    (-cubeSize, cubeSize, cubeSize)
    )

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

# Function to draw the Cube
def Cube():
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
    def __init__(self, center, velocity, color, radius):        
        self.center = center
        self.velocity = velocity
        self.color = color
        self.radius = radius
    
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
    global width, height
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
def screenResize(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small
        Height = 1
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# Function to check collisions and update the position of the balls
def update():
    global ballList, cubeSize
    # Update the position of the balls
    for i in range(len(ballList)):
        ballList[i].changePosition()
    
    # Test if each ball is colliding with other balls
    # The 'x' thing is to not check collision with the same balls two times in a row
    x = 1
    for i in range(len(ballList)):
        for j in range(len(ballList) - x):
            if((distPoints(ballList[i].center, ballList[j + x].center)) <= ballList[i].radius + ballList[j+x].radius) and ((ballList[i].getLastCollision() != (j+x)) or (ballList[j+x].getLastCollision() != i)):
                ballCollision(i, j+x)
                ballList[i].setLastCollision(j+x)
                ballList[j+x].setLastCollision(i)
        x +=1
        
    # Test the collision of the balls with the walls of the cube
    for i in range(len(ballList)):
        if (ballList[i].center[0] - ballList[i].radius < -cubeSize or ballList[i].center[0] + ballList[i].radius > cubeSize):   # x
            ballList[i].velocity[0] *= -1
            ballList[i].setLastCollision(-1)
        if (ballList[i].center[1] - ballList[i].radius < -cubeSize or ballList[i].center[1] + ballList[i].radius > cubeSize):   # y
            ballList[i].velocity[1] *= -1
            ballList[i].setLastCollision(-1)
        if (ballList[i].center[2] - ballList[i].radius < -cubeSize or ballList[i].center[2] + ballList[i].radius > cubeSize):   # z
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
        glutSolidSphere(ballList[i].radius, 20, 20)
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
    printText(1, 17, -1, "Balls: " + str(numBalls) + "  Radius: " + str(radius))
    printText(1, 33, -1, "Size of the Cube: " + str(2*cubeSize))
    glPopMatrix()

    glutSwapBuffers()
    return

# Function to create the balls in different positions, with different velocities and different collors
def inicializeBalls():
    global numBalls
    centerList = randomCenter(numBalls)
    for i in range(numBalls):
        ballList.append(Ball(centerList[i], randomVelocity(), randomColor(), radius))

# Function to give the balls the start center position
# Returns a list of vectors [x,y,z]
def randomCenter(numBalls):
    global cubeSize, radius
    vector = []

    qBall = int((cubeSize / radius))
    qBall3 = qBall ** 3

    if(qBall3 >= numBalls):

        for j in range (numBalls):  # For all the balls
            pos = newPos(qBall)

            while (checkBallInside(vector, pos)):
                pos = newPos(qBall)

            vector.append(pos)

    else: 
        print("ERROR: not possible to fit the balls into the cube. \nTry reducing the quantity of balls, make the balls smaller or increase the cubeSize")
        quit()
    
    return vector

# Function to generate a new position for the list in randomCenter() Function
# Returns the position [x,y,z]
def newPos(qBall):
    global radius
    pos = []
    if (qBall == 2):
        for i in range(3):  # X, Y, Z ( 3 times )
            randomNumber = random.choice( [-1,1] )
            pos.append(randomNumber * radius)

    elif not (qBall % 2):    # Even number
        for i in range(3):  # X, Y, Z ( 3 times )
            randomNumber = random.randint( -qBall / 2 , qBall / 2 )

            if (randomNumber > 0): 
                pos.append(randomNumber * 2 * radius - radius)
            elif (randomNumber < 0):
                pos.append(randomNumber * 2 * radius + radius)
            else:   # randomNumber == 0
                randomNumber = random.choice( [-1,1] )
                pos.append(randomNumber * radius)
    
    else:                   # Odd number
        for i in range(3):  # X, Y, Z ( 3 times )
            randomNumber = random.randint( int(-qBall / 2) , int(qBall / 2 ))
            pos.append(randomNumber * 2 *radius)
    
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
        vector.append( round(random.uniform( -maxVelocity , maxVelocity  ), 4) )
    return vector

# Function to give a ball a random color
# Returns a color [r,g,b,alfa]
def randomColor():
    global colorOn
    if(colorOn):
        color = [random.choice( [0.0,1.0] ), random.choice( [0.0,1.0] ), random.choice( [0.0,1.0] ), 1.0]
        while (color[0] == 0.0) and (color[1] == 0.0) and (color[2] == 0.0):
            color = [random.choice( [0.0,1.0] ), random.choice( [0.0,1.0] ), random.choice( [0.0,1.0] ), 1.0]
    else:
        color = [1.0,1.0,1.0,1.0]
    return color
    



def main():
    global width, height, screenName
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # Determine the size of the screen
    glutInitWindowSize(width, height)

    # The window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)

    # Create a window with the name choosen
    glutCreateWindow(screenName)

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
    glTranslatef(1.0, 0.0, -cubeSize/2)

    glPushMatrix()
    # Start Event Processing Engine
    glutMainLoop()


main()