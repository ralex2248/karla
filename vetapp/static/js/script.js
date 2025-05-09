document.addEventListener("DOMContentLoaded", function() {
    // Botón hamburguesa
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.getElementById('sidebar');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('sidebar-open');  // <--- cambio aquí
        });
    }

    // Botón "Ver Gráficos"
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        if (button.textContent.trim() === "Ver Gráficos") {
            button.addEventListener('click', function() {
                alert("¡Has clickeado el botón Ver Gráficos!");
            });
        }
    });
});
