import secrets
import os
import base64


def save_picture(img_string):
    random_hex = secrets.token_hex(8)
    from main import app
    picture_fn = random_hex + app.config['IMAGE_FORMAT']
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    with open(picture_path, 'wb') as destination:
        img_data = img_string.encode('utf-8')
        destination.write(base64.decodebytes(img_data))

    return picture_fn
