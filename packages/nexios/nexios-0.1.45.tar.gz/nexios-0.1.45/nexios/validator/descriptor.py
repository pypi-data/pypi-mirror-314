import typing
from .exceptions import ValidationError
from .fields import BaseField

class FieldDescriptor:
    def __init__(
            self,
            field: typing.Union[BaseField],
            validators: typing.List[typing.Callable] = [],
            required: bool = True,
            default: typing.Any = None
    ) -> None:
        self.field = field
        self.required = required
        self.default = default
        self.validators = validators
        self._validation_errors = []

    async def validate(self, value):
        
        from .base import Schema
        self._validation_errors.clear()

        # If the field is not required and no value is provided, return the default or None
        if not self.required and not value:
            return value

        await self.validate_required(value)

        if isinstance(self.field, Schema):
        
            nested_schema = await self.field(value)
            if not nested_schema.is_valid():
                print("nested error are",nested_schema.validation_errors)
                self._validation_errors = nested_schema.validation_errors
                
                raise ValidationError()
            return nested_schema.validated_data
        return value

        # # Otherwise, treat it as a regular field
        # try:
        #     return await self.field.validate(value)
        # except ValidationError as e:
        #     self._validation_errors.append(str(e))
        #     raise

    async def validate_required(self, value):
        #HACK : TURN BACK TO LIST IF VALIDATION ERROR STILL A DICTIONARY
        self._validation_errors = []
        if self.required and not value and self.default is None:
            self._validation_errors.append("This field is required")
            raise ValidationError("This field is required")
