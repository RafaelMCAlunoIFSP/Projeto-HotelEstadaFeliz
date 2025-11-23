import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave_secreta'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PERFIS_USUARIO = ['Administrador', 'Recepcionista', 'Camareira', 'Hóspede']