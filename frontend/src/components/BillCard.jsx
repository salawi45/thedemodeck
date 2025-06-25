import { Link } from "react-router-dom"

function BillCard({ bill }) {
  const formatDate = (dateString) => {
    if (!dateString) return "Unknown"
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  const getStatusBadge = (status) => {
    const statusMap = {
      'Introduced': 'bg-primary',
      'Referred to Committee': 'bg-info',
      'Reported by Committee': 'bg-warning',
      'Passed House': 'bg-success',
      'Passed Senate': 'bg-success',
      'Enacted': 'bg-success',
      'Vetoed': 'bg-danger',
      'Failed': 'bg-danger'
    }
    
    return statusMap[status] || 'bg-secondary'
  }

  return (
    <Link to={`/bill/${bill.id}`} className="text-decoration-none fade-in button-hover">
      <div className="card h-100 shadow-sm hover-lift transition">
        <div className="card-body p-3">
          <div className="d-flex justify-content-between align-items-start mb-2">
            <h5 className="card-title mb-1">{bill.bill_id}</h5>
            {bill.status && (
              <span className={`badge ${getStatusBadge(bill.status)}`}>
                {bill.status}
              </span>
            )}
          </div>
          
          {bill.title && (
            <p className="card-text small mb-2">
              {bill.title.length > 150 
                ? `${bill.title.substring(0, 150)}...` 
                : bill.title
              }
            </p>
          )}
          
          <div className="row text-muted small">
            {bill.introduced_date && (
              <div className="col-6">
                <strong>Introduced:</strong> {formatDate(bill.introduced_date)}
              </div>
            )}
            {bill.last_action_date && (
              <div className="col-6">
                <strong>Last Action:</strong> {formatDate(bill.last_action_date)}
              </div>
            )}
          </div>
          
          {bill.sponsor_name && (
            <p className="text-muted small mb-1 mt-2">
              <strong>Sponsor:</strong> {bill.sponsor_name}
            </p>
          )}
          
          <div className="mt-2">
            <span className="badge bg-light text-dark me-1">Congress {bill.congress}</span>
            <span className="badge bg-light text-dark">{bill.bill_type?.toUpperCase()}</span>
          </div>
        </div>
      </div>
    </Link>
  )
}

export default BillCard 