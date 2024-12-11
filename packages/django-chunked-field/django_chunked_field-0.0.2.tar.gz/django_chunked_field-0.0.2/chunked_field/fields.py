"""
This module defines a custom Django model field `ChunkedTextField` that stores data in chunks to bypass database limitations.
It includes signal handlers to manage the chunked data during model instance lifecycle events.
"""

from typing import Any, Optional

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, post_delete, post_init
from django.utils.text import Truncator

from .models import DataChunk


class ChunkedTextField(models.TextField):
    """
    A custom Django TextField that stores data in chunks to bypass database limitations.
    """

    description = "Text field that stores data in chunks to bypass database limitations."

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.truncate_length = kwargs.pop('truncate_length', 50)  # Default truncate length
        self.chunk_size = kwargs.pop('truncate_length', 4000)  # Default chunk size
        kwargs['editable'] = True  # Ensure the field is editable
        super().__init__(*args, **kwargs)
        self.concrete = False  # Make sure Django knows this is not a concrete field
        self.column = None  # Make sure Django knows this is not a concrete field

    def __str__(self) -> str:
        return self.name

    def contribute_to_class(self, cls: Any, name: str, **kwargs: Any) -> None:
        """
        Contribute the field to the model class and connect signal handlers.
        """
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, self.Descriptor(self))
        post_save.connect(self.post_save, sender=cls)
        post_delete.connect(self.post_delete, sender=cls)
        post_init.connect(self.post_init, sender=cls)

    def post_init(self, instance: Any, **kwargs: Any) -> None:
        """
        Signal handler to set the field's value from chunks after the model instance is initialized.
        """
        if instance.pk is not None:
            value = self.get_chunked_value(instance)
        else:
            value = getattr(instance, self.attname)
        setattr(instance, self.attname, value)

    def post_save(self, instance: Any, **kwargs: Any) -> None:
        """
        Signal handler to save chunks after the main model instance is saved.
        """
        value = getattr(instance, self.attname)
        if value is None:
            value = ''
            if instance._chunked_field_cache.get(self.name) is not None:
                value = instance._chunked_field_cache[self.name]
        else:
            value = str(value)

        ct = ContentType.objects.get_for_model(instance, for_concrete_model=False)
        DataChunk.objects.filter(
            content_type=ct,
            object_id=instance.pk,
            field_name=self.name
        ).delete()

        chunk_size = self.chunk_size
        chunks = [value[i:i + chunk_size] for i in range(0, len(value), chunk_size)]

        DataChunk.objects.bulk_create([
            DataChunk(
                content_type=ct,
                object_id=instance.pk,
                field_name=self.name,
                sequence=idx,
                content=chunk
            )
            for idx, chunk in enumerate(chunks)
        ])

        if hasattr(instance, '_chunked_field_cache') and self.name in instance._chunked_field_cache:
            del instance._chunked_field_cache[self.name]

    def post_delete(self, instance: Any, **kwargs: Any) -> None:
        """
        Signal handler to delete chunks when the main model instance is deleted.
        """
        ct = ContentType.objects.get_for_model(instance, for_concrete_model=False)
        DataChunk.objects.filter(
            content_type=ct,
            object_id=instance.pk,
            field_name=self.name
        ).delete()

    def get_chunked_value(self, instance: Any) -> str:
        """
        Retrieve chunks and assemble the value.
        """
        if instance.pk is None:
            return ''
        ct = ContentType.objects.get_for_model(instance, for_concrete_model=False)
        chunks = DataChunk.objects.filter(
            content_type=ct,
            object_id=instance.pk,
            field_name=self.name
        ).order_by('sequence').values_list('content', flat=True)
        value = ''.join(chunks)
        return value

    def formfield(self, form_class: Optional[forms.Field] = None, choices_form_class: Optional[forms.Field] = None,
                  **kwargs: Any) -> forms.Field:
        """
        Return a Django form field for this model field.
        """
        defaults = {'widget': forms.Textarea}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def db_type(self, connection: Any) -> Optional[str]:
        """
        Return None as this field does not have a direct database representation.
        """
        return 'varchar(1)'

    def get_prep_value(self, value: Any) -> str:
        """
        Return an empty string or placeholder to store in the database.
        """
        return ''

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> str:
        """
        Return an empty string; the real value is set in post_init.
        """
        return ''

    def value_to_string(self, obj: Any) -> str:
        """
        Return the truncated value for serialization and display.
        """
        value = self.value_from_object(obj)
        return Truncator(value).chars(self.truncate_length, truncate='...')

    class Descriptor:
        """
        Descriptor class to manage access to the chunked field value.
        """

        def __init__(self, field: 'ChunkedTextField') -> None:
            self.field = field

        def __get__(self, instance: Any, owner: Any) -> Any:
            """
            Retrieve the chunked value from the cache or database.
            """
            if instance is None:
                return self

            if not hasattr(instance, '_chunked_field_cache'):
                instance._chunked_field_cache = {}
            if self.field.name in instance._chunked_field_cache:
                return instance._chunked_field_cache[self.field.name]
            if instance.pk is None:
                return instance._chunked_field_cache.get(self.field.name, '')

            ct = ContentType.objects.get_for_model(instance, for_concrete_model=False)
            value_chunks = DataChunk.objects.filter(
                content_type=ct,
                object_id=instance.pk,
                field_name=self.field.name
            ).order_by('sequence').values_list('content', flat=True)

            value = ''.join(value_chunks)
            instance._chunked_field_cache[self.field.name] = value
            return value

        def __set__(self, instance: Any, value: Any) -> None:
            """
            Set the chunked value in the instance's dictionary and cache.
            """
            instance.__dict__[self.field.attname] = value
            if not hasattr(instance, '_chunked_field_cache'):
                instance._chunked_field_cache = {}
            instance._chunked_field_cache[self.field.name] = value
