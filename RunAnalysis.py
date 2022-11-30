import sys
import ROOT
from ROOT import TFile
import math
from math import *
import uproot
import numpy as np
import matplotlib.pyplot as plt
from Process_data_simplified import *
from ML_processing import *

input_folder = "/mnt/scratch1/novotnyp/data/"
input_PbPbdata = "user.mrybar.PbPb_MC_ForPatrik_r004_ANALYSIS.root"
input_ppdata="user.mrybar.pp_MC_P8_ForPatrik_r004_deriv_ANALYSIS.root"

#"user.mrybar.pp_MC_ForPatrik_r002_ANALYSIS.root"
#"user.mrybar.pp_MC_H7_ForPatrik_r004_deriv_ANALYSIS.root"
#"user.mrybar.PbPb_MC_ForPatrik_r002_ANALYSIS.root"

preselected_PbPbdata = {"PbPb_preselection"}
#preselected_ppdata = {"pp_inclusive_quark_P8", "pp_gluon_P8"}
#preselected_ppdata = {"P8_quark_u", "P8_quark_d", "P8_quark_s", "P8_quark_c", "P8_quark_b", "P8_gluon"}
preselected_ppdata = {"pp_inclusive_quark_P8_log_bins", "pp_gluon_P8_log_bins"}

treeName = "AntiKt4HI"
output_folder = "/mnt/scratch1/novotnyp/results/"
run_number = 29112022

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
		
		"""
                # FORM SCALAR SAMPLE
		pp_selection = Selection(input_folder+input_ppdata, treeName, "pp")
		pp_selection.FormScalarSample("/mnt/scratch1/novotnyp/data/trainingSampleScalar_"+str(run_number)+".root")
		pp_selection.SetBranchAddress()
		pp_selection.FormTrainingSample()
		pp_selection.Write()
		"""

                # pp SELECTION
		pp_selection = Selection(input_folder+input_ppdata, treeName, "pp")
		pp_selection.SetBranchAddress()
		pp_selection.BookHistograms()
		pp_selection.EventLoop()
		pp_selection.Write(output_folder+"pp_gluon_P8_log_bins")

		"""
		# pp CALCULATE RMSE
		pp_selection = Selection(input_folder+input_ppdata, treeName, "pp")
		pp_selection.SetBranchAddress()
		pp_selection.CalcRMSE()
		"""

		"""
		# PbPb SELECTION
		PbPb_selection = Selection(input_folder+input_PbPbdata, treeName, "PbPb")
		PbPb_selection.SetBranchAddress()
                PbPb_selection.BookHistograms()
                PbPb_selection.EventLoop()
                PbPb_selection.Write(output_folder+"PbPb_preselection")
		"""	
		
		"""
		# PbPb CALCULATE RMSE		
                PbPb_selection = Selection(input_folder+input_PbPbdata, treeName, "PbPb")
                PbPb_selection.SetBranchAddress()
		PbPb_selection.CalcRMSE()
		"""

# Statistics
	f.write("calculateStats flag set to "+str(calculateStats)+"\n")
	if calculateStats:

# Correlation matrix and JES/JER production
		#GenerateJERS(output_folder, preselected_ppdata, output_folder)
		# JES/JER can be produced for more datasamples, corrmatrices only for a certain one
		#GenerateCorrMatrices(output_folder, preselected_PbPbdata, output_folder)
		GenerateCorrMatrices(output_folder, preselected_ppdata, output_folder)	


### TOHLE NIZ NAS NEZAJIMA ZATIM:
# Machine learning part			
	f.write("Machine learning \n")
	print("Doing ML learning")

	# nejprve napocitat pro kazdy PbPb sample RMSE, pak pro každý sample podle centrality !


	# pro PbPb data
	# zavolam si selection::eventloop ovsem tentokrat s argument navic repair_data... if repair_data == true & type == "PbPb", tak budu jedno po druhém data opravovat a plnit příslušné histogramy... na vzniklý data file pak proste už zvaolám klasické metody modulu GenerateCorrMatrices

#Correlation test in repaired PbPb data
	# vyplotim si pres sebe Gaussiany (logaritmicke) oproti raw selekci ---> funkce compare datafiles!
	# porovnavat numericke vysledky pro ruzna run_numbers... Statistika, jak se zlepsuje performance site
	# ROC curve a integral z nej
