from ..NValidator import Schema,ValidationError
import warnings
class RequestValidatonMixin:
    validated = False
    _validation_schema = None
    validation_errors = {}
    validated_data = {}
    ok = None


    async def validate_request(self, data = None):
        if not data:
            data = await self.json, await self.data, await self.files
        else:
            data= data, #Conver to a tuple
        if not self._validation_schema:
            warnings.warn("No schema found, use @validate_request(Shema) for nexio.decorators")
            return None
        schema:Schema =  self._validation_schema()

        try:
            schema_check = schema.load({k: v for d in data for k, v in d.items()})

        except  ValidationError as err:
            self.ok = False
            self.validation_errors = err.messages
            return 
        self.ok = True
        self.validated_data =schema_check

        


    