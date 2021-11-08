// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/ChargedFinalState.hh"

namespace Rivet {


  /// @brief Add a short analysis description here
  class ATLAS_2017_I1511869 : public Analysis {
  public:

    /// Constructor
    DEFAULT_RIVET_ANALYSIS_CTOR(ATLAS_2017_I1511869);


    /// Book histograms and initialise projections before the run
    /// Initialisation
    void init() {
      const FinalState fs(Cuts::abseta < 2.5);

      FastJets antikt_04_jets(fs, FastJets::ANTIKT, 0.4, JetAlg::Muons::NONE, JetAlg::Invisibles::NONE);
      declare(antikt_04_jets, "jets");

      //f.m.
      // originally:
      //FastJets antikt_04_jets(fs, FastJets::ANTIKT, 0.4, JetAlg::NO_MUONS, JetAlg::NO_INVISIBLES);
      //declare(antikt_04_jets, "jets");
      //f.m.

      ChargedFinalState tracks(Cuts::pT > 1.0*GeV && Cuts::abseta < 2.5);
      declare(tracks, "tracks");

      Histo1DPtr h_F_z[4], h_F_pT[4], h_jet_spectra[4];
      //const vector<double> bedges = { 100., 126., 158., 398.};
      const vector<double> bedges = { 100., 398.}; // move to 10 GeV for testing
      const vector<double> zbins = {0.0050, 0.0063, 0.0079, 0.0100, 0.0158, 0.0251, 0.0398, 0.0631, 0.1000, 0.1585, 0.2512, 0.3981, 0.6310, 1.0000, 1.2589, 1.5849, 1.9953}; //TODO - check binning
	    const vector<double> pTbins = {0.50, 0.63, 1.00, 1.58, 2.51, 3.98, 6.31, 10.00, 15.85, 25.12, 39.81, 63.09, 100.00, 158.49, 251.18, 398.11, 630.96}; //TODO - check binning

      // Set up the histograms (each element is a binning in jet pT)
      for (size_t i = 0; i < 4; i++) {
        //_h_F_z[i]     = bookProfile1D(i+1, 1, 1); //TODO: when HepData available the booking need to be changed
        //_h_F_pT[i] = bookProfile1D(i+7, 1, 1); //TODO: when HepData available the booking need to be changed
        h_F_z[i] = bookHisto1D("h_F_z_" + std::to_string(i), zbins);
        h_F_pT[i] = bookHisto1D("h_F_pT_" + std::to_string(i), pTbins);
        h_jet_spectra[i] = bookHisto1D("h_jet_spectra_" + std::to_string(i), bedges);
      }
    }


    // Per-event analysis
    void analyze(const Event& event) {
	
      const Jets alljets = apply<FastJets>(event, "jets").jetsByPt(Cuts::absrap < 2.1);
      const Particles& tracks = apply<ChargedFinalState>(event, "tracks").particlesByPt();
      const double weight = event.weight();
      
      double minrap = 0., maxrap=2.1;
      
      for (size_t i = 0; i < 4; ++i) {
		
		GetRapidityCut(i, minrap, maxrap);
			
        const Jets jets = filter_select(alljets, (Cuts::pT > bedges[0] && Cuts::pT < bedges[1]) && (Cuts::absrap > minrap && Cuts::absrap < maxrap) && (Cuts::absrap > 1.2 || Cuts::absrap < 0.8) ); //TODO to be changed for jet pt dependence if needed
        const int n_jets = jets.size();
        if (n_jets == 0) continue;
        
        //Fill number of jets to correspondinng jet pt bin (bin center, currently only one bin) TODO to be changed if jet pt dependence is needed
        h_jet_spectra[i]->fill( (bedges[0] + bedges[1])/2. , n_jets*weight);
		
        for (const Jet& j : jets) {
          for (const Particle& p : tracks) {
            const double dr = deltaR(j, p, PSEUDORAPIDITY);
            if (dr > 0.4) continue;
            h_F_z[i]->fill( z(j, p, dr), weight );
            h_F_pT [i]->fill( p.pT()*GeV, weight );
          }
        }
      }

    }


	void finalize() {
        //Normalize histograms by number of jets
        for (size_t n = 0; n < h_jet_spectra[0]->numBins(); ++n) {
			for (size_t i = 0; i < 4; ++i) {
				YODA::HistoBin1D& b1 = h_jet_spectra[i]->bin(n); //bins starts from 0
				if (b1.area() > 0.) {
				    //MSG_WARNING("IN i: " << i << " bin content " << b1.area() ); //area <-> bincontent
					scale(h_F_z[i], 1./b1.area() );
					scale(h_F_pT[i], 1./b1.area() );
				}	
			}
		}	 
    }

	// To calculate longitudinal momentum fraction z
    double z (const Jet& jet, const Particle& ch, const double dR) {
      return  ch.pT()/jet.pT()*cos(dR);
    }
    
    void GetRapidityCut ( int i, double &minrap, double &maxrap ) {
    	switch ( i ) {
			case 0:
				minrap = 0.; maxrap = 2.1;
			break;
			
			case 1:
				minrap = 0.; maxrap = 0.3;
			break;
			
			case 2:
				minrap = 0.3; maxrap = 0.8;
			break;
			
			case 3:
				minrap = 1.2; maxrap = 2.1;
			break;		
		}    
    }

  private:

    Histo1DPtr h_F_z[4], h_F_pT[4], h_jet_spectra[4];
    //const vector<double> bedges = { 100., 126., 158., 398.};
    const vector<double> bedges = { 100., 398.}; // move to 10 GeV for testing
    const vector<double> zbins = {0.0050, 0.0063, 0.0079, 0.0100, 0.0158, 0.0251, 0.0398, 0.0631, 0.1000, 0.1585, 0.2512, 0.3981, 0.6310, 1.0000, 1.2589, 1.5849, 1.9953}; //TODO - check binning
	const vector<double> pTbins = {0.50, 0.63, 1.00, 1.58, 2.51, 3.98, 6.31, 10.00, 15.85, 25.12, 39.81, 63.09, 100.00, 158.49, 251.18, 398.11, 630.96}; //TODO - check binning

  };


  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(ATLAS_2017_I1511869);


}
