<template>
  <div v-if="category" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto bg-black/90 backdrop-blur-md animate-in fade-in duration-200">
    <div class="bg-[#1a1c26] w-full max-w-4xl rounded-3xl border border-slate-700 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200 my-auto select-none flex flex-col max-h-[88vh]">
      
      <!-- Modal Header -->
      <div class="p-5 border-b border-slate-800 bg-[#222434] flex items-center justify-between shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-[#F84464]/20 border border-[#F84464]/40 flex items-center justify-center text-xl">
            {{ getCategoryIcon(category) }}
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h2 class="text-lg font-black text-white">{{ getCategoryTitle(category) }}</h2>
              <span class="px-2 py-0.5 rounded bg-[#F84464] text-white text-[10px] font-bold">
                {{ category.toUpperCase() }}
              </span>
            </div>
            <p class="text-xs text-slate-400">{{ getCategorySubtitle(category) }}</p>
          </div>
        </div>
        <button 
          @click="$emit('close')"
          class="p-2 rounded-full bg-slate-800 hover:bg-[#F84464] text-slate-300 hover:text-white transition-colors cursor-pointer"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Modal Body (Scrollable) -->
      <div class="p-6 overflow-y-auto space-y-6 flex-1">

        <!-- 1. STREAM (BookMyShow Stream Premieres) -->
        <div v-if="category === 'Stream'" class="space-y-6">
          <div class="relative rounded-2xl overflow-hidden bg-gradient-to-r from-rose-950 via-slate-900 to-indigo-950 border border-slate-700 p-6 flex flex-col md:flex-row items-center gap-6">
            <img 
              src="https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=400&auto=format&fit=crop&q=80" 
              alt="Stream Premiere"
              class="w-36 h-52 object-cover rounded-xl shadow-2xl border border-slate-700 shrink-0"
            />
            <div class="space-y-3 flex-1 text-center md:text-left">
              <div class="flex flex-wrap items-center justify-center md:justify-start gap-2">
                <span class="px-2 py-0.5 rounded bg-amber-500/20 border border-amber-500/50 text-amber-400 text-[10px] font-bold">PREMIERE OF THE WEEK</span>
                <span class="text-xs text-slate-400">4K Ultra HD • Dolby Atmos 7.1</span>
              </div>
              <h3 class="text-2xl font-black text-white">Dune: Part Two (Stream Edition)</h3>
              <p class="text-xs text-slate-300 leading-relaxed max-w-xl">
                Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family. Rent or buy directly on BookMyShow Stream.
              </p>
              <div class="flex flex-wrap items-center justify-center md:justify-start gap-3 pt-2">
                <button 
                  @click="notifyAction('Rented Dune: Part Two for ₹149')"
                  class="px-5 py-2.5 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs shadow-lg shadow-[#F84464]/30 cursor-pointer transition-all"
                >
                  Rent for ₹149
                </button>
                <button 
                  @click="notifyAction('Purchased Dune: Part Two for ₹499')"
                  class="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-bold text-xs cursor-pointer transition-all"
                >
                  Buy for ₹499
                </button>
              </div>
            </div>
          </div>

          <div>
            <h4 class="text-sm font-black text-white mb-3">Trending Premieres on BMS Stream</h4>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div 
                v-for="stream in streamMovies" 
                :key="stream.title"
                class="bg-[#222434] rounded-xl overflow-hidden border border-slate-800 group hover:border-slate-600 transition-all flex flex-col"
              >
                <div class="relative h-44 overflow-hidden">
                  <img :src="stream.image" :alt="stream.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                  <span class="absolute bottom-2 left-2 px-1.5 py-0.5 rounded bg-black/80 backdrop-blur-sm text-[10px] font-bold text-amber-400">
                    ★ {{ stream.rating }}
                  </span>
                </div>
                <div class="p-3 flex-1 flex flex-col justify-between space-y-2">
                  <div>
                    <h5 class="font-bold text-xs text-white line-clamp-1">{{ stream.title }}</h5>
                    <p class="text-[10px] text-slate-400">{{ stream.languages }}</p>
                  </div>
                  <button 
                    @click="notifyAction(`Rented ${stream.title} for ₹${stream.price}`)"
                    class="w-full py-1.5 rounded-lg bg-slate-800 hover:bg-[#F84464] text-white font-bold text-[11px] transition-colors cursor-pointer"
                  >
                    Rent ₹{{ stream.price }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. EVENTS / PLAYS / SPORTS / ACTIVITIES -->
        <div v-else-if="['Events', 'Plays', 'Sports', 'Activities'].includes(category)" class="space-y-6">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-black text-white">Top {{ category }} in {{ currentCity }}</h3>
            <span class="text-xs text-slate-400">{{ getCategoryItems(category).length }} Available</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <div 
              v-for="item in getCategoryItems(category)"
              :key="item.title"
              class="bg-[#222434] rounded-2xl overflow-hidden border border-slate-800 hover:border-slate-700 transition-all flex flex-col group shadow-lg"
            >
              <div class="relative h-44 overflow-hidden">
                <img :src="item.image" :alt="item.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                <span class="absolute top-2.5 left-2.5 px-2 py-0.5 rounded-full bg-black/80 backdrop-blur-sm text-[10px] font-bold text-white border border-slate-700">
                  {{ item.tag }}
                </span>
                <span class="absolute bottom-2.5 right-2.5 px-2 py-0.5 rounded bg-emerald-950/90 border border-emerald-800 text-[10px] font-bold text-emerald-400">
                  {{ item.price }}
                </span>
              </div>
              <div class="p-4 flex-1 flex flex-col justify-between space-y-3">
                <div class="space-y-1">
                  <h4 class="font-bold text-sm text-white group-hover:text-[#F84464] transition-colors line-clamp-1">{{ item.title }}</h4>
                  <p class="text-xs text-slate-400 flex items-center gap-1">
                    <MapPin class="w-3 h-3 text-[#F84464] shrink-0" />
                    <span class="truncate">{{ item.venue }}</span>
                  </p>
                  <p class="text-[11px] text-slate-500">{{ item.date }}</p>
                </div>
                <button 
                  @click="notifyAction(`Selected tickets for ${item.title}`)"
                  class="w-full py-2.5 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs shadow-md shadow-[#F84464]/20 transition-all cursor-pointer"
                >
                  Book Now
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. BUZZ (Trailers & Entertainment News) -->
        <div v-else-if="category === 'Buzz'" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div 
              v-for="news in buzzArticles"
              :key="news.title"
              class="bg-[#222434] p-4 rounded-2xl border border-slate-800 hover:border-slate-700 transition-all space-y-3"
            >
              <div class="relative h-44 rounded-xl overflow-hidden">
                <img :src="news.image" :alt="news.title" class="w-full h-full object-cover" />
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end p-3">
                  <span class="px-2 py-0.5 rounded bg-[#F84464] text-white text-[10px] font-bold">
                    {{ news.category }}
                  </span>
                </div>
              </div>
              <h4 class="font-bold text-sm text-white hover:text-[#F84464] cursor-pointer">{{ news.title }}</h4>
              <p class="text-xs text-slate-400 line-clamp-2 leading-relaxed">{{ news.desc }}</p>
              <div class="flex items-center justify-between text-[11px] text-slate-500 pt-1 border-t border-slate-800">
                <span>{{ news.readTime }} • {{ news.date }}</span>
                <button 
                  @click="notifyAction(`Opened article: ${news.title}`)"
                  class="text-[#F84464] font-bold hover:underline cursor-pointer"
                >
                  Read Article →
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 4. OFFERS & PROMO CODES -->
        <div v-else-if="category === 'Offers'" class="space-y-5">
          <p class="text-xs text-slate-400">
            Enjoy exclusive credit card discounts, 1+1 movie deals, and cashback rewards on BookMyShow.
          </p>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div 
              v-for="offer in offerList"
              :key="offer.code"
              class="bg-[#222434] p-4 rounded-2xl border border-slate-800 space-y-3 relative overflow-hidden"
            >
              <div class="flex items-start justify-between">
                <div class="space-y-1">
                  <span class="px-2 py-0.5 rounded bg-emerald-950/80 border border-emerald-800 text-emerald-400 text-[10px] font-bold uppercase">
                    {{ offer.bank }}
                  </span>
                  <h4 class="font-black text-sm text-white mt-1">{{ offer.title }}</h4>
                </div>
                <span class="text-2xl">{{ offer.icon }}</span>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed">{{ offer.desc }}</p>
              <div class="flex items-center justify-between pt-2 border-t border-slate-800">
                <div class="font-mono text-xs font-bold text-white bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-700 tracking-wider">
                  {{ offer.code }}
                </div>
                <button 
                  @click="copyCode(offer.code)"
                  class="px-3.5 py-1.5 rounded-lg bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs cursor-pointer transition-colors shadow-md"
                >
                  {{ copiedCode === offer.code ? '✓ Copied!' : 'Copy Code' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 5. GIFT CARDS -->
        <div v-else-if="category === 'Gift Cards'" class="space-y-6">
          <div class="bg-gradient-to-r from-rose-900 to-slate-900 p-6 rounded-2xl border border-slate-700 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 text-center md:text-left">
              <span class="px-2.5 py-0.5 rounded bg-[#F84464] text-white text-[10px] font-bold uppercase">INSTANT DELIVERY</span>
              <h3 class="text-2xl font-black text-white">Gift the Magic of Cinema</h3>
              <p class="text-xs text-slate-300 max-w-md leading-relaxed">
                Send a personalized BookMyShow Gift Card for movies, live concerts, stand-up comedy, and dining.
              </p>
            </div>
            <div class="w-64 h-36 rounded-2xl bg-gradient-to-tr from-[#F84464] via-rose-600 to-amber-500 p-4 text-white shadow-2xl flex flex-col justify-between shrink-0 border border-white/20">
              <div class="flex justify-between items-center">
                <span class="font-black text-sm tracking-tight">bookmyshow</span>
                <span class="text-xs font-mono font-bold">GIFT CARD</span>
              </div>
              <div class="space-y-1">
                <div class="text-xl font-black">₹{{ selectedGiftAmount }}</div>
                <div class="text-[9px] text-white/80 uppercase tracking-widest">Valid for 1 Year across India</div>
              </div>
            </div>
          </div>

          <div class="space-y-3">
            <label class="text-xs font-bold text-slate-300 block">Select Gift Amount</label>
            <div class="grid grid-cols-4 gap-3">
              <button 
                v-for="amt in [250, 500, 1000, 2000]"
                :key="amt"
                @click="selectedGiftAmount = amt"
                class="py-3 rounded-xl border text-sm font-bold transition-all cursor-pointer text-center"
                :class="selectedGiftAmount === amt ? 'bg-[#F84464] border-[#F84464] text-white shadow-lg shadow-[#F84464]/30' : 'bg-slate-900 border-slate-800 text-slate-300 hover:border-slate-600'"
              >
                ₹{{ amt }}
              </button>
            </div>
          </div>

          <button 
            @click="notifyAction(`Gift Card voucher of ₹${selectedGiftAmount} sent to your account!`)"
            class="w-full py-3.5 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs shadow-xl shadow-[#F84464]/30 cursor-pointer transition-all"
          >
            Buy Gift Card for ₹{{ selectedGiftAmount }}
          </button>
        </div>

        <!-- 6. LIST YOUR SHOW (Partner Form) -->
        <div v-else-if="category === 'ListYourShow'" class="space-y-5">
          <div class="text-center max-w-lg mx-auto space-y-2">
            <h3 class="text-xl font-black text-white">Partner with India's Largest Entertainment Hub</h3>
            <p class="text-xs text-slate-400 leading-relaxed">
              Reach over 30 Million active ticket buyers. Host live shows, movies, sports tournaments, and workshops seamlessly.
            </p>
          </div>

          <form @submit.prevent="submitPartnerForm" class="bg-[#222434] p-6 rounded-2xl border border-slate-800 space-y-4 max-w-xl mx-auto">
            <div class="space-y-3">
              <div>
                <label class="text-xs font-bold text-slate-300 block mb-1">Event / Show Title</label>
                <input 
                  v-model="partnerForm.eventName"
                  type="text" 
                  required
                  placeholder="e.g. Hyderabad Standup Festival"
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                />
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="text-xs font-bold text-slate-300 block mb-1">Category</label>
                  <select 
                    v-model="partnerForm.category"
                    class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-[#F84464]"
                  >
                    <option>Live Comedy</option>
                    <option>Music Concert</option>
                    <option>Theatre & Plays</option>
                    <option>Sports Tournament</option>
                    <option>Workshops & Activities</option>
                  </select>
                </div>
                <div>
                  <label class="text-xs font-bold text-slate-300 block mb-1">Target City</label>
                  <input 
                    v-model="partnerForm.city"
                    type="text" 
                    required
                    placeholder="e.g. Hyderabad"
                    class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                  />
                </div>
              </div>

              <div>
                <label class="text-xs font-bold text-slate-300 block mb-1">Organizer Contact Email / Phone</label>
                <input 
                  v-model="partnerForm.contact"
                  type="text" 
                  required
                  placeholder="organizer@events.com or +91 9876543210"
                  class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
                />
              </div>
            </div>

            <button 
              type="submit"
              class="w-full py-3.5 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs shadow-lg shadow-[#F84464]/30 cursor-pointer transition-all"
            >
              Submit Listing Request
            </button>
          </form>
        </div>

        <!-- 7. CORPORATES (Corporate Booking & Vouchers) -->
        <div v-else-if="category === 'Corporates'" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-[#222434] p-5 rounded-2xl border border-slate-800 space-y-2 text-center">
              <span class="text-3xl">🏢</span>
              <h4 class="font-bold text-sm text-white">Bulk Cinema Bookings</h4>
              <p class="text-xs text-slate-400">Exclusive private auditoriums & screen bookings for company outings and product launches.</p>
            </div>
            <div class="bg-[#222434] p-5 rounded-2xl border border-slate-800 space-y-2 text-center">
              <span class="text-3xl">🎁</span>
              <h4 class="font-bold text-sm text-white">Employee Rewards</h4>
              <p class="text-xs text-slate-400">Customized BookMyShow digital movie vouchers for team incentives and festival bonuses.</p>
            </div>
            <div class="bg-[#222434] p-5 rounded-2xl border border-slate-800 space-y-2 text-center">
              <span class="text-3xl">🤝</span>
              <h4 class="font-bold text-sm text-white">Brand Alliances</h4>
              <p class="text-xs text-slate-400">Co-branded promotional campaigns reaching over 30 million entertainment consumers.</p>
            </div>
          </div>

          <div class="bg-slate-900/90 p-5 rounded-2xl border border-slate-800 flex items-center justify-between">
            <div>
              <h4 class="font-bold text-sm text-white">Ready to elevate your corporate events?</h4>
              <p class="text-xs text-slate-400">Our dedicated Enterprise Solutions team will get in touch within 2 hours.</p>
            </div>
            <button 
              @click="notifyAction('Corporate enquiry submitted! Our team will contact you shortly.')"
              class="px-5 py-2.5 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs shadow-md cursor-pointer shrink-0 transition-colors"
            >
              Connect with Enterprise
            </button>
          </div>
        </div>

      </div>

      <!-- Toast Alert Notification -->
      <div 
        v-if="toastMessage"
        class="absolute bottom-6 left-1/2 -translate-x-1/2 px-4 py-2.5 rounded-xl bg-emerald-600 text-white font-bold text-xs shadow-2xl flex items-center gap-2 animate-in slide-in-from-bottom-3 duration-200 z-50"
      >
        <CheckCircle2 class="w-4 h-4" />
        <span>{{ toastMessage }}</span>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { X, MapPin, CheckCircle2 } from 'lucide-vue-next'

const props = defineProps({
  category: { type: String, default: null },
  currentCity: { type: String, default: 'Hyderabad' }
})

const emit = defineEmits(['close'])

const copiedCode = ref(null)
const toastMessage = ref('')
const selectedGiftAmount = ref(500)

const partnerForm = ref({
  eventName: '',
  category: 'Live Comedy',
  city: props.currentCity || 'Hyderabad',
  contact: ''
})

const notifyAction = (msg) => {
  toastMessage.value = msg
  setTimeout(() => {
    toastMessage.value = ''
  }, 3000)
}

const copyCode = (code) => {
  navigator.clipboard?.writeText(code)
  copiedCode.value = code
  notifyAction(`Coupon code ${code} copied to clipboard!`)
  setTimeout(() => {
    copiedCode.value = null
  }, 3000)
}

const submitPartnerForm = () => {
  notifyAction(`Show listing enquiry for "${partnerForm.value.eventName}" received!`)
  partnerForm.value.eventName = ''
  partnerForm.value.contact = ''
}

const getCategoryIcon = (cat) => {
  const icons = {
    Stream: '📺',
    Events: '🎤',
    Plays: '🎭',
    Sports: '⚽',
    Activities: '🎪',
    Buzz: '📰',
    Offers: '🏷️',
    'Gift Cards': '🎁',
    ListYourShow: '🎬',
    Corporates: '🏢'
  }
  return icons[cat] || '🎟️'
}

const getCategoryTitle = (cat) => {
  const titles = {
    Stream: 'BookMyShow Stream',
    Events: 'Live Events & Concerts',
    Plays: 'Theatre & Plays',
    Sports: 'Sports & Matches',
    Activities: 'Amusement Parks & Activities',
    Buzz: 'Entertainment Buzz & Trailers',
    Offers: 'Exclusive Offers & Promo Deals',
    'Gift Cards': 'BookMyShow Gift Cards',
    ListYourShow: 'List Your Show on BookMyShow',
    Corporates: 'Corporate Solutions & Bulk Bookings'
  }
  return titles[cat] || cat
}

const getCategorySubtitle = (cat) => {
  const subs = {
    Stream: 'Rent & buy the biggest Hollywood & World Cinema premieres',
    Events: 'Stand-up comedy specials, music festivals & nightlife',
    Plays: 'Renowned classic and modern theatre plays near you',
    Sports: 'Live cricket, football, marathons and stadium matches',
    Activities: 'Exciting outdoor adventures, VR experiences & theme parks',
    Buzz: 'The hottest updates, trailers and reviews in cinema',
    Offers: 'Save big with partner bank cards and digital wallet discounts',
    'Gift Cards': 'Instant digital vouchers for all movies and live events',
    ListYourShow: 'Get your performance or festival listed across India',
    Corporates: 'Bulk screening packages and corporate gifting vouchers'
  }
  return subs[cat] || 'Explore the best of entertainment'
}

const streamMovies = [
  {
    title: 'Furiosa: A Mad Max Saga',
    languages: 'English, Hindi, Telugu',
    rating: '8.8/10',
    price: 199,
    image: 'https://images.unsplash.com/photo-1574267432553-4b4628081c31?w=400&auto=format&fit=crop&q=80'
  },
  {
    title: 'Oppenheimer (Collector Edition)',
    languages: 'English, Hindi',
    rating: '9.2/10',
    price: 149,
    image: 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400&auto=format&fit=crop&q=80'
  },
  {
    title: 'Kingdom of the Planet of the Apes',
    languages: 'English, Hindi, Tamil',
    rating: '8.4/10',
    price: 129,
    image: 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400&auto=format&fit=crop&q=80'
  },
  {
    title: 'Spider-Man: Across the Spider-Verse',
    languages: 'English, Hindi, Telugu, Tamil',
    rating: '9.1/10',
    price: 149,
    image: 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=400&auto=format&fit=crop&q=80'
  }
]

const getCategoryItems = (cat) => {
  if (cat === 'Events') {
    return [
      {
        title: 'Zakir Khan Live - Tathastu Tour',
        venue: 'Shilpakala Vedika, Hitech City',
        date: 'Sat, 18 Oct • 7:00 PM',
        tag: 'Stand-up Comedy',
        price: '₹799 onwards',
        image: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400&auto=format&fit=crop&q=80'
      },
      {
        title: 'Sunburn Arena ft. Alan Walker Live',
        venue: 'GMR Arena, Shamshabad',
        date: 'Sun, 26 Oct • 4:00 PM',
        tag: 'EDM Music Fest',
        price: '₹1,499 onwards',
        image: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=400&auto=format&fit=crop&q=80'
      },
      {
        title: 'Arijit Singh Symphony Concert 2026',
        venue: 'Gachibowli Stadium',
        date: 'Sat, 15 Nov • 6:30 PM',
        tag: 'Live Concert',
        price: '₹2,499 onwards',
        image: 'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=400&auto=format&fit=crop&q=80'
      }
    ]
  }
  if (cat === 'Plays') {
    return [
      {
        title: 'Mughal-E-Azam: The Grand Broadway Musical',
        venue: 'Ravindra Bharathi Auditorium',
        date: 'Fri-Sun, 24-26 Oct',
        tag: 'Classic Drama',
        price: '₹500 onwards',
        image: 'https://images.unsplash.com/photo-1469488865564-c2de10f69f96?w=400&auto=format&fit=crop&q=80'
      },
      {
        title: 'The Blue Mug ft. Ranvir Shorey',
        venue: 'NIFT Amphitheatre, Madhapur',
        date: 'Sat, 01 Nov • 6:00 PM',
        tag: 'Contemporary Theatre',
        price: '₹400 onwards',
        image: 'https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?w=400&auto=format&fit=crop&q=80'
      }
    ]
  }
  if (cat === 'Sports') {
    return [
      {
        title: 'IPL 2026: SRH vs CSK Live Clash',
        venue: 'Rajiv Gandhi International Cricket Stadium',
        date: 'Fri, 10 Apr • 7:30 PM',
        tag: 'Cricket T20',
        price: '₹1,200 onwards',
        image: 'https://images.unsplash.com/photo-1531415074868-036b1c5d53ec?w=400&auto=format&fit=crop&q=80'
      },
      {
        title: 'Hyderabad Night Marathon 2026',
        venue: 'Hitex Exhibition Centre',
        date: 'Sat, 22 Nov • 9:00 PM',
        tag: 'Marathon & Run',
        price: '₹650 onwards',
        image: 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=400&auto=format&fit=crop&q=80'
      }
    ]
  }
  // Activities
  return [
    {
      title: 'Wonderla Amusement Park Day Pass',
      venue: 'Wonderla Park, Outer Ring Road',
      date: 'Open Daily • 10:30 AM - 6:00 PM',
      tag: 'Theme Park & Water Rides',
      price: '₹1,099 onwards',
      image: 'https://images.unsplash.com/photo-1513889961551-628c1e5e2ee9?w=400&auto=format&fit=crop&q=80'
    },
    {
      title: 'Pitstop Go-Karting & VR Escape Room',
      venue: 'Inorbit Mall, Hitech City',
      date: 'Open 11:00 AM - 11:00 PM',
      tag: 'Adventure & Racing',
      price: '₹450 onwards',
      image: 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400&auto=format&fit=crop&q=80'
    }
  ]
}

const buzzArticles = [
  {
    title: 'Pushpa 2: The Rule trailer breaks all-time Indian YouTube records with 100M views',
    desc: 'Allu Arjun and Sukumar return with higher stakes and unprecedented global hype. Pre-bookings open shortly.',
    category: 'Box Office Buzz',
    readTime: '3 min read',
    date: '2 hrs ago',
    image: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=400&auto=format&fit=crop&q=80'
  },
  {
    title: 'Deadpool & Wolverine achieves ₹150 Crore milestone across Indian IMAX screens',
    desc: 'Marvel Studios secures its biggest post-pandemic opening in India driven by high-tier 3D formats.',
    category: 'Hollywood Spotlight',
    readTime: '2 min read',
    date: '5 hrs ago',
    image: 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=400&auto=format&fit=crop&q=80'
  }
]

const offerList = [
  {
    bank: 'ICICI Bank',
    title: 'Buy 1 Get 1 Free Movie Ticket',
    desc: 'Valid on ICICI Bank Coral, Rubyx and Sapphiro Credit Cards. Maximum discount ₹250 per booking.',
    code: 'ICICI250',
    icon: '💳'
  },
  {
    bank: 'HDFC Bank',
    title: 'Flat 20% Instant Discount on Diners Cards',
    desc: 'Get up to ₹200 off on all weekend IMAX and 4DX show bookings on BookMyShow.',
    code: 'HDFCDINERS',
    icon: '💎'
  },
  {
    bank: 'BookMyShow Special',
    title: 'Flat ₹50 Off on First Mobile Booking',
    desc: 'Applicable for all users on first online booking for cinema tickets and snacks combo.',
    code: 'BMS50',
    icon: '🎟️'
  },
  {
    bank: 'Axis Bank',
    title: 'Buy 1 Get 1 on Neo & My Zone Cards',
    desc: 'Valid on 2 tickets per month booked through BookMyShow app or web portal.',
    code: 'AXISBOGO',
    icon: '⚡'
  }
]
</script>
