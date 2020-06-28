# ROKBOT
Rise of Kingdoms Farming bot

## Requirements

- ADB
- Python
- Imports: ppadb, PIL, numpy (PIP install these)

## How does this work?
- Only searches for barbarians, and heal army as soon as they lose a battle;
- To choose a barbarian level, search manually for one, selecting the barb's level you want the bot to farm;
- The bot will chose the army you saved on the 4th army slot ![Select 4th slot](https://image.prntscr.com/image/8Y7qyWjXSdS-0BE36PPQaw.png)
- DOES NOT GO TROUGH THE CAPTCHA;
- This bot has been tested on BlueStacks, on a 1920x1080 screen;
- To run, double-click the batch file
- Configure your file locations in the batch file
- configure your email settings in sendEmail()s

## Troubleshooting
- Check for the kind of error on the prompt;
- You may need to set up de ADB, IDK;

## WARNING
- I don't know if you can be banned by using this, so use it at  your own risk.

## TODO
- Dynamic army selection;
- Dynamic button selection: - PARTIALLY DONE
  - Be able to change the emulator's resolution;
  - Change from fixed pixel position to percentage position; - PARTIALLY DONE
- Notification when CAPTCHA pops up; - DONE
- RSS farming bot;
