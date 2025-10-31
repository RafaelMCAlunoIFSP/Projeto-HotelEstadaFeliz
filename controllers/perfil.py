from flask import render_template, redirect, url_for, request, abort, jsonify, Blueprint, session, flash
from models.perfil import Perfil, RESERVAS

perfil_blueprint = Blueprint('perfis', __name__)

perfil_model = Perfil()


@perfil_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":

        usuario = request.form['username']
        senha = request.form['password']

        for individuo in perfil_model._usuarios:
            if individuo["nome"] == usuario and individuo["senha"] == senha:
                session['user_id'] = individuo['id']
                session['perfil_id'] = individuo['perfil']
                flash('Login realizado com sucesso!', 'success')

                if individuo['perfil'] == 'administrador':
                    return redirect(url_for('perfis.admin')) #improvisório, isso vai ser a homepage
                elif individuo['perfil'] == 'recepcionista':
                    return redirect(url_for('perfis.recepcao')) #improvisório, isso vai ser o redirect pra ação da recepção
                else:
                    return redirect(url_for('perfis.listar_usuarios')) #improvisório, isso vai ser a homepage
            else:
                flash('Login realizado com sucesso!', 'success')

    return render_template('login.html')

@perfil_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('perfil_id', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('perfis.login'))

@perfil_blueprint.route('/recepcao')
def recepcao():
    return render_template('recepcao.html', reservas = RESERVAS)

@perfil_blueprint.route('/administracao')
def administracao():
    return render_template('admin.html', perfis = perfil_model._usuarios)