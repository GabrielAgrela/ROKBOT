@ECHO ON
"C:\Users\Geremias\Desktop\platform-tools\adb.exe" kill-server
"C:\Users\Geremias\Desktop\platform-tools\adb.exe" connect localhost:21503
cd C:\Users\Geremias\github\ROKBOT
python rok.py
PAUSE
