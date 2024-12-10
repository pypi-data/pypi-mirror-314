from collections.abc import Callable
from typing import TypedDict
from typing import TypeVar

from django.core.exceptions import ValidationError
from django.forms import CharField
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.fields import Field

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack  # noqa: UP035, RUF100

_FORM_FIELD_TYPE = TypeVar("_FORM_FIELD_TYPE", bound=type[Field])


class _DRF_FIELD_KWARGS(TypedDict):
    read_only: bool
    write_only: bool
    required: bool | None
    default: object
    initial: object
    source: str
    label: str
    help_text: str
    style: str
    error_messages: dict[str, str]
    validators: list[Callable]
    allow_null: bool


def formfield_for_drf_field(
    drf_field: type[Field] | Field,
    /,
    *,
    formfield_class: _FORM_FIELD_TYPE = CharField,
    **drf_field_kwargs: Unpack[_DRF_FIELD_KWARGS],
) -> _FORM_FIELD_TYPE:
    if drf_field_kwargs:
        assert issubclass(drf_field, Field)
        drf_field = drf_field(**drf_field_kwargs)

    class FormFieldWrapper(formfield_class):
        def to_python(self, value):
            value = super().to_python(value)
            try:
                return drf_field.run_validation(value)
            except DRFValidationError as exc:
                detail = exc.detail
                if isinstance(detail, list):
                    if len(detail) == 1:
                        (detail,) = detail
                        raise ValidationError(str(detail), detail.code) from exc
                    else:
                        code = {err.code for err in detail}
                        if len(code) == 1:
                            (code,) = code
                        else:
                            code = None
                        raise ValidationError([str(err) for err in detail], code) from exc
                else:
                    raise ValidationError(exc.detail) from exc

    return FormFieldWrapper
