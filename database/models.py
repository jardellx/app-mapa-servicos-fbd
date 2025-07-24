from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db_connection import Base # Importa a Base declarativa definida em db_connection.py

class Usuario(Base):
    __tablename__ = 'usuario' 
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(10), nullable=False)
    data_nascimento = Column(Date, nullable=False)

    # Relacionamentos de herança: back_populates aponta para a propriedade na CLASSE RELACIONADA
    usuario_comum_rel = relationship("Usuario_comum", back_populates="usuario_base", uselist=False) 
    adm_rel = relationship("Adm", back_populates="usuario_base", uselist=False) 

    # Relacionamentos para as tabelas que referenciam 'Usuario' (o supertipo)
    avaliacoes = relationship("Avaliacao", back_populates="usuario_obj")
    historicos_pesquisa = relationship("Historico_De_Pesquisas", back_populates="usuario_obj")
    favoritos = relationship("Favorita", back_populates="usuario_obj")


class Usuario_comum(Base):
    __tablename__ = 'usuario_comum'
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True)
    loc_atual_coord = Column(String(100), nullable=True) # Conforme seu CREATE TABLE
    
    # Propriedade que aponta de volta para Usuario, correspondendo a 'usuario_comum_rel' em Usuario
    usuario_base = relationship("Usuario", back_populates="usuario_comum_rel") 


class Adm(Base):
    __tablename__ = 'adm'
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True)
    nivel_acesso = Column(String(100), nullable=True) # Conforme seu CREATE TABLE (nullable)
    
    # Propriedade que aponta de volta para Usuario, correspondendo a 'adm_rel' em Usuario
    usuario_base = relationship("Usuario", back_populates="adm_rel") 

    relatorios_gerados = relationship("Relatorio_Avaliacao", back_populates="adm_obj") 
    servicos_atualizados = relationship("Adm_Atualiza_Servico", back_populates="adm_obj") 


class Servico(Base):
    __tablename__ = 'servico'
    id_servico = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    horario_funcionamento = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    rua = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    numero = Column(String(10), nullable=True) 
    bairro = Column(String(100), nullable=False)

    # Relacionamentos com outras tabelas
    telefones = relationship("Telefone_servico", back_populates="servico_obj") 
    avaliacoes = relationship("Avaliacao", back_populates="servico_obj") 
    historicos_pesquisa_servico = relationship("Historico_De_Pesquisas", back_populates="servico_obj") 
    favoritos_servico = relationship("Favorita", back_populates="servico_obj") 
    relatorios_recebidos = relationship("Relatorio_Avaliacao", back_populates="servico_obj") 
    adm_atualizacoes = relationship("Adm_Atualiza_Servico", back_populates="servico_obj") 


class Telefone_servico(Base):
    __tablename__ = 'telefone_servico'
    id_servico = Column(Integer, ForeignKey('servico.id_servico'), primary_key=True)
    numero_telefone = Column(String(20), primary_key=True, nullable=False)
    servico_obj = relationship("Servico", back_populates="telefones") 


class Avaliacao(Base):
    __tablename__ = 'avaliacao'
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True) 
    id_servico = Column(Integer, ForeignKey('servico.id_servico'), primary_key=True)
    data_avaliacao = Column(Date, nullable=False)
    nota = Column(Integer, nullable=False)
    comentario = Column(Text, nullable=True)

    usuario_obj = relationship("Usuario", back_populates="avaliacoes")
    servico_obj = relationship("Servico", back_populates="avaliacoes")


class Historico_De_Pesquisas(Base):
    __tablename__ = 'historico_de_pesquisas'
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True) 
    id_servico = Column(Integer, ForeignKey('servico.id_servico'), primary_key=True)
    data_pesq = Column(Date, primary_key=True, nullable=False) 

    usuario_obj = relationship("Usuario", back_populates="historicos_pesquisa")
    servico_obj = relationship("Servico", back_populates="historicos_pesquisa_servico")


class Favorita(Base):
    __tablename__ = 'favorita'
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True)
    id_servico = Column(Integer, ForeignKey('servico.id_servico'), primary_key=True)

    usuario_obj = relationship("Usuario", back_populates="favoritos")
    servico_obj = relationship("Servico", back_populates="favoritos_servico")


class Relatorio_Avaliacao(Base):
    __tablename__ = 'relatorio_avaliacao'
    id = Column(Integer, primary_key=True)
    id_adm = Column(Integer, ForeignKey('adm.id_usuario'), nullable=True) 
    id_servico = Column(Integer, ForeignKey('servico.id_servico'), nullable=True) 
    data_geracao = Column(Date, nullable=False)
    periodo_inicial = Column(Date, nullable=False)
    periodo_final = Column(Date, nullable=False)
    conteudo_relatorio = Column(Text, nullable=False)

    adm_obj = relationship("Adm", back_populates="relatorios_gerados")
    servico_obj = relationship("Servico", back_populates="relatorios_recebidos")


class Adm_Atualiza_Servico(Base):
    __tablename__ = 'adm_atualiza_servico'
    id_usuario = Column(Integer, ForeignKey('adm.id_usuario'), primary_key=True)
    id_servico = Column(Integer, ForeignKey('servico.id_servico'), primary_key=True)

    adm_obj = relationship("Adm", back_populates="servicos_atualizados")
    servico_obj = relationship("Servico", back_populates="adm_atualizacoes")