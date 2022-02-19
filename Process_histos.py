from ROOT import TFile, gROOT, TH3, TH2D, TH1D, TF1, TCanvas, TLegend, TLatex
import numpy as np

def GenerateCorrMatrices(inputdir, source, outdir):
	f = TFile(inputdir+source)
	histos, spectra_mu, spectra_sigma = list(), list(), list()
	for key in f.GetListOfKeys(): #read list of subdirs from TFile
		cl = gROOT.GetClass(key.GetClassName())
		if not cl.InheritsFrom("TDirectoryFile"):	continue
		dirs = key.ReadObj()
		for key2 in dirs.GetListOfKeys(): #read list of keys from each TDirectory
			cl = gROOT.GetClass(key2.GetClassName())
			if not cl.InheritsFrom("TH3"):  continue
			if "eta" in key2.ReadObj().GetName() and "PbPb" in source: # key2.ReadObj() returns TH3 classes			
				mu, sigma = PrepareJESnR(key2.ReadObj(), key2.ReadObj().GetName(), outdir)
			#vectors of TH1s for each eta is returned
			#corr_JES, corr_JER = Make3DProjection(key2.ReadObj(), key2.ReadObj().GetName(), outdir)
			#histos.append(corr_JES)
			#histos.append(corr_JER)
		if "PbPb" in source:
			spectra_mu.append(mu)
			spectra_sigma.append(sigma)
	if len(spectra_mu) != 0:
		DrawJESnR(spectra_mu, "JES", outdir) # input is matrix of centrality vs. eta containing TH1 histos for both - mu and sigma
		DrawJESnR(spectra_sigma, "JER", outdir)
	#WriteIn(histos, outdir, source)

def PrepareJESnR(h_3F, name, outdir):
	nzbins = h_3F.GetNbinsZ() #projection over eta
	nxbins = h_3F.GetNbinsX() #projection over pT
	z_bins = np.asarray(h_3F.GetZaxis().GetXbins())
	x_bins = np.asarray(h_3F.GetXaxis().GetXbins())
	th1_means, th1_ress = [], []
	for jz in range(nzbins):
		h_3F.GetZaxis().SetRange(jz,jz)
		slice = h_3F.Project3D("yx")
		mean_help = TH1D("MeanOfEta_"+str(round(z_bins[jz], 1)), "#mu as function of p_{T} for defined #eta", nxbins, x_bins)
		sigma_help = TH1D("SigmaOfEta_"+str(round(z_bins[jz], 1)), "#sigma as function of p_{T} for defined #eta", nxbins, x_bins)
		for jx in range(nxbins):
			ySlice = slice.ProjectionY("meta", jx, jx)
			mu, sigma, emu, esigma = FitResponse(ySlice, outdir+"fits/JES_JER_classic/"+name+"_pT_"+str(round(x_bins[jx],1))+"_val_"+str(round(z_bins[jz],1))+".png", x_bins[jx])
			mean_help.SetBinContent(jx,mu)
			mean_help.SetBinError(jx,emu)
			sigma_help.SetBinContent(jx,sigma) # normalised
			sigma_help.SetBinError(jx,esigma) # normalised ---> However, the final output should be normalised by itself.
		th1_means.append(mean_help)
		th1_ress.append(sigma_help)
	return th1_means, th1_ress

def DrawJESnR(matrix_input, type, outdir):
	matrix_transp = transpose_list(matrix_input) 
	for centrs in matrix_transp:
		c = TCanvas("C1","",800,600)
		c.SetLogx()
		legend = TLegend(0.6,0.7,0.85,0.9)
		legend.SetFillColor(0)
		legend.SetBorderSize(1)
		#SetHStyle(centrs[0], 0)
		outname = centrs[0].GetName()

		if type == "JES":
			outname = "JES_"+outname
			centrs[0].GetYaxis().SetRangeUser(0.86,0.99)
			centrs[0].GetYaxis().SetTitle("#sigma(p_{T_{reco}}/p_{T})/(<p_{T_{reco}}/p_{T}>)")
		if type == "JER":	
			outname = "JER_"+outname
			centrs[0].GetYaxis().SetRangeUser(0.0,0.4)	
			centrs[0].GetYaxis().SetTitle("<p_{T_{reco}}/p_{T}>")
	
		centrs[0].GetXaxis().SetTitle("p_{T} [GeV]")
		legend.AddEntry(centrs[0], "Centrality = 0-10%", "l")
		centrs[0].Draw("9")
		
		for i in range (1, len(centrs)):
			#SetHStyle(centrs[i], i)
			legend.AddEntry(centrs[i], "Centrality = "+str(i*10)+"-"+str((i+1)*10)+"%", "l")
			centrs[i].Draw("9 SAME")
        
		legend.Draw("")

		eta_interval = TLatex()
		eta_interval.SetTextFont(43)
		eta_interval.SetTextSize(28)
		eta_interval.SetNDC() #coordinates setup
		eta_interval.DrawLatex(0.18,0.2,outname) #title

		c.Print(outdir+"JESnJER/"+outname+".png")
		c.Print(outdir+"JESnJER/"+outname+".pdf")
		c.Close()

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
				mu, sigma, emu, esigma = FitResponse(ySlice, outdir+"fits/"+name+"_pT_"+str(round(x_bins[jx],1))+"_val_"+str(round(z_bins[jz],1))+".png", x_bins[jx])
				if(emu <= 0.5 and esigma <= 0.5):
					corr_JES.Fill(x_bins[jx], z_bins[jz], mu)
					corr_JER.Fill(x_bins[jx], z_bins[jz], sigma)
	corr_JER.GetZaxis().SetRangeUser(0.0,0.5)
	corr_JES.GetZaxis().SetRangeUser(0.8,1.2)
	corr_JER.SetName("JER_"+name)
	corr_JES.SetName("JES_"+name)
	Draw(corr_JER, outdir+"matrices/JER_"+name+".png")
	Draw(corr_JES, outdir+"matrices/JES_"+name+".png")		
	return corr_JES, corr_JER

def FitResponse(ySlice, outname, pTt):
	mean = ySlice.GetMean()
	RMS = ySlice.GetRMS()
	if (pTt > 300):	fitF = TF1("fitF", "gaus", mean-3*RMS, mean+3*RMS)
	else: ySlice.Rebin(2)
	if (pTt < 50): fitF = TF1("fitF", "gaus", mean-RMS, mean+2*RMS)
	else: fitF = TF1("fitF", "gaus", mean-2*RMS, mean+2*RMS)
	ySlice.Fit("fitF", "RQ")
	d = TCanvas("D1","",800,600)
	d.SetLogy()
	ySlice.Draw("ep")
	d.Print(outname) #plotted even for not used plots 
	return fitF.GetParameter(1), fitF.GetParameter(2)/fitF.GetParameter(1), fitF.GetParError(1)/fitF.GetParameter(1), fitF.GetParError(2)/fitF.GetParameter(2)

def Draw(h_2F, outname):
	c = TCanvas("C1","",800,600)
	#c.SetLogx()
	#c.SetLogy()
	h_2F.Draw("colz")
	c.Print(outname)

def WriteIn(histos, outdir, source):
	f_out = TFile(outdir+"matrices/Correlations_"+source, "RECREATE")
	for matrix in histos:
		matrix.Write()
	f_out.Close()

def transpose_list(list_2d):
    flat_list = [cell for row in list_2d for cell in row]
    return [flat_list[e::len(list_2d[0])] for e in range(len(list_2d[0]))]

def arr_dimen(a):
  return [len(a)]+arr_dimen(a[0]) if(type(a) == list) else []
