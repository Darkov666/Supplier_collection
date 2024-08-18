document.addEventListener('DOMContentLoaded', function() {
    const toggleThemeButton = document.getElementById('toggleTheme');

    // Función para cambiar el tema
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    }

    // Aplicar el tema guardado en localStorage al cargar la página
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    } else {
        // Aplicar el tema del sistema nativo si no hay tema guardado
        const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const prefersLightScheme = window.matchMedia('(prefers-color-scheme: light)').matches;
        if (prefersDarkScheme) {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else if (prefersLightScheme) {
            document.documentElement.setAttribute('data-theme', 'light');
        }
    }

    // Añadir el evento de clic al botón
    toggleThemeButton.addEventListener('click', toggleTheme);
});
