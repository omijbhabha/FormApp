let fieldCounter = 1;

function addField() {
    const newField = document.createElement('div');
    newField.classList.add('field');
    newField.id = `field_${fieldCounter}`;
    newField.innerHTML = `
        <label for="field_name_${fieldCounter}">Field Name:</label>
        <input type="text" id="field_name_${fieldCounter}" name="field_name_${fieldCounter}" required>
        <label for="field_type_${fieldCounter}">Field Type:</label>
        <select id="field_type_${fieldCounter}" name="field_type_${fieldCounter}" required onchange="configureFieldOptions(${fieldCounter})">
            <option value="text">Text</option>
            <option value="integer">Integer</option>
            <option value="date">Date</option>
            <option value="checkbox">Multiple Choice (Checkbox)</option>
            <option value="dropdown">Dropdown</option>   
        </select>
        <div id="options_${fieldCounter}" class="options-container" style="display:none;">
            <button type="button" class="add-option-btn" onclick="addOption(${fieldCounter})">Add Option</button>
        </div>
        <button type="button" onclick="removeField(${fieldCounter})">Remove Field</button>
    `;
    document.getElementById('fields').appendChild(newField);
    fieldCounter++;
}

function removeField(id) {
    const field = document.getElementById(`field_${id}`);
    field.remove();
}

function configureFieldOptions(id) {
    const fieldType = document.getElementById(`field_type_${id}`).value;
    const optionsDiv = document.getElementById(`options_${id}`);
    if (fieldType === 'checkbox' || fieldType === 'dropdown') {
        optionsDiv.style.display = 'block';
    } else {
        optionsDiv.style.display = 'none';
    }
}

function addOption(fieldId) {
    const optionsContainer = document.getElementById(`options_${fieldId}`);
    const optionId = optionsContainer.children.length;
    const optionItem = document.createElement('div');
    optionItem.classList.add('option-item');
    optionItem.innerHTML = `
        <input type="text" name="field_${fieldId}_option_${optionId}" required>
        <button type="button" class="remove-option-btn" onclick="removeOption(this)">X</button>
    `;
    optionsContainer.insertBefore(optionItem, optionsContainer.lastElementChild);
}

function removeOption(button) {
    button.parentElement.remove();
}

// General initialization function
function initializePage() {
    const createFormForm = document.getElementById('createFormForm');
    if (createFormForm) {
        createFormForm.onsubmit = function() {
            const fields = document.querySelectorAll('.field');
            fields.forEach((field, index) => {
                const fieldType = document.getElementById(`field_type_${index}`).value;
                if (fieldType === 'checkbox' || fieldType === 'dropdown') {
                    const options = [];
                    const optionInputs = field.querySelectorAll('.option-item input');
                    optionInputs.forEach(input => {
                        options.push(input.value);
                    });
                    const hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = `options_${index}`;
                    hiddenInput.value = options.join(',');
                    field.appendChild(hiddenInput);
                }
            });
            return true;
        };
    }

    // Add more page-specific initializations here as needed
}

// Run initialization when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initializePage);