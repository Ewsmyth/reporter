// Get modal and button elements
const modal = document.getElementById("inputModal");
const addInputBtn = document.getElementById("addInputBtn");
const closeModal = document.getElementById("closeModal");

// Show modal when button is clicked
addInputBtn.onclick = function() {
    modal.style.display = "block";
};

// Close the modal when the close span is clicked
closeModal.onclick = function() {
    modal.style.display = "none";
};

// Close modal if user clicks outside the modal content
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

// Function to add an input to the form with a structured layout
function addInput(type, labelText) {
    const form = document.querySelector("form");

    // Retrieve the remove icon path from data attribute
    const removeIconPath = form.getAttribute("data-remove-icon");

    // Create the full-input container
    const fullInputDiv = document.createElement("div");
    fullInputDiv.className = "full-input";

    // Create the input-div for label and input
    const inputDiv = document.createElement("div");
    inputDiv.className = "input-div";

    // Create label for the input
    const label = document.createElement("label");
    label.textContent = labelText;
    label.setAttribute("for", `additional-${labelText.toLowerCase().replace(/ /g, '-')}`);

    // Create and configure new input based on type
    let newInput;
    if (type === "textarea") {
        newInput = document.createElement("textarea");
        newInput.name = `additional-${labelText.toLowerCase().replace(/ /g, '-')}`;
        newInput.placeholder = `Enter ${labelText}...`;
    } else {
        newInput = document.createElement("input");
        newInput.type = type;
        newInput.name = `additional-${labelText.toLowerCase().replace(/ /g, '-')}`;
        newInput.placeholder = `Enter ${labelText}...`;
    }

    // Append label and input to input-div
    inputDiv.appendChild(label);
    inputDiv.appendChild(newInput);

    // Create the remove-div to hold the remove button
    const removeDiv = document.createElement("div");
    removeDiv.className = "remove-div";

    // Create the remove button and add it to the remove-div
    const removeBtn = document.createElement("button");
    removeBtn.type = "button"; // Prevent form submission
    removeBtn.className = "remove-btn";
    removeBtn.onclick = function() {
        fullInputDiv.remove(); // Remove the full input structure from the form
    };

    // Add an image inside the remove button
    const removeImg = document.createElement("img");
    removeImg.src = removeIconPath; // Update with actual image path
    removeImg.alt = "Remove";
    removeImg.className = "remove-icon"; // Optional for styling

    // Append the image to the remove button
    removeBtn.appendChild(removeImg);
    removeDiv.appendChild(removeBtn);

    // Append input-div and remove-div to the full-input container
    fullInputDiv.appendChild(inputDiv);
    fullInputDiv.appendChild(removeDiv);

    // Append the full-input container to the form
    form.insertBefore(fullInputDiv, form.querySelector('input[type="submit"]'));

    // Close the modal
    modal.style.display = "none";
}
