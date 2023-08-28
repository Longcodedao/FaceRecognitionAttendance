import os
import base64

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