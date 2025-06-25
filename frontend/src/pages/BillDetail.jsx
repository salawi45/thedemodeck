import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getBillDetail, getBillVotes } from '../services/api';
import '../styles/BillDetail.css';

const BillDetail = () => {
  const { billId } = useParams();
  const [bill, setBill] = useState(null);
  const [votes, setVotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    const fetchBillData = async () => {
      try {
        setLoading(true);
        const [billData, votesData] = await Promise.all([
          getBillDetail(billId),
          getBillVotes(billId)
        ]);
        setBill(billData);
        setVotes(votesData.results || []);
      } catch (err) {
        setError('Failed to load bill data');
        console.error('Error fetching bill data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchBillData();
  }, [billId]);

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getVoteSummary = () => {
    const voteCounts = votes.reduce((acc, vote) => {
      acc[vote.vote_position] = (acc[vote.vote_position] || 0) + 1;
      return acc;
    }, {});

    return voteCounts;
  };

  const renderVoteCard = (vote) => (
    <div key={vote.id} className="vote-card">
      <div className="vote-candidate">
        <Link to={`/candidate/${vote.candidate}`} className="candidate-link">
          {vote.candidate_name}
        </Link>
      </div>
      <div className={`vote-position ${vote.vote_position.toLowerCase()}`}>
        {vote.vote_position}
      </div>
      <div className="vote-chamber">
        {vote.chamber}
      </div>
      <div className="vote-date">
        {formatDate(vote.vote_date)}
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="bill-detail-container">
        <div className="loading">Loading bill details...</div>
      </div>
    );
  }

  if (error || !bill) {
    return (
      <div className="bill-detail-container">
        <div className="error">
          {error || 'Bill not found'}
          <Link to="/bills" className="back-link">← Back to Bills</Link>
        </div>
      </div>
    );
  }

  const voteSummary = getVoteSummary();

  return (
    <div className="bill-detail-container">
      <div className="bill-header">
        <Link to="/bills" className="back-link">← Back to Bills</Link>
        <h1 className="bill-title">{bill.bill_id}: {bill.title}</h1>
        <div className="bill-meta">
          <span className="bill-type">{bill.bill_type.toUpperCase()}</span>
          <span className="bill-congress">Congress {bill.congress}</span>
          <span className="bill-status">{bill.status || 'Unknown Status'}</span>
        </div>
      </div>

      <div className="bill-tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`tab ${activeTab === 'votes' ? 'active' : ''}`}
          onClick={() => setActiveTab('votes')}
        >
          Votes ({votes.length})
        </button>
        <button 
          className={`tab ${activeTab === 'details' ? 'active' : ''}`}
          onClick={() => setActiveTab('details')}
        >
          Details
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="bill-summary">
              <h3>Summary</h3>
              <p>{bill.summary || 'No summary available'}</p>
            </div>

            <div className="bill-sponsor">
              <h3>Sponsor</h3>
              {bill.sponsor ? (
                <Link to={`/candidate/${bill.sponsor}`} className="sponsor-link">
                  {bill.sponsor_name}
                </Link>
              ) : (
                <span>No sponsor information available</span>
              )}
            </div>

            <div className="vote-summary">
              <h3>Vote Summary</h3>
              <div className="vote-counts">
                <div className="vote-count yes">
                  <span className="count">{voteSummary.Yes || 0}</span>
                  <span className="label">Yes</span>
                </div>
                <div className="vote-count no">
                  <span className="count">{voteSummary.No || 0}</span>
                  <span className="label">No</span>
                </div>
                <div className="vote-count present">
                  <span className="count">{voteSummary.Present || 0}</span>
                  <span className="label">Present</span>
                </div>
                <div className="vote-count not-voting">
                  <span className="count">{voteSummary['Not Voting'] || 0}</span>
                  <span className="label">Not Voting</span>
                </div>
              </div>
            </div>

            <div className="bill-dates">
              <h3>Important Dates</h3>
              <div className="date-item">
                <strong>Introduced:</strong> {formatDate(bill.introduced_date)}
              </div>
              <div className="date-item">
                <strong>Last Action:</strong> {formatDate(bill.last_action_date)}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'votes' && (
          <div className="votes-tab">
            <div className="votes-header">
              <h3>All Votes ({votes.length})</h3>
              <div className="vote-filters">
                <select 
                  className="vote-filter"
                  onChange={(e) => {
                    // Add filtering logic here if needed
                  }}
                >
                  <option value="">All Votes</option>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                  <option value="Present">Present</option>
                  <option value="Not Voting">Not Voting</option>
                </select>
              </div>
            </div>
            
            <div className="votes-list">
              {votes.length > 0 ? (
                votes.map(renderVoteCard)
              ) : (
                <div className="no-votes">No votes recorded for this bill</div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'details' && (
          <div className="details-tab">
            <div className="bill-details">
              <h3>Bill Details</h3>
              <div className="detail-item">
                <strong>Bill ID:</strong> {bill.bill_id}
              </div>
              <div className="detail-item">
                <strong>Congress:</strong> {bill.congress}
              </div>
              <div className="detail-item">
                <strong>Session:</strong> {bill.session || 'N/A'}
              </div>
              <div className="detail-item">
                <strong>Bill Type:</strong> {bill.bill_type}
              </div>
              <div className="detail-item">
                <strong>Bill Number:</strong> {bill.bill_number}
              </div>
              <div className="detail-item">
                <strong>Status:</strong> {bill.status || 'Unknown'}
              </div>
              <div className="detail-item">
                <strong>Short Title:</strong> {bill.short_title || 'N/A'}
              </div>
            </div>

            {bill.congress_gov_url && (
              <div className="external-links">
                <h3>External Links</h3>
                <a 
                  href={bill.congress_gov_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="external-link"
                >
                  View on Congress.gov →
                </a>
              </div>
            )}

            <div className="last-action">
              <h3>Last Action</h3>
              <div className="action-text">
                {bill.last_action_text || 'No action information available'}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BillDetail; 