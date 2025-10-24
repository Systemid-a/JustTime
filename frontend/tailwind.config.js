
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class', // 👈 CRÍTICO - Esta línea faltaba
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}