from django.db import models
from django.core import checks, exceptions

from django_json_editor_field.widgets import JSONEditorWidget

from jsonschema import validate
from jsonschema.exceptions import ValidationError


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

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        try:
            validate(instance=value, schema=self.options["schema"])
        except ValidationError as e:
            raise exceptions.ValidationError(e.message)
