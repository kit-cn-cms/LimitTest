import copy

#set up everything here

OutputDir='/nfs/dust/cms/user/shwillia/BoostedTTHScripts/LimitTest/LimitTestParallel/output/'

DoParallel=True

DoDatacards=True
DoCalculations=True
DoOutputParsing=True

DoLimits=True
DoMLFits=True

inputDir='/nfs/dust/cms/user/shwillia/BoostedTTHScripts/LimitTest/LimitTestParallel/datacards'

nominalcats=[
              'ttH_hbb_13TeV_dl_3j2t='+inputDir+'/ttH_hbb_13TeV_dl_3j2t.txt',#0
              'ttH_hbb_13TeV_dl_3j3t='+inputDir+'/ttH_hbb_13TeV_dl_3j3t.txt',#1
              'ttH_hbb_13TeV_dl_ge4j2t='+inputDir+'/ttH_hbb_13TeV_dl_ge4j2t.txt',#2
              'ttH_hbb_13TeV_dl_ge4j3t='+inputDir+'/ttH_hbb_13TeV_dl_ge4j3t.txt',#3
              'ttH_hbb_13TeV_dl_ge4jge4t='+inputDir+'/ttH_hbb_13TeV_dl_ge4jge4t.txt',#4
              'ttH_hbb_13TeV_sl_4j3t='+inputDir+'/ttH_hbb_13TeV_sl_j4_t3.txt',#5
              'ttH_hbb_13TeV_sl_4j4t_high='+inputDir+'/ttH_hbb_13TeV_sl_j4_t4_high.txt',#6
              'ttH_hbb_13TeV_sl_4j4t_low='+inputDir+'/ttH_hbb_13TeV_sl_j4_t4_low.txt',#7
              'ttH_hbb_13TeV_sl_5j3t='+inputDir+'/ttH_hbb_13TeV_sl_j5_t3.txt',#8
              'ttH_hbb_13TeV_sl_5jge4t_high='+inputDir+'/ttH_hbb_13TeV_sl_j5_tge4_high.txt',#9
              'ttH_hbb_13TeV_sl_5jge4t_low='+inputDir+'/ttH_hbb_13TeV_sl_j5_tge4_low.txt',#10
              'ttH_hbb_13TeV_sl_ge6j2t='+inputDir+'/ttH_hbb_13TeV_sl_jge6_t2.txt',#11
              'ttH_hbb_13TeV_sl_ge6j3t='+inputDir+'/ttH_hbb_13TeV_sl_jge6_t3.txt',#12
              'ttH_hbb_13TeV_sl_ge6jge4t_high='+inputDir+'/ttH_hbb_13TeV_sl_jge6_tge4_high.txt',#13
              'ttH_hbb_13TeV_sl_ge6jge4t_low='+inputDir+'/ttH_hbb_13TeV_sl_jge6_tge4_low.txt',#14
              'ttH_hbb_13TeV_sl_boosted='+inputDir+'/ttH_hbb_13TeV_sl_boosted.txt'#15
            ]

reducedCats=[]
for icat,cat in enumerate(nominalcats):
  reducedCats.append(copy.deepcopy(nominalcats))
  reducedCats[-1].pop(icat)

Scenarios=[ 
            ('nominal',nominalcats,[]),
            ('sl',nominalcats[5:],[]),
            ('dl',nominalcats[:5],[])
]
