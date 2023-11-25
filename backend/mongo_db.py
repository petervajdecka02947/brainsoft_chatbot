import motor.motor_asyncio
from config import settings


client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DB_KEY)
database = client.brainsoft  # Replace with your database name
