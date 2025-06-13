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

