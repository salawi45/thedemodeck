import { Link } from "react-router-dom";

function About() {
  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="card shadow-sm">
            <div className="card-body p-4">
              <h1 className="h2 mb-4">About Political Candidates</h1>
              
              <div className="mb-4">
                <h2 className="h4 mb-3">Our Mission</h2>
                <p className="text-muted">
                  We aim to provide comprehensive information about political candidates, 
                  making it easier for citizens to make informed decisions during elections. 
                  Our platform aggregates data from various reliable sources to present a 
                  clear picture of each candidate's background, policies, and positions.
                </p>
              </div>

              <div className="mb-4">
                <h2 className="h4 mb-3">What We Offer</h2>
                <div className="row g-4">
                  <div className="col-md-6">
                    <div className="card h-100 border-0 bg-light">
                      <div className="card-body">
                        <h3 className="h5 mb-3">
                          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" className="me-2">
                            <path
                              d="M16 4H18C19.1046 4 20 4.89543 20 6V18C20 19.1046 19.1046 20 18 20H6C4.89543 20 4 19.1046 4 18V6C4 4.89543 4.89543 4 6 4H8M16 4V2M16 4V6M8 4V2M8 4V6M8 8H16M8 12H16M8 16H10"
                              stroke="currentColor"
                              strokeWidth="2"
                              strokeLinecap="round"
                            />
                          </svg>
                          Candidate Profiles
                        </h3>
                        <p className="text-muted mb-0">
                          Detailed information about each candidate's background, 
                          experience, and political positions.
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="col-md-6">
                    <div className="card h-100 border-0 bg-light">
                      <div className="card-body">
                        <h3 className="h5 mb-3">
                          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" className="me-2">
                            <path
                              d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                              stroke="currentColor"
                              strokeWidth="2"
                              strokeLinecap="round"
                              strokeLinejoin="round"
                            />
                          </svg>
                          Policy Analysis
                        </h3>
                        <p className="text-muted mb-0">
                          Comprehensive analysis of candidates' positions on key 
                          political issues and policies.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mb-4">
                <h2 className="h4 mb-3">Our Data Sources</h2>
                <p className="text-muted">
                  We gather information from various reliable sources including:
                </p>
                <ul className="list-unstyled">
                  <li className="mb-2">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" className="me-2 text-primary">
                      <path
                        d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                    Official candidate websites and social media
                  </li>
                  <li className="mb-2">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" className="me-2 text-primary">
                      <path
                        d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                    Public voting records and legislative history
                  </li>
                  <li className="mb-2">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" className="me-2 text-primary">
                      <path
                        d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                    Verified news sources and fact-checking organizations
                  </li>
                </ul>
              </div>

              <div className="text-center mt-5">
                <Link to="/" className="btn btn-primary">
                  Explore Candidates
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default About; 