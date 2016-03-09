import sys

currentPath = "/nfs/dust/cms/user/shwillia/BoostedTTHScripts/LimitTest/LimitTestParallel/"

sys.path.append(currentPath)

from LimitTestManager import LimitTestManager

print 'YEEHAAA!'

LimitTest=LimitTestManager(currentPath)
LimitTest.CalculationsParallel()
