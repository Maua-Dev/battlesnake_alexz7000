from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

# TODO: Implement my logic here to handle the requests from Battlesnake


@app.get("/")
def read_root():
    return {
        "apiversion": "1",
        "author": "Alessandro",
        "color": "#888888",
        "head": "default",
        "tail": "default",
        "version": "0.0.1-beta"
    }


@app.post("/move")
def move():
    return{
        "move": "up",
        "shout": "Moving Up!"
    }


handler = Mangum(app, lifespan="off")

# Aqui são minhas rotas, aonde eu devo implementar minha lógica
# Todas as funções que você precisar criar deverá ser neste local
# Criar uma lista, e usar random para criar cobras aleatórias automaticamente
#
