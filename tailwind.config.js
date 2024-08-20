/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html", "./app/static/js/**/*.js"],
  theme: {
    extend: {
      colors: {
        'fastschwarz': '#2C2C2C'
      },
    },
  },
  plugins: [],
}

