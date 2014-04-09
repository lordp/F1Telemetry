F1Telemetry
===========

The code here is a basic live timing system for Codemasters F1 2013 racing game, used in conjunction with the Racing League Charts website - https://racingleaguecharts.com

## Requirements ##

You may need to install a C++ Redistributable from Microsoft. You can download this [here](https://www.microsoft.com/en-us/download/confirmation.aspx?id=29).

## Important ##

You will need to edit a file to get the game sending information out. The file is 

  C:\Users\username\Documents\my games\FormulaOne2013\hardwaresettings\hardware_settings_config.xml

and you need to look for a line near the bottom starts with "&lt;motion" and change it to the following

  &lt;motion enabled="true" ip="127.0.0.1" port="20777" delay="1" extradata="3" /&gt;

## How to use ##

1. Unzip to a convenient directory
2. Run racingleaguecharts.exe
