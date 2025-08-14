// scripts.js
document.addEventListener('DOMContentLoaded', () => {
    const themeDark = {{ theme_dark | tojson }};
    if (themeDark) {
        document.body.classList.add('dark-mode');
    }

    // Toggle dark mode (if a button exists, e.g., in settings.html)
    const toggleTheme = document.getElementById('toggleTheme');
    if (toggleTheme) {
        toggleTheme.addEventListener('click', () => {
            const isDark = document.body.classList.toggle('dark-mode');
            fetch('/toggle_theme', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ theme_dark: isDark })
            }).then(() => location.reload());
        });
    }

    // Handle modal
    window.openStripeModal = (loanId, idx) => {
        document.getElementById('stripeLoanId').value = loanId;
        document.getElementById('stripeIdx').value = idx;
        new bootstrap.Modal(document.getElementById('stripeModal')).show();
    };
});