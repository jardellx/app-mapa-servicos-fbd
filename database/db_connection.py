import os
from sqlalchemy import create_engine, text # Importar 'text' para compatibilidade
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Configurações do Banco de Dados ---
# ATENÇÃO: Substitua 'sua_senha_do_postgres' pela SUA SENHA REAL do PostgreSQL.
# NUNCA use senhas diretamente no código para produção!
DB_USER = os.getenv('DB_USER', 'postgres') 
DB_PASSWORD = os.getenv('DB_PASSWORD', 'sua_senha_do_postgres') # <--- COLOQUE SUA SENHA REAL AQUI!
DB_HOST = os.getenv('DB_HOST', 'localhost') 
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'mapaservicosbr') # Nome exato do seu banco de dados 'mapaservicosbr'

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Base = declarative_base() # Base declarativa para todos os modelos ORM
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Retorna uma sessão de banco de dados para ser usada de forma segura."""
    db = SessionLocal()
    try:
        yield db # Permite que a sessão seja usada em um bloco 'with'
    finally:
        db.close() # Garante que a sessão seja fechada após o uso

# --- Teste de Conexão (Para rodar este arquivo diretamente e verificar a conexão) ---
if __name__ == "__main__":
    print("Tentando conectar ao banco de dados...")
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1")) # Executa uma consulta simples para testar
            print("Conexão bem-sucedida ao banco de dados!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        print("Por favor, verifique as configurações (usuário, senha, host, porta, nome do banco) e se o PostgreSQL está rodando.")