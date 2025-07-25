import pandas as pd
from sqlalchemy.orm import Session
# Importa os componentes necessários dos outros ficheiros
from db_connection import SessionLocal, engine
from models import Servico, Avaliacao, Usuario

# =================================================================
# PARTE 3: OPERAÇÕES DO BACKEND
# =================================================================

# --- Funções para Serviços ---
def get_servicos_enriquecidos_df():
    """Busca todos os serviços e junta com a média de suas avaliações."""
    query = """
    SELECT 
        s.id_servico, s.nome, s.horario_funcionamento, s.categoria,
        s.rua, s.bairro, s.cidade, s.numero,
        ROUND(COALESCE(AVG(a.nota), 0), 2) as avaliacao_media,
        COUNT(a.id_servico) as total_avaliacoes
    FROM servico s
    LEFT JOIN avaliacao a ON s.id_servico = a.id_servico
    GROUP BY s.id_servico ORDER BY s.nome;
    """
    return pd.read_sql_query(query, engine, index_col='id_servico')

def add_servico(data):
    """Adiciona um novo serviço."""
    db: Session = SessionLocal()
    try:
        db.add(Servico(**data))
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()

def update_servico(id_servico, campo, valor):
    """Atualiza um serviço existente."""
    if campo in ['avaliacao_media', 'total_avaliacoes']: return False
    db: Session = SessionLocal()
    try:
        servico = db.query(Servico).filter(Servico.id_servico == id_servico).first()
        if servico:
            setattr(servico, campo, valor)
            db.commit()
            return True
        return False
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()

def delete_servicos(ids):
    """Deleta serviços e suas avaliações associadas."""
    db: Session = SessionLocal()
    try:
        db.query(Avaliacao).filter(Avaliacao.id_servico.in_(ids)).delete(synchronize_session=False)
        db.query(Servico).filter(Servico.id_servico.in_(ids)).delete(synchronize_session=False)
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()

# --- Funções para Usuários ---
def get_all_usuarios_df():
    """Busca todos os usuários."""
    return pd.read_sql_table('usuario', engine, index_col='id_usuario')

def add_usuario(data):
    """Adiciona um novo usuário."""
    try:
        data['data_nascimento'] = pd.to_datetime(data['data_nascimento']).date()
    except (ValueError, TypeError):
        # Idealmente, a notificação de erro seria tratada na UI
        print("Erro: Formato de data inválido. Use AAAA-MM-DD.")
        return False
    db: Session = SessionLocal()
    try:
        db.add(Usuario(**data))
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()

def update_usuario(id_usuario, campo, valor):
    """Atualiza um usuário existente."""
    db: Session = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if usuario: 
            if campo == 'data_nascimento': 
                try:
                    valor = pd.to_datetime(valor).date()
                except (ValueError, TypeError):
                    print("Erro: Formato de data inválido. Use AAAA-MM-DD.")
                    return False
            setattr(usuario, campo, valor)
            db.commit()
            return True
        return False
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()

def delete_usuarios(ids):
    """Deleta usuários e suas avaliações associadas."""
    db: Session = SessionLocal()
    try:
        db.query(Avaliacao).filter(Avaliacao.id_usuario.in_(ids)).delete(synchronize_session=False)
        db.query(Usuario).filter(Usuario.id_usuario.in_(ids)).delete(synchronize_session=False)
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()
