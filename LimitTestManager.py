import sys
import os
import stat
from subprocess import call
from subprocess import check_output
import ROOT
import copy
import time as timer
from QueHelper import QueHelper
import Definitions


class LimitTestManager:
  def __init__(self,currentPath):
    self.Path=currentPath
    self.Verbose=True
    
    self.OutputDir=Definitions.OutputDir
    if self.OutputDir[-1] != '/':
        self.OutputDir+='/'
        
    self.Scenarios=Definitions.Scenarios
    
    self.DoParallel=Definitions.DoParallel
    
    self.DoDatacards=Definitions.DoDatacards
    self.DoCalculations=Definitions.DoCalculations
    self.DoOutputParsing=Definitions.DoOutputParsing
    
    self.DoLimits=Definitions.DoLimits
    self.DoMLFits=Definitions.DoMLFits
    
    self.JobIDList=[]
    self.JobScriptList=[]
    self.QueHelper=""

    
  def CreateOutputPaths(self):
    if not os.path.exists(self.OutputDir):
      os.makedirs(self.OutputDir)
        
    print "output directory created"


  def SetQueHelper(self,quesystem):
    self.QueHelper=QueHelper(quesystem)


  def CreateDataCards(self):
    if not self.DoDatacards:
      return
      
    for name,cats,systs in self.Scenarios:

      if self.OutputDir[-1] != '/':
        self.OutputDir+='/'

      dummyname=self.OutputDir+'dummydatacard.txt'

      dummyfile=open(dummyname,'w')

      call(['combineCards.py']+cats, stdout=dummyfile)
      
      dummyfile.close()
      
      dummyfile=open(dummyname,'r')
      
      datacardname=self.OutputDir+'datacard_'+name+'.txt'
      datacardfile=open(datacardname,'w')
      
      for line in dummyfile:
        if line.split()[0] in systs:
          continue
        
        if line.split()[0] == 'kmax':
          splitline=line.split()
          splitline[1]=str(int(splitline[1])-len(systs))
          
          newline=''
          for word in splitline:
            newline+=word
            
            if word != splitline[-1]:
              newline+=' '
            else:
              newline+='\n'
          
          datacardfile.write(newline)
          continue          
          
        datacardfile.write(line)
      
      datacardfile.close() 
      dummyfile.close()


  def CalculationsParallel(self):
    isc = int(os.getenv('SCENARIO', '-1'))
    name = self.Scenarios[isc][0]
    
    datacardname=self.OutputDir+'datacard_'+name+'.txt'
    resultslimitname=self.OutputDir+'results_limit_'+name+'.txt'
    resultsmlfitname=self.OutputDir+'results_mlfit_'+name+'.txt'

    if self.DoLimits:
      resultslimitsfile=open(resultslimitname,'w')
      call(['combine','-M','Asymptotic',datacardname], stdout=resultslimitsfile)
      resultslimitsfile.close()

    if self.DoMLFits:
      resultsmlfitfile=open(resultsmlfitname,'w')
#      call(['combine','-M','MaxLikelihoodFit','--rMin','-10','--rMax','10','--minos','all','--plots',datacardname,'-n','_'+name], stdout=resultsmlfitfile)
#      call(['combine','-M','MaxLikelihoodFit','--rMin','-10','--rMax','10','--minos','all',datacardname,'-n','_'+name], stdout=resultsmlfitfile)
      call(['combine','-M','MaxLikelihoodFit','--rMin','-6','--rMax','6','--minos','all',datacardname,'-n','_'+name], stdout=resultsmlfitfile)
      resultsmlfitfile.close()

#      subprocess.call(['mv','*'+name+'*',self.OutputDir+"."])


  def Calculations(self):
    for name,cats,systs in self.Scenarios:

      datacardname=self.OutputDir+'datacard_'+name+'.txt'
      resultslimitname=self.OutputDir+'results_limit_'+name+'.txt'
      resultsmlfitname=self.OutputDir+'results_mlfit_'+name+'.txt'

      if self.DoLimits:
        resultslimitsfile=open(resultslimitname,'w')
        call(['combine','-M','Asymptotic',datacardname], stdout=resultslimitsfile)
        resultslimitsfile.close()

      if self.DoMLFits:
        resultsmlfitfile=open(resultsmlfitname,'w')
#        call(['combine','-M','MaxLikelihoodFit','--rMin','-10','--rMax','10','--minos','all','--plots',datacardname,'-n','_'+name], stdout=resultsmlfitfile)
        call(['combine','-M','MaxLikelihoodFit','--rMin','-6','--rMax','6','--minos','all','--plots',datacardname,'-n','_'+name], stdout=resultsmlfitfile)
        resultsmlfitfile.close()

#      subprocess.call(['mv','*'+name+'*',self.OutputDir+"."])


  def OutputParsing(self):
    
    calulatedLimitsObs=[]
    calulatedLimitsExp=[]
    
    if self.DoLimits:
      for name,cats,systs in self.Scenarios:

        resultslimitname=self.OutputDir+'results_limit_'+name+'.txt'

        resultslimitname=open(resultslimitname,'r')
        for line in resultslimitname:
          if 'Observed' in line:
            calulatedLimitsObs.append(float(line.split(' < ')[-1]))
          if 'Expected 50' in line:
            calulatedLimitsExp.append(float(line.split(' < ')[-1]))
        resultslimitname.close()

      finallimitresults=self.OutputDir+'finalresults_limit.txt'
      finallimitfile=open(finallimitresults,'w')

      for isc,(name,cats,systs) in enumerate(self.Scenarios):

        outstring=name+' expected: '

        outstring+=str(calulatedLimitsExp[isc])
        if isc > 0:
          outstring+='   ratio: {:06.4f}'.format((calulatedLimitsExp[isc]/calulatedLimitsExp[0])-1)
        
        outstring+='      observed: '
        outstring+=str(calulatedLimitsObs[isc])
        if isc > 0:
          outstring+='   ratio: {:06.4f}'.format((calulatedLimitsObs[isc]/calulatedLimitsObs[0])-1)
          
        outstring+='\n'

        finallimitfile.write(outstring)

      finallimitfile.close()

    if self.DoMLFits:
      finalmlfitresults=self.OutputDir+'finalresults_mlfit.txt'
      finalmlfitfile=open(finalmlfitresults,'w')

      for name,cats,systs in self.Scenarios:
        resultsmlfitname=self.OutputDir+'results_mlfit_'+name+'.txt'
        resultsmlfitfile=open(resultsmlfitname,'r')

        outstring=name+' '

        for line in resultsmlfitfile:
          if 'Best fit r:' in line:
            outstring+=line
            break

        finalmlfitfile.write(outstring)

        resultsmlfitfile.close()

      finalmlfitfile.close()


  def Run(self):
  
    self.CreateOutputPaths()
    
    if self.DoDatacards:
      self.CreateDataCards()
    
    if self.DoCalculations:
      if self.DoParallel:
        if not os.path.exists("PreparationScripts"):
          os.makedirs("PreparationScripts")

        mainrunline=self.QueHelper.GetRunLines()

        for isc,scenario in enumerate(self.Scenarios):
          joblines=[]
          jj=self.QueHelper.GetExecLines()
          for jjj in jj:
            joblines.append(jjj)
          joblines.append("cd "+self.Path+"\n")
          joblines.append("export SCENARIO="+str(isc)+"\n")
          joblines.append("python "+self.Path+"RunCalculations.py")

          outfile=open("PreparationScripts/"+scenario[0]+".sh","w")
          for line in joblines:
            outfile.write(line)
          outfile.close()
          st = os.stat("PreparationScripts/"+scenario[0]+".sh")
          os.chmod("PreparationScripts/"+scenario[0]+".sh", st.st_mode | stat.S_IEXEC)

          runlines=[]
          thisrl=mainrunline[0]
          runlines.append(thisrl)
          runlines[-1]=runlines[-1].replace("INSERTPATHHERE",self.Path)
          runlines[-1]=runlines[-1].replace("INSERTEXECSCRIPTHERE","PreparationScripts/"+scenario[0]+".sh")
          runfile=open("runPrep.sh","w")
          for rl in runlines:
            runfile.write(rl)
          runfile.close()
          st = os.stat("runPrep.sh")
          os.chmod("runPrep.sh", st.st_mode | stat.S_IEXEC)

          thisID=self.QueHelper.StartJob("./runPrep.sh")
          self.JobIDList.append(thisID)
          print "submitted ", "PreparationScripts/"+scenario[0]+".sh"

        #now check the que until its finished
        JobsStillRunning=True
        nJobsStillRunning=len(self.JobIDList)
        while(JobsStillRunning):
          timer.sleep(30)
          nJobsStillRunning=0
          for job in self.JobIDList:
            if self.QueHelper.GetIsJobRunning(job):
              nJobsStillRunning+=1
          if nJobsStillRunning>0:
            JobsStillRunning=True
          else:
            JobsStillRunning=False

          print nJobsStillRunning, " jobs still running"
    
      else:
        self.Calculations()

    if self.DoOutputParsing:
      self.OutputParsing()
