from fastapi import FastAPI
from mangum import Mangum
# from agent import Agent

app = FastAPI()
# agent = Agent()


@app.get("/")
def read_root():
    return{
      "apiversion": "1",
      "author": "alexZ7000",
      "color": "#888888",
      "head": "scarf",
      "tail": "coffee",
      "version": "0.0.1-beta"
    }


@app.post("/move")
def move(request: dict):
    game = request["game"]
    board = request["board"]
    you = request["you"]

    # direction = agent.get_next_move(game, board, you)
    direction = "up"
    return {"move": direction}


handler = Mangum(app, lifespan="off")

# tdd test driven development

