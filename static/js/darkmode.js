function toggleDarkMode() {
  const body = document.body;
  const toggleButton = document.getElementById('toggle-dark-mode');

  body.classList.toggle('dark-mode');
  const isDark = body.classList.contains('dark-mode');
  localStorage.setItem('dark-mode', isDark);

  if (toggleButton) {
    toggleButton.textContent = isDark ? 'Modo claro' : 'Modo oscuro';
  }
}

// Ejecutar al cargar para aplicar el modo guardado
document.addEventListener('DOMContentLoaded', function () {
  const body = document.body;
  const toggleButton = document.getElementById('toggle-dark-mode');

  if (localStorage.getItem('dark-mode') === 'true') {
    body.classList.add('dark-mode');
  }

  if (toggleButton) {
    toggleButton.textContent = body.classList.contains('dark-mode') ? 'Modo claro' : 'Modo oscuro';
  }
});
