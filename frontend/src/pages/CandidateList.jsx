"use client";

import { useState, useEffect } from "react";
import CandidateCard from "../components/CandidateCard";
import SearchAndFilter from "../components/SearchAndFilter";
import { fetchCandidates } from "../services/api";

function CandidateList() {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({});
  const [pagination, setPagination] = useState({
    next: null,
    previous: null,
    count: 0,
  });

  useEffect(() => {
    loadCandidates();
  }, []);

  const loadCandidates = async (filterParams = {}) => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchCandidates(filterParams);
      setCandidates(data.results || []);
      setPagination({
        next: data.next,
        previous: data.previous,
        count: data.count,
      });
    } catch (err) {
      setError("Failed to load candidates. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadMoreCandidates = async (url) => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(url);
      const data = await response.json();
      setCandidates(data.results || []);
      setPagination({
        next: data.next,
        previous: data.previous,
        count: data.count,
      });
    } catch (err) {
      setError("Failed to load more candidates. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    loadCandidates(newFilters);
  };

  return (
    <div className="container py-4">
      <div className="row mb-4">
        <div className="col">
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h1 className="h2 mb-2">Political Candidates</h1>
              <p className="text-muted mb-0">
                Discover and explore political candidates in your area
              </p>
            </div>

            {pagination.count > 0 && (
              <div>
                <span className="badge bg-primary rounded-pill">
                  {pagination.count} candidates found
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      <SearchAndFilter onFilterChange={handleFilterChange} />

      {loading ? (
        <div className="d-flex justify-content-center align-items-center py-5">
          <div className="text-center">
            <div className="spinner-border text-primary mb-3" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="text-muted">Loading candidates...</p>
          </div>
        </div>
      ) : error ? (
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
            <h3 className="h5 mb-2">Something went wrong</h3>
            <p className="text-muted mb-3">{error}</p>
            <button
              className="btn btn-primary"
              onClick={() => loadCandidates(filters)}
            >
              Try Again
            </button>
          </div>
        </div>
      ) : candidates.length === 0 ? (
        <div className="d-flex justify-content-center align-items-center py-5">
          <div className="text-center">
            <svg
              width="64"
              height="64"
              viewBox="0 0 24 24"
              fill="none"
              className="text-muted mb-3"
            >
              <path
                d="M20 21V19C20 16.7909 18.2091 15 16 15H8C5.79086 15 4 16.7909 4 19V21M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <h3 className="h5 mb-2">No candidates found</h3>
            <p className="text-muted mb-3">
              Try adjusting your search criteria or filters to find more
              candidates.
            </p>
            <button
              className="btn btn-outline-primary"
              onClick={() => {
                setFilters({});
                loadCandidates({});
              }}
            >
              Clear All Filters
            </button>
          </div>
        </div>
      ) : (
        <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          {candidates.map((candidate) => (
            <div key={candidate.id} className="col">
              <CandidateCard candidate={candidate} />
            </div>
          ))}
        </div>
      )}

      {(pagination.previous || pagination.next) &&
        !loading &&
        candidates.length > 0 && (
          <div className="d-flex justify-content-between align-items-center mt-4">
            <button
              className="btn btn-outline-primary d-flex align-items-center gap-2"
              onClick={() => pagination.previous && loadMoreCandidates(pagination.previous)}
              disabled={!pagination.previous}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth="1.5"
                stroke="currentColor"
                width="20"
                height="20"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M19.5 12h-15m0 0l6.75-6.75M4.5 12l6.75 6.75"
                />
              </svg>
              Previous
            </button>

            <span className="text-muted">
              Showing {candidates.length} of {pagination.count} results
            </span>

            <button
              className="btn btn-outline-primary d-flex align-items-center gap-2"
              onClick={() => pagination.next && loadMoreCandidates(pagination.next)}
              disabled={!pagination.next}
            >
              Next
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth="1.5"
                stroke="currentColor"
                width="20"
                height="20"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M4.5 12h15m0 0l-6.75-6.75M19.5 12l-6.75 6.75"
                />
              </svg>
            </button>
          </div>
        )}
    </div>
  );
}

export default CandidateList;
