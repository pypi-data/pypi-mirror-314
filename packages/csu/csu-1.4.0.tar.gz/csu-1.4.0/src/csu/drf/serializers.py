from functools import cached_property

from rest_framework.exceptions import ValidationError
from rest_framework.fields import BooleanField
from rest_framework.fields import Field
from rest_framework.serializers import Serializer
from rest_framework.utils.serializer_helpers import ReturnDict

from ..gettext_lazy import _
from ..models import BasePriceModel
from ..models import BaseStatusModel
from ..service import HTTPService


class ServiceSerializerMixin:
    context: dict

    @cached_property
    def service_instance(self) -> HTTPService:
        return self.context["service_instance"]


class AddErrorMixin:
    errors: ReturnDict
    _errors: dict
    _validated_data: dict

    def add_error(self, details: dict[str, list[str]]):
        self._validated_data = {}
        if not hasattr(self, "_errors"):
            self._errors = {}
        self._errors.update(details)
        return ValidationError(self.errors)


class RejectUnexpectedWritableMixin:
    _declared_fields: dict[str, Field]

    def __init_subclass__(cls, **kwargs):
        if not hasattr(getattr(cls, "Meta", None), "expected_writable_fields"):
            raise TypeError("Must define 'expected_writable_fields' in serializer Meta.")

        expected = cls.Meta.expected_writable_fields = set(cls.Meta.expected_writable_fields)
        actual = {name for name, field in cls._declared_fields.items() if not field.read_only}
        unexpected = actual - expected
        if unexpected:
            raise TypeError(f"Misconfigured serializer fields. Unexpected writable fields: {', '.join(unexpected)}")

    def reject_unknown(self, attrs: dict | None):
        if attrs:
            unknown_fields = set(attrs) - self.Meta.expected_writable_fields
            if unknown_fields:
                raise ValidationError({field: [_("This field is unexpected.")] for field in unknown_fields})


class ConfirmSerializer(Serializer):
    instance: BaseStatusModel | BasePriceModel

    confirm = BooleanField(required=True, initial=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        if kwargs.get("partial"):
            raise TypeError("Cannot accept a true value for 'partial'")
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        raise TypeError("This serializer can only confirm!")

    @staticmethod
    def validate_confirm(value):
        if not value:
            raise ValidationError(_("Must have a true value."))
        return value

    def validate(self, data):
        if not self.instance.can_confirm():
            raise ValidationError(_("Confirm time limit expired."))

        self.validate_issuing_limit(self.instance.price)

        return super().validate(data)


class CancelSerializer(Serializer):
    instance: BaseStatusModel | BasePriceModel

    cancel_error = _("Cannot cancel.")
    cancel = BooleanField(required=True, initial=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        if kwargs.get("partial"):
            raise TypeError("Cannot accept a true value for 'partial'")
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        raise TypeError("This serializer can only cancel!")

    @staticmethod
    def validate_cancel(value):
        if not value:
            raise ValidationError(_("Must have a true value."))
        return value

    def validate(self, data):
        if not self.instance.can_cancel():
            raise ValidationError(self.cancel_error)

        return super().validate(data)
