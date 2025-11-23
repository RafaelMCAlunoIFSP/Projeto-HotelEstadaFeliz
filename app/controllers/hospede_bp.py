from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.models import db, Hospedes, Reservas, Faturas
from .recepcao_bp import check_perfil 

hospede_bp = Blueprint('hospede_bp', __name__, url_prefix='/hospede')

@hospede_bp.route('/')
@check_perfil('Hóspede')
def painel_pessoal():
    usuario_id = session.get('usuario_id')

    hospede = db.session.execute(
        db.select(Hospedes).filter_by(id_usuario_sistema=usuario_id)
    ).scalar_one_or_none()
    
    if not hospede:
        flash('Perfil de Hóspede não associado a um registro.', 'danger')
        return redirect(url_for('auth_bp.logout'))

    reserva_ativa = db.session.execute(
        db.select(Reservas)
        .filter_by(id_hospede_principal=hospede.id_hospede)
        .filter(Reservas.status_reserva.in_(['Confirmada', 'Em Estadia']))
        .order_by(Reservas.data_checkin.desc())
    ).scalar_one_or_none()
    
    faturas = []
    if reserva_ativa:
        faturas = db.session.execute(
            db.select(Faturas).filter_by(id_reserva=reserva_ativa.id_reserva)
        ).scalars().all()

    return render_template('hospede/painel.html', 
                           hospede=hospede, 
                           reserva_ativa=reserva_ativa, 
                           faturas=faturas)