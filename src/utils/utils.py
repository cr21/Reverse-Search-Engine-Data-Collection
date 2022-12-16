import uuid


def get_unique_image_name():
    return "img-"+str(uuid.uuid1())