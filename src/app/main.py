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


def avoid_walls(board_width, board_height, possible_moves):
    remove = []

    for direction, location in possible_moves.items():
        x_out_range = (location["x"] < 0) or (location["x"] == board_width)
        y_out_range = (location["y"] < 0) or (location["y"] == board_height)

        if x_out_range or y_out_range:
            remove.append(direction)

    for direction in remove:
        del possible_moves[direction]

    return possible_moves


def avoid_snakes(possible_moves, snakes):
    remove = []

    for snake in snakes:
        for direction, location in possible_moves.items():
            if location in snake["body"]:
                remove.append(direction)

    for direction in remove:
        del possible_moves[direction]

    return possible_moves


def get_close_target(food, head):
    target = None
    min_distance = 1

    for food_location in food:
        distance = abs(head["x"] - food_location["x"]) + abs(head["y"] - food_location["y"])

        if distance < min_distance:
            min_distance = distance
            target = food_location

    return target


def move_target(possible_moves, head, target):
    if target["x"] > head["x"]:
        return "right"
    elif target["x"] < head["x"]:
        return "left"
    elif target["y"] > head["y"]:
        return "up"
    elif target["y"] < head["y"]:
        return "down"
    else:
        return random.choice(list(possible_moves.keys()))


def move_to_tail(possible_moves, head, tail):
    if tail["x"] > head["x"]:
        return "right"
    elif tail["x"] < head["x"]:
        return "left"
    elif tail["y"] > head["y"]:
        return "up"
    elif tail["y"] < head["y"]:
        return "down"
    else:
        return random.choice(list(possible_moves.keys()))


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

    snakes = board["snakes"]
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
    possible_moves = avoid_walls(board_width, board_height, possible_moves)
    possible_moves = avoid_snakes(possible_moves, snakes)

    # target = board["food"][0]
    target = get_close_target(board["food"], head)

    if len(possible_moves) > 0:
        if target is not None:
            move_snake = move_target(possible_moves, head, target)
        else:
            tail = body[-1]
            move_snake = move_to_tail(possible_moves, head, tail)
    else:
        move_snake = random.choice(list(possible_moves.keys()))

    return {
        "move": move_snake
    }


handler = Mangum(app, lifespan="off")

# tdd test driven development
