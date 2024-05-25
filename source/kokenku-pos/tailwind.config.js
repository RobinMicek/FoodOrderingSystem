/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,svelte}",
  ],

  theme: {
    extend: {
      colors: {
        primary: "#212121",
        secondary: "#008550",
        white: "#FFFFFF"
      },
      
      gridTemplateColumns: {
        '20': 'repeat(20, minmax(0, 1fr))',
      },
      gridColumn: {
        'span-19': 'span 19 / span 19',
      },
    },
  },
  
  plugins: [],
}

