"use client";

import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchCandidateById, fetchCandidateBills, fetchCandidateVotes } from "../services/api";
import BillCard from "../components/BillCard";
import VoteCard from "../components/VoteCard";

function CandidateDetail() {
  const { id } = useParams();
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState([]);
  const [similar, setSimilar] = useState([]);
  const [bills, setBills] = useState([]);
  const [votes, setVotes] = useState([]);
  const [activeTab, setActiveTab] = useState('overview');
  
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/candidate/${id}/similar/`)
    .then(response => response.json())
    .then(data => {
      setSimilar(data);
    })
    .catch(error => {
      console.error("Error fetching similar candidates:", error);
    });
  }, [id]);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/candidates/${id}/issues/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setData(data);
      })
      .catch((error) => {
        console.error("Error fetching candidate issues:", error);
      });
  }, [id]);

  useEffect(() => {
    const loadCandidateDetails = async () => {
      try {
        setLoading(true);
        const data = await fetchCandidateById(id);
        setCandidate(data);
        
        // Load bills and votes
        try {
          const billsData = await fetchCandidateBills(id);
          setBills(billsData);
        } catch (err) {
          console.error("Error loading bills:", err);
        }
        
        try {
          const votesData = await fetchCandidateVotes(id);
          setVotes(votesData);
        } catch (err) {
          console.error("Error loading votes:", err);
        }
      } catch (err) {
        setError("Failed to load candidate details");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadCandidateDetails();
  }, [id]);

  const calculateAge = (dob) => {
    if (!dob) return "Unknown";

    const birthDate = new Date(dob);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();

    if (
      monthDiff < 0 ||
      (monthDiff === 0 && today.getDate() < birthDate.getDate())
    ) {
      age--;
    }

    return age.toString();
  };

  const formatDate = (dateString) => {
    if (!dateString) return "Unknown";

    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  if (loading) {
    return (
      <div className="container py-4">
        <div className="d-flex justify-content-center align-items-center py-5">
          <div className="text-center">
            <div className="spinner-border text-primary mb-3" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="text-muted">Loading candidate details...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !candidate) {
    return (
      <div className="container py-4">
        <div className="d-flex justify-content-center align-items-center py-5">
          <div className="text-center">
            <svg
              width="48"
              height="48"
              viewBox="0 0 24 24"
              fill="none"
              className="text-danger mb-3"
            >
              <circle
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="2"
              />
              <path
                d="M15 9L9 15M9 9L15 15"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
            <h3 className="h5 mb-2">Candidate Not Found</h3>
            <p className="text-muted mb-3">
              {error || "Failed to load candidate details"}
            </p>
            <Link to="/" className="btn btn-primary">
              Back to Candidates
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case 'bills':
        return (
          <div>
            <h3 className="mb-3">Sponsored Bills</h3>
            {bills.length === 0 ? (
              <p className="text-muted">No bills sponsored by this candidate.</p>
            ) : (
              <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                {bills.map((bill) => (
                  <div key={bill.id} className="col">
                    <BillCard bill={bill} />
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      
      case 'votes':
        return (
          <div>
            <h3 className="mb-3">Voting Record</h3>
            {votes.length === 0 ? (
              <p className="text-muted">No voting record available for this candidate.</p>
            ) : (
              <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                {votes.map((vote) => (
                  <div key={vote.id} className="col">
                    <VoteCard vote={vote} />
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      
      case 'issues':
        return (
          <div>
            <h3 className="mb-3">Issues & Positions</h3>
            {data.length === 0 ? (
              <p className="text-muted">No issues data available for this candidate.</p>
            ) : (
              <div className="row">
                {data.map((item, index) => (
                  <div key={index} className="col-md-6 mb-3">
                    <div className="card">
                      <div className="card-body">
                        <h6 className="card-title">{item.issue}</h6>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      
      default:
        return (
          <div>
            <h3 className="mb-3">Overview</h3>
            <div className="row">
              <div className="col-md-6">
                <h5>Personal Information</h5>
                <ul className="list-unstyled">
                  <li><strong>Age:</strong> {calculateAge(candidate.dob)}</li>
                  <li><strong>Date of Birth:</strong> {formatDate(candidate.dob)}</li>
                  <li><strong>Last Updated:</strong> {formatDate(candidate.last_updated)}</li>
                  {candidate.bioguide_id && (
                    <li><strong>Bioguide ID:</strong> {candidate.bioguide_id}</li>
                  )}
                </ul>
              </div>
              <div className="col-md-6">
                <h5>Political Information</h5>
                <ul className="list-unstyled">
                  <li><strong>Party:</strong> {candidate.party_qid || 'Unknown'}</li>
                  <li><strong>Ideology:</strong> {candidate.ideology_qid || 'Unknown'}</li>
                </ul>
              </div>
            </div>
            
            {candidate.description && (
              <div className="mt-4">
                <h5>Description</h5>
                <p>{candidate.description}</p>
              </div>
            )}
          </div>
        );
    }
  };

  return (
    <div className="container py-4">
      <Link to="/" className="btn btn-link text-decoration-none mb-4 d-inline-flex align-items-center gap-2">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path
            d="M19 12H5M12 19L5 12L12 5"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        Back to all candidates
      </Link>

      <div className="card shadow-sm fade-in hover-lift">
        <div className="card-body">
          <div className="row align-items-center mb-4">
            <div className="col-auto">
              <div className="position-relative">
                <img
                  src={candidate.photo_url || "https://via.placeholder.com/200x200/667eea/ffffff?text=No+Photo"}
                  alt={candidate.label}
                  className="rounded-circle"
                  style={{ width: "150px", height: "150px", objectFit: "cover" }}
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = "https://via.placeholder.com/200x200/667eea/ffffff?text=No+Photo";
                  }}
                />
              </div>
            </div>

            <div className="col">
              <h1 className="h2 mb-2">{candidate.label}</h1>
              {candidate.position && (
                <h2 className="h5 text-muted mb-3 d-flex align-items-center gap-2">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path
                      d="M21 10C21 17 12 23 12 23S3 17 3 10C3 5.02944 7.02944 1 12 1C16.9706 1 21 5.02944 21 10Z"
                      stroke="currentColor"
                      strokeWidth="2"
                    />
                    <circle
                      cx="12"
                      cy="10"
                      r="3"
                      stroke="currentColor"
                      strokeWidth="2"
                    />
                  </svg>
                  {candidate.position}
                </h2>
              )}

              <div className="d-flex gap-2">
                {candidate.party_qid && (
                  <span className="badge bg-primary">{candidate.party_qid}</span>
                )}
                {candidate.ideology_qid && (
                  <span className="badge bg-secondary">{candidate.ideology_qid}</span>
                )}
              </div>
            </div>
          </div>

          {/* Navigation Tabs */}
          <ul className="nav nav-tabs mb-4" id="candidateTabs" role="tablist">
            <li className="nav-item" role="presentation">
              <button
                className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
                onClick={() => setActiveTab('overview')}
              >
                Overview
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button
                className={`nav-link ${activeTab === 'bills' ? 'active' : ''}`}
                onClick={() => setActiveTab('bills')}
              >
                Bills ({bills.length})
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button
                className={`nav-link ${activeTab === 'votes' ? 'active' : ''}`}
                onClick={() => setActiveTab('votes')}
              >
                Votes ({votes.length})
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button
                className={`nav-link ${activeTab === 'issues' ? 'active' : ''}`}
                onClick={() => setActiveTab('issues')}
              >
                Issues ({data.length})
              </button>
            </li>
          </ul>

          {/* Tab Content */}
          <div className="tab-content">
            {renderTabContent()}
          </div>
        </div>
      </div>

      {/* Similar Candidates */}
      {similar.length > 0 && (
        <div className="mt-5">
          <h3 className="mb-4">Similar Candidates</h3>
          <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            {similar.map((candidate) => (
              <div key={candidate.id} className="col">
                <Link to={`/candidate/${candidate.id}`} className="text-decoration-none">
                  <div className="card h-100 shadow-sm hover-lift transition">
                    <div className="card-body p-3">
                      <div className="text-center mb-3">
                        <img
                          src={candidate.photo_url || "https://via.placeholder.com/100"}
                          alt={candidate.label}
                          className="rounded-circle"
                          style={{ width: "80px", height: "80px", objectFit: "cover" }}
                          onError={(e) => {
                            e.target.onerror = null;
                            e.target.src = "https://via.placeholder.com/100?text=No+Image";
                          }}
                        />
                      </div>
                      <div className="text-center">
                        <h6 className="card-title mb-1">{candidate.label}</h6>
                        <p className="text-muted small mb-2">
                          Similarity: {(candidate.similarity_score * 100).toFixed(1)}%
                        </p>
                        {candidate.party_qid && (
                          <span className="badge bg-primary">{candidate.party_qid}</span>
                        )}
                      </div>
                    </div>
                  </div>
                </Link>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default CandidateDetail;
