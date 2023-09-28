from models import db, User, Post
from app import app
import datetime

if app.config['SQLALCHEMY_DATABASE_URI'] != 'postgresql:///blogly_test':
    raise Exception("Use test database to run tests!!!")

db.drop_all()
db.create_all()


jonathan_joestar = User(first_name='Jonathan', last_name='Joestar',
                        image_url='https://static.jojowiki.com/images/thumb/b/bd/latest/20221006234855/Jonathan_Infobox_Manga.png/600px-Jonathan_Infobox_Manga.png')
joseph_joestar = User(first_name='Joseph', last_name='Joestar',
                      image_url='https://static.jojowiki.com/images/thumb/e/e2/latest/20221006235618/Joseph_Joestar_Infobox_Manga.png/600px-Joseph_Joestar_Infobox_Manga.png')
jotaro_kujo = User(first_name='Jotaro', last_name='Kujo',
                   image_url='https://static.jojowiki.com/images/6/69/latest/20201130220440/Jotaro_SC_Infobox_Manga.png')
josuke_higashikata = User(first_name='Josuke', last_name='Higashikata',
                          image_url='https://static.jojowiki.com/images/thumb/a/a1/latest/20221007024100/Josuke_DU_Infobox_Manga.png/600px-Josuke_DU_Infobox_Manga.png')
giorno_giovanna = User(first_name='Giorno', last_name='Giovanna',
                       image_url='https://static.jojowiki.com/images/thumb/2/21/latest/20210313222135/Giorno_Giovanna_Infobox_Manga.png/600px-Giorno_Giovanna_Infobox_Manga.png')

post1 = Post(title='Post1', content='Hello',
             created_at=datetime.datetime.now(), user_id=1)

db.session.add_all([jonathan_joestar, joseph_joestar,
                   jotaro_kujo, josuke_higashikata, giorno_giovanna])
db.session.commit()
db.session.add(post1)
db.session.commit()
