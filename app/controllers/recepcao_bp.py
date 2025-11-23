from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.models import db, Reservas, Hospedes, Quarto
from sqlalchemy import func
from datetime import date
from .auth_bp import check_perfil


recepcao_bp = Blueprint('recepcao_bp', __name__, url_prefix='/recepcao')

@recepcao_bp.route('/')
@check_perfil('Recepcionista')
def terminal():
    # TODO: Implementar lógica de visualização de reservas do dia e quartos disponíveis
    quartos_disponiveis = db.session.execute(
        db.select(Quarto).filter(Quarto.status_limpeza == 'Limp')
    ).scalars().all()
    
    reservas_hoje = db.session.execute(
        db.select(Reservas).filter(Reservas.data_checkin == date.today())
    ).scalars().all()

    return render_template('recepcao/terminal.html', 
                           quartos_disponiveis=quartos_disponiveis, 
                           reservas_hoje=reservas_hoje)

@recepcao_bp.route('/checkin/<int:reserva_id>', methods=['POST'])
@check_perfil('Recepcionista')
def realizar_checkin(reserva_id):
    reserva = db.session.execute(
        db.select(Reservas).filter_by(id_reserva=reserva_id, status_reserva='Confirmada')
    ).scalar_one_or_none()

    if reserva:
        quarto = db.session.execute(
            db.select(Quarto).filter_by(numero_quarto=reserva.numero_quarto)
        ).scalar_one_or_none()
        
        if quarto and quarto.status_limpeza == 'Limp':
            reserva.status_reserva = 'Em Estadia'
            # TODO: Gerar a fatura inicial (diárias)
            db.session.commit()
            flash(f'Check-in do Hóspede ID {reserva.id_hospede_principal} realizado no Quarto {reserva.numero_quarto}.', 'success')
        else:
            flash('Quarto não está pronto (Sujo ou inexistente). Check-in pendente.', 'danger')
    else:
        flash('Reserva não encontrada ou não está confirmada.', 'danger')

    return redirect(url_for('.terminal'))