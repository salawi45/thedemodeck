import React, { useState, useEffect } from 'react'
import { fetchBills } from '../services/api'
import BillCard from '../components/BillCard'
import SearchAndFilter from '../components/SearchAndFilter'

function BillsList() {
  const [bills, setBills] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filters, setFilters] = useState({})
  const [pagination, setPagination] = useState({
    currentPage: 1,
    totalPages: 1,
    totalCount: 0,
    hasNext: false,
    hasPrevious: false
  })

  useEffect(() => {
    loadBills()
  }, [filters, pagination.currentPage])

  const loadBills = async () => {
    try {
      setLoading(true)
      const data = await fetchBills({
        ...filters,
        page: pagination.currentPage
      })
      
      setBills(data.results || data)
      
      // Update pagination info
      if (data.count !== undefined) {
        setPagination(prev => ({
          ...prev,
          totalCount: data.count,
          totalPages: Math.ceil(data.count / 25), // Assuming 25 items per page
          hasNext: !!data.next,
          hasPrevious: !!data.previous
        }))
      }
      
      setError(null)
    } catch (err) {
      setError('Failed to load bills')
      console.error('Error loading bills:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters)
    setPagination(prev => ({ ...prev, currentPage: 1 })) // Reset to first page when filtering
  }

  const handlePageChange = (page) => {
    setPagination(prev => ({ ...prev, currentPage: page }))
  }

  const renderPagination = () => {
    if (pagination.totalPages <= 1) return null

    const pages = []
    const maxVisiblePages = 5
    let startPage = Math.max(1, pagination.currentPage - Math.floor(maxVisiblePages / 2))
    let endPage = Math.min(pagination.totalPages, startPage + maxVisiblePages - 1)

    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1)
    }

    // Previous button
    if (pagination.hasPrevious) {
      pages.push(
        <li key="prev" className="page-item">
          <button
            className="page-link"
            onClick={() => handlePageChange(pagination.currentPage - 1)}
            disabled={loading}
          >
            &laquo; Previous
          </button>
        </li>
      )
    }

    // First page
    if (startPage > 1) {
      pages.push(
        <li key="first" className="page-item">
          <button
            className="page-link"
            onClick={() => handlePageChange(1)}
            disabled={loading}
          >
            1
          </button>
        </li>
      )
      if (startPage > 2) {
        pages.push(
          <li key="ellipsis1" className="page-item disabled">
            <span className="page-link">...</span>
          </li>
        )
      }
    }

    // Page numbers
    for (let i = startPage; i <= endPage; i++) {
      pages.push(
        <li key={i} className={`page-item ${i === pagination.currentPage ? 'active' : ''}`}>
          <button
            className="page-link"
            onClick={() => handlePageChange(i)}
            disabled={loading}
          >
            {i}
          </button>
        </li>
      )
    }

    // Last page
    if (endPage < pagination.totalPages) {
      if (endPage < pagination.totalPages - 1) {
        pages.push(
          <li key="ellipsis2" className="page-item disabled">
            <span className="page-link">...</span>
          </li>
        )
      }
      pages.push(
        <li key="last" className="page-item">
          <button
            className="page-link"
            onClick={() => handlePageChange(pagination.totalPages)}
            disabled={loading}
          >
            {pagination.totalPages}
          </button>
        </li>
      )
    }

    // Next button
    if (pagination.hasNext) {
      pages.push(
        <li key="next" className="page-item">
          <button
            className="page-link"
            onClick={() => handlePageChange(pagination.currentPage + 1)}
            disabled={loading}
          >
            Next &raquo;
          </button>
        </li>
      )
    }

    return (
      <nav aria-label="Bills pagination" className="mt-4">
        <ul className="pagination justify-content-center">
          {pages}
        </ul>
        <div className="text-center text-muted mt-2">
          Showing page {pagination.currentPage} of {pagination.totalPages} 
          ({pagination.totalCount} total bills)
        </div>
      </nav>
    )
  }

  if (loading && bills.length === 0) {
    return (
      <div className="container mt-4">
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-2">Loading bills...</p>
        </div>
      </div>
    )
  }

  if (error && bills.length === 0) {
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
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h1>Bills</h1>
            {pagination.totalCount > 0 && (
              <span className="text-muted">
                Total: {pagination.totalCount.toLocaleString()} bills
              </span>
            )}
          </div>
          
          <SearchAndFilter 
            onFilterChange={handleFilterChange}
            filterOptions={{
              congress: 'Congress',
              bill_type: 'Bill Type',
              status: 'Status'
            }}
          />
          
          {loading && bills.length > 0 && (
            <div className="text-center my-3">
              <div className="spinner-border spinner-border-sm" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              <span className="ms-2">Loading more bills...</span>
            </div>
          )}
          
          {bills.length === 0 && !loading ? (
            <div className="text-center mt-4">
              <p>No bills found.</p>
            </div>
          ) : (
            <>
              <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                {bills.map((bill) => (
                  <div key={bill.id} className="col">
                    <BillCard bill={bill} />
                  </div>
                ))}
              </div>
              
              {renderPagination()}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default BillsList 