#include "Variables.h"
Variables::Variables(){}
Variables::Variables(TString name, Int_t bin_count, Float_t lower_range, Float_t upper_range, TString type)
{
	SetName(name);
	if (type == "uni"){
		CalculateUniBins(bin_count, lower_range, upper_range);
	}
	else if (type == "log"){
		CalculateLogBins(bin_count, lower_range, upper_range);
	}
	SetBinCount();	
}

Variables::Variables(TString name, std::vector<Float_t> bins)
{
        SetName(name);
        m_bins = bins;
        SetBinCount();
}

void Variables::SetName(TString name)
{
	m_name = name;
}

void Variables::CalculateLogBins(Int_t bin_count, Float_t lower_range, Float_t upper_range)
{ 
	lower_range = log10(lower_range);
	upper_range = log10(upper_range);
	auto vlog = nzl::nice::make_logspace<std::vector<Float_t>>(lower_range, upper_range, bin_count);
	for (const auto & item : vlog) m_bins.push_back(item);
}

void Variables::CalculateUniBins(Int_t bin_count, Float_t lower_range, Float_t upper_range)
{
	Float_t step = (upper_range-lower_range)/bin_count;
	Float_t val = lower_range;
        for (int k = 0; k <= bin_count-1; k++){
                m_bins.push_back(val);
		val+=step;
        }

}

void Variables::SetBinCount()
{
	m_bin_count = m_bins.size();
}
