from flask import Flask
from werkzeug.security import generate_password_hash
from app.models.models import db, Perfis, Usuarios

def ensure_initial_data(app):
    with app.app_context():
        perfis_necessarios = app.config.get('PERFIS_USUARIO', [])
        for perfil_nome in perfis_necessarios:
            if db.session.execute(db.select(Perfis).filter_by(nome_perfil=perfil_nome)).scalar_one_or_none() is None:
                perfil = Perfis(nome_perfil=perfil_nome)
                db.session.add(perfil)
        
        db.session.commit()
        print("Perfis de usuário garantidos.")
        
        admin_perfil = db.session.execute(db.select(Perfis).filter_by(nome_perfil='Administrador')).scalar_one_or_none()
        
        if admin_perfil and db.session.execute(db.select(Usuarios).filter_by(email='admin@hotel.com')).scalar_one_or_none() is None:
            admin = Usuarios(
                nome_completo='Administrador Master',
                email='admin@hotel.com',
                senha=generate_password_hash('admin'), 
                perfil_id=admin_perfil.id
            )
            db.session.add(admin)
            db.session.commit()
            print("Administrador inicial criado (E-mail: admin@hotel.com, Senha: admin).")

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.controllers.auth_bp import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.controllers.admin_bp import admin_bp
    app.register_blueprint(admin_bp)
    
    from app.controllers.recepcao_bp import recepcao_bp
    app.register_blueprint(recepcao_bp)
    
    from app.controllers.camareira_bp import camareira_bp
    app.register_blueprint(camareira_bp)
    
    from app.controllers.hospede_bp import hospede_bp
    app.register_blueprint(hospede_bp)
    
    with app.app_context():
        db.create_all()
        ensure_initial_data(app)

    return app