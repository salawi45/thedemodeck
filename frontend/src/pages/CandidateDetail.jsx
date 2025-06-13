"use client";

import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchCandidateById } from "../services/api";

function CandidateDetail() {
  const { id } = useParams();
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState([]);
  const [similar, setSimilar] = useState([]);
  
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

      <div className="card shadow-sm">
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
                {candidate.dob && (
                  <span className="badge bg-secondary">
                    Age {calculateAge(candidate.dob)}
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Issues Section */}
          <div className="mb-4">
            <h3 className="h4 mb-3">Political Issues</h3>
            {data && data.length > 0 ? (
              <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3">
                {data.map((issue) => (
                  <div key={issue.id} className="col">
                    <div className="card h-100">
                      <div className="card-body">
                        <h4 className="card-title h6 mb-0">{issue.issue}</h4>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-muted">No issues found for this candidate.</p>
            )}
          </div>

          {/* Similar Candidates Section */}
          <div className="mb-4">
            <h3 className="h4 mb-3">Similar Candidates</h3>
            {similar && similar.length > 0 ? (
              <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3">
                {similar.map((similarCandidate) => (
                  <div key={similarCandidate.id} className="col">
                    <Link 
                      to={`/candidate/${similarCandidate.id}`} 
                      className="card h-100 text-decoration-none"
                    >
                      <div className="card-body">
                        <div className="d-flex align-items-center gap-3">
                          <img
                            src={similarCandidate.photo_url || "https://via.placeholder.com/150x150/667eea/ffffff?text=No+Photo"}
                            alt={similarCandidate.label}
                            className="rounded-circle"
                            style={{ width: "50px", height: "50px", objectFit: "cover" }}
                            onError={(e) => {
                              e.target.onerror = null;
                              e.target.src = "https://via.placeholder.com/150x150/667eea/ffffff?text=No+Photo";
                            }}
                          />
                          <div>
                            <h4 className="h6 mb-1">{similarCandidate.label}</h4>
                            {similarCandidate.party_qid && (
                              <span className="badge bg-primary mb-2">{similarCandidate.party_qid}</span>
                            )}
                            <div className="small text-muted">
                              Similarity: {Math.round(similarCandidate.similarity_score * 100)}%
                            </div>
                          </div>
                        </div>
                      </div>
                    </Link>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-muted">No similar candidates found.</p>
            )}
          </div>

          {candidate.description && (
            <div className="mb-4">
              <h3 className="h4 mb-3 d-flex align-items-center gap-2">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M12 2L2 7L12 12L22 7L12 2Z"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M2 17L12 22L22 17"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M2 12L12 17L22 12"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                About
              </h3>
              <p className="text-muted">{candidate.description}</p>
            </div>
          )}

          <div className="mb-4">
            <h3 className="h4 mb-3 d-flex align-items-center gap-2">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path
                  d="M16 4H18C19.1046 4 20 4.89543 20 6V18C20 19.1046 19.1046 20 18 20H6C4.89543 20 4 19.1046 4 18V6C4 4.89543 4.89543 4 6 4H8M16 4V2M16 4V6M8 4V2M8 4V6M8 8H16M8 12H16M8 16H10"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
              Personal Information
            </h3>
            <div className="row row-cols-1 row-cols-md-2 g-3">
              <div className="col">
                <div className="card h-100">
                  <div className="card-body">
                    <h5 className="card-title h6 text-muted mb-2">Age</h5>
                    <p className="card-text mb-0">
                      {candidate.dob ? calculateAge(candidate.dob) : "Unknown"}
                    </p>
                  </div>
                </div>
              </div>

              {candidate.dob && (
                <div className="col">
                  <div className="card h-100">
                    <div className="card-body">
                      <h5 className="card-title h6 text-muted mb-2">Date of Birth</h5>
                      <p className="card-text mb-0">{formatDate(candidate.dob)}</p>
                    </div>
                  </div>
                </div>
              )}

              <div className="col">
                <div className="card h-100">
                  <div className="card-body">
                    <h5 className="card-title h6 text-muted mb-2">Political Party</h5>
                    <p className="card-text mb-0">{candidate.party_qid || "Unknown"}</p>
                  </div>
                </div>
              </div>

              <div className="col">
                <div className="card h-100">
                  <div className="card-body">
                    <h5 className="card-title h6 text-muted mb-2">Political Ideology</h5>
                    <p className="card-text mb-0">{candidate.ideology_qid || "Unknown"}</p>
                  </div>
                </div>
              </div>

              <div className="col">
                <div className="card h-100">
                  <div className="card-body">
                    <h5 className="card-title h6 text-muted mb-2">Wikidata ID</h5>
                    <p className="card-text mb-0">{candidate.cqid}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div>
            <h3 className="h4 mb-3 d-flex align-items-center gap-2">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <circle
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="2"
                />
                <polyline
                  points="12,6 12,12 16,14"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              Last Updated
            </h3>
            <p className="text-muted mb-0">
              {new Date(candidate.last_updated).toLocaleString()}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CandidateDetail;
