# MazeGenerator


![](https://github.com/ransaked1/HangMan/blob/master/MazeMaker.png)

## Getting Started

### Prerequisites

Make sure you have python3 installed:
```
sudo apt-get install python3
```

To install PyQt5 type:
```
sudo apt-get install python3-pyqt5
sudo apt-get install pyqt5-dev-tools
sudo apt-get install qttools5-dev-tools
```

## Running the program
In root folder run:
```
python3 mazemaker.py
```

### Potential Issues
* PyQt5 uses the X11 server for display. If you are running the app on a Windows 10 Ubuntu Subsystem, you will need to download and setup Xming in Windows: https://xming.en.softonic.com/. Then export the window path in your Ubuntu environment and run the game:
```
export DISPLAY=:0.0
```
* If the game won't open on your Linux or MacOS machine you may be missing the X11 server packages. You can download them by typing:
```
sudo apt-get install xorg openbox
```
And export the windows path:
```
export DISPLAY=:0.0
```

## Built With
* [PyQt5](https://pypi.org/project/PyQt5/) - Cross-platform GUI
