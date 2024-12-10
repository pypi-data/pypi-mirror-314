# Django JSON Editor Field

The Django JSON Editor field enhances [Djangos JSON
Field](https://docs.djangoproject.com/en/stable/ref/models/fields/#django.db.models.JSONField)
add adds a [json-editor](https://github.com/json-editor/json-editor) on top.
You can use a JSON Schema to describe a form for the underlying JSON field. The
input is then stored as JSON.

# Usage

Add `django_json_editor_field` to your [INSTALLED_APPS](https://docs.djangoproject.com/en/stable/ref/settings/#std-setting-INSTALLED_APPS).

Use the field in your model:

```python
from django_json_editor_field.fields import JSONEditorField

schema = {
        "title": "My JSON Array of Objects",
        "type": "array",
        "format": "table",
        "items": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                },
                "start": {
                    "type": "string",
                    "format": "date",
                },
                "end": {
                    "type": "string",
                    "format": "date",
                }
            }
        }
}

data = JSONEditorField(schema=schema)
```


[json-editor](https://github.com/json-editor/json-editor?tab=readme-ov-file#options) has some options. You can set
them using the `options` argument to the JSONEditorField.

```
options = {
    "theme": "bootstrap4",
    "disable_collapse": True,
}
schema = {
    ...
}
data = JSONEditorField(schema=schema, options=options)
```

Internally, the schema gets added to the `schema` attribute of the options and only the `options` object gets passed on
to the json-editor. This means you can also define the `schema` as part of the options directly.
