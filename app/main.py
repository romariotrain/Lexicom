from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import redis.asyncio as redis

app = FastAPI()

redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)


class WriteDataModel(BaseModel):
    # Валидация номера телефона
    phone: str = Field(..., pattern=r'^\+?\d{10,15}$')
    address: str


@app.post("/write_data")
async def write_data(data: WriteDataModel):
    """
    Эндпоинт для записи или обновления данных (номер телефона и адрес).
    """
    try:
        await redis_client.set(data.phone, data.address)
        return {"status": "success", "message": "Data has been written/updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/check_data")
async def check_data(phone: str):
    """
    Эндпоинт для получения данных по номеру телефона.
    """
    address = await redis_client.get(phone)
    print(address)
    if not address:
        raise HTTPException(status_code=404, detail="Data not found.")
    return {"address": address}




