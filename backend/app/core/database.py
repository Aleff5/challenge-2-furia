from tortoise import Tortoise 
import os


db_url = os.getenv("DB")

async def init_db():
    await Tortoise.init(
        db_url= "postgres://postgres:admin@localhost:5432/FuriaHub",  
        modules={
            "models": [
        "app.models.user",
        "app.models.events",
        "app.models.sorteios",
        "app.models.games"
    ]
}

    )
    await Tortoise.generate_schemas()
