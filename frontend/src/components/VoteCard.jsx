
function VoteCard({ vote }) {
  const formatDate = (dateString) => {
    if (!dateString) return "Unknown"
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  const getVoteBadge = (position) => {
    const voteMap = {
      'Yes': 'bg-success',
      'No': 'bg-danger',
      'Present': 'bg-warning',
      'Not Voting': 'bg-secondary'
    }
    
    return voteMap[position] || 'bg-secondary'
  }

  return (
    <div className="card h-100 shadow-sm">
      <div className="card-body p-3">
        <div className="d-flex justify-content-between align-items-start mb-2">
          <h6 className="card-title mb-1">{vote.candidate_name}</h6>
          <span className={`badge ${getVoteBadge(vote.vote_position)}`}>
            {vote.vote_position}
          </span>
        </div>
        
        {vote.bill && (
          <div className="text-decoration-none">
            <p className="text-muted small mb-2">
              <strong>Bill:</strong> {vote.bill_id}
            </p>
            
            {vote.bill_title && (
              <p className="card-text small mb-2 text-primary">
                {vote.bill_title.length > 100 
                  ? `${vote.bill_title.substring(0, 100)}...` 
                  : vote.bill_title
                }
              </p>
            )}
          </div>
        )}
        
        <div className="row text-muted small">
          <div className="col-6">
            <strong>Date:</strong> {formatDate(vote.vote_date)}
          </div>
          <div className="col-6">
            <strong>Chamber:</strong> {vote.chamber}
          </div>
        </div>
        
        <div className="mt-2">
          <span className="badge bg-light text-dark me-1">Roll {vote.roll_call}</span>
          <span className="badge bg-light text-dark">Congress {vote.congress}</span>
        </div>
      </div>
    </div>
  )
}

export default VoteCard 