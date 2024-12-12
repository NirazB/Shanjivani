// Optional JavaScript for dashboard interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Example: Add some basic interactivity or data refresh mechanism
    function updateDashboard() {
        // In a real application, this would fetch fresh data from the server
        console.log('Dashboard data refresh triggered');
    }

    // Refresh data every 5 minutes
    setInterval(updateDashboard, 5 * 60 * 1000);

    // Optional hover effects
    const cards = document.querySelectorAll('.resource-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('shadow-lg');
        });
        card.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-lg');
        });
    });
});