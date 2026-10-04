<template>
  <div
    v-if="authStore.isAuthModalOpen"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm transition-all"
    @click.self="authStore.closeAuthModal()"
  >
    <div class="w-full max-w-md bg-[#181A24] border border-white/10 rounded-2xl p-6 sm:p-8 shadow-2xl animate-in fade-in zoom-in duration-200">
      <div class="flex items-center justify-between pb-4 border-b border-white/10 mb-6">
        <div>
          <h3 class="text-xl font-bold text-white">
            {{ authStore.authModalMode === 'login' ? 'Welcome Back' : 'Create an Account' }}
          </h3>
          <p class="text-xs text-slate-400 mt-1">
            {{ authStore.authModalMode === 'login' ? 'Sign in to reserve your tickets' : 'Join TicketLocal for instant seat holds' }}
          </p>
        </div>
        <button
          @click="authStore.closeAuthModal()"
          class="text-slate-400 hover:text-white text-lg transition-colors"
        >
          ✕
        </button>
      </div>

      <!-- Quick Demo Login Banner -->
      <div
        v-if="authStore.authModalMode === 'login'"
        class="mb-5 p-3 rounded-xl bg-[#F84464]/10 border border-[#F84464]/30 flex items-center justify-between gap-2"
      >
        <div class="text-xs">
          <div class="font-bold text-white">Quick Demo Account</div>
          <div class="text-[11px] text-slate-300 font-mono">demo@ticketlocal.com</div>
        </div>
        <button
          @click="fillDemoAccount"
          class="px-3 py-1 rounded-lg bg-[#F84464] hover:bg-[#e03353] text-white text-xs font-bold transition-all shadow shadow-[#F84464]/30 shrink-0"
        >
          Fill Demo
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div v-if="authStore.authModalMode === 'register'">
          <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Full Name
          </label>
          <input
            v-model="name"
            type="text"
            required
            placeholder="John Citizen"
            class="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464] transition-colors text-sm"
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Email Address
          </label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="you@example.com"
            class="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464] transition-colors text-sm"
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Password
          </label>
          <input
            v-model="password"
            type="password"
            required
            minlength="6"
            placeholder="••••••••"
            class="w-full px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-[#F84464] transition-colors text-sm"
          />
        </div>

        <div v-if="errorMessage" class="text-xs text-rose-400 font-medium">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3 rounded-xl bg-[#F84464] hover:bg-[#e03353] text-white text-sm font-bold transition-all shadow-lg shadow-[#F84464]/30 hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50 disabled:pointer-events-none mt-2"
        >
          <span v-if="loading">Processing...</span>
          <span v-else>
            {{ authStore.authModalMode === 'login' ? 'Sign In to Continue' : 'Create Account' }}
          </span>
        </button>
      </form>

      <div class="mt-6 text-center text-xs text-slate-400">
        <template v-if="authStore.authModalMode === 'login'">
          Don't have an account?
          <button
            @click="authStore.openRegister()"
            class="text-[#F84464] font-bold hover:underline ml-1"
          >
            Sign Up
          </button>
        </template>
        <template v-else>
          Already have an account?
          <button
            @click="authStore.openLogin()"
            class="text-[#F84464] font-bold hover:underline ml-1"
          >
            Sign In
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useToastStore } from '../stores/toast'

const authStore = useAuthStore()
const toastStore = useToastStore()

const name = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

function fillDemoAccount() {
  email.value = 'demo@ticketlocal.com'
  password.value = 'Demo@1234'
}

async function handleSubmit() {
  loading.value = true
  errorMessage.value = ''
  try {
    let res
    if (authStore.authModalMode === 'login') {
      res = await authStore.login(email.value, password.value)
    } else {
      res = await authStore.register(name.value, email.value, password.value)
    }

    if (res.success) {
      toastStore.success(authStore.authModalMode === 'login' ? 'Logged in successfully!' : 'Account registered!')
      name.value = ''
      email.value = ''
      password.value = ''
    } else {
      errorMessage.value = res.error
    }
  } finally {
    loading.value = false
  }
}
</script>
