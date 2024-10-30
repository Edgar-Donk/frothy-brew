import subprocess
import re

def getScreenDimensions():
    xrandrOutput = str(subprocess.Popen(['xrandr'], stdout=subprocess.PIPE).communicate()[0])
    matchObj = re.findall(r'current\s(\d+) x (\d+)', xrandrOutput)
    if matchObj:
        return (int(matchObj[0][0]), int(matchObj[0][1]))

screenWidth, screenHeight = getScreenDimensions()
print(f'{screenWidth} x {screenHeight}')