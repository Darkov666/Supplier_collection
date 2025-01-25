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
      colors: {
        newlime: '#dee720',
        newlimel: '#f8ffdf',
        newlimes: '#f7febe',
        azulsunny: '#0e7490d9'
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
    styled: true,
    base: true,
    utils: true,
    logs: true,
    rtl: false,
    prefix: "",
    darkTheme: false,  // Cambiado a booleano
    themes: [
      "light",
      "dark",
    ]
  },
};
