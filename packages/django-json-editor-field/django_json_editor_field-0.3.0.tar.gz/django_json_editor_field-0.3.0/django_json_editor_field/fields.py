from django.db import models
from django.core import checks

from django_json_editor_field.widgets import JSONEditorWidget


class JSONEditorField(models.JSONField):
    def __init__(self, blank=True, *args, **kwargs):
        self.options = kwargs.pop("options", {})
        if "schema" not in self.options.keys():
            self.options["schema"] = kwargs.pop("schema", {})
        super().__init__(blank=blank, *args, **kwargs)

    def check(self, **kwargs):
        return [*super().check(**kwargs), *self._check_options()]

    def _check_options(self):
        if not self.options.get("schema"):
            return [checks.Error("JSONEditorFields must define a 'schema' attribute or an 'options' attribute with a 'schema' key", obj=self)]
        return []

    def formfield(self, *args, **kwargs):
        kwargs["widget"] = JSONEditorWidget(options=self.options)
        return super().formfield(*args, **kwargs)
