from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import db, Usuarios, Perfis
from functools import wraps
from sqlalchemy import func
from .admin_bp import login_required

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')


def check_perfil(perfil_nome_necessario):
    def wrapper(f):
        @login_required
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('perfil_nome') != perfil_nome_necessario:
                flash(f'Acesso negado. Apenas o perfil "{perfil_nome_necessario}" pode acessar esta função.', 'danger')
                return redirect(url_for('auth_bp.login'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = db.session.execute(
            db.select(Usuarios).filter_by(email=email)
        ).scalar_one_or_none()

        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['perfil_id'] = usuario.perfil_id
            
            perfil_nome = db.session.execute(
                db.select(Perfis.nome_perfil).filter_by(id=usuario.perfil_id)
            ).scalar_one()

            session['perfil_nome'] = perfil_nome
            
            flash(f'Bem-vindo, {usuario.nome_completo} ({perfil_nome})!', 'success')
            
            if perfil_nome == 'Administrador':
                return redirect(url_for('admin_bp.dashboard'))
            # TODO: Adicionar redirecionamento para Recepcionista, Camareira, Hóspede
            return redirect(url_for('auth_bp.login'))
        else:
            flash('Email ou senha incorretos.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('auth_bp.login'))