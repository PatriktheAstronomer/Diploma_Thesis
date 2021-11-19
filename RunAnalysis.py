import sys
import ROOT
from ROOT import TFile
import math
from math import *
import uproot
import numpy as np
from matplotlib import pyplot as plt

input_folder = "/mnt/scratch1/novotnyp/data/"
input_PbPbdata = "user.mrybar.PbPb_MC_ForPatrik_r002_ANALYSIS.root"
input_ppdata = "user.mrybar.pp_MC_ForPatrik_r002_ANALYSIS.root"
preselected_PbPbdata = "PbPb_test_2.root"
preselected_ppdata = "pp_test_2.root"
treeName = "AntiKt4HI"
output_folder = "/mnt/scratch1/novotnyp/results/"
run_number = 2

doCompile = True # flag variable declaring, which macros should be compiled and which not
doSelection = True # flag specifying whether to do a new selection or use preprocessed pp and PbPb data
doML = False # flag specifying, wherther ML learining and testing should be done

if __name__ == '__main__':
#Initialization

	f=open("run_"+str(run_number)+".txt","w+")
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

		pp_selection.EventLoop(50000)                  
		PbPb_selection.EventLoop(50000)

		pp_selection.Write(output_folder+"pp_test_0")
		PbPb_selection.Write(output_folder+"PbPb_test_0")
#Statistics
#	with uproot.open(output_folder+preselected_PbPbdata) as PbPb_data:
#		for key in PbPb_data:
#			print(PbPb_data[key].values())

	# change structure after implementation of Variables class... then for each var, for each centrality prepare matrix var_val vs. pT
			
	f.write("doML flag set to "+str(doML)+"\n")

	#if doML:

	#ML-training on the pp_training
	
	# bude potreba skalarni vstup
	# Zde bude dulezita aplikace nastavenych parametru NN

	#ML-used on PbPb data
	# Udelam si kopii daneho pole, vyprazdnim ho a pak pres kazdy vstup ziskam pres NN vytup, ten plnim
	# mozne vyuzity kodu od Jennifer

#Correlation test in repaired PbPb data
	# Vypocet JES a JER map, pro neopravena i opravena data 
	# vyplotim si pres sebe Gaussiany (logaritmicke) oproti raw selekci
	# ! pokud je doML, tak volam porovnani,	jinak dostanu prazdny hist po oprave...
	# porovnavat numericke vysledky pro ruzna run_numbers...na to bude specialni fce...Compare done tests
