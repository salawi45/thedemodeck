"use client"

import { useState, useEffect } from "react"

function SearchAndFilter({ onFilterChange }) {
  const [searchText, setSearchText] = useState("")
  const [showFilters, setShowFilters] = useState(false)
  const [filters, setFilters] = useState({})

  // State for dynamic filter options
  const [parties, setParties] = useState([])
  const [ideologies, setIdeologies] = useState([])
  const [loading, setLoading] = useState(false)

  // Fetch unique parties and ideologies from API on component mount
  useEffect(() => {
    const fetchFilterOptions = async () => {
      try {
        setLoading(true)
        const baseUrl = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000"
        
        // Fetch parties
        const partiesResponse = await fetch(`${baseUrl}/api/parties/`)
        if (!partiesResponse.ok) {
          throw new Error(`HTTP error! status: ${partiesResponse.status}`)
        }
        const partiesData = await partiesResponse.json()
        
        // Fetch ideologies
        const ideologiesResponse = await fetch(`${baseUrl}/api/ideologies/`)
        if (!ideologiesResponse.ok) {
          throw new Error(`HTTP error! status: ${ideologiesResponse.status}`)
        }
        const ideologiesData = await ideologiesResponse.json()

        // Process parties
        const uniqueParties = partiesData.map(party => ({
          name: party,
          count: 1 // Since we're getting unique values, each appears once
        })).sort((a, b) => a.name.localeCompare(b.name))

        // Process ideologies
        const uniqueIdeologies = ideologiesData.map(ideology => ({
          name: ideology,
          count: 1 // Since we're getting unique values, each appears once
        })).sort((a, b) => a.name.localeCompare(b.name))

        console.log("Processed parties:", uniqueParties)
        console.log("Processed ideologies:", uniqueIdeologies)

        setParties(uniqueParties)
        setIdeologies(uniqueIdeologies)
      } catch (error) {
        console.error("Error fetching filter options:", error)
        console.error("Error details:", {
          message: error.message,
          stack: error.stack
        })
        // fallback to default options if fetch fails
        setParties([
          { name: "Democratic Party", count: 0 },
          { name: "Republican Party", count: 0 },
          { name: "Independent", count: 0 },
        ])
        setIdeologies([
          { name: "Conservatism", count: 0 },
          { name: "Liberalism", count: 0 },
          { name: "Progressivism", count: 0 },
        ])
      } finally {
        setLoading(false)
      }
    }

    fetchFilterOptions()
  }, [])

  // Handle search text changes
  const handleSearch = (e) => {
    const text = e.target.value
    setSearchText(text)
    onFilterChange({ ...filters, search: text })
  }

  // Toggle visibility of filter panel
  const toggleFilters = () => {
    setShowFilters(!showFilters)
  }

  // Apply filters including search text
  const applyFilters = () => {
    onFilterChange({ ...filters, search: searchText })
  }

  // Reset all filters and search text
  const resetFilters = () => {
    setFilters({})
    setSearchText("")
    onFilterChange({})
  }

  // Update a single filter key
  const updateFilter = (key, value) => {
    setFilters((prev) => {
      if (prev[key] === value) {
        const newFilters = { ...prev }
        delete newFilters[key]
        return newFilters
      }
      return { ...prev, [key]: value }
    })
  }

  const activeFilterCount = Object.keys(filters).length

  return (
    <div className="card shadow-sm mb-4">
      <div className="card-body">
        <div className="d-flex align-items-center gap-3 mb-3">
          <div className="input-group flex-grow-1">
            <span className="input-group-text bg-white border-end-0">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path
                  d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
            </span>
            <input
              type="text"
              className="form-control border-start-0"
              placeholder="Search candidates by name..."
              value={searchText}
              onChange={handleSearch}
            />
          </div>

          <button 
            className="btn btn-outline-primary d-flex align-items-center gap-2" 
            onClick={toggleFilters}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path
                d="M3 4.6C3 4.03995 3 3.75992 3.10899 3.54601C3.20487 3.35785 3.35785 3.20487 3.54601 3.10899C3.75992 3 4.03995 3 4.6 3H19.4C19.9601 3 20.2401 3 20.454 3.10899C20.6422 3.20487 20.7951 3.35785 20.891 3.54601C21 3.75992 21 4.03995 21 4.6V6.33726C21 6.58185 21 6.70414 20.9724 6.81923C20.9479 6.92127 20.9075 7.01881 20.8526 7.10828C20.7908 7.2092 20.7043 7.29568 20.5314 7.46863L14.4686 13.5314C14.2957 13.7043 14.2092 13.7908 14.1474 13.8917C14.0925 13.9812 14.0521 14.0787 14.0276 14.1808C14 14.2959 14 14.4182 14 14.6627V17L10 21V14.6627C10 14.4182 10 14.2959 9.97237 14.1808C9.94787 14.0787 9.90747 13.9812 9.85264 13.8917C9.7908 13.7908 9.70432 13.7043 9.53137 13.5314L3.46863 7.46863C3.29568 7.29568 3.2092 7.2092 3.14736 7.10828C3.09253 7.01881 3.05213 6.92127 3.02763 6.81923C3 6.70414 3 6.58185 3 6.33726V4.6Z"
                stroke="currentColor"
                strokeWidth="2"
              />
            </svg>
            Filters
            {activeFilterCount > 0 && (
              <span className="badge bg-primary rounded-pill">{activeFilterCount}</span>
            )}
          </button>
        </div>

        {showFilters && (
          <div className="border-top pt-3">
            <div className="row g-4">
              <div className="col-md-6">
                <div className="mb-3">
                  <h5 className="mb-3">Political Party</h5>
                  <div className="d-flex flex-wrap gap-2">
                    {loading ? (
                      <p className="text-muted">Loading parties...</p>
                    ) : (
                      parties.map((party) => (
                        <button
                          key={party.name}
                          className={`btn btn-sm ${filters.party_qid === party.name ? 'btn-primary' : 'btn-outline-primary'}`}
                          onClick={() => updateFilter("party_qid", party.name)}
                        >
                          {party.name} ({party.count})
                        </button>
                      ))
                    )}
                  </div>
                </div>
              </div>

              <div className="col-md-6">
                <div className="mb-3">
                  <h5 className="mb-3">Political Ideology</h5>
                  <div className="d-flex flex-wrap gap-2">
                    {loading ? (
                      <p className="text-muted">Loading ideologies...</p>
                    ) : (
                      ideologies.map((ideology) => (
                        <button
                          key={ideology.name}
                          className={`btn btn-sm ${filters.ideology_qid === ideology.name ? 'btn-primary' : 'btn-outline-primary'}`}
                          onClick={() => updateFilter("ideology_qid", ideology.name)}
                        >
                          {ideology.name} ({ideology.count})
                        </button>
                      ))
                    )}
                  </div>
                </div>
              </div>

              <div className="col-12">
                <div className="mb-3">
                  <h5 className="mb-3">Age Range</h5>
                  <div className="row g-3 align-items-end">
                    <div className="col-md-5">
                      <label className="form-label">Min Age</label>
                      <input
                        type="number"
                        className="form-control"
                        value={filters.min_age || ""}
                        onChange={(e) =>
                          updateFilter("min_age", e.target.value ? Number(e.target.value) : "")
                        }
                        placeholder="18"
                        min="18"
                        max="100"
                      />
                    </div>
                    <div className="col-md-2 text-center">
                      <span className="text-muted">to</span>
                    </div>
                    <div className="col-md-5">
                      <label className="form-label">Max Age</label>
                      <input
                        type="number"
                        className="form-control"
                        value={filters.max_age || ""}
                        onChange={(e) =>
                          updateFilter("max_age", e.target.value ? Number(e.target.value) : "")
                        }
                        placeholder="100"
                        min="18"
                        max="100"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="d-flex justify-content-end gap-2 mt-3">
              <button className="btn btn-outline-secondary" onClick={resetFilters}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" className="me-1">
                  <path
                    d="M3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12Z"
                    stroke="currentColor"
                    strokeWidth="2"
                  />
                  <path d="M9 9L15 15M15 9L9 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                </svg>
                Reset All
              </button>
              <button className="btn btn-primary" onClick={applyFilters}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" className="me-1">
                  <path
                    d="M20 6L9 17L4 12"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                Apply Filters
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default SearchAndFilter
