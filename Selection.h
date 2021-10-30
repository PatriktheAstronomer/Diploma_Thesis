#ifndef SELECTION_H
#define SELECTION_H

#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TBrowser.h"
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"
#include "TRandom.h"
#include <math.h>
#include <string>
#include <iostream>


class Selection
{
private:
	TFile *m_source;
	TString m_treeName; 	
	TTree *m_tree;
	TTree *m_treeout;
	Float_t m_centralityBinsN;
	Float_t m_eta_veto = 2.8;
	bool m_dataType;
	Long64_t m_nEntries;
	
protected:
	Int_t event_Centrality;
	double MC_weight;
	std::vector<Float_t> * jet_eta = 0;
	std::vector<Float_t> * jet_pt = 0;
	std::vector<Float_t> * jet_rtrk = 0;
	std::vector<Float_t> * jet_ntrk = 0;
	std::vector<Float_t> * jet_width = 0;
	std::vector<Float_t> * truth_jet_pt = 0;
	std::vector<Int_t> * truth_jet_flavor = 0;

	Float_t centralityBins[45];
	Float_t responseBins[100];
	Float_t jetptBins[28]={42.5, 47.5, 53, 59.5, 67, 75, 84, 94.5, 106, 119, 133.5, 149.5, 168, 189, 212, 237.5, 266.5, 299, 335.5, 376.5, 422.5, 474, 531.5, 596.5, 669.5, 751, 842.5, 945.5};
        //logarithmic binning

	TH3F * h_3F = nullptr;
	std::vector<std::string> vars = {"jet_rtrk", "jet_ntrk", "jet_width"};
	std::vector<std::vector<TH3F*>> responseCentrVars;

public:
	Selection(TString source, TString treeName, TString type);
	void SetSource(TString source);
	void SetTreeName(TString treeName);
	void SetDataType(TString type);
	void GetTTree();
	
	void SetBranchAddress();
	void BookHistograms();
	void EventLoop(Long64_t nEntries = 0);
	void Write(string outfile);
};


#endif
