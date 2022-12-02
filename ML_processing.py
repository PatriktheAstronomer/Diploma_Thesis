import numpy as np
import uproot
import lzma
import os
import pickle
import sys

import sklearn.model_selection
import sklearn.neural_network
import sklearn.pipeline


# we do not apply any cuts or vetos! we just do standardization and feature engineering

def read_scalar_datafile(source, tree, list_of_input_branches, target_branch):
	events = uproot.open(source+":"+tree)
	dataset = []
	for branch in list_of_input_branches:
		dataset.append(events[branch].array(library="np"))
	dataset = np.array(dataset)
	target = events[target_branch].array(library="np")
	return dataset, target
	# dataset and target arrays are used for training

# in various types of MLs ve perform and plot some kind of grid search

def model_training(dataset, target, oudir, model_name): 
        x_train, x_test, t_train, t_test = sklearn.model_selection.train_test_split(dataset.T, target, test_size=0.001, random_state=42)
	normalizer = sklearn.preprocessing.StandardScaler()

	mlp = sklearn.neural_network.MLPClassifier(hidden_layer_sizes = (500, ), alpha=par, max_iter=300)

	# sestavit model, zjednodusit vahy (asi neni nutne, dokud neni obludne velky), ulozit ho

	#musit to delat uz nacisto, tedy nacist si tady data a nacvicit nejaky model a ulozit ho -> MLP z week 4, BDT z week 9
	# pomoci splitu budu nejprve cvicit na velmi malych samplech... treba 1/1000, celych dat, pak na vetsich celcich
	#udelat si target i na klasifikaci, ten se proste lisi jen tim, ze jeho target branch je jina
	pass

def predict(source, outname, tree, list_of_input_branches, target_branch, model_name):
	#zkusit si cteni neskalarniho filu a jeho upravu... 
        # tzn. vytvořit druhý file, který bude mit dane RMSE nebo tak neco... copy structure... 
	#RMSE mi zase napocia cecko, to uz umim i pro PbPb
	#slovnik-like check, chci si byt jisty, ze se dodrzuji vsechny zakony zachovani... zavislost pseudorapidity a pT napr. poskytuje zajimavy constrain
	pass



	# pokud ma i nativni soubor jet_flavour (myslim si, ze ne, tak bych ji proste poslali do target branch... jinak rozdelime na funkce predict_regress a predict_class
        # tak ci tak na predict class chci merit accuracy
