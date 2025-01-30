$(document).ready(function () {
    // Live Clock Update
    function updateClock() {
        let now = new Date();
        let timeString = now.toLocaleTimeString("fr-FR", { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        $("#clock").text("🕒 " + timeString);
    }
    setInterval(updateClock, 1000);
    updateClock();
});