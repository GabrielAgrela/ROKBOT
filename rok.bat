@ECHO ON
"C:\Users\Geremias\Desktop\platform-tools\adb.exe" kill-server
"C:\Users\Geremias\Desktop\platform-tools\adb.exe" -s emulator-5554 shell input touchscreen swipe 50 820 50 820 200
cd C:\Users\Geremias\github\ROKBOT
python rok.py
PAUSE
