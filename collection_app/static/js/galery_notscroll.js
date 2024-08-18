document.addEventListener('DOMContentLoaded', function () {
  // Define the function at the global level
  window.goToSlide = function (slideNumber) {
      const slideId = `#slide${slideNumber}`;
      const slideElement = document.querySelector(slideId);
      if (slideElement) {
          slideElement.scrollIntoView({ behavior: 'smooth' });
      }
  };

  // Then bind the function to the events
  document.querySelectorAll('.carousel a').forEach(button => {
      button.addEventListener('click', function(event) {
          event.preventDefault(); // Evita el comportamiento por defecto del enlace
          const slideNumber = this.getAttribute('href').replace('#slide', '');
          goToSlide(slideNumber);
      });
  });
});
