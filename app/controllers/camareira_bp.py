from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.models import db, Quarto
from .recepcao_bp import check_perfil


camareira_bp = Blueprint('camareira_bp', __name__, url_prefix='/camareira')

@camareira_bp.route('/')
@check_perfil('Camareira')
def lista_quartos():
    quartos = db.session.execute(
        db.select(Quarto).order_by(Quarto.numero_quarto)
    ).scalars().all()

    return render_template('camareira/lista_quartos.html', quartos=quartos)

@camareira_bp.route('/status/<string:numero_quarto>', methods=['POST'])
@check_perfil('Camareira')
def atualizar_status(numero_quarto):
    quarto = db.session.execute(
        db.select(Quarto).filter_by(numero_quarto=numero_quarto)
    ).scalar_one_or_none()
    
    novo_status = request.form.get('novo_status')
    
    if quarto and novo_status in ['Limp', 'Sujo', 'Em Limpeza']:
        quarto.status_limpeza = novo_status
        db.session.commit()
        flash(f'Status do Quarto {numero_quarto} atualizado para "{novo_status}".', 'success')
    else:
        flash('Quarto não encontrado ou status inválido.', 'danger')

    return redirect(url_for('.lista_quartos'))