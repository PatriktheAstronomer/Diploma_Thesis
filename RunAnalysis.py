import sys
import ROOT
from ROOT import TFile
import math
from math import *
import sklearn
import uproot
import numpy as np
import matplotlib.pyplot as plt
from Process_data_simplified import *
from ML_processing import *

input_folder = "/mnt/scratch1/novotnyp/data/"
input_PbPbdata = "user.mrybar.PbPb_MC_ForPatrik_r004_ANALYSIS.root"

#input_PbPbdata = "PbPb_cleaned.root"
# repaired/PbPb_repaired_RR2.root

input_ppdata = "user.mrybar.pp_MC_P8_ForPatrik_r004_deriv_ANALYSIS.root"

#"user.mrybar.pp_MC_ForPatrik_r002_ANALYSIS.root"
#"user.mrybar.pp_MC_H7_ForPatrik_r004_deriv_ANALYSIS.root"
#"user.mrybar.PbPb_MC_ForPatrik_r002_ANALYSIS.root"

preselected_PbPbdata = {"PbPb_preselection"}
#preselected_ppdata = {"pp_inclusive_quark_P8", "pp_gluon_P8"}
#preselected_ppdata = {"P8_quark_u", "P8_quark_d", "P8_quark_s", "P8_quark_c", "P8_quark_b", "P8_gluon"}
preselected_ppdata = {"pp_inclusive_quark_P8_log_bins", "pp_gluon_P8_log_bins"}

treeName = "AntiKt4HI"
output_folder = "/mnt/scratch1/novotnyp/results/"
run_number = 7122022

doCompile = True # flag variable declaring, which macros should be compiled and which not
doSelection = True # flag specifying whether to do a new selection or use preprocessed pp and PbPb data
calculateStats = False # flag specifying whether to do calculate statistical quantities or not
doML_training = False # flag specifying, whether ML training (on pp samples) should be done
doML_testing = False # flag specifying, whether ML testing (on PbPb samples) should be done

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
		pp_selection.FormScalarSample("/mnt/scratch1/novotnyp/data/pp_class_train_extended_geo_2_abs_eta.root")
		pp_selection.SetBranchAddress()
		pp_selection.FormTrainingSample()
		pp_selection.Write()
		"""
		"""
                # pp SELECTION
		pp_selection = Selection(input_folder+input_ppdata, treeName, "pp")
		pp_selection.SetBranchAddress()
		pp_selection.BookHistograms()
		pp_selection.EventLoop()
		pp_selection.Write(output_folder+"pp_test")
		"""
	
		"""
		# pp CALCULATE RMSE
		pp_selection = Selection(input_folder+input_ppdata, treeName, "pp")
		pp_selection.SetBranchAddress()
		pp_selection.CalcRMSE()
		"""
		
		# PbPb SELECTION
		PbPb_selection = Selection(input_folder+input_PbPbdata, treeName, "PbPb")
		PbPb_selection.SetBranchAddress()
		PbPb_selection.BookHistograms()
		PbPb_selection.EventLoop(10000)
		PbPb_selection.Write(output_folder+"PbPb_preselection")			
		
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


# Machine learning part			
	if doML_training:
		f.write("Machine training \n")
		print("Doing ML training")
		tree = "training_dataset"
		source = input_folder + "HyPe_train.root"  #"trainingSampleScalar_4122022.root"

		list_of_input_branches = ["jet_eta_scalar", "jet_pt_scalar", "jet_ntrk_scalar", "jet_N90_scalar"] #, "jet_rtrk_scalar"]
		target_branch = "jet_response_scalar" # "truth_jet_pt_scalar"
		dataset, target_regress, mc_weights = read_scalar_datafile(source, tree, list_of_input_branches, target_branch, True)

		list_of_input_branches = []
		target_branch = "truth_jet_flavor_scalar"
		_, target_class, _ = read_scalar_datafile(source, tree, list_of_input_branches, target_branch) 

		outdir = output_folder+"model/"
		model_training(dataset, target_regress, mc_weights, outdir, "HIST_0", "regressor")

	if doML_testing:
		outdir = output_folder+"model/"
		input_PbPbdata = "PbPb_cleaned.root"
		list_of_input_branches = ["jet_eta", "jet_pt", "jet_ntrk", "jet_N90", "jet_SumPtTrk"]
		predict(input_folder, input_PbPbdata,  outdir, "imbalanced_Forest_class_Py", list_of_input_branches, "classifier")

# ROC curve a integral z nej -> zajimave pro klasifikaci ?
