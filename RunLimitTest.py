import sys

currentPath = "/nfs/dust/cms/user/shwillia/BoostedTTHScripts/LimitTest/LimitTestParallel/"

sys.path.append(currentPath)

from LimitTestManager import LimitTestManager

LimitTest=LimitTestManager(currentPath)
LimitTest.SetQueHelper('NAFSL6')
LimitTest.Run()
