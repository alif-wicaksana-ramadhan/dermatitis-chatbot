// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@nuxt/icon'],
  runtimeConfig:{
    public:{
      backendUrl: "http://152.118.31.20:8081"
    },
    backendUrl: "http://dermatitis_backend:8000"
  }
})