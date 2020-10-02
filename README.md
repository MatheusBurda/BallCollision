# Ball Collision

This project simulates a 3D elastic collision between balls inside a closed box conserving the kinetic energy.

![BallCollision](/Extras/BallCollision2.gif)

## Getting Started

These instructions will get you a copy of the project and it's dependencies. As well as how to run it on your local system.

### Prerequisites

You will need to install:

* [Git](https://git-scm.com/downloads)
* [Python 3.6+](https://www.python.org/downloads/)
* PyOpenGL

For Linux:
```
sudo apt install python3-pip (If You don't have pip installed)

pip3 install pyopengl

sudo apt-get install freeglut3-dev
```

For Windows:

Download [PyOpenGL Windows](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl)

And then:
```
pip install path-to-the-whl-file-that-you-downloaded
```

### Installing

Clone the repository:

```
git clone https://github.com/MatheusBurda/BallCollision.git
```

## Running the tests

Linux:
```
pyhton3 BallCollision.py
```
Windows:
```
py BallCollision.py
```

Optional arguments:
```
usage: BallCollision.py [-h] [--width WIDTH] [--height HEIGHT]
                        [-n NUM_BALLS] [-r RADIUS] [-v MAX_VELOCITY]
                        [--no-color] [-s SIZE]

optional arguments:
  -h, --help            show this help message and exit
  --width WIDTH         screen width. Defaults to 800
  --height HEIGHT       screen height. Defaults to 600
  -n NUM_BALLS, --num-balls NUM_BALLS
                        amount of balls used in the simulation. Defaults to 15
  -r RADIUS, --radius RADIUS
                        radius of balls. Defaults to 0.45
  -v MAX_VELOCITY, --max-velocity MAX_VELOCITY
                        max velocity allowed. Defaults to 0.005
  --no-color            toggle colored balls off
  -s SIZE, --size SIZE  size of the cube that contains the balls. Defaults to 2
```

A window should pop up with the simulation.

To stop the simulation just close the window.

## Authors

* **[Matheus Burda](https://github.com/MatheusBurda)** - *start to end* 
* **[Vinícius Couto](https://github.com/vcoutasso)** - *FPS counter and argument parser* 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
