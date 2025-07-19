// Sidebar toggle logic
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('mainContent');
const toggleBtn = document.getElementById('sidebarToggle');
function setSidebarState(collapsed) {
    if (collapsed) {
        sidebar.classList.add('sidebar-collapsed');
        mainContent.style.marginLeft = '60px';
        localStorage.setItem('sidebar-collapsed', '1');
    } else {
        sidebar.classList.remove('sidebar-collapsed');
        mainContent.style.marginLeft = '220px';
        localStorage.setItem('sidebar-collapsed', '0');
    }
    // Show/hide tooltips for nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        if (collapsed) {
            link.setAttribute('title', link.getAttribute('data-tooltip'));
        } else {
            link.removeAttribute('title');
        }
    });
}
toggleBtn.addEventListener('click', function() {
    setSidebarState(!sidebar.classList.contains('sidebar-collapsed'));
});
// Restore sidebar state
if (localStorage.getItem('sidebar-collapsed') === '1') {
    setSidebarState(true);
} else {
    setSidebarState(false);
}

// Auto-logout after inactivity (client-side fallback)
let sessionTimeout = 15 * 60 * 1000; // 15 minutes
let logoutUrl = "{% url 'logout' %}";
let timeoutHandle;
function resetTimeout() {
    clearTimeout(timeoutHandle);
    timeoutHandle = setTimeout(function() {
        window.location.href = logoutUrl;
    }, sessionTimeout);
}
document.addEventListener('mousemove', resetTimeout);
document.addEventListener('keydown', resetTimeout);
document.addEventListener('click', resetTimeout);
resetTimeout();

// Highlight active sidebar link based on current URL
(function() {
    const path = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link[data-nav-name]');
    navLinks.forEach(link => {
        if (link.href && path === new URL(link.href).pathname) {
            link.classList.add('active');
        }
        // Optionally, handle "Children" subpages:
        if (link.dataset.navName === "children" && (
            path.startsWith("{% url 'children:children' %}".replace(/\/$/, "")) ||
            path.startsWith("{% url 'children:add_child' %}".replace(/\/$/, "")) ||
            path.startsWith("{% url 'children:child_dashboard' hcc_number='dummy' %}".replace('dummy', ''))
        )) {
            link.classList.add('active');
        }
    });
})();