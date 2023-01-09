import numpy as np
import awkward as ak
import uproot
import lzma
import os
import pickle
import sys

import sklearn
import sklearn.metrics
import sklearn.model_selection
import sklearn.neural_network
import sklearn.pipeline
import sklearn.ensemble

# we do not apply any cuts or vetos! we just do standardization and feature engineering

def read_scalar_datafile(source, tree, list_of_input_branches, target_branch, weights = False):
	events = uproot.open(source+":"+tree)
	dataset = np.array([], dtype = np.float32)
	for branch in list_of_input_branches:
		dataset = np.append(dataset, events[branch].array(library="np").astype(np.float32))
	target = events[target_branch].array(library="np").astype(np.float32)
	if weights:
		mc_weights = events["MC_weight_scalar"].array(library="np").astype(np.float32) # zkontrolovat, jestli je v poradku a nepřeteče
	else:
		mc_weights = np.ones_like(target)

	return dataset, target, mc_weights
	# dataset and target arrays are used for training

# in various types of MLs ve perform and plot some kind of grid search

def model_training(dataset, target, mc_weights, outdir, model_name, model_type): 
	print("Data loaded, training begins")
	x_train, x_test, mc_train, mc_test, t_train, t_test = sklearn.model_selection.train_test_split(dataset.T.reshape(-1,4), target, mc_weights, test_size=0.5, random_state=42)
	#x_train = dataset.T.reshape(-1,5)
	#t_train = target
	# config	epochs	datasample_size	RMSE_per_each centrality and overall
	if model_type == "regressor":
		# MLP, smaller and quicker
		# melo by smysl udelat subsampling na 1000 siti treba
		"""	
		scaler = sklearn.preprocessing.StandardScaler()
		poly = sklearn.preprocessing.PolynomialFeatures(3)
		mlp = sklearn.neural_network.MLPRegressor(hidden_layer_sizes = (500, ), max_iter=300) # later alpha, tunning
		model = sklearn.pipeline.Pipeline(steps=[('scaler', scaler), ('poly', poly), ('mlp', mlp)]) #otestovat
		model.fit(x_train, t_train)

		#MLP speed-up simplification to float32 numerics
		for i in range(len(mlp.coefs_)): mlp.coefs_[i] = mlp.coefs_[i].astype(np.float32)
		for i in range(len(mlp.intercepts_)): mlp.intercepts_[i] = mlp.intercepts_[i].astype(np.float32)
		"""

		model = sklearn.ensemble.HistGradientBoostingRegressor() # most basic setup

		#model = sklearn.ensemble.GradientBoostingRegressor(n_estimators=50, max_depth=6)
		#model = sklearn.neural_network.MLPRegressor(hidden_layer_sizes = (300, ), max_iter=300) # later play with alpha
		#model = sklearn.ensemble.RandomForestRegressor(n_estimators=10, max_leaf_nodes=301, min_samples_split = 10000, criterion="poisson")
		
		model.fit(x_train, t_train) # after saving the model! Might be dangerous, in case we have big feature space
		prediction = model.predict(x_test)
		rmse = sklearn.metrics.mean_squared_error(t_test, prediction)
		print(model_name, " RMSE is ",str(rmse))

	elif model_type == "classifier":
		pass

	with lzma.open(outdir+model_name+".model", "wb") as model_file:
		pickle.dump(model, model_file)

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
			batch_prediction = []
			for e in range(len(batch)): # batch is a group of j-matricies of i-jets time d-features -> loop event in events
				event_data = []
				for feature in range(len(list_of_input_branches)):
					event_data.append(batch[e][feature])
				event_data = np.array(event_data)
				try:
					# response based
					# event_prediction = (event_data[1]/model.predict(event_data.T)).tolist()
					# truth_pt based					
					event_prediction = model.predict(event_data.T).tolist()
				except:
					event_prediction = event_data[1].tolist()

				batch_prediction.append(event_prediction)
			try:
				outfile["AntiKt4HI"].extend({val_name: ak.Array(batch_prediction)})
			except:
				outfile["AntiKt4HI"] = ({val_name: ak.Array(batch_prediction)})      # later we can also try to correct dubblet (pt, eta)

def create_final_file(source, list_of_input_branches_to_copy, model_name, model_type):
	pass # nutnost vzit cisty file a prekopirovat do nej predikci, plus stare vetve a to do jednoho stromu, aby se mi to snadno davalo do testovani...



