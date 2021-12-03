from ROOT import TFile, gROOT, TH3, TH2D, TH1, TF1, TCanvas
import numpy as np

def GenerateCorrMatrices(source, outdir):
	f = TFile(source)
	for key in f.GetListOfKeys(): #read list of subdirs from TFile
		cl = gROOT.GetClass(key.GetClassName())
		if not cl.InheritsFrom("TDirectoryFile"):	continue
		dirs = key.ReadObj()
		for key2 in dirs.GetListOfKeys(): #read list of keys from each TDirectory
			cl = gROOT.GetClass(key2.GetClassName())
			if not cl.InheritsFrom("TH3"):  continue
			Make3DProjection(key2.ReadObj(), key2.ReadObj().GetName(), outdir)

def Make3DProjection(h_3F, name, outdir):
	nzbins = h_3F.GetNbinsZ() #projection over var_vals
	nxbins = h_3F.GetNbinsX() #projection over pT
	z_bins = np.asarray(h_3F.GetZaxis().GetXbins())
	x_bins = np.asarray(h_3F.GetXaxis().GetXbins())
	corr_JES = TH2D("JES", "JES", nxbins, x_bins, nzbins, z_bins)
	corr_JES.SetStats(0)
	corr_JER = TH2D("JER", "JER", nxbins, x_bins, nzbins, z_bins)
	corr_JER.SetStats(0)
	for jz in range(nzbins):
		h_3F.GetZaxis().SetRange(jz,jz)		
		slice = h_3F.Project3D("yx")
		for jx in range(nxbins):
			ySlice = slice.ProjectionY("meta", jx, jx)
			if(ySlice.GetEntries() > 25):
				mu, sigma = FitResponse(ySlice, outdir+"fits/"+name+"_pT_"+str(round(x_bins[jx],1))+"_val_"+str(round(z_bins[jz],1))+".png")
				corr_JES.Fill(x_bins[jx], z_bins[jz], mu)
				corr_JER.Fill(x_bins[jx], z_bins[jz], sigma)
	Draw(corr_JER, outdir+"matrices/JER_"+name+".png")
	Draw(corr_JES, outdir+"matrices/JES_"+name+".png")		

def FitResponse(ySlice, outname):
	mean = ySlice.GetMean()
	RMS = ySlice.GetRMS()
	fitF = TF1("fitF", "gaus", mean-2*RMS, mean+2*RMS)
	ySlice.Fit("fitF", "RQ")
	d = TCanvas("D1","",800,600)
	ySlice.Draw("ep")
	d.Print(outname)
	return fitF.GetParameter(1), fitF.GetParameter(2)/fitF.GetParameter(1)

def Draw(h_2F, outname):
	c = TCanvas("C1","",800,600);
	#c.SetLogx()
	#c.SetLogy()
	h_2F.Draw("colz")
	c.Print(outname)
