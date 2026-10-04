const API_BASE = '/api'

export async function fetchJson(url, options = {}) {
  const res = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!res.ok) {
    let errorMsg = `HTTP Error ${res.status}`
    try {
      const data = await res.json()
      errorMsg = data.detail || errorMsg
    } catch (e) {
      // ignore json parse error
    }
    const err = new Error(errorMsg)
    err.status = res.status
    throw err
  }

  return res.json()
}

export const api = {
  // Cities
  async getCities() {
    return fetchJson(`${API_BASE}/cities`)
  },

  // Movies
  async getMovies(featured = false) {
    return fetchJson(`${API_BASE}/movies?featured=${featured}`)
  },

  async getMovieDetail(movieId) {
    return fetchJson(`${API_BASE}/movies/${movieId}`)
  },

  // Theaters
  async getTheaters(city = 'Hyderabad') {
    return fetchJson(`${API_BASE}/theaters?city=${encodeURIComponent(city)}`)
  },

  // Shows
  async getShows(params = {}) {
    const query = new URLSearchParams()
    if (params.city) query.append('city', params.city)
    if (params.date) query.append('date', params.date)
    if (params.movie_id) query.append('movie_id', params.movie_id)
    if (params.theater_id) query.append('theater_id', params.theater_id)
    if (params.format) query.append('format', params.format)

    return fetchJson(`${API_BASE}/shows?${query.toString()}`)
  },

  // Seats & Locking
  async getShowSeats(showId, userId = '') {
    return fetchJson(`${API_BASE}/shows/${showId}/seats?user_id=${encodeURIComponent(userId)}`)
  },

  async lockSeats(showId, seatIds, userId) {
    return fetchJson(`${API_BASE}/shows/${showId}/lock-seats`, {
      method: 'POST',
      body: JSON.stringify({ seat_ids: seatIds, user_id: userId }),
    })
  },

  async releaseSeats(showId, seatIds, userId) {
    return fetchJson(`${API_BASE}/shows/${showId}/release-seats`, {
      method: 'POST',
      body: JSON.stringify({ seat_ids: seatIds, user_id: userId }),
    })
  }
  ,

  // Checkout & Fees
  async calculateFees(showId, seatIds) {
    return fetchJson(`${API_BASE}/checkout/calculate`, {
      method: 'POST',
      body: JSON.stringify({ show_id: showId, seat_ids: seatIds }),
    })
  },

  async processCheckout(payload) {
    return fetchJson(`${API_BASE}/checkout/pay`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  // Ticket Verification
  async getTicket(bookingRef) {
    return fetchJson(`${API_BASE}/tickets/${encodeURIComponent(bookingRef)}`)
  },

  // Auth / Guest session
  async getGuestSession() {
    return fetchJson(`${API_BASE}/auth/guest`, { method: 'POST' })
  },

  // Admin APIs
  async getAdminStats() {
    return fetchJson(`${API_BASE}/admin/stats`)
  },

  async addMovie(payload) {
    return fetchJson(`${API_BASE}/admin/movies`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async updateMovie(movieId, payload) {
    return fetchJson(`${API_BASE}/admin/movies/${movieId}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    })
  },

  async deleteMovie(movieId) {
    return fetchJson(`${API_BASE}/admin/movies/${movieId}`, {
      method: 'DELETE',
    })
  },

  async addTheater(payload) {
    return fetchJson(`${API_BASE}/admin/theaters`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async updateTheater(theaterId, payload) {
    return fetchJson(`${API_BASE}/admin/theaters/${theaterId}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    })
  },

  async deleteTheater(theaterId) {
    return fetchJson(`${API_BASE}/admin/theaters/${theaterId}`, {
      method: 'DELETE',
    })
  },

  async addScreen(payload) {
    return fetchJson(`${API_BASE}/admin/screens`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async deleteScreen(screenId) {
    return fetchJson(`${API_BASE}/admin/screens/${screenId}`, {
      method: 'DELETE',
    })
  },

  async addShow(payload) {
    return fetchJson(`${API_BASE}/admin/shows`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async deleteShow(showId) {
    return fetchJson(`${API_BASE}/admin/shows/${showId}`, {
      method: 'DELETE',
    })
  },
}

