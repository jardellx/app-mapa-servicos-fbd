from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
# Importa a Base declarativa do ficheiro de conexão
from db_connection import Base 

# =================================================================
# PARTE 2: MODELOS DO BANCO DE DADOS
# =================================================================

class Usuario(Base):
    __tablename__ = 'usuario' 
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(10), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    
    avaliacoes = relationship("Avaliacao", back_populates="usuario_obj")

class Servico(Base):
    __tablename__ = 'servico'
    id_servico = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    horario_funcionamento = Column(String(100), nullable=False)
    categoria = Column('categoria', String(50), nullable=False)
    rua = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    numero = Column(String(10), nullable=True) 
    bairro = Column(String(100), nullable=False)

    avaliacoes = relationship("Avaliacao", back_populates="servico_obj")

class Avaliacao(Base):
    __tablename__ = 'avaliacao'
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True)
    id_servico = Column(Integer, ForeignKey('servico.id_servico'), primary_key=True)
    data_avaliacao = Column(Date, nullable=False)
    nota = Column(Integer, nullable=False)
    comentario = Column(Text, nullable=True)

    usuario_obj = relationship("Usuario", back_populates="avaliacoes")
    servico_obj = relationship("Servico", back_populates="avaliacoes")

# Adicione aqui as outras classes do seu banco de dados (Adm, Usuario_comum, etc.)
# se precisar interagir com elas no backend. Por enquanto, apenas as essenciais
# para a aplicação atual estão incluídas.

