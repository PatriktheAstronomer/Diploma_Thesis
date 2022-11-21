from ROOT import TFile, gROOT, TH3, TH2D, TH1D, TF1, TCanvas, TLegend, TLatex
import numpy as np
from numpy import nan
import matplotlib.pyplot as plt
import pylab

import sys
sys.path.insert(0, '/home/novotnyp/Diploma_Thesis/lib')
from TH1_style import *


# set for 15 markers and 15 colors
markers = ["o", "v", "<", ">", "^", "s", "P", "*", "+", "X", "D", "p", "d", "h", "x"]
cm = pylab.get_cmap("gist_rainbow")


eta_bins = [0.0, 0.3, 0.8, 1.2, 1.8, 2.1, 3.2, 4.5] # HARD-TYPED NOT NECESSARLY, BUT NOT CHANGED OFTEN

def GenerateJERS(inputdir, source, outdir):
	print("Generation JES/JER")
	spectra_mu_pp, spectra_sigma_pp, fits_pp, spectra_mu_PbPb, spectra_sigma_PbPb = list(), list(), list(), list(), list()
	tfiles = list() # to prevent closing of TFiles, when opening another one
	source = sorted(source)
	for s in source:
		print ("Running for source "+s)
		tfiles.append(TFile(inputdir+s+".root"))
		for key in tfiles[-1].GetListOfKeys(): #read list of subdirs from TFile
			cl = gROOT.GetClass(key.GetClassName())
			if not cl.InheritsFrom("TDirectoryFile"):	continue
			dirs = key.ReadObj()
			for key2 in dirs.GetListOfKeys(): #read list of keys from each TDirectory
				cl = gROOT.GetClass(key2.GetClassName())
				if not cl.InheritsFrom("TH3"):	continue
				if "eta" in key2.ReadObj().GetName():
					#for JES/JER in pp case, comparison of several inputs... from sources, whereas for PbPb	it's several TH3 in one	source
					if "PbPb" in s:
						mu, sigma = PrepareJESnR(key2.ReadObj(), key2.ReadObj().GetName(), outdir)
						spectra_mu_PbPb.append(mu)
						spectra_sigma_PbPb.append(sigma)
						# ZKUSME ZDE PRIDAT PBPB FIT A PLOTNOUT... POKUD BUDE FUNGOVAT, TAK ZJEDNODUSSIM pp a PbPb set type podle len(source) !!!
						# ZUSTANE UZ PAK JEN JEDEN IF A JEDNO TROJVOLANI PRINTU

						continue
						# returns native TH1 in eta bins
					if "pp" in s:
						mu, sigma, fit = PrepareJESnR(key2.ReadObj(), key2.ReadObj().GetName(), outdir)
						spectra_mu_pp.append(mu)
						spectra_sigma_pp.append(sigma)
						fits_pp.append(fit)

	# first iterator goes over datasamples, the second one over etas, that's why transpose the matrix of plots first inside Draw options
	if len(spectra_mu_pp) !=0:
		DrawJESnR(spectra_mu_pp, "JES_pp", outdir, source)
		DrawJESnR(spectra_sigma_pp, "JER_pp", outdir, source)
		DrawResponse(fits_pp, outdir, source)
	if len(spectra_mu_PbPb) != 0:
		DrawJESnR(spectra_mu_PbPb, "JES_PbPb", outdir) 
		DrawJESnR(spectra_sigma_PbPb, "JER_PbPb", outdir)

# correlation matricies and profiles
def GenerateCorrMatrices(inputdir, source, outdir): 
	print("Generating correlation matrices")
	corr_JES_matrix, corr_JER_matrix, corr_count_matrix, corr_count_pT_integrated_matrix = list(), list(), list(), list()
	tfiles = list() # to prevent closing of TFiles, when opening another one
	var_names = list()
	source = sorted(source)
	for s in source:
		corr_JES_helper, corr_JER_helper, corr_count_helper, corr_count_pT_integrated_helper = list(), list(), list(), list()
		print ("Running for source "+s)
		tfiles.append(TFile(inputdir+s+".root"))
		for key in tfiles[-1].GetListOfKeys(): #read list of subdirs from TFile
			cl = gROOT.GetClass(key.GetClassName())
			if not cl.InheritsFrom("TDirectoryFile"):	continue
			dirs = key.ReadObj()
			var_keys_helper = list()
			for key2 in dirs.GetListOfKeys(): #read list of keys from each TDirectory
				cl = gROOT.GetClass(key2.GetClassName())
				if not cl.InheritsFrom("TH3"):  continue
		
				print("3D matrix processed: "+key2.ReadObj().GetName())
				var_keys_helper.append(key2.ReadObj().GetName())

				if len(source) != 1: # ZATIM ZKOUSKA JEN PRO pp, pak bude i pro jednotlive CENTRALITY ???
				
					x_bins, z_bins, corr_JES, corr_JER, corr_count, corr_count_pT_integrated = Make3DProjection(key2.ReadObj(), key2.ReadObj().GetName(), outdir)
					corr_JES_helper.append([x_bins, z_bins, corr_JES])
					corr_JER_helper.append([x_bins, z_bins, corr_JER])
					corr_count_helper.append([x_bins, z_bins, corr_count])
					corr_count_pT_integrated_helper.append(corr_count_pT_integrated)

		var_names = var_keys_helper #its the same for all sources

		corr_JES_matrix.append(corr_JES_helper)
		corr_JER_matrix.append(corr_JER_helper)
		corr_count_matrix.append(corr_count_helper)
		corr_count_pT_integrated_matrix.append(corr_count_pT_integrated_helper)

	# Aplikujeme vstup pro PbPb casem ---> budu to tam chctit dostat stejne jako ted... ruzne centrality naplnim do source...
        # bude-li jen jeden source na vstupu, tak ulozim veci, jak jdou po centralitach a jen upravim source list, aby mi je to porovnalo
        # ono nakonec v PbPb nechci delat studie, tam budou data obecna... jen studie v centralite, naopak v pp ty studie delat chci... resp asi je chci i v PbPb, ale jen jednou
        # to uz si pripadne porovnam oddelene

	if len(corr_JES_matrix):
		DrawMatrices(corr_JES_matrix, outdir, var_names, source, "JES")
		DrawMatrices(corr_JER_matrix, outdir, var_names, source, "JER")
		DrawMatrices(corr_count_matrix, outdir, var_names, source, "count")
		DrawCounts(corr_count_pT_integrated_matrix, outdir, var_names, source)
		DrawProfiles(corr_JES_matrix, corr_JER_matrix, outdir, var_names, source)

def PrepareJESnR(h_3F, name, outdir):
	nzbins = h_3F.GetNbinsZ() #projection over eta
	nybins = h_3F.GetNbinsY() #response
	nxbins = h_3F.GetNbinsX() #projection over pT
	z_bins = np.asarray(h_3F.GetZaxis().GetXbins())
	y_bins = np.asarray(h_3F.GetYaxis().GetXbins())
	x_bins = np.asarray(h_3F.GetXaxis().GetXbins())
	means, ress, fits = [], [], []
	x_coordinate = [np.mean([x_bins[i], x_bins[i+1]]) for i in range(0, nxbins)]
	y_coordinate = [np.mean([y_bins[i], y_bins[i+1]]) for i in range(nybins)]
	for jz in range(nzbins):
		h_3F.GetZaxis().SetRange(jz,jz)
		slice = h_3F.Project3D("yx")
		JES_0, JES_1, JER_0, JER_1, fits_by_pT = [], [], [], [], []
		for jx in range(nxbins):
			ySlice = slice.ProjectionY("meta", jx, jx)
			fit_vals = []
			for bin in range(0, nybins):
				fit_vals.append(ySlice.GetBinContent(bin))
	
			mu, sigma, emu, esigma = nan, nan, nan, nan #Nan isnt plotted
			if(ySlice.GetEntries() > 25):
				mu, sigma, emu, esigma = FitResponse(ySlice, outdir+"fits/JES_JER_classic/"+name+"_pT_"+str(round(x_bins[jx],1))+"_val_"+str(round(z_bins[jz],1))+".png", x_bins[jx])
			JES_0.append(mu)
			JES_1.append(emu)
			JER_0.append(sigma/mu)
			JER_1.append(sigma*np.sqrt((esigma/sigma)*(esigma/sigma)+(emu/mu)*(emu/mu))) #error propagation
			fits_by_pT.append([y_coordinate, fit_vals])

		means.append([x_coordinate, JES_0, JES_1])
		ress.append([x_coordinate, JER_0, JER_1])
		fits.append([x_coordinate, fits_by_pT]) 

	return means, ress, fits #returns almost (error)graphs implicitly

def DrawJESnR(matrix_input, type, outdir, *comparison_labels): # v comparison_labels jsou sources
	type_appendix, type_suffix = type.split("_")
	matrix_input = transpose_list(matrix_input)
	for index, vct_datasamples in enumerate(matrix_input): #eta loop
		fig = plt.figure()
		plt.xscale("log")
		plt.xlabel("$p_{T}$")
		if type_appendix == "JES":
			plt.ylim([0.9, 1.1])
			plt.ylabel("$\mu$ response") #to be improved - better label
		elif type_appendix == "JER":
			plt.ylim([0.0, 0.3])
			plt.ylabel("$\sigma$ of response") #to be improved - better label

		plt.title(type_appendix+" for eta "+str(eta_bins[index])+"-"+str(eta_bins[index+1]))
		for data in vct_datasamples: #datasamples loop
			plt.errorbar(data[0], data[1], yerr=data[2], linestyle="None", marker='o')  #to be improved - various markers, f. e. from enumerate
		
		if type_suffix == "pp":
			plt.legend(comparison_labels[0]) # [0] just for string processing reasons
		elif type_suffix == "PbPb":
			plt.legend(("0-10 %", "10-20 %", "20-30 %", "30-40 %", "40-50 %", "50-60 %", "60-70 %", "70-80 %"))

		if type_appendix == "JES":
			plt.hlines(1, vct_datasamples[0][0][0], vct_datasamples[0][0][-1], color="black")

		plt.savefig(outdir+"/JESnJER/"+type_appendix+str(eta_bins[index])+".png")
		plt.close()

def DrawResponse(matrix_input, outdir, comparison_labels): #compares flavours, not centralities... thus impossible to be used for PbPb the classical way
	print("Draw responses")
	matrix_input = transpose_list(matrix_input)
	for index, vct_pT in enumerate(matrix_input): #eta loop
		vct_pT = transpose_list(vct_pT)
		pT_data = vct_pT[0]
		fit_vals = vct_pT[1]
		for k in range (len(pT_data[0])): #pT loop
			#pT_data_extended = np.append(pT_data[j, 1000) ---> implementnout dole, pT_data.T[0] poslu do pT_data_extended...
			#eta_bins_extended = np.append(eta_bins, 4.0)
			fig = plt.figure()
			for j in range (len(pT_data)): #dataset loop
				if np.sum(fit_vals[j][k][1]) == 0:
					continue
				plt.plot(fit_vals[j][k][0], fit_vals[j][k][1], linestyle="None", marker='o', ms = 10)
			plt.yscale("log")
	
			#print(str(eta_bins[index+1]), str(round(pT_data[j][k+1])))
			#plt.title("response in range of eta ("+str(eta_bins[index])+", "+str(eta_bins[index+1])+") & pT ("+str(round(pT_data[j][k]))+", "+str(round(pT_data[j][k+1]+")")))
			
			plt.xlabel("response")
			plt.ylabel("count [a. u.]")
			plt.legend(comparison_labels)
			plt.savefig(outdir+"/response/eta_"+str(eta_bins[index])+"_pT_"+str(round(pT_data[j][k]))+".png")
			plt.close()

def DrawCounts(matrix_input, outdir, names, sources):
	print("Draw count profiles") # sources se vykresli pres sebe
	for k in range(len(matrix_input[0])):	#vars loop
			name = names[k]
			fig = plt.figure()
			plt.title("Profile for "+ name)
			plt.ylabel("relative count")
			plt.xlabel(name.split("_")[0])
			for i in range(len(matrix_input)): #source vars	
				plt.plot(matrix_input[i][k][0], matrix_input[i][k][1], linestyle="None", marker=markers[i], ms = 10) #small number of inputs, handle color setting on its own
			plt.legend(sources)
			plt.savefig(outdir+"/counts/"+name+".png", dpi=300)
			plt.close()

def DrawProfiles(matrix_input, matrix_2_input, outdir, names, sources):
	# each pT integrated resp(var) dependence is an independent dataline... all of them are placed in one, the same figure -> from JES, JER taken as errorbar
	print("Draw profiles") # sources se vykresli vedle sebe
	pT_bins = [str(np.round(matrix_input[0][0][0][l]))+"-"+str(np.round(matrix_input[0][0][0][l+1])) for l in range(len(matrix_input[0][0][0])-1)]
	for k in range(len(matrix_input[0])):   #vars loop
		name = names[k]
		fig, ax = plt.subplots(ncols=len(matrix_input), nrows=1, figsize=(15*np.sqrt(len(matrix_input)), 15))
		ax[0].set_xlabel(name.split("_")[0])
		ax[0].set_ylabel("response") # pridat mu+-sigma
		ax[0].set_ylim([0.8, 1.2])
		for i in range(len(matrix_input)): #source var
			pt_count = len(matrix_input[i][k][0])-1
			for j in range(pt_count): #filling each pT dataline  with unc. as it's resolution
				y_coordinate = [np.mean([matrix_input[i][k][1][index], matrix_input[i][k][1][index+1]]) for index in range(0, len(matrix_input[i][k][1])-1)] #index begins at zero
				# y_coordinate in 2D matrix is the var coordinate
				ax[i].errorbar(y_coordinate, transpose_list(matrix_input[i][k][2])[j], yerr=transpose_list(matrix_2_input[i][k][2])[j], linestyle="None", mec=cm(1.*j/pt_count), marker=markers[j], ms = 10)
			ax[i].set_xlabel(name.split("_")[0])
			ax[i].set_title("Corr matrix for "+sources[i])
			ax[i].set_ylim([0.8, 1.2])
			ax[i].legend(pT_bins) # dataseries labels

		plt.savefig(outdir+"/profiles/"+name+".png", dpi=300)
		plt.close()

def DrawMatrices(matrix_input, outdir, names, sources, matrix_type):
	print("Draw matrices " + matrix_type) # sources se vykresli vedle sebe
	if matrix_type == "JES": # Zvetos controls boundaries and outliers
		Zvetos = [0.8, 1.2]
	elif matrix_type == "JER":
		Zvetos = [0.0, 0.5]
	else:
		Zvetos = [0, 1]

	for k in range(len(matrix_input[0])):   #vars loop
			name = names[k]
			fig, ax = plt.subplots(ncols=len(matrix_input), nrows=1, figsize=(15*np.sqrt(len(matrix_input)), 15))
			ax[0].set_ylabel(name.split("_")[0])
			Z = np.array([])
			for i in range(len(matrix_input)): # we need to set a common colorscale, to be able to compare values
				Z = np.append(Z, matrix_input[i][k][2])
				Z = Z[~np.isnan(Z)] #NaN filter
			for i in range(len(matrix_input)): #source vars
				plc = ax[i].pcolormesh(matrix_input[i][k][0], matrix_input[i][k][1], matrix_input[i][k][2], vmin=max(Z.min(), Zvetos[0]), vmax=min(Z.max(), Zvetos[1]))
				ax[i].set_xlabel("pT")
				ax[i].set_title("Corr matrix for "+sources[i])
				ax[i].set_xscale("log")
			fig.colorbar(plc, ax=ax[len(ax)-1])
			plt.savefig(outdir+"/matrices/"+matrix_type+"_"+name+".png", dpi=300) #give dpi to all inputs in the quality for master thesis
			plt.close()

def Make3DProjection(h_3F, name, outdir):
	nzbins = h_3F.GetNbinsZ() #projection over var_vals
	nxbins = h_3F.GetNbinsX() #projection over pT
	z_bins = np.asarray(h_3F.GetZaxis().GetXbins())
	z_coordinate = [np.mean([z_bins[i], z_bins[i+1]]) for i in range(nzbins)]
	x_bins = np.asarray(h_3F.GetXaxis().GetXbins())	
	total_jet_count = h_3F.Integral()
	corr_JES, corr_JER, corr_count, corr_count_pT_integrated = [], [], [], []
	for jz in range(1, nzbins+1):
		h_3F.GetZaxis().SetRange(jz,jz)				
		corr_JES_val, corr_JER_val, corr_count_val = [], [], []		
		corr_count_per_slice = 0
		for jx in range(1, nxbins+1):
			h_3F.GetXaxis().SetRange(jx,jx)
			ySlice = h_3F.Project3D("y")
			zSlice = h_3F.Project3D("z")
			corr_count_val_pT = zSlice.Integral()/total_jet_count
			corr_count_val.append(corr_count_val_pT)
			corr_count_per_slice += corr_count_val_pT
			mu, sigma, emu, esigma = nan, nan, nan, nan		
			if(ySlice.GetEntries() > 25):
				mu, sigma, emu, esigma = FitResponse(ySlice, outdir+"fits/"+name+"_pT_"+str(round(x_bins[jx-1],1))+"_val_"+str(round(z_bins[jz-1],1))+".png", x_bins[jx-1])
				if(emu > 0.5 or esigma > 0.5):
					mu, sigma = nan, nan	
			corr_JES_val.append(mu)
			corr_JER_val.append(sigma/mu)
		corr_count_pT_integrated.append([z_coordinate[jz-1], corr_count_per_slice])
		corr_JES.append(corr_JES_val)
		corr_JER.append(corr_JER_val)
		corr_count.append(corr_count_val)

	return x_bins, z_bins, corr_JES, corr_JER, corr_count, transpose_list(corr_count_pT_integrated)

def FitResponse(ySlice, outname, pTt):
	mean = ySlice.GetMean()
	RMS = ySlice.GetRMS()
	if (pTt > 300):	fitF = TF1("fitF", "gaus", mean-3*RMS, mean+3*RMS)
	else: ySlice.Rebin(2)
	if (pTt < 50): fitF = TF1("fitF", "gaus", mean-1.5*RMS, mean+2*RMS)
	else: fitF = TF1("fitF", "gaus", mean-2*RMS, mean+2*RMS)
	ySlice.Fit("fitF", "RQ")
	d = TCanvas("D1","",800,600)
	d.SetLogy()
	ySlice.Draw("ep")
	d.Print(outname) #plotted even for not used plots 
	return fitF.GetParameter(1), fitF.GetParameter(2)/fitF.GetParameter(1), fitF.GetParError(1)/fitF.GetParameter(1), fitF.GetParError(2)/fitF.GetParameter(2)

def transpose_list(list_2d):
    flat_list = [cell for row in list_2d for cell in row]
    return [flat_list[e::len(list_2d[0])] for e in range(len(list_2d[0]))]

# useful debug function
def arr_dimen(a):
  return [len(a)]+arr_dimen(a[0]) if(type(a) == list) else []
