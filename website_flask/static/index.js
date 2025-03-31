// Timeout the alert messages 
setTimeout(function() {
    var flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        flashMessages.style.display = 'none';
    }
}, 10000); // 10000 ms = 10 seconds