#include "Variables.h"
Variables::Variables(){}
Variables::Variables(TString name, Int_t bin_count, Float_t lower_range, Float_t upper_range)
{
	SetName(name);
	CalculateUniBins(bin_count, lower_range, upper_range);
	SetBinCount();	
}


Variables::Variables(TString name, Float_t lower_range, Float_t upper_range)
{
        SetName(name);
        CalculateLogBins(lower_range, upper_range);
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

void Variables::CalculateLogBins(Float_t lower_range, Float_t upper_range)
{ 
	lower_range = log10(lower_range);
	int i = 0;
	while(upper_range > pow(10, lower_range + i* m_firstBinWidth)){
		m_bins.push_back(pow(10, lower_range + i * m_firstBinWidth));
		i++;
	}
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
