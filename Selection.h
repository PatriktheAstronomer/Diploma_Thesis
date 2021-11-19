#ifndef SELECTION_H
#define SELECTION_H

#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TBrowser.h"
#include "TSystem.h"
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"
#include "TRandom.h"
#include <math.h>
#include <string>
#include <iostream>

#include "Variables.h"

class Selection: public Variables
{
protected:
	TFile *m_source;
	TString m_treeName; 	
	TTree *m_tree;
	TTree *m_treeout;
	Float_t m_centralityBinsN;
	Float_t m_eta_veto = 2.8;
	bool m_dataType;
	Long64_t m_nEntries;
	Int_t event_Centrality;
	double MC_weight;
	std::vector<Float_t> * jet_eta = 0;
	std::vector<Float_t> * jet_pt = 0;
	std::vector<Float_t> * jet_rtrk = 0;
	std::vector<Float_t> * jet_ntrk = 0;
	std::vector<Float_t> * jet_width = 0;
	std::vector<Float_t> * truth_jet_pt = 0;
	std::vector<Int_t> * truth_jet_flavor = 0;

	TH3F * h_3F = nullptr;
	std::vector<std::vector<TH3F*>> responseCentrVars;

 	//variables declaration --- handtyped
        Variables pT = Variables("pT", 10, 1000);
        Variables response = Variables("response", 50, 0, 2);

        Variables ntrk = Variables("ntrk", 20, 0, 20);
        Variables rtrk = Variables("rtrk", 20, 0, 1);
        Variables width = Variables("width", 20, 0, 1);
        std::vector<Variables> InspectedVars = {ntrk, rtrk, width};

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
