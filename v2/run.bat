@echo off
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Starting Intrusion Detection System...
python intrusion_detector.py

pause
