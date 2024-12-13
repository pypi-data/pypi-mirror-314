import typing
from .descriptor import FieldDescriptor
from .exceptions import ValidationError

class SchemaMeta(type):
    
    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        new_class._fields = {}
        new_class._kwargs = {}
        for key,value in dct.items():
            

            if isinstance(value, FieldDescriptor):

                new_class._fields[key] = value
                setattr(cls,key,value)
            
            new_class._kwargs[key] = value
        return new_class
    
    


class BaseSchema(metaclass = SchemaMeta):
     def __init__(self):
        
        self._validation_errors = {}
        self._data = {}
        self._called = False
        self._validated_data = {}

class Schema(BaseSchema):
    
    def __init__(self):
        
        super().__init__()

    async def validate(self):
        pass 
    
    def is_valid(self):
        assert self._called == True, "__call__ must be callaed before accessing other validator methoods"
        if len(self.validation_errors.items()) == 0:
            return True
        return False
   
    
    async def __call__(self, *_data_dicts :typing.Dict) -> typing.Any:
        for dicts in _data_dicts:
            if not isinstance(dicts,dict):
                self.cheking = True
                self.validation_errors['error'] = "Expected type dict"
                self._called = True
                return self
                
        data  = {k: v for d in _data_dicts for k, v in d.items()}
        self._validation_errors.clear()
            
        self.declared_fields :typing.Dict[str,typing.Type[FieldDescriptor]] = self.__class__._fields
        
        self.cheking = True
        
        for field_name, descriptor in self.declared_fields.items():
            try:
                value = await descriptor.validate(data.get(field_name))

                #per custom field validator
                try:
                    defined_validator = getattr(self,f"validate_{field_name}",None)
                    if callable(defined_validator):
                        value = await defined_validator(value)
                except (ValidationError, ValueError) as e:
                    self._validation_errors[field_name] = descriptor._validation_errors
                    
                self._validated_data[field_name] = value
            except (ValidationError,ValueError) as e:
                setattr(self,"error",True)
                self._validation_errors[field_name] = descriptor._validation_errors
            

            
            setattr(self,field_name,data.get(field_name))
        
        try:
            await self.validate()
        except Exception as e:
            self.validation_errors['errors']= str(e)
        self._called = True
        return self
    
    
    
    @property
    def validation_errors(self):
        
        return self._validation_errors
    
    @property
    def validated_data(self):
        return self._validated_data

            
    
            
        
    




