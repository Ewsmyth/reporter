document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.getElementById('flash-messages');

    if (flashMessages) {
        // Add a timeout to hide the flash messages after 5 seconds
        setTimeout(function() {
            flashMessages.style.transition = 'opacity 0.5s ease';
            flashMessages.style.opacity = '0'; // Fade out
            setTimeout(() => flashMessages.style.display = 'none', 500); // Hide after fade-out
        }, 5000); // 5000 milliseconds = 5 seconds

      // Start the progress bar animation
      flashMessages.querySelectorAll('.progress-bar').forEach(bar => {
            bar.style.transition = 'width 5s linear'; // Set transition for smooth progress
            bar.style.width = '100%'; // Animate to full width over 5 seconds
      });

      // Add click event listener for the close buttons
      flashMessages.querySelectorAll('.close-flash').forEach(button => {
            button.addEventListener('click', function() {
                const flashMessage = this.parentElement;
                flashMessage.style.transition = 'opacity 0.5s ease';
                flashMessage.style.opacity = '0';
                setTimeout(() => flashMessage.style.display = 'none', 500);
            });
      });
    }
});
