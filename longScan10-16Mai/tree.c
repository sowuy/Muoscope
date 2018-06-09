#include "Riostream.h"
#include "TString.h"
#include "TFile.h"
#include "TTree.h"
#include "TSystem.h"


void tree(){

    TString dir = gSystem->UnixPathName("angularDistribution_2.txt");
    dir.ReplaceAll("tree.C","");
    dir.ReplaceAll("/.","/");

    
    TFile *f = new TFile("angularDistribution_2.root","RECREATE");
     
    TTree *T = new TTree("T", "data from txt file");
    Int_t currentIgnoreLevel = gErrorIgnoreLevel;
    T-> ReadFile("angularDistribution_2.txt", "phi:theta");

    gErrorIgnoreLevel = currentIgnoreLevel;


      
    
    //f->Write();

}
