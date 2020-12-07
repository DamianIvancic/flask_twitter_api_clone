import requests
import base64

BASE = "http://127.0.0.1:5000"


# Just examples of what the requests should look like

def register(username, password):
    return requests.post(BASE + '/register', json={"username": username, "password": password})


def login(username, password):
    return requests.post(BASE + '/login', json={"username": username, "password": password})


# all the routes that require the used to be logged in need to receive an auth_token
def follow(followed_username, auth_token):
    return requests.post(BASE + '/follow', json={"followed_username": followed_username}, headers={"auth_token": auth_token})


def unfollow(followed_username, auth_token):
    return requests.delete(BASE + '/unfollow', json={"followed_username": followed_username}, headers={"auth_token": auth_token})


def create_post_no_image(body, auth_token):
    return requests.post(BASE + '/create_post', json={"body": body}, headers={"auth_token": auth_token})


def create_post_with_image(body, path_to_image, auth_token):
    with open(path_to_image, 'rb') as img_file:
        img_data = base64.encodebytes(img_file.read())
        img_string = img_data.decode('utf-8')

        return requests.post(BASE + '/create_post', json={"body": body, "img_string": img_string},
                             headers={"auth_token": auth_token})


def delete_post(post_id, auth_token):
    return requests.delete(BASE + '/delete_post', json={"post_id": post_id},
                         headers={"auth_token": auth_token})


def public_timeline():
    return requests.get(BASE + '/public_timeline')


# with filtering (example times)
def public_timeline_with_filtering(after, before):
    headers = {"after": after, "before": before}
    return requests.get(BASE + '/public_timeline', headers=headers)


def private_timeline(auth_token):
    return requests.get(BASE + '/private_timeline', headers={"auth_token": auth_token})












