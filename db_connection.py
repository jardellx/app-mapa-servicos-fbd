import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# =================================================================
# PARTE 1: CONEXÃO COM O BANCO DE DADOS
# =================================================================
# ATENÇÃO: A sua senha está aqui.
DB_USER = os.getenv('DB_USER', 'postgres') 
DB_PASSWORD = os.getenv('DB_PASSWORD', 'jardel2011')
DB_HOST = os.getenv('DB_HOST', 'localhost') 
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'mapaservicosbr')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Cria o "motor" de conexão
engine = create_engine(DATABASE_URL)

# Cria uma Base para os modelos declarativos
Base = declarative_base()

# Cria uma fábrica de sessões para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para testar a conexão ao executar este ficheiro diretamente
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ Conexão com o banco de dados bem-sucedida!")
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")

