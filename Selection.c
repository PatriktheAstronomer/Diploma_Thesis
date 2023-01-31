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

void Selection::FormScalarSample(TString outname)
{
	m_outfile = new TFile(outname, "recreate");
	m_treeout = new TTree("training_dataset", "");
	CreateBranchScalar();
	training_flag = true;
}

void Selection::SetBranchAddress(std::vector<TString> list_of_branches_to_activate)
{
	/*
	for (auto branch in list_of_branches_to_activate){
		switch(branch){
			case "MC_weight":
				m_tree->SetBranchAddress("MC_weight",&MC_weight);
   				break;
			case "jet_eta":
				m_tree->SetBranchAddress("jet_eta",&jet_eta);
   				break;
			case "jet_pt":
				m_tree->SetBranchAddress("jet_pt",&jet_pt);
				break;   	
			case "jet_ntrk":
				m_tree->SetBranchAddress("jet_ntrk",&jet_ntrk);
   				break;
			case "jet_SumPtTrk": // pregenerovat casem i zakladni vstupni file, abych si vytvoril rtrk
				m_tree->SetBranchAddress("jet_SumPtTrk",&jet_SumPtTrk);
				break;   	
			case "jet_width:
				m_tree->SetBranchAddress("jet_width",&jet_width);
   				break;
			case "jet_N90":
				m_tree->SetBranchAddress("jet_N90", &jet_N90);
   				break;
			case "jet_EnergyPerSampling":
				m_tree->SetBranchAddress("jet_EnergyPerSampling", &jet_EnergyPerSampling);
   				break;
			case "corr_jet_pt":
				m_tree->SetBranchAddress("corr_jet_pt", &corr_jet_pt);
   				break;
			case "truth_jet_pt":
				m_tree->SetBranchAddress("truth_jet_pt",&truth_jet_pt);
				break;
			case "truth_jet_flavor":
   				m_tree->SetBranchAddress("truth_jet_flavor",&truth_jet_flavor);
				break;   	
			case "event_Centrality":
				m_tree->SetBranchAddress("event_Centrality",&event_Centrality);
   				break;
		}
	}
	*/
        m_tree->SetBranchAddress("MC_weight",&MC_weight);
        m_tree->SetBranchAddress("jet_eta",&jet_eta);
        m_tree->SetBranchAddress("jet_pt",&jet_pt);
        m_tree->SetBranchAddress("jet_ntrk",&jet_ntrk);
        m_tree->SetBranchAddress("jet_SumPtTrk",&jet_SumPtTrk);
        m_tree->SetBranchAddress("jet_width",&jet_width);
        m_tree->SetBranchAddress("jet_N90", &jet_N90);
        m_tree->SetBranchAddress("jet_EnergyPerSampling", &jet_EnergyPerSampling);
	//m_tree->SetBranchAddress("corr_jet_pt", &corr_jet_pt); ---> odstranit
	m_tree->SetBranchAddress("truth_jet_pt",&truth_jet_pt);
        m_tree->SetBranchAddress("truth_jet_flavor",&truth_jet_flavor);
        m_tree->SetBranchAddress("event_Centrality",&event_Centrality);
}

void Selection::CreateBranchScalar()
{
   std::cout << "Setting branch address for scalar variables" << "\n";
   m_treeout->Branch("MC_weight_scalar", &MC_weight_scalar, "MC_weight/D"); 
   // of course MC_weight is scalar all the time, however there each occurance of this value is multiplied by jet size
   m_treeout->Branch("jet_eta_scalar", &jet_eta_scalar, "float");
   m_treeout->Branch("jet_pt_scalar", &jet_pt_scalar, "float");
   m_treeout->Branch("jet_ntrk_scalar", &jet_ntrk_scalar, "float");
   m_treeout->Branch("jet_rtrk_scalar", &jet_rtrk_scalar, "float"); 
   m_treeout->Branch("jet_width_scalar", &jet_width_scalar, "float");
   m_treeout->Branch("jet_N90_scalar", &jet_N90_scalar, "float");
   m_treeout->Branch("truth_jet_pt_scalar", &truth_jet_pt_scalar, "float");
   m_treeout->Branch("jet_response_scalar", &jet_response_scalar, "float");
   m_treeout->Branch("truth_jet_flavor_scalar", &truth_jet_flavor_scalar, "float");
// used in the scalar generator process
   
   // extended_1
   m_treeout->Branch("jet_peta_scalar", &jet_peta_scalar, "float");

   // geo_extension
   m_treeout->Branch("jet_EMB_fraction", &jet_EMB_fraction, "float");
   m_treeout->Branch("jet_EME_fraction", &jet_EME_fraction, "float");
   m_treeout->Branch("jet_HEC_fraction", &jet_HEC_fraction, "float");
   m_treeout->Branch("jet_TILE_fraction", &jet_TILE_fraction, "float");
   m_treeout->Branch("jet_FCAL_fraction", &jet_FCAL_fraction, "float");
   // geo_extension_2
   m_treeout->Branch("jet_TILE_BAR_fraction", &jet_TILE_BAR_fraction, "float");
   m_treeout->Branch("jet_TILE_EXTENDED_fraction", &jet_TILE_EXTENDED_fraction, "float");
}

void Selection::BookHistograms()
{
    InspectedVars.insert(InspectedVars.end(), EnergySamplingVars.begin(), EnergySamplingVars.end());

    for(int iCent = 0; iCent < m_centralityBinsN; iCent++){
	std::vector<TH3F*> helping_vct;
   	for (auto &var : InspectedVars){
		std::string name = "";
		name.append(var.m_name);
		name.append("_cent");
		name.append(std::to_string(iCent));
		name.append("_type");
		name.append(std::to_string(m_dataType));
		h_3F = new TH3F(name.data(), ";jet p_{T} [GeV]", pT.m_bin_count-1, pT.m_bins.data(), response.m_bin_count-1, response.m_bins.data(), var.m_bin_count-1, var.m_bins.data());
		h_3F->GetXaxis()->SetTitle("pT");
		h_3F->GetYaxis()->SetTitle("response");
		h_3F->GetZaxis()->SetTitle(var.m_name);
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
                                Float_t pTt = truth_jet_pt->at(j);
                                Float_t pTr = jet_pt->at(j);

				// if (pTr  == -999) continue; // mismatching ---> contained in the next ones
				if (pTr < 20 && m_dataType == 0) continue; // ! pT veto per jet in pp
				if (pTr < 30 && m_dataType == 1) continue; // ! pT veto per jet in PbPb

				// jet flavor selection - d, u, s, c, b & g -> 1, 2, 3, 4, 5 a 21
				// placed in the name of datasample
				//if (truth_jet_flavor->at(j) < 1 || truth_jet_flavor->at(j) > 5) continue;
				//if (truth_jet_flavor->at(j) != 21) continue;				

		
				std::vector<Float_t> inspectedVars = {jet_eta->at(j), jet_ntrk->at(j), jet_N90->at(j), jet_width->at(j)}; //rucne setupovane

// temporal -> till we start to handle calo values per partes
				std::vector<Float_t> energySamplingVars;
			
				for (unsigned int k = 0; k < EnergySamplingVars.size(); k++) energySamplingVars.push_back(jet_EnergyPerSampling->at(j).at(k));
				inspectedVars.insert(inspectedVars.end(), energySamplingVars.begin(), energySamplingVars.end());
				unsigned int varCount = inspectedVars.size();


				// V ramci optimatimalizace by bylo zajimave se podivat, jestli se tohle vubec deje... prijde mi superfluous ---> otestovat postupne v pp in PbPb
				if (pTr  <= 0 || pTt  <= 0) continue; // matched based distance
				if (event_Centrality < 0) continue;					

				for (unsigned int k = 0; k < varCount; k++){
					responseCentrVars[event_Centrality][k]->Fill(pTt, pTr/pTt, inspectedVars[k], MC_weight);
					// pp is written into 0th component of the responseCentrVars, PbPb into 0-7th as pp has the value 0
				}
			}
                }
     	}
}

void Selection::FormTrainingSample(Long64_t nEntries)
{
	int debug_counter = 0;
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
                                Float_t pTt = truth_jet_pt->at(j);
                                Float_t pTr = jet_pt->at(j);

                                // if (pTr  == -999) continue; // mismatching ---> contained in the next ones
                                if (pTr <= 0) continue; // ! pT veto per jet in pp
				if (truth_jet_flavor->at(j) < 1) continue;

                                if (training_flag && !m_dataType){
					debug_counter++;
					MC_weight_scalar = MC_weight;
                                        jet_pt_scalar = jet_pt->at(j);
                                        jet_eta_scalar = abs(jet_eta->at(j));
                                        jet_ntrk_scalar = jet_ntrk->at(j);
                                        jet_rtrk_scalar = jet_SumPtTrk->at(j)/jet_pt->at(j)/1000; //MeV to GeV
                                        jet_width_scalar = jet_width->at(j);
                                        jet_N90_scalar = jet_N90->at(j);
					jet_response_scalar = jet_pt->at(j)/truth_jet_pt->at(j); //binned later variously before used for classification-based regression
                                        truth_jet_pt_scalar = truth_jet_pt->at(j);

					// extension 1
					jet_peta_scalar = jet_pt->at(j) * jet_eta->at(j);

					//filing pro binary
					if (truth_jet_flavor->at(j) == 21){
						truth_jet_flavor_scalar = -1; // gluon
					}
					else{
						truth_jet_flavor_scalar	= 1; // kvark 
					}
                                        //truth_jet_flavor_scalar = truth_jet_flavor->at(j);

					// geo extension
					std::vector<Float_t> energies = jet_EnergyPerSampling->at(j);
					jet_EMB_fraction = jet_EME_fraction = jet_HEC_fraction = jet_TILE_fraction = jet_FCAL_fraction = 0;
				
					for (int i = 0; i < 4; i++){
						jet_EMB_fraction += energies.at(i);
						jet_EME_fraction += energies.at(4+i);
						jet_HEC_fraction += energies.at(8+i);
					}
					for (int i = 12; i < 21; i++) jet_TILE_fraction += energies.at(i);
					for (int i = 21; i < 24; i++) jet_FCAL_fraction += energies.at(i);
					// geo extension 2
					jet_TILE_BAR_fraction = jet_TILE_EXTENDED_fraction = 0;
					for (int i = 12; i < 16; i++) jet_TILE_BAR_fraction += energies.at(i);
                                        for (int i = 20; i < 24; i++) jet_TILE_EXTENDED_fraction += energies.at(i);

                                m_treeout->Fill();
                                }
			}
		}
	}
	std::cout << "number of scalar inputs written: "<< debug_counter << std::endl;
}



void Selection::CalcRMSE(Float_t jetPtVeto, bool corrected_file) // mismatching solved by pT veto
{
	// if file is corrected, we calculate metrics and work with corr_jet_pt in RMSE calculations instead of truth_jet_pt
        int statSize = 1;
	std::vector<Int_t> number_of_records(m_centralityBinsN, 0);
	std::vector<Float_t> error_vec(m_centralityBinsN, 0);

	if (corrected_file){
	        Float_t improved_count;
		Float_t worsen_count;
                for (Long64_t i=0 ; i<m_nEntries; i++){
                        m_tree->GetEntry(i);
                        if (i != 0){
                                double power=std::floor(log10(i));
                                statSize=(int)std::pow(10.,power);
                        }
                        if (i%statSize==0) std::cout << "Processing event: " << i << std::endl;
                        Int_t jet_size = truth_jet_pt->size();
                        if (jet_size){
                                for (int j = 0; j < jet_size; j++){
                                        if (corr_jet_pt->at(j) < jetPtVeto) continue; // pT veto for given statistics to be described
                                        error_vec[event_Centrality] += (corr_jet_pt->at(j)-truth_jet_pt->at(j))*(corr_jet_pt->at(j)-truth_jet_pt->at(j));
                                        number_of_records[event_Centrality]++;
					if (abs(corr_jet_pt->at(j) - truth_jet_pt->at(j)) <= abs(jet_pt->at(j) - truth_jet_pt->at(j))) improved_count++;
					else worsen_count++;
				}
                        }
                }
        	std::cout.precision(5);
		std::cout << "Improvement ratio is  " << improved_count/worsen_count << std::endl;
	}
	else{
        	for (Long64_t i=0 ; i<m_nEntries; i++){
                	m_tree->GetEntry(i);
                	if (i != 0){
                        	double power=std::floor(log10(i));
                        	statSize=(int)std::pow(10.,power);
                	}
                	if (i%statSize==0) std::cout << "Processing event: " << i << std::endl;
                	Int_t jet_size = truth_jet_pt->size();
                	if (jet_size){
                        	for (int j = 0; j < jet_size; j++){
                                	if (jet_pt->at(j) < jetPtVeto) continue; // pT veto for given statistics to be described
					error_vec[event_Centrality] += (jet_pt->at(j)-truth_jet_pt->at(j))*(jet_pt->at(j)-truth_jet_pt->at(j));
					number_of_records[event_Centrality]++;
				}
			}
		}
	}
	std::cout.precision(5);
	for (int c=0; c < m_centralityBinsN; c++) {
		std::cout << "Centrality " << c << " has RMSE " << sqrt(error_vec[c]/number_of_records[c]) << std::endl;
	}
	std::cout << "Overall centrality is " << sqrt(std::accumulate(error_vec.begin(), error_vec.end(), 0.0)/std::accumulate(number_of_records.begin(), number_of_records.end(), 0));

}


void Selection::Write(string outName)
{
	if(training_flag && !m_dataType){
		std::cout << "pp training dataset processed" << "\n";
		m_outfile->Write();
		std::cout << m_outfile->GetName() << " datafile saved" << "\n";
		m_outfile->Close();
	}

	else{
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
				delete responseCentrVars.at(c).at(d);
			}
		}
		f_out->Close();
		std::cout << f_out->GetName() << " datafile saved" << "\n";
	}
	m_source->Close();
}
