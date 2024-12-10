window.addEventListener('load', () => {
    JSONEditor.defaults.options.theme = "bootstrap4";
    JSONEditor.defaults.options.disable_collapse = true;
    JSONEditor.defaults.options.disable_edit_json = true;
    JSONEditor.defaults.options.disable_properties = true;
    JSONEditor.defaults.options.disable_array_reorder = true;
    JSONEditor.defaults.options.disable_array_delete_last_row = true;
    JSONEditor.defaults.options.disable_array_delete_all_rows = true;
    JSONEditor.defaults.options.prompt_before_delete = false;
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
