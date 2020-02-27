from flask.cli import FlaskGroup
from random import choice
from app import app
from models import Base, add_user, add_post
import json
cli = FlaskGroup(app)

@cli.command('reset-db')
def reset_db():
    Base.metadata.drop_all()
    Base.metadata.create_all()

@cli.command('fill-db')
def fill_db():
    with open('./MOCK_POSTS.json') as f:
        mock_posts = json.load(f)
    with open('./MOCK_USERS.json') as f:
        mock_users = json.load(f)
    usernames = []
    for user in mock_users:
        usernames.append(user['name'])
        add_user(**user)
    for post in mock_posts:
        add_post(username=choice(usernames), **post)


if __name__ == '__main__':
    cli()