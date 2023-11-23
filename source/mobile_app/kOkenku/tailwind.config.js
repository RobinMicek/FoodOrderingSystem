/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue}"
  ],

  theme: {
    extend: {
      
      colors: {
        primary: "#212121",
        secondary: "#008550",
        white: "#FFFFFF"
      },

      spacing: {
        '1vh': '1vh',
        '2vh': '2vh',
        '3vh': '3vh',
        '4vh': '4vh',
        '5vh': '5vh',
        '7vh': '7vh',
        '10vh': '10vh',
        '20vh': '20vh',
        '25vh': '25vh',
        '30vh': '30vh',

  
        '2vw': '2vw',
        '5vw': '5vw',
      },

      fontSize: {
        'xs': '0.75rem'
      },
    },
  },

  plugins: [],
}