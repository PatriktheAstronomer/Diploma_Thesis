#ifndef PROCESS_H
#define PROCESS_H

#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TF1.h"
#include "TH2.h"
#include "TH3.h"
#include "TDirectory.h"
#include "TKey.h"
#include <vector>
#include <iostream>

class Process
{
private:
	TFile *m_source;
public:
	std::vector<std::string> histogram_name;
	std::vector<std::vector<std::vector<float>>> processed_data;

	Process(TString source);
	void ReadFile();
	void MakeProjections(TH3F* h_3F);
	std::vector<float> FitResponse(TH1D* h_1D);
};
#endif

