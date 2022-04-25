import sys
import ROOT
from ROOT import TFile
import math
from math import *
import uproot
import numpy as np
#import pandas as pd
from matplotlib import pyplot as plt
from Process_histos import *

input_folder = "/mnt/scratch1/novotnyp/data/"
input_PbPbdata = "user.mrybar.PbPb_MC_ForPatrik_r002_ANALYSIS.root"
input_ppdata = "user.mrybar.pp_MC_ForPatrik_r002_ANALYSIS.root"
preselected_PbPbdata = {"PbPb_7"}
preselected_ppdata = {"pp_u_quark", "pp_d_quark", "pp_s_quark", "pp_gluon"}
treeName = "AntiKt4HI"
output_folder = "/mnt/scratch1/novotnyp/results/"
run_number = 8

doCompile = True # flag variable declaring, which macros should be compiled and which not
doSelection = False # flag specifying whether to do a new selection or use preprocessed pp and PbPb data
calculateStats = True # flag specifying whether to do calculate statistical quantities or not
doML = False # flag specifying, wherther ML learining and testing should be done

if __name__ == '__main__':
#Initialization
	ROOT.gErrorIgnoreLevel = 3000 # Only error messages in ROOT

	f=open(output_folder+"run_"+str(run_number)+".txt","w+")
	f.write("Run number "+str(run_number)+" file: \n")

	print ("Headers declaration...")
	ROOT.gInterpreter.Declare('#include "Selection.h"')
	ROOT.gInterpreter.Declare('#include "Variables.h"')

	f.write("doCompile flag set to "+str(doCompile)+"\n")
	if doCompile:
		print ("Macros compiling...")
		ROOT.gSystem.CompileMacro("Selection.c")
		ROOT.gSystem.CompileMacro("Variables.c")
	else:
		print ("Macros loaded as compiled")
		ROOT.gSystem.Load("Selection_c.so")
		ROOT.gSystem.Load("Variables_c.so")

	f.write("doSelection flag set to "+str(doSelection)+"\n")
	if doSelection:
		from ROOT import Selection
		from ROOT import Variables
		
		pp_selection = Selection(input_folder+input_ppdata, treeName, "pp")
		pp_selection.FormScalarSample("/mnt/scratch1/novotnyp/data/trainingSampleScalar_"+str(run_number)+".root")
		PbPb_selection = Selection(input_folder+input_PbPbdata, treeName, "PbPb")

		# veto method will be added in the future ---> It will create vars and vetos from configure file
	
		pp_selection.SetBranchAddress()
		PbPb_selection.SetBranchAddress()
	
		pp_selection.BookHistograms()
		PbPb_selection.BookHistograms()

		pp_selection.EventLoop()                  
		PbPb_selection.EventLoop()

		pp_selection.Write(output_folder+"pp_gluon")
		PbPb_selection.Write(output_folder+"PbPb_"+str(run_number))

# Statitics
	f.write("calculateStats flag set to "+str(calculateStats)+"\n")
	if calculateStats:

# Correlation matrix and JES/JER production
                # JES/JER can be produced for more datasamples, corrmatrices only for	a certain one
		#GenerateCorrMatrices(output_folder, preselected_PbPbdata, output_folder)
		GenerateCorrMatrices(output_folder, preselected_ppdata, output_folder)	

# Machine learning part			
	f.write("doML flag set to "+str(doML)+"\n")
	if doML:
		with uproot.open(input_folder+input_ppdata) as pp_data:
			for key in pp_data:
				print(np.asarray(pp_data[key].values()))
	# read pp_scalar_sample input...

	#ML-training on the pp_training
	# KERAS, budeme pocitat na GPU farme CERNu	


	# pro PbPb data
	# zavolam si selection::eventloop ovsem tentokrat s argument navic repair_data... if repair_data == true & type == "PbPb", tak budu jedno po druhém data opravovat a plnit příslušné histogramy... na vzniklý data file pak proste už zvaolám klasické metody modulu GenerateCorrMatrices

#Correlation test in repaired PbPb data
	# vyplotim si pres sebe Gaussiany (logaritmicke) oproti raw selekci ---> funkce compare datafiles!
	# porovnavat numericke vysledky pro ruzna run_numbers... Statistika, jak se zlepsuje performance site
	# ROC curve a integral z nej -> snad bude mit implementovane v sobe KERAS
