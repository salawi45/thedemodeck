import React, { useState, useEffect } from 'react'
import { fetchVotes } from '../services/api'
import VoteCard from '../components/VoteCard'
import SearchAndFilter from '../components/SearchAndFilter'

function VotesList() {
  const [votes, setVotes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filters, setFilters] = useState({})

  useEffect(() => {
    loadVotes()
  }, [filters])

  const loadVotes = async () => {
    try {
      setLoading(true)
      const data = await fetchVotes(filters)
      setVotes(data.results || data)
      setError(null)
    } catch (err) {
      setError('Failed to load votes')
      console.error('Error loading votes:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters)
  }

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-2">Loading votes...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      </div>
    )
  }

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-12">
          <h1 className="mb-4">Votes</h1>
          
          <SearchAndFilter 
            onFilterChange={handleFilterChange}
            filterOptions={{
              vote_position: 'Vote Position',
              chamber: 'Chamber',
              congress: 'Congress'
            }}
          />
          
          {votes.length === 0 ? (
            <div className="text-center mt-4">
              <p>No votes found.</p>
            </div>
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
      </div>
    </div>
  )
}

export default VotesList 