# <img src="docs/videos/load_anim.gif" width="50" align="center" style="padding-bottom: 8px"/> SMO AutoSplit

Neural network based auto splitter for Super Mario Odyssey.

<img src="docs/videos/application_demo.gif" width="800" align="center"/>

## Table of Contents
- [ SMO AutoSplit](#-smo-autosplit)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Compatibility](#compatibility)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Pre-Built](#pre-built)
    - [From source](#from-source)
  - [Getting started](#getting-started)
  - [Split types](#split-types)
  - [Troubleshooting](#troubleshooting)
  - [Credits](#credits)
  - [Author](#author)

## Features
**Minimal setup required:** There's no need to create split images like with [AutoSplit](https://github.com/Toufool/Auto-Split). All split types are ready to use without any setup.

**Capture OBS sources through virtual cam:** The auto splitter captures the game screen directly from a video source, like a capture card or an OBS virtual cam. Therefore you don't need to open a preview window to capture from.

**Start timer automatically:** The timer can be started manually or automatically either when starting a new game or when setting the time and date (for DSTA).

**Split on all moon types:** The auto splitter can detect a normal moon get, a story moon get and a multi moon get.

**Split on kingdom end:** The auto splitter can detect all kingdom ends, such as cap, cascade, lost and even moon.

**Split on various fadeouts:** The auto splitter can detect fadeouts such as cutscene skips, fade to black, subarea entry / exit and world map fadeouts.

**Automatic updates:** The application automatically checks if there is a new version available and downloads / installs patches once it is closed.

## Compatibility
Tested on **Windows 10** with **AverMedia Live Gamer 4k** capture card

Compatible python versions: **3.7**, **3.8**, **3.9**<br/>
Incompatible python versions: **2.X**, **3.10**

## Requirements
Your capture card should be able to output a 60FPS video stream with a resolution of at least 854x480p. The video can be uncompressed or compressed (tested with YouTube video).

## Installation
### Pre-Built
You can download the latest version [here](https://github.com/LordAsdi/SMO_AutoSplit/releases/latest). For older versions, check the [releases page](https://github.com/LordAsdi/SMO_AutoSplit/releases).<br/>
Once downloaded, unzip the file and start **SMO AutoSplit.exe**.<br/>
To set up OBS virtual cam and livesplit server, see the [getting started page](https://lordasdi.github.io/SMO_AutoSplit/getting_started.html) on the website.

### From source
Download and unzip the source code.<br/>
It is recommended to create a virtual environment before installing dependencies.<br/>
Run `pip install -r requirements.txt` to install all dependencies.<br/>
Run `python SMO_AutoSplit.py` to start the application.<br/>
To build an executable, first change the `hookspath` in `win.spec` to match your environment.<br/>
Run `pyinstaller -y win.spec` to start the build process. The executable will be located inside the `dist/win` directory.

## Getting started
Check out the [getting started page](https://lordasdi.github.io/SMO_AutoSplit/getting_started.html) on the website.

## Split types
|**Moon get** <br/> <img width=249 src="docs/videos/moon.gif"/>|**Storymoon get** <br/> <img width=249 src="docs/videos/moon story.gif"/>|**Multimoon get** <br/> <img width=249 src="docs/videos/moon multi.gif"/>|
|-|-|-|
|**Cap kingdom end** <br/> <img width=249 src="docs/videos/kingdom cap.gif"/>|**Kingdom end** <br/> <img width=249 src="docs/videos/kingdom odyssey.gif"/>|**Moon kingdom end** <br/> <img width=249 src="docs/videos/kingdom moon.gif"/>|
|**Odyssey banner** <br/> <img width=249 src="docs/videos/odyssey.gif"/>|**World map fadeout** <br/> <img width=249 src="docs/videos/world map.gif"/>|**Cutscene skip** <br/> <img width=249 src="docs/videos/cutscene.gif"/>|
|**Black screen** <br/> <img width=249 src="docs/videos/black screen.gif"/>|**White screen** <br/> <img width=249 src="docs/videos/white screen.gif"/>|**Subarea fadeout** <br/> <img width=249 src="docs/videos/subarea.gif"/>|
|**Compass disappear** <br/> <img width=249 src="docs/videos/compass.gif"/>|||

## Troubleshooting
If you have problems with the auto splitter, check out the [faq section](https://lordasdi.github.io/SMO_AutoSplit/faq.html) on the website. Otherwise you can join the official [discord server](https://discord.gg/tuXWe4S7r2) to ask for help or [open an issue](https://github.com/LordAsdi/SMO_AutoSplit/issues) on GitHub.

The application log file can be found in `C:/Users/User/AppData/Local/Lord Asdi/SMO AutoSplit/application.log`

## Credits
[AutoSplit64](https://github.com/Kainev/AutoSplit64) and [Star Classifier For Mario 64](https://github.com/gcervantes8/Star-Classifier-For-Mario-64) for inspiring this project.

[Simple PySide Base](https://github.com/Wanderson-Magalhaes/Simple_PySide_Base) for the GUI base.

[PyUpdater](https://github.com/Digital-Sapphire/PyUpdater) for automatic updates.

## Author
Lord Asdi
