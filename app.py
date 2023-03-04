from fastapi import FastAPI
from routes.user import user
from routes.category import category
from routes.game import game


app = FastAPI()

app.include_router(user)
app.include_router(category)
app.include_router(game)





