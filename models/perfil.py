class Perfil():
    _usuarios = [
        { 'id': 1, 'nome': "Kleber", 'email': "kleber@gmail.com", 'perfil': "administrador", 'senha': "123" },
        { 'id': 2, 'nome': "Clarissa", 'email': "clarissa@gmail.com", 'perfil': "recepcionista", 'senha': "321"},
        { 'id': 3, 'nome': "Evellyn", 'email': "evellyn@gmail.com", 'perfil': "camareira", 'senha': "012"},
        { 'id': 4, 'nome': "Pablo", 'email': "pablo@gmail.com", 'perfil': "hospede", 'senha': "210"}
    ]

class Quarto():
    _quartos = [
        { 'numero quarto': "101A", 'tipo': 1, 'status limpeza': "Limpo", 'localizacao': "Bloco A - Andar 1" }
    ]

class TiposQuarto():
    _tipos_quartos = [
        { 'id tipo': "", 'nome tipo': "", 'capacidade maxima': "", 'preco diaria base': "", 'descricao': ""}
    ]

class Hospedes():
    _hospedes = [
        { 'id': 1, 'nome': "", 'documento': "", 'telefone': "", 'email': "", 'id usuario sistema': "" }
    ]

RESERVAS = [
    {
        'id': 1,
        'id_hospede_principal': 10,
        'numero_quarto': 201,
        'data_checkin': "2025-11-10",
        'data_checkout': "2025-11-13",
        'status_reserva': "Confirmada",
        'valor_total': 750.00
    },
    {
        'id': 2,
        'id_hospede_principal': 11,
        'numero_quarto': 102,
        'data_checkin': "2025-10-28",
        'data_checkout': "2025-10-31",
        'status_reserva': "Check-in Realizado",
        'valor_total': 300.00
    },
    {
        'id': 3,
        'id_hospede_principal': 12,
        'numero_quarto': None,
        'data_checkin': "2026-01-05",
        'data_checkout': "2026-01-10",
        'status_reserva': "Pré_Reserva",
        'valor_total': 500.00
    },
    {
        'id': 4,
        'id_hospede_principal': 13,
        'numero_quarto': 301,
        'data_checkin': "2025-09-01",
        'data_checkout': "2025-09-02",
        'status_reserva': "Concluída",
        'valor_total': 500.00
    },
    {
        'id': 5,
        'id_hospede_principal': 10,
        'numero_quarto': None,
        'data_checkin': "2025-12-24",
        'data_checkout': "2025-12-28",
        'status_reserva': "Cancelada",
        'valor_total': 800.00
    },
    {
        'id': 6,
        'id_hospede_principal': 11,
        'numero_quarto': 101,
        'data_checkin': "2025-11-20",
        'data_checkout': "2025-11-25",
        'status_reserva': "Confirmada",
        'valor_total': 500.00
    },
    {
        'id': 7,
        'id_hospede_principal': 12,
        'numero_quarto': 202,
        'data_checkin': "2025-10-30",
        'data_checkout': "2025-11-01",
        'status_reserva': "Check_in_Realizado",
        'valor_total': 500.00
    }
]

class Servicos():
    _servicos = [
        { 'id': 1, 'nome': "", 'preco': ""}
    ]

class Faturas():
    _faturas = [
        { 'id': 1, 'id reserva': "", 'data emissao': "", 'valor servicos': "", 'valor diarias': "", 'status pagamento': "" }
    ]

class ItensFatura():
    _itens_fatura = [
        { 'id item': "", 'id fatura': "", 'id servico': "", 'quantidade': "", 'preco unitario registro': "", 'data consumo': ""}
    ]