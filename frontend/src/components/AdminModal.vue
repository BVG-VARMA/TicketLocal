<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto bg-black/90 backdrop-blur-md animate-in fade-in duration-200">
    <div class="bg-[#181a24] w-full max-w-5xl rounded-3xl border border-slate-700 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200 my-auto select-none max-h-[92vh] flex flex-col">
      
      <!-- Admin Modal Header -->
      <div class="p-5 border-b border-slate-800 bg-[#202230] flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-amber-500 to-[#F84464] text-white flex items-center justify-center shadow-lg shadow-[#F84464]/20 font-black">
            <ShieldCheck class="w-5 h-5 text-white" />
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h2 class="text-lg font-black text-white">CinePass Cinema Admin Portal</h2>
              <span class="px-2 py-0.5 rounded bg-amber-500/20 border border-amber-500/40 text-[10px] font-black text-amber-400 uppercase tracking-wider">
                Admin Control
              </span>
            </div>
            <p class="text-xs text-slate-400">Manage Movies, Theaters, Screens, Tiered Seating & Showtimes</p>
          </div>
        </div>

        <button 
          @click="$emit('close')"
          class="p-2 rounded-full bg-slate-800 hover:bg-[#F84464] text-slate-300 hover:text-white transition-colors cursor-pointer"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex items-center gap-2 px-6 pt-3 bg-[#1e202d] border-b border-slate-800 overflow-x-auto no-scrollbar text-xs font-bold">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="flex items-center gap-2 px-4 py-3 border-b-2 transition-all cursor-pointer whitespace-nowrap"
          :class="activeTab === tab.id ? 'border-[#F84464] text-white bg-slate-800/40 rounded-t-xl' : 'border-transparent text-slate-400 hover:text-slate-200'"
        >
          <component :is="tab.icon" class="w-4 h-4" :class="activeTab === tab.id ? 'text-[#F84464]' : ''" />
          <span>{{ tab.label }}</span>
        </button>
      </div>

      <!-- Status / Alert Message -->
      <div v-if="alertMessage" class="mx-6 mt-4 p-3.5 rounded-2xl text-xs flex items-center justify-between gap-3 animate-in fade-in" :class="alertType === 'success' ? 'bg-emerald-950/80 border border-emerald-500 text-emerald-200' : 'bg-rose-950/80 border border-rose-500 text-rose-200'">
        <div class="flex items-center gap-2">
          <CheckCircle2 v-if="alertType === 'success'" class="w-4 h-4 text-emerald-400 shrink-0" />
          <AlertTriangle v-else class="w-4 h-4 text-rose-400 shrink-0" />
          <span>{{ alertMessage }}</span>
        </div>
        <button @click="alertMessage = ''" class="font-bold text-xs hover:underline cursor-pointer">Dismiss</button>
      </div>

      <!-- Main Tab Content Area -->
      <div class="flex-1 overflow-y-auto p-6 space-y-6">

        <!-- TAB 1: DASHBOARD STATS -->
        <div v-if="activeTab === 'overview'" class="space-y-6">
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            <div class="bg-[#222434] p-4 rounded-2xl border border-slate-800 flex flex-col justify-between">
              <span class="text-xs font-bold text-slate-400">Total Movies</span>
              <div class="text-2xl font-black text-white mt-2">{{ stats.total_movies }}</div>
              <span class="text-[10px] text-emerald-400 font-semibold mt-1">Live in Catalog</span>
            </div>
            <div class="bg-[#222434] p-4 rounded-2xl border border-slate-800 flex flex-col justify-between">
              <span class="text-xs font-bold text-slate-400">Theaters</span>
              <div class="text-2xl font-black text-white mt-2">{{ stats.total_theaters }}</div>
              <span class="text-[10px] text-indigo-400 font-semibold mt-1">Active Venues</span>
            </div>
            <div class="bg-[#222434] p-4 rounded-2xl border border-slate-800 flex flex-col justify-between">
              <span class="text-xs font-bold text-slate-400">Screens</span>
              <div class="text-2xl font-black text-white mt-2">{{ stats.total_screens }}</div>
              <span class="text-[10px] text-amber-400 font-semibold mt-1">IMAX & Atmos</span>
            </div>
            <div class="bg-[#222434] p-4 rounded-2xl border border-slate-800 flex flex-col justify-between">
              <span class="text-xs font-bold text-slate-400">Active Shows</span>
              <div class="text-2xl font-black text-white mt-2">{{ stats.total_shows }}</div>
              <span class="text-[10px] text-rose-400 font-semibold mt-1">Scheduled</span>
            </div>
            <div class="bg-[#222434] p-4 rounded-2xl border border-slate-800 flex flex-col justify-between">
              <span class="text-xs font-bold text-slate-400">Citizen Bookings</span>
              <div class="text-2xl font-black text-white mt-2">{{ stats.total_bookings }}</div>
              <span class="text-[10px] text-emerald-400 font-semibold mt-1">Tickets Issued</span>
            </div>
            <div class="bg-[#222434] p-4 rounded-2xl border border-slate-800 flex flex-col justify-between">
              <span class="text-xs font-bold text-slate-400">Total Revenue</span>
              <div class="text-xl font-black text-[#F84464] mt-2">₹{{ stats.total_revenue.toLocaleString('en-IN') }}</div>
              <span class="text-[10px] text-slate-400 font-semibold mt-1">Gross Sales</span>
            </div>
          </div>

          <!-- Quick Action Shortcuts -->
          <div class="bg-gradient-to-r from-[#202230] to-[#282136] p-6 rounded-3xl border border-slate-800">
            <h3 class="text-sm font-black text-white uppercase tracking-wider mb-2">Quick Administration Actions</h3>
            <p class="text-xs text-slate-400 mb-5">Seamlessly add new blockbuster movies, expand theater networks across cities, or schedule dynamic showtimes.</p>
            
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <button 
                @click="activeTab = 'movies'"
                class="p-4 rounded-2xl bg-slate-900/80 hover:bg-[#F84464]/20 border border-slate-700 hover:border-[#F84464] text-left transition-all group cursor-pointer"
              >
                <div class="text-2xl mb-2">🎬</div>
                <h4 class="text-xs font-bold text-white group-hover:text-[#F84464]">Add New Movie</h4>
                <p class="text-[11px] text-slate-400 mt-1">Upload poster, genres, runtime & rating</p>
              </button>

              <button 
                @click="activeTab = 'theaters'"
                class="p-4 rounded-2xl bg-slate-900/80 hover:bg-indigo-500/20 border border-slate-700 hover:border-indigo-500 text-left transition-all group cursor-pointer"
              >
                <div class="text-2xl mb-2">🏛️</div>
                <h4 class="text-xs font-bold text-white group-hover:text-indigo-400">Add Theater & Screens</h4>
                <p class="text-[11px] text-slate-400 mt-1">Create cinema hall & auto-generate BMS seat tiers</p>
              </button>

              <button 
                @click="activeTab = 'shows'"
                class="p-4 rounded-2xl bg-slate-900/80 hover:bg-emerald-500/20 border border-slate-700 hover:border-emerald-500 text-left transition-all group cursor-pointer"
              >
                <div class="text-2xl mb-2">🎟️</div>
                <h4 class="text-xs font-bold text-white group-hover:text-emerald-400">Schedule Showtimes</h4>
                <p class="text-[11px] text-slate-400 mt-1">Assign movies to screens with date & pricing</p>
              </button>
            </div>
          </div>
        </div>

        <!-- TAB 2: MOVIES MANAGER -->
        <div v-else-if="activeTab === 'movies'" class="space-y-6">
          
          <!-- Add Movie Form Card -->
          <div class="bg-[#202230] p-6 rounded-3xl border border-slate-800 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 class="text-sm font-black text-white">Add New Movie to CinePass</h3>
                <p class="text-xs text-slate-400">Publish movie info, runtime, certificate, and poster</p>
              </div>
              <button 
                @click="fillMoviePreset"
                class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-[#F84464] text-xs font-bold border border-slate-700 transition-colors cursor-pointer"
              >
                ✨ Fill Sample Blockbuster
              </button>
            </div>

            <form @submit.prevent="submitMovie" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-xs">
              
              <div>
                <label class="font-bold text-slate-300 block mb-1">Movie Title *</label>
                <input 
                  v-model="movieForm.title" 
                  required 
                  type="text" 
                  placeholder="e.g. Avatar: Fire and Ash" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">Genres (comma separated) *</label>
                <input 
                  v-model="movieForm.genres" 
                  required 
                  type="text" 
                  placeholder="Action, Sci-Fi, Adventure" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">Languages *</label>
                <input 
                  v-model="movieForm.languages" 
                  required 
                  type="text" 
                  placeholder="Hindi, English, Telugu, Tamil" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">Certificate *</label>
                <select 
                  v-model="movieForm.certificate" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-[#F84464]"
                >
                  <option value="U">U (Universal)</option>
                  <option value="UA">UA (Parental Guidance)</option>
                  <option value="A">A (Adults Only)</option>
                </select>
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">Duration (minutes) *</label>
                <input 
                  v-model.number="movieForm.duration_min" 
                  required 
                  type="number" 
                  min="30" 
                  max="300"
                  placeholder="150" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">Rating (e.g. 9.1) *</label>
                <input 
                  v-model.number="movieForm.rating" 
                  required 
                  type="number" 
                  step="0.1" 
                  min="1" 
                  max="10"
                  placeholder="8.9" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div class="sm:col-span-2">
                <label class="font-bold text-slate-300 block mb-1">Poster Image URL *</label>
                <input 
                  v-model="movieForm.poster_url" 
                  required 
                  type="url" 
                  placeholder="https://images.unsplash.com/photo-..." 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">Release Date *</label>
                <input 
                  v-model="movieForm.release_date" 
                  required 
                  type="date" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div class="sm:col-span-3">
                <label class="font-bold text-slate-300 block mb-1">Synopsis / Storyline *</label>
                <textarea 
                  v-model="movieForm.synopsis" 
                  required 
                  rows="2"
                  placeholder="Enter high-octane cinematic storyline and movie plot..." 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                ></textarea>
              </div>

              <div class="sm:col-span-3 flex items-center justify-between pt-2">
                <label class="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" v-model="movieForm.is_featured" class="w-4 h-4 rounded text-[#F84464] focus:ring-0 bg-slate-900 border-slate-700" />
                  <span class="font-bold text-slate-300">Set as Featured Hero Banner Movie</span>
                </label>

                <button 
                  :disabled="saving"
                  type="submit" 
                  class="px-6 py-3 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs shadow-lg shadow-[#F84464]/30 disabled:opacity-50 transition-all cursor-pointer flex items-center gap-2"
                >
                  <Plus class="w-4 h-4" />
                  <span>{{ saving ? 'Publishing...' : 'Add Movie to Catalog' }}</span>
                </button>
              </div>

            </form>
          </div>

          <!-- Existing Movies Table -->
          <div class="bg-[#202230] p-6 rounded-3xl border border-slate-800 space-y-4">
            <h3 class="text-sm font-black text-white">Current Movie Catalog ({{ movies.length }})</h3>

            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs text-slate-300">
                <thead class="text-[11px] uppercase bg-slate-900 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th class="py-3 px-4">Movie</th>
                    <th class="py-3 px-4">Genres & Certificate</th>
                    <th class="py-3 px-4">Duration</th>
                    <th class="py-3 px-4">Rating</th>
                    <th class="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-800/80">
                  <tr v-for="m in movies" :key="m.id" class="hover:bg-slate-800/40">
                    <td class="py-3 px-4 flex items-center gap-3">
                      <img :src="m.poster_url" class="w-10 h-14 object-cover rounded-lg shadow" />
                      <div>
                        <span class="font-bold text-white text-sm block">{{ m.title }}</span>
                        <span class="text-[11px] text-slate-400">{{ m.languages }}</span>
                      </div>
                    </td>
                    <td class="py-3 px-4">
                      <span class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px] font-bold text-slate-200 mr-2">
                        {{ m.certificate }}
                      </span>
                      <span>{{ m.genres }}</span>
                    </td>
                    <td class="py-3 px-4">{{ m.duration_min }} mins</td>
                    <td class="py-3 px-4 text-amber-400 font-bold">★ {{ m.rating }}/10</td>
                    <td class="py-3 px-4 text-right">
                      <button 
                        @click="handleDeleteMovie(m.id)"
                        class="p-2 rounded-lg bg-rose-950/60 hover:bg-rose-900 border border-rose-800 text-rose-300 transition-colors cursor-pointer"
                        title="Delete Movie"
                      >
                        <Trash2 class="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>

        <!-- TAB 3: THEATERS & SCREENS -->
        <div v-else-if="activeTab === 'theaters'" class="space-y-6">
          
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            <!-- Add Theater Form -->
            <div class="bg-[#202230] p-6 rounded-3xl border border-slate-800 space-y-4">
              <h3 class="text-sm font-black text-white border-b border-slate-800 pb-3">1. Add New Theater Venue</h3>
              
              <form @submit.prevent="submitTheater" class="space-y-3.5 text-xs">
                <div>
                  <label class="font-bold text-slate-300 block mb-1">City Name *</label>
                  <input 
                    v-model="theaterForm.city_name" 
                    required 
                    type="text" 
                    placeholder="e.g. Hyderabad, Mumbai, Bengaluru" 
                    class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                  />
                </div>

                <div>
                  <label class="font-bold text-slate-300 block mb-1">Theater Name *</label>
                  <input 
                    v-model="theaterForm.name" 
                    required 
                    type="text" 
                    placeholder="e.g. CinePass IMAX Multiplex, Banjara Hills" 
                    class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                  />
                </div>

                <div>
                  <label class="font-bold text-slate-300 block mb-1">Address *</label>
                  <input 
                    v-model="theaterForm.address" 
                    required 
                    type="text" 
                    placeholder="e.g. Road No 2, Banjara Hills, Hyderabad" 
                    class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                  />
                </div>

                <div>
                  <label class="font-bold text-slate-300 block mb-1">Amenities</label>
                  <input 
                    v-model="theaterForm.amenities" 
                    type="text" 
                    placeholder="Parking, Food Court, Wheelchair Access, M-Ticket, Dolby Atmos" 
                    class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                  />
                </div>

                <button 
                  :disabled="saving"
                  type="submit" 
                  class="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-lg shadow-indigo-600/30 transition-all cursor-pointer flex items-center justify-center gap-2"
                >
                  <Plus class="w-4 h-4" />
                  <span>{{ saving ? 'Saving...' : 'Add Theater Venue' }}</span>
                </button>
              </form>
            </div>

            <!-- Add Screen & BMS Seating Form -->
            <div class="bg-[#202230] p-6 rounded-3xl border border-slate-800 space-y-4">
              <h3 class="text-sm font-black text-white border-b border-slate-800 pb-3">2. Add Screen with BookMyShow Tiered Seats</h3>

              <form @submit.prevent="submitScreen" class="space-y-3.5 text-xs">
                <div>
                  <label class="font-bold text-slate-300 block mb-1">Select Theater *</label>
                  <select 
                    v-model="screenForm.theater_id" 
                    required 
                    class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-[#F84464]"
                  >
                    <option v-for="t in theaters" :key="t.id" :value="t.id">
                      {{ t.name }} (ID: {{ t.id }})
                    </option>
                  </select>
                </div>

                <div>
                  <label class="font-bold text-slate-300 block mb-1">Screen Name *</label>
                  <input 
                    v-model="screenForm.name" 
                    required 
                    type="text" 
                    placeholder="e.g. Screen 1 - Laser IMAX" 
                    class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                  />
                </div>

                <div>
                  <label class="font-bold text-slate-300 block mb-1">Format *</label>
                  <select 
                    v-model="screenForm.format" 
                    class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-[#F84464]"
                  >
                    <option value="IMAX 3D">IMAX 3D</option>
                    <option value="Dolby Atmos 4K">Dolby Atmos 4K</option>
                    <option value="4DX 3D">4DX 3D</option>
                    <option value="Standard 2D">Standard 2D</option>
                  </select>
                </div>

                <div class="grid grid-cols-3 gap-2">
                  <div>
                    <label class="font-bold text-slate-300 block mb-1">Recliner Rows (₹350)</label>
                    <input v-model.number="screenForm.rows_recliner" type="number" min="0" max="6" class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-center" />
                  </div>
                  <div>
                    <label class="font-bold text-slate-300 block mb-1">Prime Rows (₹220)</label>
                    <input v-model.number="screenForm.rows_prime" type="number" min="1" max="10" class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-center" />
                  </div>
                  <div>
                    <label class="font-bold text-slate-300 block mb-1">Classic Rows (₹150)</label>
                    <input v-model.number="screenForm.rows_classic" type="number" min="0" max="10" class="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-center" />
                  </div>
                </div>

                <div class="p-2.5 bg-slate-900/60 rounded-xl border border-slate-800 text-[11px] text-slate-400">
                  Total Capacity: <strong class="text-white">{{ (screenForm.rows_recliner + screenForm.rows_prime + screenForm.rows_classic) * screenForm.seats_per_row }} seats</strong> (Auto-configured with BMS Aisle Layout)
                </div>

                <button 
                  :disabled="saving || !theaters.length"
                  type="submit" 
                  class="w-full py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-lg shadow-emerald-600/30 transition-all cursor-pointer flex items-center justify-center gap-2"
                >
                  <Plus class="w-4 h-4" />
                  <span>{{ saving ? 'Configuring Seats...' : 'Create Screen & Seat Layout' }}</span>
                </button>
              </form>
            </div>

          </div>

          <!-- Existing Theaters List -->
          <div class="bg-[#202230] p-6 rounded-3xl border border-slate-800 space-y-4">
            <h3 class="text-sm font-black text-white">Configured Theaters ({{ theaters.length }})</h3>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="t in theaters" :key="t.id" class="p-4 rounded-2xl bg-slate-900 border border-slate-800 flex items-start justify-between gap-3">
                <div>
                  <h4 class="font-black text-white text-sm">{{ t.name }}</h4>
                  <p class="text-xs text-slate-400 mt-0.5">{{ t.address }}</p>
                  <div class="flex flex-wrap gap-1.5 mt-2">
                    <span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300">
                      {{ t.screens ? t.screens.length : 0 }} Screens
                    </span>
                    <span class="px-2 py-0.5 rounded bg-indigo-950/80 border border-indigo-800 text-[10px] text-indigo-400">
                      {{ t.amenities.split(',')[0] }}
                    </span>
                  </div>
                </div>

                <button 
                  @click="handleDeleteTheater(t.id)"
                  class="p-2 rounded-lg bg-rose-950/60 hover:bg-rose-900 border border-rose-800 text-rose-300 transition-colors cursor-pointer"
                  title="Delete Theater"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

        </div>

        <!-- TAB 4: SHOWTIME SCHEDULER -->
        <div v-else-if="activeTab === 'shows'" class="space-y-6">
          
          <!-- Schedule Show Form -->
          <div class="bg-[#202230] p-6 rounded-3xl border border-slate-800 space-y-4">
            <h3 class="text-sm font-black text-white border-b border-slate-800 pb-3">Schedule Show for CinePass Cinemas</h3>

            <form @submit.prevent="submitShow" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
              
              <div>
                <label class="font-bold text-slate-300 block mb-1">Select Movie *</label>
                <select 
                  v-model="showForm.movie_id" 
                  required 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-[#F84464]"
                >
                  <option v-for="m in movies" :key="m.id" :value="m.id">
                    {{ m.title }}
                  </option>
                </select>
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">Select Theater Screen *</label>
                <select 
                  v-model="showForm.screen_id" 
                  required 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-[#F84464]"
                >
                  <template v-for="t in theaters" :key="t.id">
                    <option v-for="s in (t.screens || [])" :key="s.id" :value="s.id">
                      {{ t.name }} - {{ s.name }} ({{ s.format }})
                    </option>
                  </template>
                </select>
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">Show Date *</label>
                <input 
                  v-model="showForm.show_date" 
                  required 
                  type="date" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">Start Time (HH:MM) *</label>
                <input 
                  v-model="showForm.start_time" 
                  required 
                  type="time" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">End Time (HH:MM) *</label>
                <input 
                  v-model="showForm.end_time" 
                  required 
                  type="time" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">Language *</label>
                <input 
                  v-model="showForm.language" 
                  required 
                  type="text" 
                  placeholder="Telugu, Hindi, English" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">Format *</label>
                <select 
                  v-model="showForm.format" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-[#F84464]"
                >
                  <option value="IMAX 3D">IMAX 3D</option>
                  <option value="Dolby Atmos 4K">Dolby Atmos 4K</option>
                  <option value="4DX 3D">4DX 3D</option>
                  <option value="Standard 2D">Standard 2D</option>
                </select>
              </div>

              <div>
                <label class="font-bold text-slate-300 block mb-1">Surge Multiplier (1.0 - 2.0)</label>
                <input 
                  v-model.number="showForm.surge_multiplier" 
                  type="number" 
                  step="0.05" 
                  min="1.0" 
                  max="2.5" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div class="sm:col-span-2 lg:col-span-4 flex justify-end pt-2">
                <button 
                  :disabled="saving || !movies.length"
                  type="submit" 
                  class="px-8 py-3 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs shadow-lg shadow-[#F84464]/30 transition-all cursor-pointer flex items-center gap-2"
                >
                  <Calendar class="w-4 h-4" />
                  <span>{{ saving ? 'Scheduling...' : 'Schedule & Publish Show' }}</span>
                </button>
              </div>

            </form>
          </div>

          <!-- Existing Shows List -->
          <div class="bg-[#202230] p-6 rounded-3xl border border-slate-800 space-y-4">
            <h3 class="text-sm font-black text-white">Scheduled Shows ({{ scheduledShows.length }})</h3>

            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs text-slate-300">
                <thead class="text-[11px] uppercase bg-slate-900 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th class="py-3 px-4">Movie</th>
                    <th class="py-3 px-4">Theater / Screen</th>
                    <th class="py-3 px-4">Date & Time</th>
                    <th class="py-3 px-4">Format / Language</th>
                    <th class="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-800/80">
                  <tr v-for="s in scheduledShows" :key="s.id" class="hover:bg-slate-800/40">
                    <td class="py-3 px-4 font-bold text-white">{{ s.movie?.title }}</td>
                    <td class="py-3 px-4">{{ s.theater?.name }} • {{ s.screen?.name }}</td>
                    <td class="py-3 px-4">
                      <span class="text-slate-300 font-semibold">{{ s.show_date }}</span>
                      <span class="text-emerald-400 font-mono ml-2">{{ s.start_time }}</span>
                    </td>
                    <td class="py-3 px-4">
                      <span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] font-bold text-slate-300 mr-2">
                        {{ s.format }}
                      </span>
                      <span>{{ s.language }}</span>
                    </td>
                    <td class="py-3 px-4 text-right">
                      <button 
                        @click="handleDeleteShow(s.id)"
                        class="p-2 rounded-lg bg-rose-950/60 hover:bg-rose-900 border border-rose-800 text-rose-300 transition-colors cursor-pointer"
                        title="Cancel Show"
                      >
                        <Trash2 class="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { 
  X, ShieldCheck, Film, Building2, Calendar, BarChart3, 
  Plus, Trash2, CheckCircle2, AlertTriangle 
} from 'lucide-vue-next'
import { api } from '../services/api'

const props = defineProps({
  isOpen: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'data-updated'])

const activeTab = ref('overview')
const saving = ref(false)
const alertMessage = ref('')
const alertType = ref('success')

const tabs = [
  { id: 'overview', label: 'Overview & Stats', icon: BarChart3 },
  { id: 'movies', label: 'Movies Manager', icon: Film },
  { id: 'theaters', label: 'Theaters & Screens', icon: Building2 },
  { id: 'shows', label: 'Show Scheduler', icon: Calendar },
]

const stats = reactive({
  total_movies: 0,
  total_theaters: 0,
  total_screens: 0,
  total_shows: 0,
  total_bookings: 0,
  total_revenue: 0,
})

const movies = ref([])
const theaters = ref([])
const scheduledShows = ref([])

// Forms
const movieForm = reactive({
  title: '',
  genres: '',
  languages: 'Hindi, Telugu, English',
  certificate: 'UA',
  duration_min: 155,
  rating: 8.8,
  poster_url: '',
  release_date: new Date().toISOString().split('T')[0],
  synopsis: '',
  is_featured: false,
})

const theaterForm = reactive({
  city_name: 'Hyderabad',
  name: '',
  address: '',
  amenities: 'Parking, Food Court, Wheelchair Access, M-Ticket, Dolby Atmos',
})

const screenForm = reactive({
  theater_id: null,
  name: 'Screen 1 - Laser IMAX',
  format: 'IMAX 3D',
  rows_recliner: 2,
  rows_prime: 4,
  rows_classic: 4,
  seats_per_row: 18,
})

const showForm = reactive({
  movie_id: null,
  screen_id: null,
  show_date: new Date().toISOString().split('T')[0],
  start_time: '19:30',
  end_time: '22:15',
  language: 'English',
  format: 'IMAX 3D',
  surge_multiplier: 1.0,
})

function showAlert(msg, type = 'success') {
  alertMessage.value = msg
  alertType.value = type
  setTimeout(() => {
    if (alertMessage.value === msg) alertMessage.value = ''
  }, 4000)
}

function fillMoviePreset() {
  movieForm.title = 'Gladiator II: Rise of the Colosseum'
  movieForm.genres = 'Action, Historical, Drama, Epic'
  movieForm.languages = 'English, Hindi, Telugu'
  movieForm.certificate = 'A'
  movieForm.duration_min = 160
  movieForm.rating = 9.2
  movieForm.poster_url = 'https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=800&auto=format&fit=crop'
  movieForm.synopsis = 'Years after witnessing the death of the revered hero Maximus, Lucius enters the Colosseum after his home is conquered by the tyrannical Emperors.'
  movieForm.is_featured = true
}

async function fetchAdminData() {
  try {
    const [st, mList, tList, sList] = await Promise.all([
      api.getAdminStats(),
      api.getMovies(),
      api.getTheaters(),
      api.getShows()
    ])
    Object.assign(stats, st)
    movies.value = mList
    theaters.value = tList
    scheduledShows.value = sList

    if (tList.length && !screenForm.theater_id) {
      screenForm.theater_id = tList[0].id
    }
    if (mList.length && !showForm.movie_id) {
      showForm.movie_id = mList[0].id
    }
    if (tList.length && tList[0].screens?.length && !showForm.screen_id) {
      showForm.screen_id = tList[0].screens[0].id
    }
  } catch (e) {
    console.error('Failed to load admin stats:', e)
  }
}

async function submitMovie() {
  saving.value = true
  try {
    await api.addMovie(movieForm)
    showAlert(`Successfully added movie "${movieForm.title}" to CinePass!`)
    movieForm.title = ''
    movieForm.poster_url = ''
    movieForm.synopsis = ''
    await fetchAdminData()
    emit('data-updated')
  } catch (e) {
    showAlert(e.message || 'Failed to add movie', 'error')
  } finally {
    saving.value = false
  }
}

async function handleDeleteMovie(id) {
  if (!confirm('Are you sure you want to delete this movie?')) return
  try {
    await api.deleteMovie(id)
    showAlert('Movie deleted successfully.')
    await fetchAdminData()
    emit('data-updated')
  } catch (e) {
    showAlert(e.message || 'Failed to delete movie', 'error')
  }
}

async function submitTheater() {
  saving.value = true
  try {
    const res = await api.addTheater(theaterForm)
    showAlert(`Successfully added theater "${theaterForm.name}"!`)
    theaterForm.name = ''
    theaterForm.address = ''
    await fetchAdminData()
    screenForm.theater_id = res.id
    emit('data-updated')
  } catch (e) {
    showAlert(e.message || 'Failed to add theater', 'error')
  } finally {
    saving.value = false
  }
}

async function handleDeleteTheater(id) {
  if (!confirm('Are you sure you want to delete this theater and its screens?')) return
  try {
    await api.deleteTheater(id)
    showAlert('Theater deleted successfully.')
    await fetchAdminData()
    emit('data-updated')
  } catch (e) {
    showAlert(e.message || 'Failed to delete theater', 'error')
  }
}

async function submitScreen() {
  saving.value = true
  try {
    await api.addScreen(screenForm)
    showAlert(`Screen "${screenForm.name}" created with BookMyShow seat layout!`)
    await fetchAdminData()
    emit('data-updated')
  } catch (e) {
    showAlert(e.message || 'Failed to create screen', 'error')
  } finally {
    saving.value = false
  }
}

async function submitShow() {
  saving.value = true
  try {
    await api.addShow(showForm)
    showAlert('Show successfully scheduled on CinePass!')
    await fetchAdminData()
    emit('data-updated')
  } catch (e) {
    showAlert(e.message || 'Failed to schedule show', 'error')
  } finally {
    saving.value = false
  }
}

async function handleDeleteShow(id) {
  if (!confirm('Are you sure you want to cancel this scheduled show?')) return
  try {
    await api.deleteShow(id)
    showAlert('Show deleted successfully.')
    await fetchAdminData()
    emit('data-updated')
  } catch (e) {
    showAlert(e.message || 'Failed to delete show', 'error')
  }
}

watch(() => props.isOpen, (open) => {
  if (open) fetchAdminData()
})

onMounted(() => {
  if (props.isOpen) fetchAdminData()
})
</script>
