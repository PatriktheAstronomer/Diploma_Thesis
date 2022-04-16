#include "TFile.h"
#include "TKey.h"
#include "TH1F.h"
#include "TH1D.h"
#include "TH2F.h"
#include "TH2D.h"
#include "TH3D.h"
#include "TF1.h"
#include "TPad.h"
#include "TCanvas.h"
#include <iostream>
#include <TStyle.h>
#include "TMarker.h"
#include "TLine.h"
#include "TText.h"
#include "TLatex.h"
#include "TMath.h"
#include "TTree.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TGraphAsymmErrors.h"
#include <sstream>

void SetHStyle( TH1* his, int iflag);
void SetHStyle_open( TH1F* his, int iflag);


void SetHStyle( TH1* his, int iflag)
{
    his->SetLineWidth(2);
	his->SetStats(0);
	his->GetXaxis()->SetLabelFont(43);
	his->GetXaxis()->SetLabelSize(32);
	his->GetXaxis()->SetTitleSize(36);
	his->GetXaxis()->SetTitleOffset(1.1);
	his->GetXaxis()->SetTitleFont(43);
	his->GetYaxis()->SetLabelFont(43);
	his->GetYaxis()->SetLabelSize(32);
	his->GetYaxis()->SetTitleSize(36);
	his->GetYaxis()->SetTitleOffset(1.1);
	his->GetYaxis()->SetTitleFont(43);
	
	//Set Color
	if( iflag == 0 ){
		his->SetLineColor(kBlack);
		his->SetLineWidth(2);
		his->SetMarkerColor(kBlack);
		his->SetMarkerStyle(20);
		his->SetMarkerSize(1.2);
  	} 
  	else if(iflag == 1 ){
		his->SetLineColor(kRed+1);
		his->SetLineWidth(2);
		his->SetMarkerColor(kRed+1);
		his->SetMarkerStyle(21);
		his->SetMarkerSize(1.2);
  	}
  	else if(iflag == 2 ){
		his->SetLineColor(kBlue+1);
		his->SetLineWidth(2);
		his->SetMarkerColor(kBlue+1);
		his->SetMarkerStyle(22);
		his->SetMarkerSize(1.5);
  	}
  	else if(iflag == 3 ){
		his->SetLineColor(kGreen+2);
		his->SetLineWidth(2);
		his->SetMarkerColor(kGreen+2);
		his->SetMarkerStyle(34);
		his->SetMarkerSize(1.5);
  	}
  	else if(iflag == 4 ){
		his->SetLineColor(kOrange+1);
		his->SetLineWidth(2);
		his->SetMarkerColor(kOrange+1);
		his->SetMarkerStyle(29);
		his->SetMarkerSize(1.6);
  	}
  	else if(iflag == 5 ){
		his->SetLineColor(kViolet);
		his->SetLineWidth(2);
		his->SetMarkerColor(kViolet);
		his->SetMarkerStyle(33);
		his->SetMarkerSize(1.6);
  	}
  	else if(iflag == 6 ){
		his->SetLineColor(kCyan+1);
		his->SetLineWidth(2);
		his->SetMarkerColor(kCyan+1);
		his->SetMarkerStyle(34);
		his->SetMarkerSize(1.6);
  	}
  	else if(iflag == 7 ){
		his->SetLineColor(2);
		his->SetLineWidth(2);
		his->SetMarkerColor(2);
		his->SetMarkerStyle(28);
		his->SetMarkerSize(1.7);
  	}
  	else if(iflag == 8 ){
		his->SetLineColor(kRed+3);
		his->SetLineWidth(2);
		his->SetMarkerColor(kRed+3);
		his->SetMarkerStyle(25);
		his->SetMarkerSize(1.1);
  	}
  	if( iflag == 9 ){
		his->SetLineColor(kBlack);
		his->SetLineWidth(2);
		his->SetMarkerColor(kBlack);
		his->SetMarkerStyle(24);
		his->SetMarkerSize(1.2);
  	} 
  	else if(iflag == 10 ){
		his->SetLineColor(kRed+1);
		his->SetLineWidth(2);
		his->SetMarkerColor(kRed+1);
		his->SetMarkerStyle(25);
		his->SetMarkerSize(1.2);
  	}
  	else if(iflag == 11 ){
		his->SetLineColor(kBlue+1);
		his->SetLineWidth(2);
		his->SetMarkerColor(kBlue+1);
		his->SetMarkerStyle(26);
		his->SetMarkerSize(1.5);
  	}
  	else if(iflag == 12 ){
		his->SetLineColor(kGreen+2);
		his->SetLineWidth(2);
		his->SetMarkerColor(kGreen+2);
		his->SetMarkerStyle(32);
		his->SetMarkerSize(1.5);
  	}
  	else if(iflag == 13 ){
		his->SetLineColor(kOrange+1);
		his->SetLineWidth(2);
		his->SetMarkerColor(kOrange+1);
		his->SetMarkerStyle(30);
		his->SetMarkerSize(1.6);
  	}   
 
  
}

void SetHStyle_open( TH1* his, int iflag)
{
    his->SetLineWidth(2);
	his->SetStats(0);
	his->GetXaxis()->SetLabelFont(43);
	his->GetXaxis()->SetLabelSize(30);
	his->GetXaxis()->SetTitleSize(32);
	his->GetXaxis()->SetTitleOffset(1.2);
	his->GetXaxis()->SetTitleFont(43);
	his->GetYaxis()->SetLabelFont(43);
	his->GetYaxis()->SetLabelSize(30);
	his->GetYaxis()->SetTitleSize(32);
	his->GetYaxis()->SetTitleOffset(1.2);
	his->GetYaxis()->SetTitleFont(43);
	
	//Set Color
	if( iflag == 0 ){
		his->SetLineColor(kBlack);
		his->SetLineWidth(2);
		his->SetMarkerColor(kBlack);
		his->SetMarkerStyle(24);
		his->SetMarkerSize(1.2);
  	} 
  	else if(iflag == 1 ){
		his->SetLineColor(kRed+1);
		his->SetLineWidth(2);
		his->SetMarkerColor(kRed+1);
		his->SetMarkerStyle(25);
		his->SetMarkerSize(1.2);
  	}
  	else if(iflag == 2 ){
		his->SetLineColor(kBlue+1);
		his->SetLineWidth(2);
		his->SetMarkerColor(kBlue+1);
		his->SetMarkerStyle(26);
		his->SetMarkerSize(1.5);
  	}
  	else if(iflag == 3 ){
		his->SetLineColor(kGreen+2);
		his->SetLineWidth(2);
		his->SetMarkerColor(kGreen+2);
		his->SetMarkerStyle(32);
		his->SetMarkerSize(1.5);
  	}
  	else if(iflag == 4 ){
		his->SetLineColor(kOrange+1);
		his->SetLineWidth(2);
		his->SetMarkerColor(kOrange+1);
		his->SetMarkerStyle(30);
		his->SetMarkerSize(1.6);
  	}
  	else if(iflag == 5 ){
		his->SetLineColor(kViolet);
		his->SetLineWidth(2);
		his->SetMarkerColor(kViolet);
		his->SetMarkerStyle(27);
		his->SetMarkerSize(1.6);
  	}
  	else if(iflag == 6 ){
		his->SetLineColor(kCyan+1);
		his->SetLineWidth(2);
		his->SetMarkerColor(kCyan+1);
		his->SetMarkerStyle(34);
		his->SetMarkerSize(1.6);
  	}
  	else if(iflag == 7 ){
		his->SetLineColor(46);
		his->SetLineWidth(2);
		his->SetMarkerColor(46);
		his->SetMarkerStyle(21);
		his->SetMarkerSize(1.1);
  	}
  	else if(iflag == 8 ){
		his->SetLineColor(kRed+3);
		his->SetLineWidth(2);
		his->SetMarkerColor(kRed+3);
		his->SetMarkerStyle(25);
		his->SetMarkerSize(1.1);
  	}    
}
