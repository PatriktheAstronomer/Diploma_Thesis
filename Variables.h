#ifndef VARIABLES_H
#define VARIABLES_H

#include "TROOT.h"
#include <vector>
#include <iostream>
#include "lib/logspace.hpp"


class Variables
{
public:
	TString m_name;	
	Float_t m_bin_count;
	Float_t m_lower_range;
	Float_t m_upper_range;
	std::vector<Float_t> m_bins;

	Variables();
	Variables(TString name, Int_t bin_count, Float_t lower_range, Float_t upper_range, TString type);
	Variables(TString name, std::vector<Float_t> bins);
	void SetName(TString name);
	void CalculateLogBins(Int_t bin_count, Float_t lower_range, Float_t upper_range);
	void CalculateUniBins(Int_t bin_count, Float_t lower_range, Float_t upper_range);
	void SetBinCount();
};

#endif
