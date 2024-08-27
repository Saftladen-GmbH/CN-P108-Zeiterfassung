/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html", "./app/static/js/**/*.js"],
  theme: {
    extend: {
      colors: {
        'fastschwarz': '#2C2C2C',
        'hellgrau': '#F5F5F5',
        'grau': '#D9D9D9',
        'dunkelgrau': '#949494',
        'gelb': '#FCD147',
        'orange': '#FE833F',
        'rot': '#FF615D',
        'darkblue': '#035388',
        'blau': '#0286CA',
        'hellblau': '#30E7F4',
      },
    },
  },
  plugins: [],
}

