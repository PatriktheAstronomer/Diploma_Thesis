import numpy as np
import uproot
#from root_numpy import array2root, root2array
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

# we do not apply any cuts or vetos! we just do standardization and feature engineering

def read_scalar_datafile(source, tree, list_of_input_branches, target_branch):
	events = uproot.open(source+".root:"+tree)
	dataset = []
	for branch in list_of_input_branches:
		dataset.append(events[branch].array(library="np"))
	dataset = np.array(dataset)
	target = events[target_branch].array(library="np")
	return dataset, target
	# dataset and target arrays are used for training of a datafile

# in various types of MLs ve perform and plot some kind of grid search

def model_training(dataset, target, model): 
	normalizer = sklearn.preprocessing.StandardScaler() # scaling based on profiles
	# ruzne transformery https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html#sphx-glr-auto-examples-preprocessing-plot-all-scaling-py
	poly = sklearn.preprocessing.PolynomialFeatures() # --- to do GridScan ---> that's fine, we dont have much features, but we have a lot's of records
	
	# z modelu vyzkousime MLP, log. regression a boosted decision tree
	#produce model
	# save it


	#https://gist.github.com/betatim/fe991eead446875f07e3
	# ---> Jako vystup pickes daneho modelu


def predict(model_paths, datafile_to_be_calibrated, outfile_name):
	pass

# ---> Udela se predikce a file se ulozi jako ROOT file, na nem se v C zas udela cela analyza...
