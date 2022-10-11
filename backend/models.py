from pydantic import BaseModel, Field           #-----IMPORT MODELPATTERNS-----
from bson.objectid import ObjectId as BsonId    #-----HANDLING MONGODB ObjectID WITH Bson-----


class PydanticObjectId(BsonId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls,v):
        if not isinstance(v, BsonId):
            raise TypeError("Object Id required")
        return str(v)  


#-----RAW INPUT MODEL-----    
class NewTask(BaseModel):
    # username: str
    description: str
    done: bool = False
    
    
#-----RAW MODEL WITH _Id ALIAS(MONGODB)-----  
class Task(NewTask):
    id: PydanticObjectId = Field(..., alias="_id")  


#-----USER MODEL-----
class User(BaseModel):
    username: str
    password: str