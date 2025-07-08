import { API_BASE_URL, ENDPOINTS } from "../config/api"

export const fetchCandidates = async (filters = {}) => {
  try {
    let url = `${API_BASE_URL}${ENDPOINTS.candidates}`

    if (Object.keys(filters).length > 0) {
      const params = new URLSearchParams()

      if (filters.party_qid) params.append("party_qid", filters.party_qid)
      if (filters.ideology_qid) params.append("ideology_qid", filters.ideology_qid)
      if (filters.min_age) params.append("min_age", filters.min_age)
      if (filters.max_age) params.append("max_age", filters.max_age)
      if (filters.search) params.append("search", filters.search)
      if (filters.chamber) params.append("chamber", filters.chamber)

      url += `?${params.toString()}`
    }

    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error("Error fetching candidates:", error)
    throw error
  }
}

export const fetchCandidateById = async (id) => {
  try {
    const response = await fetch(`${API_BASE_URL}${ENDPOINTS.candidates}${id}/`)

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error(`Error fetching candidate with ID ${id}:`, error)
    throw error
  }
}

export const fetchBills = async (filters = {}) => {
  try {
    let url = `${API_BASE_URL}${ENDPOINTS.bills}`

    if (Object.keys(filters).length > 0) {
      const params = new URLSearchParams()

      if (filters.congress) params.append("congress", filters.congress)
      if (filters.bill_type) params.append("bill_type", filters.bill_type)
      if (filters.status) params.append("status", filters.status)
      if (filters.search) params.append("search", filters.search)
      if (filters.page) params.append("page", filters.page)

      url += `?${params.toString()}`
    }

    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error("Error fetching bills:", error)
    throw error
  }
}

export const fetchBillById = async (id) => {
  try {
    const response = await fetch(`${API_BASE_URL}${ENDPOINTS.bills}${id}/`)

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error(`Error fetching bill with ID ${id}:`, error)
    throw error
  }
}

// Only use the custom endpoint for single bill detail
export const fetchBillByBillId = async (billId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/bills/by-bill-id/${billId}/`)
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error(`Error fetching bill with bill_id ${billId}:`, error)
    throw error
  }
}

// Alias for BillDetail component (single bill detail only)
export const getBillDetail = fetchBillByBillId

export const fetchCandidateBills = async (candidateId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/candidates/${candidateId}/bills/`)

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error(`Error fetching bills for candidate ${candidateId}:`, error)
    throw error
  }
}

export const fetchCandidateVotes = async (candidateId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/candidates/${candidateId}/votes/`)

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error(`Error fetching votes for candidate ${candidateId}:`, error)
    throw error
  }
}

export const fetchBillVotes = async (billId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/bills/${billId}/votes/`)

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error(`Error fetching votes for bill ${billId}:`, error)
    throw error
  }
}

// Alias for BillDetail component
export const getBillVotes = fetchBillVotes

export const fetchVotes = async (filters = {}) => {
  try {
    let url = `${API_BASE_URL}${ENDPOINTS.votes}`

    if (Object.keys(filters).length > 0) {
      const params = new URLSearchParams()

      if (filters.vote_position) params.append("vote_position", filters.vote_position)
      if (filters.chamber) params.append("chamber", filters.chamber)
      if (filters.congress) params.append("congress", filters.congress)
      if (filters.search) params.append("search", filters.search)

      url += `?${params.toString()}`
    }

    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error("Error fetching votes:", error)
    throw error
  }
}

