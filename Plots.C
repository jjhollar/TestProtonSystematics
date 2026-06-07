void Plots()
{
  TFile *f1 = TFile::Open("all_collect_systematics.root");
  TGraphErrors *g1 = (TGraphErrors *)f1->Get("multi rp-1/combined");

  g1->Draw();
  g2->SetLineColor(4);
}

void Resolution()
{
  TFile *f1 = TFile::Open("proton_reco_resolution/resolution_th_Large_level_1_validation.root");
  TFile *f3 = TFile::Open("proton_reco_resolution/resolution_th_Large_level_3_validation.root");
  TFile *f2 = TFile::Open("proton_reco_resolution/resolution_th_Large_level_2_validation.root");
  TFile *f4 = TFile::Open("proton_reco_resolution/resolution_th_Large_level_4_validation.root");

  TGraphErrors *gr1 = (TGraphErrors *)f1->Get("multi rp/0/g_rms_de_xi_vs_xi_simu");
  TGraphErrors *gr2 = (TGraphErrors *)f2->Get("multi rp/0/g_rms_de_xi_vs_xi_simu");
  TGraphErrors *gr3 = (TGraphErrors *)f3->Get("multi rp/0/g_rms_de_xi_vs_xi_simu");
  TGraphErrors *gr4 = (TGraphErrors *)f4->Get("multi rp/0/g_rms_de_xi_vs_xi_simu");

  gr4->SetLineColor(2); gr4->Draw();
  gr3->SetLineColor(4); gr3->Draw("same");
  gr2->SetLineColor(3); gr2->Draw("same");
  gr1->SetLineColor(1); gr1->Draw("same");
  
}

