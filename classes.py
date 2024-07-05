class User:
    def __init__(self, ID, nome, email, genero, dataNascimento, data, pais):
        self.ID = ID
        self.nome = nome
        self.email = email
        self.genero = genero
        self.dataNascimento = dataNascimento
        self.data = data
        self.pais = pais
    
    def __str__(self):
        return f"{self.ID}, {self.nome}, {self.email}, {self.genero}, {self.dataNascimento}, {self.data}, {self.pais}"
    
    def values(self):
        return f"'{self.nome}', '{self.email}', '{self.genero}', '{self.dataNascimento}', '{self.data}', '{self.pais}'"

class Channel:
    def __init__(self, ID, nome, apelido):
        self.ID = ID
        self.nome = nome
        self.apelido = apelido
        self.qtdInscritos = 0
        self.qtdVideos = 0
        self.qtdViews = 0
    
    def __str__(self):
        return f"{self.ID}, {self.nome}, {self.apelido}, {self.qtdInscritos}, {self.qtdVideos}, {self.qtdViews}"
    
    def values(self):
        return f"'{self.nome}', '{self.apelido}'"
    
class User_Channel:
    def __init__(self, IDUser, IDChannel, cargo):
        self.IDUser = IDUser
        self.IDChannel = IDChannel
        self.cargo = cargo
    
    def __str__(self):
        return f"{self.IDUser}, {self.IDChannel}, {self.cargo}"
    
    def values(self):
        return f"{self.IDUser}, {self.IDChannel}, '{self.cargo}'"

class Video:
    def __init__(self, ID, IDChannel, titulo, qualidade, framerate, data, descricao, visibilidade, audiencia, restricaoIdade):
        self.ID = ID
        self.IDChannel = IDChannel
        self.titulo = titulo
        self.qualidade = qualidade
        self.framerate = framerate
        self.data = data
        self.descricao = descricao
        self.visibilidade = visibilidade
        self.audiencia = audiencia
        self.restricaoIdade = restricaoIdade
    
    
    
    def __str__(self):
        return f"{self.ID}, {self.IDChannel}, {self.titulo}, {self.qualidade}, {self.framerate}, {self.data}, {self.descricao}, {self.visibilidade}, {self.audiencia}, {self.restricaoIdade}"
    
    def values(self):
        return f"{self.IDChannel}, '{self.titulo}', {self.qualidade}, {self.framerate}, '{self.data}', '{self.descricao}', '{self.visibilidade}', '{self.audiencia}', '{self.restricaoIdade}'"

class Comment:
    def __init__(self, ID, IDVideo, IDUser, texto, data, coracao, resposta):
        self.ID = ID
        self.IDVideo = IDVideo
        self.IDUser = IDUser
        self.texto = texto
        self.data = data
        self.qtdRespostas = 0
        self.coracao = coracao
        self.resposta = resposta
    
    def __str__(self):
        return f"{self.ID}, {self.IDUser}, {self.IDVideo}, {self.texto}, {self.data}, {self.qtdRespostas}, {self.coracao}, {self.resposta}"
    
    def values(self):
        return f"{self.IDVideo}, '{self.IDUser}', '{self.texto}', '{self.data}', {self.resposta if self.resposta else 'NULL'}, {self.coracao}"
    
class View:
    def __init__(self, IDUser, IDVideo, data):
        self.IDUser = IDUser
        self.IDVideo = IDVideo
        self.data = data
    
    def __str__(self):
        return f"{self.IDUser}, {self.IDVideo}, {self.data}"
    
    def values(self):
        return f"{self.IDUser}, {self.IDVideo}, '{self.data}'"
    
class Like:
    def __init__(self, IDUser, IDVideo, data, acao):
        self.IDUser = IDUser
        self.IDVideo = IDVideo
        self.data = data
        self.acao = acao
    
    def __str__(self):
        return f"{self.IDUser}, {self.IDVideo}, {self.data}, {self.acao}"
    
    def values(self):
        return f"{self.IDUser}, {self.IDVideo}, '{self.data}', {self.acao}"

class Subscriptions:
    def __init__(self, IDUser, IDCanal, data):
        self.IDUser = IDUser
        self.IDCanal = IDCanal
        self.data = data
    
    def __str__(self):
        return f"{self.IDUser}, {self.IDCanal}, {self.data}"
    
    def values(self):
        return f"{self.IDUser}, {self.IDCanal}, '{self.data}'"
    
from json import JSONEncoder
class CustomJSONEnconder(JSONEncoder):
    def default(self, o):
        return o.__dict__

import datetime
def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__