#include "Selection.h"
Selection::Selection(TString source, TString treeName, TString type)
{
	SetDataType(type);
	SetSource(source);
	SetTreeName(treeName);
	GetTTree();
}

void Selection::SetDataType(TString type)
{
  if(type == "pp"){
	m_dataType = 0;
	m_centralityBinsN = 1;
  }
  else if(type =="PbPb"){
	m_dataType = 1;
	m_centralityBinsN = 7;
  }
  else{
	std::cout << "Unknow data type inserted\n";
  }
}

void Selection::SetSource(TString source)
{
  m_source = new TFile(source);
}

void Selection::SetTreeName(TString treeName)
{
  m_treeName = treeName;
}

void Selection::GetTTree()
{
 m_tree = (TTree*)m_source->Get(m_treeName);
 m_nEntries = m_tree->GetEntries();
}

void Selection::SetBranchAddress()
{
   m_tree->SetBranchAddress("MC_weight",&MC_weight);
   m_tree->SetBranchAddress("jet_eta",&jet_eta);
   m_tree->SetBranchAddress("jet_pt",&jet_pt);
   m_tree->SetBranchAddress("jet_ntrk",&jet_ntrk);
   m_tree->SetBranchAddress("jet_rtrk",&jet_rtrk);
   m_tree->SetBranchAddress("jet_width",&jet_width);
   m_tree->SetBranchAddress("truth_jet_pt",&truth_jet_pt);
   m_tree->SetBranchAddress("truth_jet_flavor",&truth_jet_flavor);
   m_tree->SetBranchAddress("event_Centrality",&event_Centrality);
}

void Selection::BookHistograms()
{
   for(int j=1; j<=45; j++){ // 45 bins from 0 to 4.5
        centralityBins[j-1] = float(j)/10;
   }
   for(int k=1; k<=100; k++){ // 50 bins from 0 to 2
        responseBins[k-1] = float(k)/50;
   }
   
   for(int iCent = 0; iCent <= m_centralityBinsN; iCent++){
	std::vector<TH3F*> helping_vct;
   	for (auto &var : vars){
		std::string name = "h3_resp_";
		name.append(var);
		name.append("_cent");
		name.append(std::to_string(iCent));
		h_3F = new TH3F(name.data(), ";jet p_{T} [GeV]", sizeof(jetptBins)/sizeof(jetptBins[0]) - 1 , jetptBins, sizeof(responseBins)/sizeof(responseBins[0]) - 1 , responseBins, sizeof(centralityBins)/sizeof(centralityBins[0]) - 1 , centralityBins);
   		h_3F->Sumw2();
		helping_vct.push_back(h_3F);
	}
	responseCentrVars.push_back(helping_vct);
   }
}

void Selection::EventLoop(Long64_t nEntries)
{
	if(!nEntries) nEntries = this->m_nEntries;
	int statSize = 1;
	for (Long64_t i=0 ; i<nEntries; i++) {
        	m_tree->GetEntry(i);
        	if(i!=0){
            		double power=std::floor(log10(i));
            		statSize=(int)std::pow(10.,power);
        	}
		if(i%statSize==0) std::cout << "Processing event: " << i << std::endl;
        	Int_t jet_size = truth_jet_pt->size();
        	if (jet_size){
                	for (int j = 0; j < jet_size; j++){
				if (jet_pt->at(j) == -999) continue; // mismatching
				if (fabs(jet_eta->at(j)) > m_eta_veto) continue;
				Float_t pTt = truth_jet_pt->at(j);
				Float_t pTr = jet_pt->at(j);
				std::vector<Float_t> inspectedVars = {jet_rtrk->at(j), jet_ntrk->at(j), jet_width->at(j)};			
				Int_t varCount = inspectedVars.size();				

        			// if (fabs(truth_jet_flavor->at(j)) == 21 || truth_jet_flavor->at(j) < 0) continue;
				if (jet_pt->at(j) <= 0 || truth_jet_pt->at(j) <= 0) continue; // matched based distance
				if (event_Centrality < 0) continue;						
				for (int k = 0; k < varCount; k++){ 
					responseCentrVars[event_Centrality][k]->Fill(pTt, pTr/pTt, inspectedVars[j], MC_weight);
					// pp is written into 0th component of the responseCentrVars, PbPb into 1-7th
				}
			}
                }
     	}
}

void Selection::Write(string outName)
{
   outName.append(".root");
   TFile *f_out = new TFile(outName.data(), "RECREATE");
   for (auto &vcts : responseCentrVars){
	for (auto &histo : vcts){
        histo->Write();
	}
   }
   f_out->Close();
   m_source->Close();
}
