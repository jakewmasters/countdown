# countdown

A simple countdown timer built with Tkinter. 

## Overview

This project was heavily inspired by [Tkinter By Example](https://github.com/Dvlv/Tkinter-By-Example). 

I wrote this program in order to learn more about GUI programming. 

At a high level, the program instantiates a Tkinter class that serves as the main GUI. 
It then spawns a worker thread which renders the remaining time in the background. 
I added some validation code to ensure valid timestamps. 

Despite the code being a bit messy, it (probably) shouldn't break if you download it and run it with `$ python countdown.py`. 