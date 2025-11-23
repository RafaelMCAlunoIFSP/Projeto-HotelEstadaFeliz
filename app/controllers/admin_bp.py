from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from app.models.models import db, Perfis, Usuarios, TiposQuarto
from functools import wraps

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('perfil_nome') != 'Administrador':
            flash('Acesso negado. Apenas administradores podem acessar esta função.', 'danger')
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    try:
        total_usuarios = db.session.execute(db.select(db.func.count(Usuarios.id))).scalar_one()
        total_tipos_quarto = db.session.execute(db.select(db.func.count(TiposQuarto.id_tipo))).scalar_one()
        
    except Exception as e:
        total_usuarios = 0
        total_tipos_quarto = 0
        
    return render_template('admin/dashboard.html', 
                           total_usuarios=total_usuarios, 
                           total_tipos_quarto=total_tipos_quarto)

@admin_bp.route('/perfis')
@login_required
@admin_required
def listar_perfis():
    perfis = db.session.execute(db.select(Perfis).order_by(Perfis.nome_perfil)).scalars().all()
    
    return render_template('admin/perfis_lista.html', perfis=perfis)

@admin_bp.route('/perfis/form', defaults={'perfil_id': None}, methods=['GET', 'POST'])
@admin_bp.route('/perfis/form/<int:perfil_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def gerenciar_perfil(perfil_id):
    perfil = None
    if perfil_id:
        perfil = db.session.execute(db.select(Perfis).filter_by(id=perfil_id)).scalar_one_or_none()
        if perfil is None:
            flash('Perfil não encontrado.', 'danger')
            return redirect(url_for('.listar_perfis'))

    if request.method == 'POST':
        nome = request.form.get('nome_perfil')
        
        if perfil:
            perfil.nome_perfil = nome
            flash(f'Perfil "{nome}" atualizado com sucesso!', 'success')
        else:
            novo_perfil = Perfis(nome_perfil=nome)
            db.session.add(novo_perfil)
            flash(f'Perfil "{nome}" criado com sucesso!', 'success')

        db.session.commit()
        return redirect(url_for('.listar_perfis'))

    return render_template('admin/perfis_form.html', perfil=perfil)

@admin_bp.route('/perfis/excluir/<int:perfil_id>', methods=['POST'])
@login_required
@admin_required
def excluir_perfil(perfil_id):
    perfil = db.session.execute(db.select(Perfis).filter_by(id=perfil_id)).scalar_one_or_none()
    
    if perfil:
        usuarios_associados = db.session.execute(db.select(Usuarios).filter_by(perfil_id=perfil_id)).scalar_one_or_none()
        if usuarios_associados:
            flash('Não é possível excluir o perfil. Existem usuários associados a ele.', 'danger')
            return redirect(url_for('.listar_perfis'))
        
        db.session.delete(perfil)
        db.session.commit()
        flash(f'Perfil "{perfil.nome_perfil}" excluído com sucesso.', 'success')
    else:
        flash('Perfil não encontrado.', 'danger')

    return redirect(url_for('.listar_perfis'))