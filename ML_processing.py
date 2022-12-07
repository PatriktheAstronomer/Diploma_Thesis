import numpy as np
import uproot
import lzma
import os
import shutil
import pickle
import sys

import sklearn.model_selection
import sklearn.neural_network
import sklearn.pipeline


# we do not apply any cuts or vetos! we just do standardization and feature engineering

def read_scalar_datafile(source, tree, list_of_input_branches, target_branch):
	events = uproot.open(source+":"+tree)
	dataset = np.array([])
	for branch in list_of_input_branches:
		dataset = np.append(dataset, events[branch].array(library="np"))
	target = events[target_branch].array(library="np")
	return dataset, target
	# dataset and target arrays are used for training

# in various types of MLs ve perform and plot some kind of grid search

def model_training(dataset, target, outdir, model_name, type): 
	#x_train, x_test, t_train, t_test = sklearn.model_selection.train_test_split(dataset.T, target, test_size=0.9, random_state=42)
	#normalizer = sklearn.preprocessing.StandardScaler()
	# na zacatek muzu mit uplne noob site, ale je potřeba pak data správně škálovat
	# v diplomce ideálně tabulka typu, v druhe bude to same, ale misto RMSE tam bude accuracy
	# config	epochs	datasample_size	RMSE_per_each centrality and overall	

	if type == "regression":
		model = sklearn.neural_network.MLPRegressor(hidden_layer_sizes = (50, 500, ), max_iter=300) # later play with alpha
		model.fit(dataset.T, target)

	elif type == "classification":
		pass

	with lzma.open(outdir+model_name+".model", "wb") as model_file:
		pickle.dump(model, model_file)


	# sestavit model, zjednodusit vahy (asi neni nutne, dokud neni obludne velky), ulozit ho

	#musit to delat uz nacisto, tedy nacist si tady data a nacvicit nejaky model a ulozit ho -> MLP z week 4, BDT z week 10, na classifikaci kNN
	# pomoci splitu budu nejprve cvicit na velmi malych samplech... treba 1/1000, celych dat, pak na vetsich celcich

def predict(dir, source, outname, tree, list_of_input_branches, model_address):
	# works the same for regressors and classifier and any model in general
	with lzma.open(model_address, "rb") as model_file:
		model = pickle.load(model_file)
        
	shutil.copyfile(dir+source, dir+outname)
	events = uproot.open(dir+source+":"+tree) #input tree for reading

	for batch in events.iterate(step_size="200 kB", filter_name = list_of_input_branches, library = "pd"):
		print(len(batch.T))
		predictions = []
		for j in range(len(batch)): # batch is a group of j-matricies of i-jets time d-features 
			"""
			print(len(batch.T))
			event_predictions = []
			fol l in range(len(batch[1][j])):
				if batch[1][j][l] > 30: # place here later 0 GeV; eta is always the first one, pT the second one
					prediction = model.predict(batch[0][j][l], batch[1][j][l], batch[2][j][l], batch[3][j][l]) #set better here, later on
					event_predictions.append(prediction)	                

	        		else:
					predictions.append(dato[1][j][l]) // keep the same pT
			predictions.append(event_predictions)

			print(batch[1][j], "original")
			print(event_predictions, "repaired")
			"""
		

	# Selection::WriteInVal(prediction) // https://root.cern.ch/root/roottalk/roottalk01/0363.html vs. https://indico.cern.ch/event/840667/contributions/3527109/attachments/1908764/3153297/uproot-irisfellow-final.pdf
	# POTŘEBUJU VSTUPNI FILY VYCISTIT, ABYCH DO MODEL.PREDICT MOHL CPAT KRASNE matici features x jets z jednoho eventu...
