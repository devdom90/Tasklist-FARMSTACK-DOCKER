#-----IMPORT MOTOR FOR NON-BLOCKING MONGODB DRIVER FOR ASYNC----
from motor.motor_asyncio import AsyncIOMotorClient  


#-----CREATE ASYNC CLIENT AND CREATE MONGODB COLLECTIONS-----

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.tasklist            
tasks_collection = db.tasks    #-----TASKELEMENT DATABASE COLLECTION----
user_collection = db.user      #-----USER DATABASE COLLECTION----- 