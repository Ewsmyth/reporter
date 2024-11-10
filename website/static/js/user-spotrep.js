// Store a reference to the currently visible help text
let currentlyVisibleHelpText = null;

// Select all help buttons and add event listeners to each
document.querySelectorAll('a[id^="helpButton"]').forEach(button => {
    button.addEventListener('click', function () {
        // Get the corresponding help text ID by replacing "helpButton" with "helpText"
        const helpTextId = this.id.replace('helpButton', 'helpText');
        const helpText = document.getElementById(helpTextId);

        // If there is currently a visible help text and it's not the one being clicked, hide it
        if (currentlyVisibleHelpText && currentlyVisibleHelpText !== helpText) {
            currentlyVisibleHelpText.classList.add('hidden');
        }

        // Toggle the 'hidden' class of the clicked help text
        helpText.classList.toggle('hidden');

        // If the help text is now visible, update the reference; otherwise, clear it
        if (!helpText.classList.contains('hidden')) {
            currentlyVisibleHelpText = helpText;
            
            // Adjust the position of the help text to appear directly above the button
            helpText.style.position = 'absolute';
            helpText.style.left = `${this.offsetLeft - 55}px`;
            helpText.style.top = `${this.offsetTop - helpText.offsetHeight - 5}px`;
        } else {
            currentlyVisibleHelpText = null;
        }
    });
});
