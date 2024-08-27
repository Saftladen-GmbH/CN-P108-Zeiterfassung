/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html", "./app/static/js/**/*.js"],
  theme: {
    extend: {
      colors: {
        'fastschwarz': '#2C2C2C',
        'grau-dunkel': '#949494',
        'grau': '#D9D9D9',
        'grau-hell': '#F5F5F5',
        'gelb': '#FCD147',
        'orange': '#FE833F',
        'rot': '#FF615D',
        'dunkelblau': '#035388',
        'blau': '#0286CA',
        'türkis': '#30E7f4'
      },
    },
  },
  plugins: [],
}

