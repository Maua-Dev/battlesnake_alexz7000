from fastapi import FastAPI
from mangum import Mangum
import random
from scipy import spatial

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


def get_target_close(foods, head):
    coordinates = []

    if len(foods) == 0:
        return None

    for food in foods:
        coordinates.append((food["x"], food["y"]))

    tree = spatial.KDTree(coordinates)
    closest_food = tree.query([(head["x"], head["y"])])[1]
    return foods[closest_food[0]]  # return foods[closest_food]

'''
    if len(foods) > 0:
        closest_food = foods[0]
        closest_distance = spatial.distance.euclidean((head["x"], head["y"]), (closest_food["x"], closest_food["y"]))

        for food in foods:
            distance = spatial.distance.euclidean((head["x"], head["y"]), (food["x"], food["y"]))
            if distance < closest_distance:
                closest_distance = distance
                closest_food = food

        return closest_food
    else:
        return None
'''


def move_target(possible_moves, head, target):
    distance_x = abs(head["x"] - target["x"])
    distance_y = abs(head["y"] - target["y"])

    for direction, location in possible_moves.items():
        new_distance_x = abs(location["x"] - target["x"])
        new_distance_y = abs(location["y"] - target["y"])

        if new_distance_y < distance_y or new_distance_x < distance_x:
            return direction

    return list(possible_moves.keys())[0]

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
    target = get_target_close(board["food"], head)

    if len(possible_moves) > 0:
        if target is not None:
            move_snake = move_target(possible_moves, head, target)
        else:
            move_snake = random.choice(list(possible_moves.keys()))
    else:
        move_snake = "right"
        print("Mechendo pra direita pq n existe outros movimentos possiveis")
    return {
        "move": move_snake
    }


handler = Mangum(app, lifespan="off")

# tdd test driven development
