from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import redis.asyncio as redis

app = FastAPI()

redis_client = redis.Redis(host="redis", port=6379,
                           db=0, decode_responses=True)


class WriteDataModel(BaseModel):
    # Валидация номера телефона
    phone: str = Field(..., pattern=r"^\+?\d{10,15}$")
    address: str


class AddressResponseModel(BaseModel):
    address: str


class WriteDataResponseModel(BaseModel):
    status: str
    message: str


@app.post("/write_data", response_model=WriteDataResponseModel)
async def create_data(data: WriteDataModel):
    """
    Эндпоинт для создания новой записи (номер телефона и адрес).
    """
    # Проверяем, существует ли уже запись
    existing_address = await redis_client.get(data.phone)
    if existing_address:
        raise HTTPException(
            status_code=400, detail="Data already exists. "
                                    "Use update endpoint to modify it.")

    await redis_client.set(data.phone, data.address)
    return WriteDataResponseModel(
        status="success",
        message="Data has been created successfully."
    )



@app.put("/write_data", response_model=WriteDataResponseModel)
async def update_data(data: WriteDataModel):
    """
    Эндпоинт для обновления существующей записи (номер телефона и адрес).
    """

    # Проверяем, существует ли запись
    existing_address = await redis_client.get(data.phone)
    if not existing_address:
        raise HTTPException(
            status_code=404, detail="Data not found. "
                                    "Use create endpoint to add new data.")

    await redis_client.set(data.phone, data.address)
    return WriteDataResponseModel(
        status="success",
        message="Data has been updated successfully."
    )



@app.get("/check_data", response_model=AddressResponseModel)
async def check_data(phone: str):
    """
    Эндпоинт для получения данных по номеру телефона.
    """
    address = await redis_client.get(phone)
    if not address:
        raise HTTPException(status_code=404, detail="Data not found.")
    return {"address": address}




