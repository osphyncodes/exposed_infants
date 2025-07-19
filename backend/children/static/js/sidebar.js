// Sidebar toggle removed: sidebar is always fixed and visible.
    // Wait until DOM is ready
        document.addEventListener("DOMContentLoaded", function () {
            // Select all alerts with class 'auto-dismiss'
            const alerts = document.querySelectorAll('.auto-dismiss');

            alert(23)

            alerts.forEach(function (alert) {
            // Hide after 4 seconds (4000ms)
            setTimeout(function () {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                bsAlert.display = 'none'
            }, 4000);
            });
        });