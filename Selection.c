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
	m_centralityBinsN = 8;
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
    for(int iCent = 0; iCent < m_centralityBinsN; iCent++){
	std::vector<TH3F*> helping_vct;
   	for (auto &var : InspectedVars){
		std::string name = "h3_resp_";
		name.append(var.m_name);
		name.append("_cent");
		name.append(std::to_string(iCent));
		name.append("_type");
		name.append(std::to_string(m_dataType));
		std::cout << var.m_name << iCent << m_dataType << "\n";
		h_3F = new TH3F(name.data(), ";jet p_{T} [GeV]", pT.m_bin_count-3, pT.m_bins.data(), response.m_bin_count-3, response.m_bins.data(), var.m_bin_count-3, var.m_bins.data());
		h_3F->Sumw2();
		helping_vct.push_back(h_3F);
	}

	responseCentrVars.push_back(helping_vct);
   } 
   // a bin to bin plotit promenne...
   // vse pak zapisu do sady matic dle centrality a var! --- 1 sada pro meany a druha pro sigmy
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

				std::vector<Float_t> inspectedVars = {jet_ntrk->at(j), jet_rtrk->at(j), jet_width->at(j)}; // tato cast se setupuju rukou! musi sedet poradi!!!			
				unsigned int varCount = inspectedVars.size();

				if (InspectedVars.size() != varCount){
					std::cout << "Wrong setup of inspected variables";
					exit (EXIT_FAILURE);
				}
							
        			// if (fabs(truth_jet_flavor->at(j)) == 21 || truth_jet_flavor->at(j) < 0) continue;
				if (jet_pt->at(j) <= 0 || truth_jet_pt->at(j) <= 0) continue; // matched based distance
				if (event_Centrality < 0) continue;					
				for (unsigned int k = 0; k < varCount; k++){ 
					responseCentrVars[event_Centrality][k]->Fill(pTt, pTr/pTt, inspectedVars[j], MC_weight);
					// pp is written into 0th component of the responseCentrVars, PbPb into 0-7th as pp has the value 0
				}
			}
                }
     	}
}

void Selection::Write(string outName)
{
   outName.append(".root");
   TFile *f_out = new TFile(outName.data(), "RECREATE");
   for (unsigned int c = 0; c < responseCentrVars.size(); c++){
	std::string name = "centrality_";
	name.append(std::to_string(c));
	f_out->cd();
	gDirectory->mkdir(name.data());
	for (unsigned int d = 0; d < responseCentrVars.at(c).size(); d++){
		f_out->cd(name.data());
        	responseCentrVars.at(c).at(d)->Write();
	}
   }
   f_out->Close();
   m_source->Close();
}
