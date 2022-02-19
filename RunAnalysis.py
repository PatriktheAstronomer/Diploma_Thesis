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
preselected_PbPbdata = "PbPb_test_2.root"
preselected_ppdata = "pp_test_0.root"
treeName = "AntiKt4HI"
output_folder = "/mnt/scratch1/novotnyp/results/"
run_number = 5

doCompile = False # flag variable declaring, which macros should be compiled and which not
doSelection = False # flag specifying whether to do a new selection or use preprocessed pp and PbPb data
calculateStats = True # flag specifying whether to do calculate statistical quantities or not
doML = False # flag specifying, wherther ML learining and testing should be done

if __name__ == '__main__':
#Initialization

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
		PbPb_selection = Selection(input_folder+input_PbPbdata, treeName, "PbPb")
	
		pp_selection.SetBranchAddress()
		PbPb_selection.SetBranchAddress()
		
		pp_selection.BookHistograms()
		PbPb_selection.BookHistograms()

		pp_selection.EventLoop()                  
		PbPb_selection.EventLoop()

		pp_selection.Write(output_folder+"pp_test_0")
		PbPb_selection.Write(output_folder+"PbPb_test_0")


# Statitics
	f.write("calculateStats flag set to "+str(calculateStats)+"\n")
	if calculateStats:

# Correlation matrix and JES/JER production
		GenerateCorrMatrices(output_folder, "PbPb_test_0.root", output_folder)
		GenerateCorrMatrices(output_folder, "pp_test_0.root", output_folder)	
	
# Machine learning part, creation of scalar training dataset ----> via a function in preselection??			
	f.write("doML flag set to "+str(doML)+"\n")
	if doML:
		with uproot.open(input_folder+input_ppdata) as pp_data:
			for key in pp_data:
				print(np.asarray(pp_data[key].values()))

	#ML-training on the pp_training
	# KERAS, budeme pocitat na GPU farme CERNu	

	# bude potreba skalarni vstup
	# Zde bude dulezita aplikace nastavenych parametru NN

	#ML-used on PbPb data
	# Udelam si kopii daneho pole, vyprazdnim ho a pak pres kazdy vstup ziskam pres NN vytup, ten plnim
	# mozne vyuzity kodu od Jennifer

#Correlation test in repaired PbPb data
	# Vypocet JES a JER map opravena data 
	# vyplotim si pres sebe Gaussiany (logaritmicke) oproti raw selekci ---> funkce compare datafiles!
	# porovnavat numericke vysledky pro ruzna run_numbers... Statistika, jak se zlepsuje performance site
	# ROC curve
