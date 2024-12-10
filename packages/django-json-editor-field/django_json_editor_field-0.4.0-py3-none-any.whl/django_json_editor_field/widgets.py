from django.forms.widgets import Textarea


class JSONEditorWidget(Textarea):
    template_name = "widgets/json_editor_widget.html"

    class Media:
        js = [
            "https://cdn.jsdelivr.net/npm/@json-editor/json-editor@latest/dist/jsoneditor.min.js",
            "js/jsonwidget.js",
        ]
        css = {
            "all": ["css/jsonwidget.css"],
        }

    def __init__(self, options={}, *args, **kwargs):
        self.options = options
        super().__init__(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)
        ctx["options"] = self.options
        return ctx
