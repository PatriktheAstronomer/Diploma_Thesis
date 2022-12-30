
import numpy as np
import awkward as ak
import uproot
import lzma
import os
import pickle
import sys

import sklearn
import sklearn.model_selection
import sklearn.neural_network
import sklearn.pipeline
import sklearn.ensemble

# we do not apply any cuts or vetos! we just do standardization and feature engineering

def read_scalar_datafile(source, tree, list_of_input_branches, target_branch):
	events = uproot.open(source+":"+tree)
	dataset = np.array([]) # mozna nam dokonce staci float32, 16..., zamyslet se...
	for branch in list_of_input_branches:
		dataset = np.append(dataset, events[branch].array(library="np"))
	target = events[target_branch].array(library="np")
	return dataset, target
	# dataset and target arrays are used for training

# in various types of MLs ve perform and plot some kind of grid search

def model_training(dataset, target, outdir, model_name, type): 
	#x_train, x_test, t_train, t_test = sklearn.model_selection.train_test_split(dataset.T.reshape(-1,5), target, test_size=0.0, random_state=42)
	x_train = dataset.T.reshape(-1,5)
	t_train = target
	#normalizer = sklearn.preprocessing.StandardScaler()
	# config	epochs	datasample_size	RMSE_per_each centrality and overall	

	if type == "regressor":
		model = sklearn.ensemble.GradientBoostingRegressor(max_leaf_nodes=3001, min_samples_split = 10000) #HistGradient, až to Martin nainstaluje
		#model = sklearn.neural_network.MLPRegressor(hidden_layer_sizes = (300, ), max_iter=300) # later play with alpha
		model.fit(x_train, t_train)
		# vypisovat po epochach???

	elif type == "classifier":
		pass

	with lzma.open(outdir+model_name+".model", "wb") as model_file:
		pickle.dump(model, model_file)


	# sestavit model, zjednodusit vahy (asi neni nutne, dokud neni obludne velky), ulozit ho

def predict(dir, source, outdir, model_name, list_of_input_branches, model_type):
	# works the same for regressors and classifier and any model in general
	with lzma.open(outdir+model_name+".model", "rb") as model_file: #model address si budu muset vytvorit z model_name a nějaký statický dir...
		model = pickle.load(model_file)
        
	events = uproot.open(dir+source+":"+"AntiKt4HI") #input tree for reading

	if model_type == "regressor":
		val_name = "corr_jet_pt"
	elif model_type == "classifier": #first we will work only with regressors
		val_name = "pred_jet_flavour"

	with uproot.recreate(outdir+"/"+model_name+".root") as outfile:
		for batch, report in events.iterate(step_size="10 MB", filter_name = list_of_input_branches, library = "np", report = True):
			print(report)
			batch = np.array([batch[branch] for branch in list_of_input_branches]).T
			batch_prediction = np.array([])
			for e in range(len(batch)): # batch is a group of j-matricies of i-jets time d-features -> loop event in events
				event_data = []
				for feature in range(len(list_of_input_branches)):
					event_data.append(batch[e][feature])
				event_data = np.array(event_data)
				try:
					event_prediction = event_data[1]/model.predict(event_data.T) #differs for GBDT and MLP, pT cut in training set
				except:
					event_prediction = event_data[1]

				batch_prediction = np.append(batch_prediction, event_prediction)
			try:
				outfile["AntiKt4HI"].extend({val_name: ak.Array(batch_prediction)})
			except:
				outfile["AntiKt4HI"] = ({val_name: ak.Array(batch_prediction)})      # later we can also try to correct dubblet (pt, eta)

def create_final_file(source, list_of_input_branches_to_copy, model_name, model_type):
	pass # nutnost vzit cisty file a prekopirovat do nej predikci, plus stare vetve a to do jednoho stromu, aby se mi to snadno davalo do testovani...



