import sys
import ROOT
from ROOT import TFile
import math
from math import *
import uproot

import PloFitter # my own module, which derives histograms and statistics

input_folder = "/mnt/scratch1/novotnyp/data/"
input_PbPbdata = "user.mrybar.PbPb_MC_ForPatrik_r002_ANALYSIS.root"
input_ppdata = "user.mrybar.pp_MC_ForPatrik_r002_ANALYSIS.root"
preselected_PbPbdata = ""
preselected_ppdata = ""
treeName = "AntiKt4HI"
output_folder = "/mnt/scratch1/novotnyp/results/"
run_number = 0

doCompile = True # flag variable declaring, which macros should be compiled and which not
doSelection = True # flag specifying whether to do a new selection or use preprocessed pp and PbPb data
doML = False # flag specifying, wherther ML learining and testing should be done

if __name__ == '__main__':
#Initialization

	f=open("run_"+str(run_number)+".txt","w+")
	f.write("Run number "+str(run_number)+" file: \n")

	print ("Headers declaration...")
	ROOT.gInterpreter.Declare('#include "Selection.h"')

	f.write("doCompile flag set to "+str(doCompile)+"\n")
	if doCompile:
		print ("Macros compiling...")
		ROOT.gSystem.CompileMacro("Selection.c")
	else:
		print ("Macros loaded as compiled")
		ROOT.gSystem.CompileMacro("Selection_c.so")

	f.write("doSelection flag set to "+str(doSelection)+"\n")
	if doSelection:
		from ROOT import Selection

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

	else: 
		pp_selected = uproot.open(preselected_ppdata)[treeName]
		PbPb_selected = uproot.open(preselected_PbPbdata)[treeName]

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
