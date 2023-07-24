from fastapi import FastAPI, Request
from mangum import Mangum
#from agent import Agent

app = FastAPI()
#agent = Agent()


@app.get("/")
def read_root():
    return{
      "apiversion": "1",
      "author": "alexZ7000",
      "color": "#888888",
      "head": "default",
      "tail": "default",
      "version": "0.0.1-beta"
    }

@app.post("/move")
def move(request: Request):
    data = request.json()
    game = data["game"]
    board = data["board"]
    you = data["you"]

    #direction = agent.get_next_move(game, board, you)
    direction = "up"
    return {"move": direction}

handler = Mangum(app, lifespan="off")
