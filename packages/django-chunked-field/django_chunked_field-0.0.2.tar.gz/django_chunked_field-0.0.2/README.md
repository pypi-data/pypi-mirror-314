# Django Chunked Field

This project provides a custom Django field, `ChunkedTextField`, designed to handle large text data by splitting it into
manageable chunks for storage in a separate database table. Unlike traditional text fields, which may face size
limitations in certain database systems, `ChunkedTextField` bypasses these constraints while seamlessly integrating with
Django's ORM. It works transparently with serializers, admin interfaces, and other ORM features, allowing developers to
store and retrieve large text data without changing their application logic. The field is particularly useful in
applications requiring efficient management of text data exceeding database limits, ensuring scalability and ease of
use.

## Features

- Store large text data exceeding database field size limits.
- Seamlessly integrates with Django's admin and ORM.
- Customizable truncation for admin display.

## Installation

1. Install the package using pip:
    ```sh
    pip install django-chunked-field
    ```

2. Add `chunked_field` to your `INSTALLED_APPS` in your Django settings:
    ```python
    INSTALLED_APPS = [
        ...
        'chunked_field',
    ]
    ```

3. Run the migrations to create the necessary database tables:
    ```sh
    python manage.py migrate
    ```

## Usage

### Defining a Model

To use the `ChunkedTextField`, define it in your model as follows:

```python
from django.db import models
from chunked_field.fields import ChunkedTextField


class MyModel(models.Model):
   large_text = ChunkedTextField(truncate_length=100, chunk_size=4000)
```

### Admin Integration

To display the `DataChunk` model in the Django admin, register it in `admin.py`:

```python
from django.contrib import admin
from chunked_field.models import DataChunk


@admin.register(DataChunk)
class DataChunkAdmin(admin.ModelAdmin):
   list_display = ('content_type', 'object_id', 'field_name', 'sequence')
   list_filter = ('content_type', 'field_name')
   search_fields = ('content',)
```

### Signal Handlers

The `ChunkedTextField` automatically handles the chunking and reassembly of data using Django signals. You do not need
to manually manage these operations.

## License

This project is licensed under the MIT License.

```

This update includes installation instructions, usage examples, and admin integration details.