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
	//std::vector<Float_t> * jet_rtrk = 0;
	std::vector<Float_t> * jet_ntrk = 0;
	std::vector<Float_t> * jet_width = 0;
	std::vector<std::vector<Float_t>> *  jet_EnergyPerSampling = 0;
	std::vector<Float_t> * jet_N90 = 0;
	std::vector<Float_t> * truth_jet_pt = 0;
	std::vector<Float_t> * truth_jet_flavor = 0;
        Float_t jet_eta_scalar;
        Float_t jet_pt_scalar;
        Float_t jet_rtrk_scalar;
        Float_t jet_ntrk_scalar;
        Float_t jet_width_scalar;
	Float_t jet_N90_scalar;
	Float_t truth_jet_pt_scalar;
        Int_t truth_jet_flavor_scalar;

	TH3F * h_3F = nullptr;
	std::vector<std::vector<TH3F*>> responseCentrVars;

 	//variables declaration ------------------------ handtyped
 
    	//loop filling InspectedVars with Variables type with filled constructors values taken from configfile
        // InspectedVars je zde, já to jen v rámci Configure naplním

	Variables pT = Variables("pT", 30, 1050);
        Variables response = Variables("response", 99, 0, 2);
	Variables eta = Variables("eta", {0.0, 0.3, 0.8, 1.2, 2.1, 2.8, 3.2, 4.5});
        Variables ntrk = Variables("ntrk", 40, 0, 40);
	Variables N90 = Variables("N90", 40, 0, 40);
        //Variables sumpTtrk = Variables("SumpTtrk", 100, 0, 1000000000); // ?? proper norm ?? move back to rtrk

	// only trks above 4 GeV used, ghost associated trks
        Variables width = Variables("width", 20, 0, 1);

        std::vector<Variables> InspectedVars = {eta, ntrk, N90, width}; // eta is the first, for purpose of JES/JER diagrams
	
	// section with calo variables:
	Variables PreSamplerB = Variables("Rel. fraction of E in PreSamplerB", 50, 0, 1);
	Variables EMB1 = Variables("Rel. fraction of E in EMB1", 50, 0, 1);
	Variables EMB2 = Variables("Rel. fraction of E in EMB2", 50, 0, 1);
	Variables EMB3 = Variables("Rel. fraction of E in EMB3", 50, 0, 1);

	Variables PreSamplerE = Variables("Rel. fraction of E in PreSamplerE", 50, 0, 1);
        Variables EME1 = Variables("Rel. fraction of E in EME1", 50, 0, 1);
        Variables EME2 = Variables("Rel. fraction of E in EME2", 50, 0, 1);
        Variables EME3 = Variables("Rel. fraction of E in EME3", 50, 0, 1);

        Variables HEC0 = Variables("Rel. fraction of E in HEC0", 50, 0, 1);
        Variables HEC1 = Variables("Rel. fraction of E in HEC1", 50, 0, 1);
        Variables HEC2 = Variables("Rel. fraction of E in HEC2", 50, 0, 1);
        Variables HEC3 = Variables("Rel. fraction of E in HEC3", 50, 0, 1);

        Variables TileBar0 = Variables("Rel. fraction of E in TileBar0", 50, 0, 1);
        Variables TileBar1 = Variables("Rel. fraction of E in TileBar1", 50, 0, 1);
        Variables TileBar2 = Variables("Rel. fraction of E in TileBar2", 50, 0, 1);
        
	Variables TileGap1 = Variables("Rel. fraction of E in TileGap1", 50, 0, 1);
        Variables TileGap2 = Variables("Rel. fraction of E in TileGap2", 50, 0, 1);
        Variables TileGap3 = Variables("Rel. fraction of E in TileGap3", 50, 0, 1);

	Variables TileExt0 = Variables("Rel. fraction of E in TileExt0", 50, 0, 1);
        Variables TileExt1 = Variables("Rel. fraction of E in TileExt1", 50, 0, 1);
        Variables TileExt2 = Variables("Rel. fraction of E in TileExt2", 50, 0, 1);

        Variables FCAL0 = Variables("Rel. fraction of E in FCAL0", 50, 0, 1);
        Variables FCAL1 = Variables("Rel. fraction of E in FCAL1", 50, 0, 1);
        Variables FCAL2 = Variables("Rel. fraction of E in FCAL2", 50, 0, 1);

	std::vector<Variables> EnergySamplingVars = {PreSamplerB, EMB1, EMB2, EMB3, PreSamplerE, EME1, EME2, EME3, HEC0, HEC1, HEC2, HEC3,
	TileBar0, TileBar1, TileBar2, TileGap1, TileGap2, TileGap3, TileExt0, TileExt1, TileExt2, FCAL0, FCAL1, FCAL2};	

	// end of the declaration --------------------------------

	Selection(TString source, TString treeName, TString type);
	void Configure(TString variables_data, TString vetos_data); // dopsat v C++, adresa na cteni .data filu, nejdriv variables, pak i vetos...

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
