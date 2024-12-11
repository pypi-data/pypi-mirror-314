from django.db import models

from django.db import models
from chunked_field.fields import ChunkedTextField


class MyModel(models.Model):
    name = models.CharField(max_length=255)
    content = ChunkedTextField(truncate_length=100)  # Adjust truncate_length as needed
    json_data = ChunkedTextField()

    def __str__(self):
        return self.name
