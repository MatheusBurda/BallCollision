# Ball Collision

This project simulates a 3D elastic collision between balls inside a closed box conserving the kinetic energy.

![BallCollision](/Videos/BallCollision.gif)

## Getting Started

These instructions will get you a copy of the project and it's dependencies. As well as how to run it on your local system.

### Prerequisites

You will need to install:

* [Git](https://git-scm.com/downloads)
* [Python 3.6+](https://www.python.org/downloads/)

For linux:
```
sudo apt install python3-pip (If You don't have pip installed)

pip3 install pyopengl

sudo apt-get install freeglut3-dev
```

For windows:

Download [PyOpenGL Windows](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl)

And then:
```
pip install path-to-the-whl-file-that-you-downloaded
```

### Installing

Clone the repository:

```
git clone https://github.com/MatheusBurda/BallCollision.git

cd BallCollision
```

## Running the tests

On the beggining of the BallCollision.py file you will find multiple defines
```
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
```
You can change them as you wish, then save the file and run
```
pyhton3 BallCollision.py
```
For windows:
```
py BallCollision.py
```

A window should pop up with the simulation.

To stop the simulation just close the window.

## Authors

* **[Matheus Burda](https://github.com/MatheusBurda)** - *start to end* 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details