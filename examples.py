# Written by Vojtech Pleskot (vojtech.pleskot@cern.ch)

from ROOT import gROOT, TH1, TH1D, THStack, TLine, TF1
import ROOT

from PyRooPlotting.TH1_helpers import TH1_helper
from PyRooPlotting.layout_helpers import layout_helper
from PyRooPlotting.plotting_helpers import simplePlot
from PyRooPlotting.plotting_helpers import ratioPlot





######################################################
### Working plotting examples
######################################################

def main():
    gROOT.SetBatch(True)
    gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
    TH1.AddDirectory(False)
    TH1.SetDefaultSumw2(True)
    # -----------------------
    # Prepare objects to plot
    # --------------------
    hGaus = TH1D("hGaus", "hGaus", 50, 0, 100)
    for i in range(10000):
        hGaus.Fill(ROOT.gRandom.Gaus(20, 5))
    hGaus.SetLineColor(1)
    hGaus.SetFillColor(ROOT.kOrange)
    hGaus.SetFillStyle(1001)
    hGaus2 = TH1D("hGaus2", "hGaus2", 50, 0, 100)
    for i in range(10000):
        hGaus2.Fill(ROOT.gRandom.Exp(10))
    hGaus2.SetLineColor(1)
    hGaus2.SetFillColor(ROOT.kGreen + 1)
    hGaus2.SetFillStyle(1001)
    hGaus3 = TH1D("hGaus3", "hGaus3", 50, 0, 100)
    for i in range(10000):
        hGaus3.Fill(ROOT.gRandom.Gaus(60, 8))
    hGaus3.SetLineColor(1)
    hGaus3.SetFillColor(ROOT.kRed + 1)
    hGaus3.SetFillStyle(1001)
    hGaus4 = TH1D("hGaus4", "hGaus4", 50, 0, 100)
    for i in range(10000):
        hGaus4.Fill(ROOT.gRandom.Gaus(40, 10))
    hGausSum = hGaus4.Clone()
    hGaus4.SetLineColor(1)
    hGaus4.SetFillColor(ROOT.kAzure - 9)
    hGaus4.SetFillStyle(1001)
    hGausSum.Add(hGaus3)
    hGausSum.SetLineColor(4)
    hGausSum.SetLineWidth(3)
    hGausSum.SetLineStyle(2)
    s = THStack("s", "")
    s.Add(hGaus.Clone())
    s.Add(hGaus4.Clone())
    gr = hGaus.Clone()
    gr.Add(hGaus2)
    gr.Add(hGaus3)
    hh = TH1_helper()
    gr = hh.histoToGraph(gr)
    gr.SetFillStyle(1001)
    gr.SetFillColor(ROOT.kGray)
    line = TLine(40, 70, 40, 2100)
    line.SetLineColor(2)
    line.SetLineStyle(1)
    line.SetLineWidth(2)
    func = TF1("func", "20*x*x*exp(-0.1*x)", 0, 70)
    func.SetLineColor(1)
    func.SetLineWidth(2)
    # -----------------------
    # Start plotting
    # --------------------
    exampleSimplePlot(gr, line, func)
    exampleRatioPlot(hGaus3, s)
    exampleSimplePlotFrozenLayout(gr, func)
    return

###############################################################
### Draw the simplest possible plot: one rectangle in a TCanvas
###############################################################

def exampleSimplePlot(gr, line, func):
    ph = simplePlot()
    ph.setStyle(24)
    lh = layout_helper()
    # Prepare canvas and pads
    pads = ph.canvasAndPads(False)
    # pads[0].SetLogx()
    # Calculate text objects coordinates
    #    and draw all objects.
    plots = [gr, line, func]
    lh.resetAttributes(pad = pads[0], plots = plots
                       , xMin = 0, xMax = 80
                       , yMin = 0
                       , legendNCol = 1
                       , letAtlasLabelFloat = False, yMaxOffset = 0.05, yMinOffset = 0.05
                       , textPlotsDist = 0.04999
                       , considerUncertainties = True
                       , topTextPosY = ph.topTextPosY, bottomTextPosY = ph.bottomTextPosY
                       , verbose = True, entryHeight = 0.065
                       , putTextAtTheTop = True, putTextAtTheBottom = True
    )
    atlasLabels = ["#font[72]{ATLAS} Internal", "13 TeV, 3.2 fb^{-1}"]
    lh.addLabel(atlasLabels)
    legList = []
    legList.append([gr, "TGraph", "f"])
    legList.append([func, "TF1", "l"])
    legList.append([line, "TLine", "l"])
    lh.addLegend([l[1] for l in legList])
    decorations = ["text", "another text", "another text"]
    lh.addText(decorations)
    if not lh.placeAllTextToPad():
        lh.clearStorage()
        lh.resetAttributesToNone()
        for p in pads:
            p.IsA().Destructor(p)
        return
    # Drawing the pad frame
    ph.drawFrame(lh.getFrame().Clone(), "#it{p}_{T} [GeV]", "Events")
    # Drawing text objects to the pad frame
    ph.drawTextBox(atlasLabels, lh.labelCoordinates()["TLatexPositions"])
    ph.drawLegend(legList, lh.legendCoordinates(0))
    ph.drawTextBox(decorations, lh.textCoordinates(0)["TLatexPositions"])
    gr.Draw("2 same")
    line.Draw()
    func.Draw("same")
    pads[0].RedrawAxis()
    pads[len(pads) - 1].SaveAs("exampleSimplePlot.eps")
    # Terminate the session
    lh.clearStorage()
    lh.resetAttributesToNone()
    for p in pads:
        p.IsA().Destructor(p)
    return


###############################################################
### Draw a ratio plot: two rectangles in a TCanvas:
###    - the top one is larger
###    - the bottom one is designed to contain ratios
###############################################################

def exampleRatioPlot(hGaus, hStack):
    fitf = TF1("fitf", "gaus", 30, 90);
    hGaus.Fit("fitf", "R0");
    hGaus.SetMarkerStyle(20)
    hGaus.SetMarkerColor(1)
    hGaus.SetLineColor(1)
    fitf.SetLineColor(2)
    ph = ratioPlot()
    ph.setStyle(24)
    lh = layout_helper()
    # Prepare canvas and pads
    pads = ph.canvasAndPads(False)
    #pads[0].SetLogx()
    #pads[1].SetLogy()
    #pads[1].SetLogx()
    # ----------------------
    # Top pad
    # ----------------------
    # Setup layout helper
    plots = [hGaus, fitf, hStack]
    lh.resetAttributes(pad = pads[0], plots = plots
                       , xMin = 30, xMax = 90
                       , yMin = 0
                       , legendNCol = 1
                       , letAtlasLabelFloat = False, yMaxOffset = 0.05, yMinOffset = 0.05
                       , textPlotsDist = 0.04999
                       , considerUncertainties = True
                       , topTextPosY = ph.topTextPosY, bottomTextPosY = ph.bottomTextPosY
                       , verbose = True, entryHeight = 0.065
                       , putTextAtTheTop = True, putTextAtTheBottom = True
    )
    atlasLabels = ["#font[72]{ATLAS} Internal", "13 TeV, 3.2 fb^{-1}"]
    lh.addLabel(atlasLabels)
    legList = []
    legList.append([hGaus, "hGaus", "p"])
    legList.append([fitf, "fitf", "l"])
    for h in hStack.GetHists():
        legList.append([h, h.GetName(), "f"])
    lh.addLegend([l[1] for l in legList])
    decorations = ["text", "text", "text", "another text", "another text"]
    lh.addText(decorations)
    # Calculate the optimal layout
    if not lh.placeAllTextToPad():
        return
    # Drawing the top pad frame
    ph.drawTopFrame(lh.getFrame().Clone(), "Events")
    # Drawing text objects to the top pad frame
    ph.drawTextBox(atlasLabels, lh.labelCoordinates()["TLatexPositions"])
    ph.drawLegend(legList, lh.legendCoordinates(0))
    ph.drawTextBox(decorations, lh.textCoordinates(0)["TLatexPositions"])
    hStack.Draw("same hist")
    hGaus.Draw("same p")
    fitf.Draw("same")
    pads[0].RedrawAxis()
    # ----------------------
    # Bottom pad
    # ----------------------
    # Prepare the ratio and TLine at one
    hRat = hGaus.Clone()
    for ib in range(1, hGaus.GetNbinsX() + 1):
        x = hGaus.GetBinCenter(ib)
        fx = fitf.Eval(x)
        if abs(hGaus.GetBinContent(ib)) > 1.e-9:
            rat = hGaus.GetBinContent(ib) / fx
            err = hGaus.GetBinError(ib) / fx
        else:
            rat = 1.
            err = 0.
        hRat.SetBinContent(ib, rat)
        hRat.SetBinError(ib, err)
    line = ph.lineAtOne(30, 90)
    # Setup layout_helper
    lh.resetAttributes(pad = pads[1], plots = [hRat, line]
                       , xMin = 30, xMax = 90
                       , verbose = True
                       , considerUncertainties = False
                       , yMinOffset = 0.06, yMaxOffset = 0.06
    )
    # Calculate the optimal layout
    if not lh.placeAllTextToPad():
        lh.clearStorage()
        lh.resetAttributesToNone()
        for p in pads:
            p.IsA().Destructor(p)
        return
    # Draw objects
    ph.drawBottomFrame(lh.getFrame().Clone(), "#it{p}_{T} [GeV]", "Ratio ")
    line.Draw()
    hRat.Draw("same")
    lh.pad.RedrawAxis()
    pads[len(pads) - 1].SaveAs("exampleRatioPlot.eps")
    # Terminate the session
    lh.clearStorage()
    lh.resetAttributesToNone()
    for p in pads:
        p.IsA().Destructor(p)
    return
    

###############################################################
### Draw the simplest possible plot: one rectangle in a TCanvas
### Decide the content of panels yourself instead of letting 
### the tool do it.
###############################################################

def exampleSimplePlotFrozenLayout(gr, func):
    ph = simplePlot()
    ph.setStyle(24)
    lh = layout_helper()
    # Prepare canvas and pads
    pads = ph.canvasAndPads(False)
    # Calculate text objects coordinates
    #    and draw all objects.
    plots = [gr, func]
    lh.resetAttributes(pad = pads[0], plots = plots
                       , xMin = 0, xMax = 80
                       , yMaxOffset = 0.05, yMinOffset = 0.05
                       , textPlotsDist = 0.04999
                       , topTextPosY = ph.topTextPosY, bottomTextPosY = ph.bottomTextPosY
                       , verbose = 1, entryHeight = 0.065
                       , placePredefinedPanels = True
    )
    atlasLabels = ["#font[72]{ATLAS} Internal", "13 TeV, 3.2 fb^{-1}"]
    # add atlasLabels to the top left panel
    lh.addTextToPredefinedPanel(atlasLabels, "TL")
    legList = []
    legList.append([gr, "TGraph", "f"])
    legList.append([func, "TF1", "l"])
    # add legend to the top right panel
    lh.addLegendToPredefinedPanel([l[1] for l in legList], 1, "TR")
    decorations = ["decoration", "text", "another text"]
    # add decorations to the top right panel
    lh.addTextToPredefinedPanel(decorations, "TR")
    decorations2 = ["decoration 2", "text", "another text"]
    # add decorations2 to the bottom right panel
    lh.addTextToPredefinedPanel(decorations2, "BR")
    if not lh.placeAllTextToPad():
        lh.clearStorage()
        lh.resetAttributesToNone()
        for p in pads:
            p.IsA().Destructor(p)
        return
    # Drawing the pad frame
    ph.drawFrame(lh.getFrame().Clone(), "#it{p}_{T} [GeV]", "Events")
    # Drawing text objects to the pad frame
    ph.drawTextBox(atlasLabels, lh.textCoordinates(0)["TLatexPositions"])
    ph.drawLegend(legList, lh.legendCoordinates(0))
    ph.drawTextBox(decorations, lh.textCoordinates(1)["TLatexPositions"])
    ph.drawTextBox(decorations2, lh.textCoordinates(2)["TLatexPositions"])
    gr.Draw("2 same")
    func.Draw("same")
    pads[0].RedrawAxis()
    pads[len(pads) - 1].SaveAs("exampleSimplePlotFrozenLayout.eps")
    # Terminate the session
    lh.clearStorage()
    lh.resetAttributesToNone()
    for p in pads:
        p.IsA().Destructor(p)
    return


if __name__ == '__main__': 
    main()


