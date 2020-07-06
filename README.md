# ROKBOT
Rise of Kingdoms Farming bot

## Requirements

- ADB
- Python
- Imports: ppadb, PIL, numpy, yagmail (PIP install these)
- Enable adb on your device (even on emulators)

## What it does and how it works
- Only searches for barbarians, and heal army as soon as they lose a battle:<img src="/media/defeatExample.gif?raw=true" width="800px">
- To choose a barbarian level, search manually for one, selecting the barb's level you want the bot to farm:<img src="/media/victoryExample.gif?raw=true" width="800px">
- The bot will chose the army you saved on the 4th army slot: <img src="/media/chooseArmyExample.png?raw=true" width="800px">
- DOES NOT GO TROUGH THE CAPTCHA;
- This bot has been tested on BlueStacks, on a 1920x1080 screen;
- To run, double-click the batch file;
- Configure your file locations in the batch file;
- Configure your email settings in sendEmail();
- Sends an email when there's a CAPTCHA or when you are out of AP;
- When an ally asks for help, ROKBOT automatically taps the notification<
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
