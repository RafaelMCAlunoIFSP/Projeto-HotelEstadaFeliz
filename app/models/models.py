from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

    
class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(80), nullable=False)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfis.id'))

    def __repr__(self):
        return f'<Usuario: {self.nome} - ID: {self.id}>'
    
class Perfis(db.Model):
    __tablename__ = 'perfis'

    id = db.Column(db.Integer, primary_key=True)
    nome_perfil = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario: {self.nome} - ID: {self.id}>'

class TiposQuarto(db.Model):
    __tablename__ = 'tipos_quarto'

    id_tipo = db.Column(db.Integer, primary_key=True)
    nome_tipo = db.Column(db.String(80), unique=True, nullable=False)
    capacidade_maxima = db.Column(db.Integer, nullable=False)
    preco_diaria_base = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(100))

class Quarto(db.Model):
    __tablename__ = 'quartos'

    numero_quarto = db.Column(db.String(10), primary_key=True, unique=True)
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipos_quarto.id_tipo'), nullable=False)
    status_limpeza = db.Column(db.String(20), nullable=False, default='Sujo')
    localizacao = db.Column(db.String(50))

class Hospedes(db.Model):
    __tablename__ = 'hospedes'

    id_hospede = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(150), nullable=False)
    documento = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(20),)
    email = db.Column(db.String(100), unique=True)
    id_usuario_sistema = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

class Reservas(db.Model):
    __tablename__ = 'reservas'

    id_reserva = db.Column(db.Integer, primary_key=True)
    id_hospede_principal = db.Column(db.Integer, db.ForeignKey('hospedes.id_hospede'), nullable=False)
    numero_quarto = db.Column(db.String(10), db.ForeignKey('quartos.numero_quarto'))
    data_checkin = db.Column(db.Date, nullable=False)
    data_checkout = db.Column(db.Date, nullable=False)
    status_reserva = db.Column(db.String(30), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)

class Servicos(db.Model):
    __tablename__ = 'servicos'

    id_servico = db.Column(db.Integer, primary_key=True)
    nome_servico = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

class Faturas(db.Model):
    __tablename__ = 'faturas'

    id_fatura = db.Column(db.Integer, primary_key=True)
    id_reserva = db.Column(db.Integer, db.ForeignKey('reservas.id_reserva'), nullable=False)
    data_emissao = db.Column(db.DateTime, nullable=False)
    valor_servicos = db.Column(db.Float, nullable=False)
    valor_diarias = db.Column(db.Float, nullable=False)
    status_pagamento = db.Column(db.String(20), nullable=False)

class ItensFatura(db.Model):
    __tablename__ = 'itens_fatura'

    id_item = db.Column(db.Integer, primary_key=True)
    id_fatura = db.Column(db.Integer, db.ForeignKey('faturas.id_fatura'), nullable=False)
    id_servico = db.Column(db.Integer, db.ForeignKey('servicos.id_servico'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario_registro = db.Column(db.Float, nullable=False)
    data_consumo = db.Column(db.DateTime, nullable=False)