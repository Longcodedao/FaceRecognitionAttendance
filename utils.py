import os
import base64
from datetime import datetime, time

def setupPathImage(image, name):
    image_json = image.split(",")[1]
    decoded_image_data = base64.b64decode(image_json)
    path_image = f"data/images/{name}/{name}.jpeg"

    # Save the image
    if not os.path.exists(f"data/images/{name}"):
        os.makedirs(f"data/images/{name}")

    # print(os.path.exists(path_image))

    if os.path.exists(f"/{path_image}"):
        os.remove(f"/{path_image}")
        print("Path has been cleared")

    with open(path_image, "wb") as image_file:
        image_file.write(decoded_image_data)

    return path_image


def check_datetime(time_input, time_output):
    
    hour_input = time_input.hour
    minute_input = time_input.minute
    second_input = time_input.second
    
    hour_output = time_output.hour
    minute_output = time_output.minute
    second_output = time_output.second
    
    # Compare the extracted components
    if hour_input > hour_output:
        return True
    elif hour_input == hour_output and minute_input > minute_output:
        return True
    elif hour_input == hour_output and minute_input == minute_output and second_input >= second_output:
        return True
    else:
        return False