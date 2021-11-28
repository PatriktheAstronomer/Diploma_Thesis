#include "Process.h"

Process::Process(TString source){
	m_source = new TFile(source); 
	ReadFile();
}

void Process::ReadFile()
{	
	for (TObject* keyAsObj : *m_source->GetListOfKeys()){ // read subdir keys from TFile
		TKey* key = static_cast<TKey*>(keyAsObj);
		TClass *cl = gROOT->GetClass(key->GetClassName());
		if (!cl->InheritsFrom("TDirectoryFile")) continue;
		TDirectoryFile* Dirs = (TDirectoryFile*)key->ReadObj();
		for (TObject* keyAsObj : *Dirs->GetListOfKeys()){ // read keys from each TDirectory
			TKey *key = static_cast<TKey*>(keyAsObj);
			TClass *cl = gROOT->GetClass(key->GetClassName());		
			if (!cl->InheritsFrom("TH3")) continue;
			MakeProjections((TH3F*)key->ReadObj());
			std::string var_name = key->GetName();
			histogram_name.push_back(var_name);
		}

	}
}

void Process::MakeProjections(TH3F* h_3F)
{
	std::vector<float> pT;
	std::vector<float> var_val;
	std::vector<float> mu;
	std::vector<float> sigma;
	Int_t nzbins = h_3F->GetNbinsZ(); // projection over var_vals
	Int_t nxbins = h_3F->GetNbinsX(); // projection over pT
	for(int k = 0; k < nzbins; k++){ 
		h_3F->GetZaxis()->SetRange(k,k);
		TH2F *slice = (TH2F*) h_3F->Project3D("xy");
		for (int j = 1; j < nxbins; j++){
			pT.push_back(j);
			var_val.push_back(k);
			TH1D *ySlice = slice->ProjectionY("meta",j,j);
			std:vector<float> fitres = FitResponse(ySlice); 
			mu.push_back(fitres.at(0));
			sigma.push_back(fitres.at(1));
		}
	}
	std::vector<std::vector<float>> histo_stats {pT, var_val, mu, sigma};
	processed_data.push_back(histo_stats);
}


std::vector<float> Process::FitResponse(TH1D* h_1D)
{
	std:vector<float> fit_params;
	Float_t Mean = h_1D->GetMean();
	Float_t RMS  = h_1D->GetRMS();
	TF1 *fitF = new TF1("fitF", "gaus", Mean-2*RMS, Mean+2*RMS);
	if(h_1D->GetEntries() > 20){ // bottom limit on number of entries to achieve suitable fit quality
		h_1D->Fit("fitF", "RN");
		fit_params.push_back(fitF->GetParameter(1));
		fit_params.push_back(fitF->GetParameter(2)/fitF->GetParameter(1)); // normalised sigma	}
	}
	else{
		fit_params.push_back(-666);
		fit_params.push_back(-666);
	}
	return fit_params;
// musim do nejakeho trash uloziste ukladat ty fity samotne... zatim jedu negraficky
// nevime, co vraci za hodnoty
}

