import requests
import json
import random
import string
from time import sleep

API_DOMAIN = 'http://127.0.0.1:8000/api'
USERNAME_LENGTH = 10
PASSWORD_LENGTH = 12
STATUS_HTTP_SUCCESS = set([200, 201])
CONFIG_FILE_PATH = 'bot_config.json'
HEADERS = {'Content-Type': 'application/json',
           }
SLEEP_PER_REQUEST = 0.5


def read_configuration(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)


def create_users(number_of_users):
    users = []
    for _ in range(number_of_users):
        username = get_random_string(USERNAME_LENGTH)
        password = get_random_string(PASSWORD_LENGTH)
        user_data = {
            'username': username,
            'password': password
        }
        response = requests.post(
            f'{API_DOMAIN}/users/', data=user_data)
        if response.ok:
            token = get_user_token(user_data)
            if token:
                user_data['token'] = token
                users.append(user_data)
                sleep(SLEEP_PER_REQUEST)
    return users


def get_user_token(user):
    response = requests.post(f'{API_DOMAIN}/users/auth/', data=user)
    if response.ok:
        response = response.json()
        return response['token']


def create_posts(users, max_posts_per_user):
    posts = []
    for user in users:
        token = user['token']
        post_amount = random.randint(0, max_posts_per_user)
        for _ in range(post_amount):
            title = get_random_string(10)
            description = get_random_string(50)
            post_data = {
                'title': title,
                'description': description
            }
            response = requests.post(
                f'{API_DOMAIN}/posts/',
                data=post_data,
                headers={'Authorization': f'Bearer {token}'}
            )
            if response.ok:
                response = response.json()
                posts.append(response)
                sleep(SLEEP_PER_REQUEST)
    return posts


def like_posts(users, posts, max_likes_per_user):
    if len(posts) > 0:
        for user in users:
            token = user['token']
            post_liked = set()
            like_amount = random.randint(0, max_likes_per_user)
            post_amount = len(posts)
            for _ in range(like_amount):
                post_idx = random.randint(0, post_amount - 1)
                while post_idx in post_liked:
                    post_idx = random.randint(0, post_amount - 1)
                post_id = posts[post_idx]['id']
                response = requests.post(
                    f'{API_DOMAIN}/posts/likes/{post_id}/',
                    headers={'Authorization': f'Bearer {token}'}
                )
                sleep(SLEEP_PER_REQUEST)
                if response.ok:
                    post_liked.add(post_idx)


def get_random_string(length):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


if __name__ == '__main__':
    print('Running...')
    conf = read_configuration(CONFIG_FILE_PATH)
    users = create_users(conf['number_of_users'])
    posts = create_posts(users, conf['max_posts_per_user'])
    like_posts(users, posts, conf['max_likes_per_user'])
    print('Done')
