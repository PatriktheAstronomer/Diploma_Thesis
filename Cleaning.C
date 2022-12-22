#include "TFile.h"
#include "TTree.h"

void Cleaning(){
   string iFilnename = "/mnt/scratch1/novotnyp/data/user.mrybar.PbPb_MC_ForPatrik_r004_ANALYSIS.root";
   string oFilnename = "/mnt/scratch1/novotnyp/data/PbPb_cleaned.root";
  
   //Get old file, old tree and set top branch address
   TFile *oldfile = new TFile(iFilnename.c_str());
   TTree *oldtree = (TTree*)oldfile->Get("AntiKt4HI");  
  
   Long64_t nentries = oldtree->GetEntries();
  
   // pridat pozdeji sem jeste centralitu, abych mohl provadet full studii
   std::vector<Float_t> * jet_eta = 0;
   std::vector<Float_t> * jet_pt = 0;
   std::vector<Int_t> * jet_ntrk = 0; // je tohle to jedine, co potrebujeme?
   std::vector<Float_t> * jet_width = 0;
   std::vector<Float_t> * jet_SumPtTrk = 0;
   std::vector<Float_t> * jet_N90 = 0;

   oldtree->SetBranchAddress("jet_eta",&jet_eta);
   oldtree->SetBranchAddress("jet_pt",&jet_pt);
   oldtree->SetBranchAddress("jet_ntrk",&jet_ntrk);
   oldtree->SetBranchAddress("jet_SumPtTrk",&jet_SumPtTrk);
   oldtree->SetBranchAddress("jet_width",&jet_width);
   oldtree->SetBranchAddress("jet_N90", &jet_N90);
   oldtree->SetBranchStatus("*",1);

   //Create a new file + a clone of old tree in new file
   TFile *newfile = new TFile(oFilnename.c_str(),"recreate");
   TTree *newtree = oldtree->CloneTree(0);

   for (Long64_t i=0; i<nentries; i++) {
      oldtree->GetEntry(i);
      for (Long64_t j=jet_eta->size()-1; j >= 0; j--){ // substracting from vector from the end
          jet_SumPtTrk->at(j) = jet_SumPtTrk->at(j)/jet_pt->at(j)/1000; //MeV to GeV conversion
          if (jet_pt->at(j)  < 0){ //remove mismatched jets
              jet_eta->erase(jet_eta->begin()+j);
              jet_pt->erase(jet_pt->begin()+j);
              jet_ntrk->erase(jet_ntrk->begin()+j);
              jet_width->erase(jet_width->begin()+j);
              jet_SumPtTrk->erase(jet_SumPtTrk->begin()+j);
              jet_N90->erase(jet_N90->begin()+j);
	  }
      }
      newtree->Fill();
   }
   newtree->AutoSave();
   delete oldfile;
   delete newfile;
}


