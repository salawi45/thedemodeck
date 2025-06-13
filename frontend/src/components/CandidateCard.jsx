import { Link } from "react-router-dom"

function CandidateCard({ candidate }) {
  const calculateAge = (dob) => {
    if (!dob) return "Unknown"

    const birthDate = new Date(dob)
    const today = new Date()
    let age = today.getFullYear() - birthDate.getFullYear()
    const monthDiff = today.getMonth() - birthDate.getMonth()

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--
    }

    return age.toString()
  }

  return (
    <Link to={`/candidate/${candidate.id}`} className="text-decoration-none">
      <div className="card h-100 shadow-sm transition">
        <div className="card-body p-3">
          <div className="text-center mb-3">
            <img
              src={candidate.photo_url || "https://via.placeholder.com/150"}
              alt={candidate.label}
              className="rounded-circle img-fluid"
              style={{ width: "150px", height: "150px", objectFit: "cover" }}
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = "https://via.placeholder.com/150?text=No+Image";
              }}
            />
          </div>
          <div className="text-center">
            <h3 className="card-title h5 mb-2">{candidate.label}</h3>
            {candidate.position && <p className="text-muted mb-2">{candidate.position}</p>}
            {candidate.description && <p className="card-text small mb-2">{candidate.description}</p>}
            {candidate.dob && <p className="text-muted mb-1">Age: {calculateAge(candidate.dob)}</p>}
            {candidate.party_qid && <p className="badge bg-primary mb-1">{candidate.party_qid}</p>}
            {candidate.ideology_qid && <p className="badge bg-secondary">{candidate.ideology_qid}</p>}
          </div>
        </div>
      </div>
    </Link>
  )
}

export default CandidateCard
