from faker import Faker
import random
from datetime import *
from classes import *
import numpy as np
import operator
import json
import psycopg2
import getpass

insert_into_psql = True

password = getpass.getpass("Enter password (press enter for default):\n")
port = input("Enter port (press enter for default):\n")
if len(password) == 0:
    password = 'postgres'
if len(port) == 0:
    port = '5432'

conn = psycopg2.connect(dbname="postgres",
                        host="localhost",
                        user="postgres",
                        password=password,
                        port=port)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname='youtube'")
if cursor.fetchone():
    cursor.execute("DROP DATABASE youtube")
cursor.execute("CREATE DATABASE youtube")
cursor.close()
conn.close()

conn = psycopg2.connect(dbname="youtube",
                        host="localhost",
                        user="postgres",
                        password=password,
                        port=port)
conn.autocommit = True
cursor = conn.cursor()

cursor.execute(open("tables.sql", "r").read())
cursor.execute(open("triggers.sql", "r").read())

fake = Faker()
fake.seed_instance(7675139)
random.seed(7675139)
np.random.seed(7675139)

user_quantity = 50000

user_channel_percentage = 5

channel_quantity = user_quantity + 0
main_channel_percentage = 20

video_quantity = 50000
video_main_channel_chance = 95
video_description_max_size = 20,500
main_video_percentage = 20
main_main_video_percentage = 5

comment_quantity = 1000000
comment_reply_chance = 10
comment_heart_chance = 2
comment_not_public_chance = 10
comment_on_main_video_percentage = 90
comment_on_main_main_video_percentage = 80
comment_max_size = 10,300

views_quantity = comment_quantity + 4000000
view_on_main_video_percentage = 70
view_on_main_main_video_percentage = 80
views_not_public_chance = 10

likes_quantity = 0
likes_percentage = 25,50
likes_dislike_percentage = 5
likes_invert_percentage = 10

subs_quantity = 0
subs_percentage = 17, 27

usuarios = []
canais = []
usuario_canal = []
videos = []
comentarios = []
visualizacoes = []
gosteis = []
inscricoes = []

#USUARIOS - START

while len(usuarios) < user_quantity:
    
    print ("user: "+str(len(usuarios)+1)+"/"+str(user_quantity))
    
    id_user = len(usuarios)+1
    name = fake.name().replace('\'', ' ')
    email = fake.email().replace('\'', ' ')
    gender = random.choice(['M', 'F'])
    
    mean = date.today() - timedelta(days=365.25 * 29)

    std = 365.25 * 20

    min_date = date.today() - timedelta(days=365.25 * 115)
    max_date = date.today() - timedelta(days=365.25 * 12)
    
    while True:
        offset = np.random.normal(loc=0, scale=std)
        birth = mean + timedelta(days=int(offset))
        if min_date <= birth <= max_date:
            break
    
    creation = fake.date_time_between(max(birth + timedelta(days=365.25 * 12), date(2000, 1, 1)), date.today())
    
    country = fake.country().replace('\'', ' ')
    
    usuarios.append(User(id_user, name, email, gender, birth, creation, country))
    if insert_into_psql:
        cursor.execute(f"INSERT INTO usuario (nome, email, genero, dataNascimento, data, paisOrigem) VALUES({usuarios[-1].values()})")
    
#USUARIOS - END

#CANAIS - START

for i in usuarios:
    
    print ("channel: "+str(len(canais)+1)+"/"+str(channel_quantity))
    
    id_channel = len(canais)+1
    id_user = i.ID
    name = i.nome
    username = fake.user_name().replace('\'', ' ')
    
    canais.append(Channel(id_channel, name, username))
    usuario_canal.append(User_Channel(id_user, id_channel, 'owner'))
    
    if insert_into_psql:
        cursor.execute(f"INSERT INTO canal (nome, apelido) VALUES({canais[-1].values()})")
        cursor.execute(f"INSERT INTO UsuarioCanal (idUsuario, idCanal, cargo) VALUES({usuario_canal[-1].values()})")

main_channels = set()

while len(main_channels) < channel_quantity / 100 * main_channel_percentage:
    main_channels.add(random.randint(1, channel_quantity))

while len(usuario_canal) < len(usuarios) + len(usuarios)/100 * user_channel_percentage:
    id_channel = random.choice(list(main_channels))
    function = random.choices(['editor', 'mod'], weights=(30, 70), k=1)[0]
    while (id_user := random.randint(1, user_quantity)) == id_channel or (User_Channel(id_user, id_user, function)) in usuario_canal:
        continue
    usuario_canal.append(User_Channel(id_user, id_channel, function))
    
    if insert_into_psql:
        cursor.execute(f"INSERT INTO UsuarioCanal (idUsuario, idCanal, cargo) VALUES({usuario_canal[-1].values()})")


#CANAIS - END

#VIDEOS - START

while len(videos) < video_quantity:
    
    print ("video: "+str(len(videos)+1)+"/"+str(video_quantity))
    
    id_video = len(videos)+1
    title = fake.sentence(nb_words=10).replace('\'', ' ')
    quality = random.choices([144, 240, 360, 480, 720, 1080, 2160], weights=(1, 3, 7, 2, 44, 42, 1), k=1)[0]
    fps = random.choices([25, 30, 50, 60], weights=(3, 70, 2, 25), k=1)[0]
    release_date = fake.date_time_between(date(2000, 1, 1), date.today())
    description = '' if random.randint(0, video_description_max_size[1]) < video_description_max_size[0] else fake.text(max_nb_chars=random.randint(video_description_max_size[0],video_description_max_size[1]))
    visibility = random.choices(['publico', 'nao-listado', 'privado'], weights=(80, 10, 10), k=1)[0]
    public = random.choices(['infantil', 'todos'], weights=(10, 90), k=1)[0]
    
    
    if public == 'todos':
        age_restriction = 'todos'
    else:
        age_restriction = random.choices(['adultos', 'todos'], weights=(10, 90), k=1)[0]
    
    if random.uniform(0, 100) <= video_main_channel_chance:
        id_channel = random.choice(list(main_channels))
    else:
        id_channel = random.randint(1, channel_quantity)
    
    videos.append(Video(id_video, id_channel, title, quality, fps, release_date, description, visibility, public, age_restriction))
    
    if insert_into_psql:
        cursor.execute(f"INSERT INTO video (idCanal, titulo, qualidade, framerate, data, descricao, visibilidade, audiencia, restricaoIdade) VALUES({videos[-1].values()})")
    
#VIDEOS - END

main_videos = set()
main_main_videos = set()

while len(main_videos) < video_quantity / 100 * main_video_percentage:
    while videos[(id_video := random.randint(1, video_quantity))-1].visibilidade != 'publico' or random.uniform(0, 100) <= views_not_public_chance:
        continue
    main_videos.add (id_video)

while len(main_main_videos) < video_quantity / 100 * main_main_video_percentage:
    main_main_videos.add (random.choice(list(main_videos)))
#COMENTARIOS - START


while len(comentarios) < comment_quantity:
    
    print ("comment: "+str(len(comentarios)+1)+"/"+str(comment_quantity))
    
    id_comment = len(comentarios)+1
    id_user = random.randint(1, user_quantity)
    id_reply = None
    text = fake.text(max_nb_chars=random.randint(comment_max_size[0],comment_max_size[1])).replace('\'', ' ')
    
    if random.uniform(0, 100) > comment_reply_chance or len(comentarios) < 1:
        if random.uniform(0, 100) <= comment_on_main_video_percentage:
            if random.uniform(0, 100) <= comment_on_main_main_video_percentage:
                id_video = random.choice(list(main_main_videos))
            else:
                id_video = random.choice(list(main_videos))
        else:
            while videos[(id_video := random.randint(1, video_quantity))-1].audiencia == 'infantil' and (videos[id_video-1].visibilidade == 'publico' or random.uniform(0, 100) <= comment_not_public_chance):
                continue
    else:
        while comentarios[(id_reply := random.randint(1, len(comentarios)))-1].resposta:
            continue
        id_video = comentarios[id_reply-1].IDVideo
    
    publish_date = fake.date_time_between(comentarios[id_reply-1].data if id_reply else videos[id_video-1].data, date.today())
    
    if random.uniform(0, 100) <= comment_heart_chance:
        coracao = True
    else:
        coracao = False
    
    comentarios.append(Comment(id_comment, id_video, id_user, text, publish_date, coracao, id_reply))
    
    if insert_into_psql:
        cursor.execute(f"INSERT INTO comentario (idVideo, idUsuario, texto, data, resposta, coracao) VALUES ({comentarios[-1].values()})")
    
#COMENTARIOS - END

#VISUALIZACOES - START

user_view_tuples = set()
views_not_repeated = []
for i in range (video_quantity):
    views_not_repeated.append([])

for c in comentarios:
    
    print ("view: "+str(len(visualizacoes)+1)+"/"+str(views_quantity))
    
    id_user = c.IDUser
    id_video = c.IDVideo

    data = c.data
    visualizacoes.append(View(id_user, id_video, data))
    
    if insert_into_psql:
        cursor.execute(f"INSERT INTO visualizacao (idUsuario, idVideo, data) VALUES ({visualizacoes[-1].values()})")
        
    if (id_user, id_video) not in user_view_tuples:
        views_not_repeated[id_video-1].append(visualizacoes[-1])
        user_view_tuples.add((id_user, id_video))

while len(visualizacoes) < views_quantity:
    
    print ("view: "+str(len(visualizacoes)+1)+"/"+str(views_quantity))
    
    if random.uniform(0, 100) <= view_on_main_video_percentage:
        if random.uniform(0, 100) <= view_on_main_main_video_percentage:
            id_video = random.choice(list(main_main_videos))
        else:
            id_video = random.choice(list(main_videos))
    else:
        while videos[(id_video := random.randint(1, video_quantity))-1].visibilidade != 'publico' or random.uniform(0, 100) <= views_not_public_chance:
            continue
    id_user = random.randint(1, user_quantity)
    
    mean = videos[id_video-1].data
    std = 120
    min_date = mean
    max_date = datetime.datetime.now()
    
    while True:
        offset = np.random.normal(loc=0, scale=std)
        view_date = mean + timedelta(days=offset)
        if min_date <= view_date <= max_date:
            break
    
    visualizacoes.append(View(id_user, id_video, view_date))
    if insert_into_psql:
        cursor.execute(f"INSERT INTO visualizacao (idUsuario, idVideo, data) VALUES ({visualizacoes[-1].values()})")
    
    if (id_user, id_video) not in user_view_tuples:
        views_not_repeated[id_video-1].append(visualizacoes[-1])
        user_view_tuples.add((id_user, id_video))

#VISUALIZACOES - END

qtt_views = 0
for i in views_not_repeated:
    qtt_views += len(i)

backup_views_not_repeated = list(views_not_repeated)

current_video_id = 0
while current_video_id < video_quantity:
    current_video_views = list(backup_views_not_repeated[current_video_id])
    
    print ("likes_on_video: "+str(current_video_id+1)+"/"+str(video_quantity))
    
    if random.uniform(0, 100) <= likes_dislike_percentage:
        action = False
    else:
        action = True
    
    if (len(current_video_views)) != 0:
        quantity_views_current_video = len(current_video_views)
        current_video_percentage_views = random.randint(likes_percentage[0], likes_percentage[1])
        quantity_to_like = int(quantity_views_current_video - quantity_views_current_video / 100 * current_video_percentage_views)
        while len(current_video_views) > quantity_to_like:
            likes_quantity += 1
            user = random.choice(current_video_views)
            id_user = user.IDUser
            id_video = current_video_id
            data = user.data
            if action == True:
                if random.uniform(0, 100) <= likes_invert_percentage:
                    gosteis.append(Like(id_user, id_video+1, data, False))
                else:
                    gosteis.append(Like(id_user, id_video+1, data, True))
            else:
                if random.uniform(0, 100) <= likes_invert_percentage:
                    gosteis.append(Like(id_user, id_video+1, data, True))
                else:
                    gosteis.append(Like(id_user, id_video+1, data, False))
            if insert_into_psql:
                cursor.execute(f"INSERT INTO gostei (idUsuario, idVideo, data, acao) VALUES ({gosteis[-1].values()})")
            current_video_views.remove(user)

    current_video_id += 1

random.shuffle(gosteis)

subs_not_repeated = set()
current_video_id = 0
while current_video_id < video_quantity:
    current_video_views = list(backup_views_not_repeated[current_video_id])
    
    print ("subs_on_video: "+str(current_video_id+1)+"/"+str(video_quantity))
    
    if (len(current_video_views)) != 0:
        quantity_views_current_video = len(current_video_views)
        current_video_percentage_views = random.randint(subs_percentage[0], subs_percentage[1])
        quantity_to_sub = int(quantity_views_current_video - quantity_views_current_video / 100 * current_video_percentage_views)
        while len(current_video_views) > quantity_to_sub:
            user = random.choice(current_video_views)
            id_user = user.IDUser
            id_video = current_video_id
            id_channel = videos[id_video].IDChannel
            data = user.data
            if (id_user, id_channel) not in subs_not_repeated:
                inscricoes.append(Subscriptions(id_user, id_channel, data))
                if insert_into_psql:
                    cursor.execute(f"INSERT INTO inscricao (idUsuario, idCanal, data) VALUES ({inscricoes[-1].values()})")
                subs_not_repeated.add((id_user, id_channel))
            current_video_views.remove(user)

    current_video_id += 1

cursor.execute(f"VACUUM")

cursor.close()
conn.close()
