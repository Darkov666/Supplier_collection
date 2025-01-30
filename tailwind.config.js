/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './collection_app/templates/**/*.html',
    './static/js/**/*.js',
    './collection_app/**/*.py',
    './node_modules/flowbite/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        poppins: ["Poppins", "sans-serif"],
        montserrat: ["Montserrat", "sans-serif"],
        playfair: ["Playfair Display", "serif"],
        inter: ["Inter", "sans-serif"],
        nunito: ["Nunito", "sans-serif"],
        roboto: ["Roboto", "sans-serif"],
        caveat: ["Caveat", "cursive"],
      },
      colors: {
        newlime: "#dee720",
        newlimel: "#f8ffdf",
        newlimes: "#f7febe",
        azulsunny: "#0e7490d9",
      },
    },
  },
  plugins: [
    require('daisyui'),
    require('flowbite/plugin'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
  daisyui: {
    themes: [
      {
        mytheme: {
          "primary": "#FEC007",
          "secondary": "#047857",
          "accent": "#38BDF8",
          "neutral": "#111827",
          "base-100": "#ffffff",
          "info": "#3ABFF8",
          "success": "#36D399",
          "warning": "#FBBD23",
          "error": "#F87272",
          "font": "caveat",
        },
      },
      "light",
      "dark"
    ],
    styled: true,
    base: true,
    utils: true,
    logs: true,
    rtl: false,
    prefix: "",
  },
};
