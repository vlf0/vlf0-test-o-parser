from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import main

app = FastAPI()


class NotificationRequest(BaseModel):
    product_amount: int


@app.post("/send-notification/")
async def send_notification_endpoint(request: NotificationRequest):
    b_data = await main.redis.get('ids')
    if b_data is not None:
        ids_list = b_data.decode('UTF-8').split(' ')
        try:
            for user in ids_list:
                await main.bot.send_message(int(user), f'Задача на парсинг товаров с сайта Ozon завершена.'
                                                       f' Сохранено: {request.product_amount} товаров.', parse_mode='')
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9000)
