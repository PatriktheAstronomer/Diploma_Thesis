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
public:
	TFile *m_source;
	TString m_treeName;
	TString scalarFileName; 	
	TTree *m_tree;
	TTree *m_treeout;
	Float_t m_centralityBinsN;
	Float_t m_eta_veto = 2.8;
	bool m_dataType;
	Long64_t m_nEntries;
	Int_t event_Centrality;
	double MC_weight;
	double MC_weight_scalar;
	std::vector<Float_t> * jet_eta = 0;
	std::vector<Float_t> * jet_pt = 0;
	std::vector<Float_t> * jet_rtrk = 0;
	std::vector<Float_t> * jet_ntrk = 0;
	std::vector<Float_t> * jet_width = 0;
	std::vector<Float_t> * truth_jet_pt = 0;
	std::vector<Int_t> * truth_jet_flavor = 0;
        Float_t jet_eta_scalar;
        Float_t jet_pt_scalar;
        Float_t jet_rtrk_scalar;
        Float_t jet_ntrk_scalar;
        Float_t jet_width_scalar;
	Float_t truth_jet_pt_scalar;
        Int_t truth_jet_flavor_scalar;

	TH3F * h_3F = nullptr;
	std::vector<std::vector<TH3F*>> responseCentrVars;

 	//variables declaration ------------------------ handtyped
        Variables pT = Variables("pT", 10, 1000);
        Variables response = Variables("response", 99, 0, 2);

	Variables eta = Variables("eta", {0.0,0.3,0.8,1.2,2.1,2.8,3.2,4.5});
        Variables ntrk = Variables("ntrk", 20, 0, 20);
        Variables rtrk = Variables("rtrk", 20, 0, 1);
        Variables width = Variables("width", 20, 0, 1);
        std::vector<Variables> InspectedVars = {eta, ntrk, rtrk, width}; // eta is the first, for porpose of JES/JER diagrams

	// end of the declaration --------------------------------

	Selection(TString source, TString treeName, TString type);
	void SetSource(TString source);
	void SetTreeName(TString treeName);
	void SetDataType(TString type);
	void GetTTree();
	
	void SetBranchAddress();
	void SetBranchAddress_Scalar();
	void BookHistograms();
	void EventLoop(Long64_t nEntries = 0);
	void Write(string outfile);
};


#endif
