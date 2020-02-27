from sqlalchemy import Column, Integer, Text, DateTime, Date, ForeignKey, String, create_engine, Boolean, Table
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
import datetime
engine = create_engine('sqlite:///app.sqlite', echo=True)
Base = declarative_base(bind=engine)

association_table = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)
class Abstract(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=datetime.datetime.now)

class User(Abstract, Base):
    __tablename__ = 'users'
    name = Column(String(30), unique=True, nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    password = Column(String(50), nullable=False)

    user_posts = relationship('Post')
    favorite_posts = relationship(
        'Post',
        secondary = association_table, 
        back_populates="liked_by")
    def __str__(self):
        return ' | '.join([self.id, self.name, self.email, self.password])

class Post(Abstract, Base):
    __tablename__ = 'posts'
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(60), unique=True, nullable=False)
    content = Column(String(240), nullable=False)
    url = Column(Text, unique=True, nullable=False)
    rating = Column(Integer, default=0)
    tags = Column(Text, nullable=False)
    author = relationship('User')
    liked_by = relationship('User', secondary=association_table, back_populates="favorite_posts")
    def __str__(self):
        return ' | '.join([self.id, self.user_id, self.title, self.url])

def add_user(name, email, password):
    engine = create_engine('sqlite:///app.sqlite', echo=True)
    session = Session(bind=engine)
    new_user = User(name=name, email=email, password=password)
    try:
        session.add(new_user)
        session.commit()
        session.close()
    except IntegrityError:
        session.close()
        return None

def add_post(username, title, content, url, rating, tags):
    engine = create_engine('sqlite:///app.sqlite', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(name=username).first()
    user_posts = user.user_posts
    new_post = Post(title=title, content=content, url=url, rating=rating, tags=tags)
    try:
        user_posts.append(new_post)
        session.commit()
        session.close()
    except IntegrityError:
        session.close()
        return None    

def get_posts():
    engine = create_engine('sqlite:///app.sqlite', echo=True)
    session = Session(bind=engine)
    posts = session.query(Post).all()
    session.close()
    return posts

def like_post(username, post_id):
    engine = create_engine('sqlite:///app.sqlite', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(name=username).first()
    post = session.query(User).get(post_id)
    user_fav_posts = user.favorite_posts
    if post not in user_fav_posts:
        user_fav_posts.append(post)
    else:
        user_fav_posts.remove(post)
    session.commit()
    session.close()