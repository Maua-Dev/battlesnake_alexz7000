from fastapi import FastAPI
from mangum import Mangum
import random

app = FastAPI()


def avoid_my_body(body, possible_moves):
    remove = []

    for direction, location  in possible_moves.items():
        if location in body:
            remove.append(direction)

    for direction in remove:
        del possible_moves[direction]

    return possible_moves


@app.get("/")
def read_root():
    return{
      "apiversion": "1",
      "author": "alexZ7000",
      "color": "#0000FF",
      "head": "scarf",
      "tail": "coffee",
      "version": "0.0.1-beta"
    }


@app.post("/move")
def move(request: dict):
    print("A cobra vai andar...")
    print(request)
    game = request["game"]
    board = request["board"]
    you = request["you"]

    head = you["head"]
    body = you["body"]
    board_height = board["height"]
    board_width = board["width"]

    possible_moves = {
        "up": {
            "x": head["x"],
            "y": head["y"] + 1
        },
        "down": {
            "x": head["x"],
            "y": head["y"] - 1
        },
        "left": {
            "x": head["x"] - 1,
            "y": head["y"]
        },
        "right": {
            "x": head["x"] + 1,
            "y": head["y"]
        }
    }

    possible_moves = avoid_my_body(body, possible_moves)
    move_snake = random.choice(list(possible_moves.keys()))
    return {
        "move": move_snake,
    }


handler = Mangum(app, lifespan="off")

# tdd test driven development