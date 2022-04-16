from math import sqrt
import ROOT
from ROOT import kBlack, kBlue, kRed, kGreen, kOrange, kViolet, kCyan, kGray, kAzure
from ROOT import TH1

def SetHStyle(his, flag, FullColor = False, NotFilled = False):

    his.SetLineWidth(2)
    #his.SetStats(0)
    his.GetXaxis().SetLabelFont(43)
    his.GetXaxis().SetLabelSize(32)
    his.GetXaxis().SetTitleSize(36)
    his.GetXaxis().SetTitleOffset(1.1)
    his.GetXaxis().SetTitleFont(43)
    his.GetYaxis().SetLabelFont(43)
    his.GetYaxis().SetLabelSize(32)
    his.GetYaxis().SetTitleSize(36)
    his.GetYaxis().SetTitleOffset(1.1)
    his.GetYaxis().SetTitleFont(43)
    
    #Set Color
    if  flag == 0 :
        his.SetLineColor(kBlack)
        if not his.InheritsFrom(TH1.Class()) and not FullColor and not NotFilled: his.SetFillColorAlpha(kGray, 1.0);
        elif FullColor: his.SetFillColor(kBlack)
        his.SetLineWidth(2)
        his.SetMarkerColor(kBlack)
        his.SetMarkerStyle(20)
        his.SetMarkerSize(1.4)
 
    elif flag == 1 :
        his.SetLineColor(kRed+1)
        if not his.InheritsFrom(TH1.Class()) and not FullColor and not NotFilled: his.SetFillColorAlpha(kRed-10, 0.80);
        elif FullColor: his.SetFillColor(kRed+1)
        his.SetLineWidth(2)
        his.SetMarkerColor(kRed+1)
        his.SetMarkerStyle(21)
        his.SetMarkerSize(1.4)

    elif flag == 2 :
        his.SetLineColor(kAzure-3)
        if not his.InheritsFrom(TH1.Class()) and not FullColor and not NotFilled: his.SetFillColorAlpha(kAzure-9, 0.70);
        elif FullColor: his.SetFillColor(kAzure-3)
        his.SetLineWidth(2)
        his.SetMarkerColor(kBlue+1)
        his.SetMarkerStyle(22)
        his.SetMarkerSize(1.7)

    elif flag == 3 :
        his.SetLineColor(kGreen+2)
        if not his.InheritsFrom(TH1.Class()) and not FullColor and not NotFilled: his.SetFillColorAlpha(kGreen-10, 0.60);
        elif FullColor: his.SetFillColor(kGreen+2)
        his.SetLineWidth(2)
        his.SetMarkerColor(kGreen+2)
        his.SetMarkerStyle(34)
        his.SetMarkerSize(1.7)

    elif flag == 4 :
        his.SetLineColor(kOrange+1)
        his.SetLineWidth(2)
        if not his.InheritsFrom(TH1.Class()) and not FullColor and not NotFilled: his.SetFillColorAlpha(kOrange-9, 0.90);
        elif FullColor: his.SetFillColor(kOrange+1)
        his.SetMarkerColor(kOrange+1)
        his.SetMarkerStyle(29)
        his.SetMarkerSize(1.9)

    elif flag == 5 :
        his.SetLineColor(kViolet)
        if not his.InheritsFrom(TH1.Class()) and not FullColor and not NotFilled: his.SetFillColorAlpha(kViolet-4, 0.30);
        elif FullColor: his.SetFillColor(kViolet)
        his.SetLineWidth(2)
        his.SetMarkerColor(kViolet)
        his.SetMarkerStyle(33)
        his.SetMarkerSize(1.7)

    elif flag == 6 :
        his.SetLineColor(kCyan+1)
        if FullColor: his.SetFillColor(kCyan+1)
        his.SetLineWidth(2)
        his.SetMarkerColor(kCyan+1)
        his.SetMarkerStyle(34)
        his.SetMarkerSize(1.6)

    elif flag == 7 :
        his.SetLineColor(kBlue-10)
        if FullColor: his.SetFillColor(kBlue-10)
        his.SetLineWidth(2)
        his.SetMarkerColor(kBlue-10)
        his.SetMarkerStyle(34)
        his.SetMarkerSize(1.6)

    elif flag == 8 :
        his.SetLineColor(kRed+3)
        his.SetLineWidth(2)
        his.SetMarkerColor(kRed+3)
        his.SetMarkerStyle(25)
        his.SetMarkerSize(1.1)

    elif flag == 9 :
        his.SetLineColor(kBlack)
        his.SetLineWidth(2)
        his.SetMarkerColor(kBlack)
        his.SetMarkerStyle(24)
        his.SetMarkerSize(1.2)
 
    elif flag == 10 :
        his.SetLineColor(kRed+1)
        his.SetLineWidth(2)
        his.SetMarkerColor(kRed+1)
        his.SetMarkerStyle(25)
        his.SetMarkerSize(1.2)

    elif flag == 11 :
        his.SetLineColor(kBlue+1)
        his.SetLineWidth(2)
        his.SetMarkerColor(kBlue+1)
        his.SetMarkerStyle(26)
        his.SetMarkerSize(1.5)

    elif flag == 12 :
        his.SetLineColor(kGreen+2)
        his.SetLineWidth(2)
        his.SetMarkerColor(kGreen+2)
        his.SetMarkerStyle(32)
        his.SetMarkerSize(1.5)

    elif flag == 13 :
        his.SetLineColor(kOrange+1)
        his.SetLineWidth(2)
        his.SetMarkerColor(kOrange+1)
        his.SetMarkerStyle(30)
        his.SetMarkerSize(1.6)

def SetHStyle_open(his, flag):

    his.SetLineWidth(2)
    #his.SetStats(0)
    his.GetXaxis().SetLabelFont(43)
    his.GetXaxis().SetLabelSize(30)
    his.GetXaxis().SetTitleSize(32)
    his.GetXaxis().SetTitleOffset(1.2)
    his.GetXaxis().SetTitleFont(43)
    his.GetYaxis().SetLabelFont(43)
    his.GetYaxis().SetLabelSize(30)
    his.GetYaxis().SetTitleSize(32)
    his.GetYaxis().SetTitleOffset(1.2)
    his.GetYaxis().SetTitleFont(43)
    
    #Set Color
    if  flag == 0 :
        his.SetLineColor(kBlack)
        if not his.InheritsFrom(TH1.Class()): his.SetFillColorAlpha(kGray, 1.0);
        his.SetLineWidth(2)
        his.SetMarkerColor(kBlack)
        his.SetMarkerStyle(24)
        his.SetMarkerSize(1.2)
 
    elif flag == 1 :
        his.SetLineColor(kRed+1)
        his.SetLineWidth(2)
        his.SetMarkerColor(kRed+1)
        his.SetMarkerStyle(25)
        his.SetMarkerSize(1.2)

    elif flag == 2 :
        his.SetLineColor(kBlue+1)
        his.SetLineWidth(2)
        his.SetMarkerColor(kBlue+1)
        his.SetMarkerStyle(26)
        his.SetMarkerSize(1.5)

    elif flag == 3 :
        his.SetLineColor(kGreen+2)
        his.SetLineWidth(2)
        his.SetMarkerColor(kGreen+2)
        his.SetMarkerStyle(32)
        his.SetMarkerSize(1.5)

    elif flag == 4 :
        his.SetLineColor(kOrange+1)
        his.SetLineWidth(2)
        his.SetMarkerColor(kOrange+1)
        his.SetMarkerStyle(30)
        his.SetMarkerSize(1.6)

    elif flag == 5 :
        his.SetLineColor(kViolet)
        his.SetLineWidth(2)
        his.SetMarkerColor(kViolet)
        his.SetMarkerStyle(27)
        his.SetMarkerSize(1.6)

    elif flag == 6 :
        his.SetLineColor(kCyan+1)
        his.SetLineWidth(2)
        his.SetMarkerColor(kCyan+1)
        his.SetMarkerStyle(34)
        his.SetMarkerSize(1.6)

    elif flag == 7 :
        his.SetLineColor(46)
        his.SetLineWidth(2)
        his.SetMarkerColor(46)
        his.SetMarkerStyle(21)
        his.SetMarkerSize(1.1)

    elif flag == 8 :
        his.SetLineColor(kRed+3)
        his.SetLineWidth(2)
        his.SetMarkerColor(kRed+3)
        his.SetMarkerStyle(25)
        his.SetMarkerSize(1.1)

def SetTH2Style(h2, xlabel, ylabel, XYmin = None, XYmax = None, logX = None, logY = None, logZ = None):
    SetH2Style(h2)
    h2.GetXaxis().SetTitle(xlabel)
    if XYmin > 0 and XYmax > 0 : h2.GetXaxis().SetRangeUser(XYmin,XYmax)
    h2.GetYaxis().SetTitle(ylabel)
    h2.GetYaxis().SetRangeUser(XYmin,XYmax)
    h2.GetXaxis().SetRangeUser(XYmin,XYmax)
    minimum = ROOT.Double(0.)
    maximum = ROOT.Double(10e10)
    h2.GetMinimumAndMaximum(minimum,maximum)
    minimum = h2.GetMinimum(1e-10)
    h2.GetZaxis().SetRangeUser(minimum,maximum)
    gPad.SetLogx(logX)
    gPad.SetLogy(logY)
    gPad.SetLogz(logZ)
    
def SetH2Style(his):
    his.SetStats(0)
    his.GetXaxis().SetLabelFont(43)
    his.GetXaxis().SetLabelSize(26)
    his.GetXaxis().SetTitleSize(28)
    his.GetXaxis().SetTitleOffset(1.1)
    his.GetXaxis().SetTitleFont(43)
    his.GetYaxis().SetLabelFont(43)
    his.GetYaxis().SetLabelSize(26)
    his.GetYaxis().SetTitleSize(28)
    his.GetYaxis().SetTitleOffset(1.1)
    his.GetYaxis().SetTitleFont(43)   
