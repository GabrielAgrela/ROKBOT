# ROKBOT
Rise of Kingdoms multi-functionalities bot

## Requirements
- ADB
- Python
- Install with pip necessary imports
- Enable adb on your device (even on emulators)
- install tesseract and change to your path inside rok.py (follow AllTech's tutorial: https://youtu.be/4DrCIVS5U3Y)

## What it does  
- Does the Clarion Call challenge;
- Farms for you;
- Only searches for barbarians, and heal army as soon as they lose a battle:<img src="/media/defeatExample.gif?raw=true" width="800px">
- Choose the level you want ROKBOT to farm:<img src="/media/victoryExample.gif?raw=true" width="800px">
- The bot will choose the army you saved on the 4th army slot: <img src="/media/chooseArmyExample.png?raw=true" width="800px">
- Does the lyceum challenge for you (last update, rokbot has a 30/30 correct answers): <img src="/media/lyceumExample.gif?raw=true" width="800px">
- Sends an email when there's a CAPTCHA or when you are out of AP;
- When an ally asks for help, ROKBOT automatically taps the notification (while farming only);

## How it works

- Clarion Call bot: choose the level (in game slider) of the barbarians you wish to farm (most efficient is the max level you can win in a single battle), tap out, click the clarion call button
- Farming RSS bot: click the button when you are in the map view, choose the level before clicking the button;
- Farming Barbarians bot: click the button and attack manually one barbarian with the level you wish to farm;
- Lyceum bot: choose either the preliminary or the midterm/finals as soon as you start the challenge, click it again for the next question and so on;

## Configurations
- This bot has been tested on BlueStacks, 1920x1080 320dpi (many functions will not work if this dpi value isn't met, resolution can be changed in the code tho');
- Configure your email settings in sendEmail();
- Configure your file locations in the batch file;
- To run, double-click the batch file;

## Useful info
- DOES NOT GO TROUGH THE CAPTCHA;
- BEEP DEBUG SYSTEM:
	- beep = help pressed
	- boop = 1st attack
	- boop boop = new Attack
	- boop beep = healing
	- beep boop beep = sending email

## Troubleshooting
- Check for the kind of error on the prompt;
- You may need to set up the ADB, IDK;

## WARNING
- I don't know if you can be banned by using this, so use it at  your own risk.

## TODO
- Dynamic army selection;
- Dynamic button selection: - DONE
  - Be able to change the emulator's resolution; - DONE
  - Change from fixed pixel position to percentage position; - DONE
- Notification when CAPTCHA pops up; - DONE
- RSS farming bot: - DONE
	- Select gatherers (1 to 4 army slots);
	- Select level of the RSS deposit;
- Graphical interface;
- Update README with farm functionality example;
- Update README with lyceum functionality example; - DONE
