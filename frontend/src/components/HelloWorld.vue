<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto bg-black/90 backdrop-blur-md">
    <div class="bg-[#1a1c26] w-full max-w-md rounded-3xl border border-slate-700 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200 my-auto select-none">
      
      <!-- Modal Header -->
      <div class="p-5 border-b border-slate-800 bg-[#222434] flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-xl bg-[#F84464]/20 border border-[#F84464]/40 flex items-center justify-center">
            <User class="w-4 h-4 text-[#F84464]" />
          </div>
          <div>
            <h2 class="text-base font-black text-white">
              {{ isEditingProfile ? 'Edit Profile & Name' : isOtpStep ? 'Verify OTP' : isLoggedIn ? 'My Account' : 'Login / Register' }}
            </h2>
            <p class="text-[10px] text-slate-400">BookMyShow Citizen Experience</p>
          </div>
        </div>
        <button 
          @click="$emit('close')"
          class="p-2 rounded-full bg-slate-800 hover:bg-[#F84464] text-slate-300 hover:text-white transition-colors"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Mode 1: Logged In & View / Edit Name -->
      <div v-if="isLoggedIn && !isEditingProfile" class="p-6 space-y-5">
        <div class="flex items-center gap-4 bg-[#222434] p-4 rounded-2xl border border-slate-800">
          <div class="w-14 h-14 rounded-2xl bg-[#F84464] text-white font-black text-2xl flex items-center justify-center shadow-lg shadow-[#F84464]/30">
            {{ (userName || 'U')[0].toUpperCase() }}
          </div>
          <div class="flex-1">
            <div class="flex items-center gap-2">
              <h3 class="font-black text-lg text-white">{{ userName }}</h3>
              <span class="px-2 py-0.2 rounded bg-emerald-950/60 border border-emerald-800 text-[10px] font-bold text-emerald-400">
                Active
              </span>
            </div>
            <p class="text-xs text-slate-400 mt-0.5">{{ userEmail }}</p>
            <p class="text-[11px] text-slate-500">{{ userPhone }}</p>
          </div>
        </div>

        <div class="space-y-2">
          <button
            @click="isEditingProfile = true"
            class="w-full py-3 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs flex items-center justify-center gap-2 shadow-lg shadow-[#F84464]/20 transition-all"
          >
            <Edit3 class="w-4 h-4" />
            <span>Change Name & Profile Details</span>
          </button>

          <button
            @click="handleLogout"
            class="w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-rose-400 hover:text-rose-300 font-bold text-xs flex items-center justify-center gap-2 border border-slate-700 transition-all"
          >
            <LogOut class="w-4 h-4" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>

      <!-- Mode 2: Edit Profile & Change Name -->
      <div v-else-if="isEditingProfile" class="p-6 space-y-4">
        <div class="space-y-3">
          <div>
            <label class="text-xs font-bold text-slate-300 block mb-1">Your Full Name</label>
            <input 
              v-model="editName"
              type="text" 
              placeholder="e.g. Rahul Sharma"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
            />
          </div>

          <div>
            <label class="text-xs font-bold text-slate-300 block mb-1">Email Address</label>
            <input 
              v-model="editEmail"
              type="email" 
              placeholder="rahul@example.com"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
            />
          </div>

          <div>
            <label class="text-xs font-bold text-slate-300 block mb-1">Phone Number</label>
            <input 
              v-model="editPhone"
              type="tel" 
              placeholder="+91 98765 43210"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
            />
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button
            @click="isEditingProfile = false"
            class="flex-1 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs transition-colors"
          >
            Cancel
          </button>
          <button
            @click="saveProfileChanges"
            class="flex-1 py-3 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs shadow-lg shadow-[#F84464]/30 transition-all flex items-center justify-center gap-1.5"
          >
            <Check class="w-4 h-4" />
            <span>Save Name</span>
          </button>
        </div>
      </div>

      <!-- Mode 3: OTP Verification Step -->
      <div v-else-if="isOtpStep" class="p-6 space-y-4">
        <div class="text-center">
          <p class="text-xs text-slate-400">
            We sent a 4-digit verification code to <strong class="text-white">{{ inputIdentifier }}</strong>
          </p>
          <span class="inline-block px-2.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[11px] font-mono font-bold mt-2">
            Demo OTP: 1234
          </span>
        </div>

        <div>
          <label class="text-xs font-bold text-slate-300 block mb-1">Enter 4-Digit Code</label>
          <input 
            v-model="otpCode"
            maxlength="4"
            type="text" 
            placeholder="1234"
            class="w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-center tracking-[0.5em] text-lg font-mono font-bold text-white placeholder-slate-600 focus:outline-none focus:border-[#F84464]"
          />
        </div>

        <button
          @click="verifyOtp"
          class="w-full py-3.5 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs shadow-lg shadow-[#F84464]/30 transition-all flex items-center justify-center gap-2"
        >
          <CheckCircle2 class="w-4 h-4" />
          <span>Verify & Login</span>
        </button>

        <button
          @click="isOtpStep = false"
          class="w-full text-center text-xs text-slate-400 hover:text-white"
        >
          ← Change mobile number / email
        </button>
      </div>

      <!-- Mode 4: Initial Login / Mobile input -->
      <div v-else class="p-6 space-y-5">
        <div>
          <label class="text-xs font-bold text-slate-300 block mb-1.5">Mobile Number or Email</label>
          <div class="relative">
            <input 
              v-model="inputIdentifier"
              type="text" 
              placeholder="e.g. 9876543210 or yourname@gmail.com"
              class="w-full pl-4 pr-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464]"
            />
          </div>
        </div>

        <button
          :disabled="!inputIdentifier.trim()"
          @click="sendOtp"
          class="w-full py-3.5 rounded-xl bg-[#F84464] hover:bg-[#e23353] text-white font-bold text-xs shadow-lg shadow-[#F84464]/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
        >
          <span>Continue</span>
          <ArrowRight class="w-4 h-4" />
        </button>

        <div class="relative my-4 text-center">
          <div class="absolute inset-0 flex items-center"><div class="w-full border-t border-slate-800"></div></div>
          <span class="relative bg-[#1a1c26] px-3 text-[11px] font-bold text-slate-500 uppercase">OR CONTINUE WITH</span>
        </div>

        <!-- Quick 1-Click Social Sign-In -->
        <div class="grid grid-cols-2 gap-3">
          <button
            @click="quickSocialLogin('Google')"
            class="py-2.5 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-200 flex items-center justify-center gap-2 transition-colors"
          >
            <span>🌐</span>
            <span>Google</span>
          </button>
          <button
            @click="quickSocialLogin('Apple')"
            class="py-2.5 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-200 flex items-center justify-center gap-2 transition-colors"
          >
            <span>🍎</span>
            <span>Apple</span>
          </button>
        </div>

        <p class="text-[10px] text-slate-500 text-center leading-relaxed">
          I agree to the <span class="text-slate-400 hover:underline">Terms & Conditions</span> and <span class="text-slate-400 hover:underline">Privacy Policy</span> of BookMyShow.
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { X, User, Edit3, LogOut, Check, CheckCircle2, ArrowRight } from 'lucide-vue-next'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  currentUser: { type: Object, default: () => ({ guest_name: 'Guest User', guest_email: '', guest_phone: '' }) },
  isLoggedIn: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'update-user', 'login-success', 'logout'])

const isEditingProfile = ref(false)
const isOtpStep = ref(false)
const inputIdentifier = ref('')
const otpCode = ref('1234')

const userName = ref(props.currentUser?.guest_name || 'Guest User')
const userEmail = ref(props.currentUser?.guest_email || 'user@bookmyshow.com')
const userPhone = ref(props.currentUser?.guest_phone || '+91 98765 43210')

const editName = ref(userName.value)
const editEmail = ref(userEmail.value)
const editPhone = ref(userPhone.value)

watch(() => props.currentUser, (newVal) => {
  if (newVal) {
    userName.value = newVal.guest_name || 'Guest User'
    userEmail.value = newVal.guest_email || 'user@bookmyshow.com'
    userPhone.value = newVal.guest_phone || '+91 98765 43210'
    editName.value = userName.value
    editEmail.value = userEmail.value
    editPhone.value = userPhone.value
  }
}, { immediate: true })

const sendOtp = () => {
  if (!inputIdentifier.value.trim()) return
  if (inputIdentifier.value.includes('@')) {
    editEmail.value = inputIdentifier.value
    editName.value = inputIdentifier.value.split('@')[0]
  } else {
    editPhone.value = inputIdentifier.value
    editName.value = 'User ' + inputIdentifier.value.slice(-4)
  }
  isOtpStep.value = true
}

const verifyOtp = () => {
  userName.value = editName.value || 'BookMyShow User'
  userEmail.value = editEmail.value || 'user@bookmyshow.com'
  userPhone.value = editPhone.value || '+91 98765 43210'
  
  emit('login-success', {
    guest_id: `bms_user_${Date.now()}`,
    guest_name: userName.value,
    guest_email: userEmail.value,
    guest_phone: userPhone.value
  })
  
  isOtpStep.value = false
  emit('close')
}

const quickSocialLogin = (provider) => {
  const sampleName = provider === 'Google' ? 'Alex Mercer (Google)' : 'Alex (Apple)'
  userName.value = sampleName
  userEmail.value = `alex.${provider.toLowerCase()}@bookmyshow.com`
  
  emit('login-success', {
    guest_id: `bms_${provider.toLowerCase()}_${Date.now()}`,
    guest_name: userName.value,
    guest_email: userEmail.value,
    guest_phone: '+91 98765 43210'
  })
  
  emit('close')
}

const saveProfileChanges = () => {
  if (!editName.value.trim()) return
  userName.value = editName.value
  userEmail.value = editEmail.value
  userPhone.value = editPhone.value

  emit('update-user', {
    guest_name: userName.value,
    guest_email: userEmail.value,
    guest_phone: userPhone.value
  })

  isEditingProfile.value = false
}

const handleLogout = () => {
  emit('logout')
  isEditingProfile.value = false
  isOtpStep.value = false
  inputIdentifier.value = ''
  emit('close')
}
</script>
