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

	Variables pT = Variables("pT", 15, 30, 1050, "log");
        Variables response = Variables("response", 99, 0, 2, "uni");
	Variables eta = Variables("eta", {0.0, 0.3, 0.8, 1.2, 2.1, 2.8, 3.2, 4.5});
        Variables ntrk = Variables("ntrk", 20, 0.01, 50, "log");
	Variables N90 = Variables ("N90", 50, 0.01, 50.265, "uni");
        //Variables sumpTtrk = Variables("SumpTtrk", 100, 0, 1000000000); // ?? proper norm ?? move back to rtrk

	// only trks above 4 GeV used, ghost associated trks
        Variables width = Variables("width", 30, 0.0001, 1, "log");

        std::vector<Variables> InspectedVars = {eta, ntrk, N90, width}; // eta is the first, for purpose of JES/JER diagrams
	
	// section with calo variables:
	Variables PreSamplerB = Variables("Rel. fraction of E in PreSamplerB", 30, 0.0001, 1, "log");
	Variables EMB1 = Variables("Rel. fraction of E in EMB1", 30, 0.0001, 1, "log");
	Variables EMB2 = Variables("Rel. fraction of E in EMB2", 30, 0.0001, 1, "log");
	Variables EMB3 = Variables("Rel. fraction of E in EMB3", 30, 0.0001, 1, "log");

	Variables PreSamplerE = Variables("Rel. fraction of E in PreSamplerE", 30, 0.0001, 1, "log");
        Variables EME1 = Variables("Rel. fraction of E in EME1", 30, 0.0001, 1, "log");
        Variables EME2 = Variables("Rel. fraction of E in EME2", 30, 0.0001, 1, "log");
        Variables EME3 = Variables("Rel. fraction of E in EME3", 30, 0.0001, 1, "log");

        Variables HEC0 = Variables("Rel. fraction of E in HEC0", 30, 0.0001, 1, "log");
        Variables HEC1 = Variables("Rel. fraction of E in HEC1", 30, 0.0001, 1, "log");
        Variables HEC2 = Variables("Rel. fraction of E in HEC2", 30, 0.0001, 1, "log");
        Variables HEC3 = Variables("Rel. fraction of E in HEC3", 30, 0.0001, 1, "log");

        Variables TileBar0 = Variables("Rel. fraction of E in TileBar0", 30, 0.0001, 1, "log");
        Variables TileBar1 = Variables("Rel. fraction of E in TileBar1", 30, 0.0001, 1, "log");
        Variables TileBar2 = Variables("Rel. fraction of E in TileBar2", 30, 0.0001, 1, "log");
        
	Variables TileGap1 = Variables("Rel. fraction of E in TileGap1", 30, 0.0001, 1, "log");
        Variables TileGap2 = Variables("Rel. fraction of E in TileGap2", 30, 0.0001, 1, "log");
        Variables TileGap3 = Variables("Rel. fraction of E in TileGap3", 30, 0.0001, 1, "log");

	Variables TileExt0 = Variables("Rel. fraction of E in TileExt0", 30, 0.0001, 1, "log");
        Variables TileExt1 = Variables("Rel. fraction of E in TileExt1", 30, 0.0001, 1, "log");
        Variables TileExt2 = Variables("Rel. fraction of E in TileExt2", 30, 0.0001, 1, "log");

        Variables FCAL0 = Variables("Rel. fraction of E in FCAL0", 30, 0.0001, 1, "log");
        Variables FCAL1 = Variables("Rel. fraction of E in FCAL1", 30, 0.0001, 1, "log");
        Variables FCAL2 = Variables("Rel. fraction of E in FCAL2", 30, 0.0001, 1, "log");

	std::vector<Variables> EnergySamplingVars = {PreSamplerB, EMB1, EMB2, EMB3, PreSamplerE, EME1, EME2, EME3, HEC0, HEC1, HEC2, HEC3,
	TileBar0, TileBar1, TileBar2, TileGap1, TileGap2, TileGap3, TileExt0, TileExt1, TileExt2, FCAL0, FCAL1, FCAL2};	

	// end of the declaration --------------------------------

	Selection(TString source, TString treeName, TString type);
	void SetSource(TString source);
	void SetTreeName(TString treeName);
	void SetDataType(TString type);
	void GetTTree();

	void FormScalarSample(TString outname);	
	void SetBranchAddress();
	void CreateBranchScalar();
	void BookHistograms();
	void EventLoop(Long64_t nEntries = 0);
	void FormTrainingSample(Long64_t nEntries = 0);
	void CalcRMSE(Float_t jetPtVeto = 0);
	void Write(string outfile = "");
};


#endif
