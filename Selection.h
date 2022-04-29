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
#include <fstream>
#include <iostream>

#include "Variables.h"

class Selection: public Variables
{
public:
	TFile *m_source;
	TFile *m_outfile;
	TString m_treeName;
	TTree *m_tree;
	TTree *m_treeout;
	Float_t m_centralityBinsN;
	bool training_flag = false;
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
	std::vector<Float_t> * truth_jet_flavor = 0;
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
 	/*---> will be moved sideaway
    	loop filling InspectedVars with Variables type with filled constructors values taken from configfile
        // InspectedVars je zde, já to jen v rámci Configure naplním
	*/
	Variables pT = Variables("pT", 50, 1050);
        Variables response = Variables("response", 99, 0, 2);

	Variables eta = Variables("eta", {0.0,0.3,0.8,1.2,2.1,2.8,3.2,4.5});
        Variables ntrk = Variables("ntrk", 20, 0, 20);
        Variables rtrk = Variables("rtrk", 20, 0, 1);
	// only trks above 4 GeV used, ghost associated trks
        Variables width = Variables("width", 20, 0, 1);

        std::vector<Variables> InspectedVars = {eta, ntrk, rtrk, width}; // eta is the first, for porpose of JES/JER diagrams

	// end of the declaration --------------------------------

	Selection(TString source, TString treeName, TString type);
	void Configure(TString variables_data, TString vetos_data);
	// dopsat v C++, adresa na cteni .data filu, nejdriv variables, pak i vetos...

	void SetSource(TString source);
	void SetTreeName(TString treeName);
	void SetDataType(TString type);
	void GetTTree();

	void FormScalarSample(TString outname);	
	void SetBranchAddress();
	void CreateBranchScalar();
	void BookHistograms();
	void EventLoop(Long64_t nEntries = 0);
	void Write(string outfile);
};


#endif
