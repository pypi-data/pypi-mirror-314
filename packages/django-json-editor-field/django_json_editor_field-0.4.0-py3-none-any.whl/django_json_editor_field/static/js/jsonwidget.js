window.addEventListener('load', () => {
    document.querySelectorAll(".jsoneditorwidget").forEach(function(element) {
        optionsContainer = element.nextElementSibling;
        options = JSON.parse(optionsContainer.textContent);
        editor = new JSONEditor(element.parentNode, options);
        editor.on('ready', () => {
            element.style.display = 'none';
            if (JSON.parse(element.value)) {
                editor.setValue(JSON.parse(element.value));
            }
        });
        editor.on('change', () => {
            if (element) {
                element.value = JSON.stringify(editor.getValue());
            }
        });
    });
});
