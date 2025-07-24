import pandas as pd
from sqlalchemy.orm import Session
from db_connection import SessionLocal, engine
import models

def get_all_servicos_df():
    """Busca todos os serviços e retorna como um DataFrame pandas."""
    print("BACKEND: Buscando todos os serviços do banco de dados real.")
    try:
        # Usar pandas para ler diretamente a query é eficiente para visualização
        df = pd.read_sql_table('servico', engine, index_col='id_servico')
        # Garante que a coluna 'Categoria' seja referenciada corretamente
        df.rename(columns={'Categoria': 'categoria'}, inplace=True)
        return df
    except Exception as e:
        print(f"Erro ao buscar serviços: {e}")
        # Retorna um dataframe vazio em caso de erro
        return pd.DataFrame()

def add_servico(servico_data: dict):
    """Adiciona um novo serviço ao banco de dados."""
    db: Session = SessionLocal()
    try:
        # Cria uma nova instância do modelo Servico
        novo_servico = models.Servico(**servico_data)
        db.add(novo_servico)
        db.commit()
        db.refresh(novo_servico)
        print(f"BACKEND: Serviço '{novo_servico.nome}' adicionado com id {novo_servico.id_servico}.")
        return novo_servico
    except Exception as e:
        print(f"Erro ao adicionar serviço: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def update_servico(id_servico: int, campo: str, novo_valor: str):
    """Atualiza um campo de um serviço existente."""
    db: Session = SessionLocal()
    try:
        servico = db.query(models.Servico).filter(models.Servico.id_servico == id_servico).first()
        if servico:
            setattr(servico, campo, novo_valor)
            db.commit()
            print(f"BACKEND: Serviço id={id_servico} atualizado. Campo '{campo}' para '{novo_valor}'.")
            return True
        return False
    except Exception as e:
        print(f"Erro ao atualizar serviço: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def delete_servicos(ids_para_deletar: list):
    """Deleta um ou mais serviços do banco de dados."""
    db: Session = SessionLocal()
    try:
        db.query(models.Servico).filter(models.Servico.id_servico.in_(ids_para_deletar)).delete(synchronize_session=False)
        db.commit()
        print(f"BACKEND: Serviços com IDs {ids_para_deletar} deletados.")
        return True
    except Exception as e:
        print(f"Erro ao deletar serviços: {e}")
        db.rollback()
        return False
    finally:
        db.close()
