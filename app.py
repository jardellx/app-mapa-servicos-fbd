import panel as pn
import pandas as pd
import os
import traceback
import param
from sqlalchemy import create_engine, text, Column, Integer, String, Date, func, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship

# =================================================================
# PARTE 1: CONEXÃO COM O BANCO DE DADOS
# =================================================================
DB_USER = os.getenv('DB_USER', 'postgres') 
DB_PASSWORD = os.getenv('DB_PASSWORD', 'jardel2011')
DB_HOST = os.getenv('DB_HOST', 'localhost') 
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'mapaservicosbr')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URL)
    Base = declarative_base()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    DB_CONNECTION_OK = True
except Exception as e:
    DB_CONNECTION_OK = False
    DB_CONNECTION_ERROR = traceback.format_exc()

# =================================================================
# PARTE 2: MODELOS DO BANCO DE DADOS (COMPLETOS)
# =================================================================
class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(10), nullable=False)
    data_nascimento = Column(Date, nullable=False)

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

# Tabelas de relacionamento (necessárias para a lógica de remoção)
class Adm(Base): __tablename__ = 'adm'; id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True)
class Usuario_comum(Base): __tablename__ = 'usuario_comum'; id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True)
class Avaliacao(Base): __tablename__ = 'avaliacao'; id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True); id_servico = Column(Integer, ForeignKey('servico.id_servico'), primary_key=True); nota = Column(Integer)
class Favorita(Base): __tablename__ = 'favorita'; id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True); id_servico = Column(Integer, ForeignKey('servico.id_servico'), primary_key=True)
class Historico_De_Pesquisas(Base): __tablename__ = 'historico_de_pesquisas'; id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True); id_servico = Column(Integer, ForeignKey('servico.id_servico'), primary_key=True); data_pesq = Column(Date, primary_key=True)
class Telefone_servico(Base): __tablename__ = 'telefone_servico'; id_servico = Column(Integer, ForeignKey('servico.id_servico'), primary_key=True); numero_telefone = Column(String, primary_key=True)
class Adm_Atualiza_Servico(Base): __tablename__ = 'adm_atualiza_servico'; id_usuario = Column(Integer, ForeignKey('adm.id_usuario'), primary_key=True); id_servico = Column(Integer, ForeignKey('servico.id_servico'), primary_key=True)
class Relatorio_Avaliacao(Base): __tablename__ = 'relatorio_avaliacao'; id = Column(Integer, primary_key=True); id_adm = Column(Integer, ForeignKey('adm.id_usuario')); id_servico = Column(Integer, ForeignKey('servico.id_servico'))

# =================================================================
# PARTE 3: OPERAÇÕES DO BACKEND (COM REMOÇÃO CORRIGIDA)
# =================================================================
# --- Funções para Serviços ---
def get_servicos_enriquecidos_df():
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
    if not all(data.get(k) for k in ['nome', 'categoria', 'horario_funcionamento', 'rua', 'bairro', 'cidade']):
        pn.state.notifications.error("Preencha todos os campos obrigatórios!", duration=4000); return False
    db = SessionLocal()
    try: db.add(Servico(**data)); db.commit(); return True
    except: db.rollback(); return False
    finally: db.close()

def update_servico(id_servico, campo, valor):
    if campo in ['avaliacao_media', 'total_avaliacoes']: return False
    db = SessionLocal()
    try:
        servico = db.query(Servico).filter(Servico.id_servico == id_servico).first()
        if servico: setattr(servico, campo, valor); db.commit(); return True
        return False
    except: db.rollback(); return False
    finally: db.close()

def delete_servicos(ids):
    db = SessionLocal()
    try:
        db.query(Adm_Atualiza_Servico).filter(Adm_Atualiza_Servico.id_servico.in_(ids)).delete(synchronize_session=False)
        db.query(Relatorio_Avaliacao).filter(Relatorio_Avaliacao.id_servico.in_(ids)).delete(synchronize_session=False)
        db.query(Favorita).filter(Favorita.id_servico.in_(ids)).delete(synchronize_session=False)
        db.query(Historico_De_Pesquisas).filter(Historico_De_Pesquisas.id_servico.in_(ids)).delete(synchronize_session=False)
        db.query(Avaliacao).filter(Avaliacao.id_servico.in_(ids)).delete(synchronize_session=False)
        db.query(Telefone_servico).filter(Telefone_servico.id_servico.in_(ids)).delete(synchronize_session=False)
        db.query(Servico).filter(Servico.id_servico.in_(ids)).delete(synchronize_session=False)
        db.commit(); return True
    except Exception as e:
        print(f"Erro ao deletar serviço: {e}"); db.rollback(); return False
    finally: db.close()

# --- Funções para Usuários ---
def get_all_usuarios_df():
    return pd.read_sql_table('usuario', engine, index_col='id_usuario')

def add_usuario(data):
    if not all(data.get(k) for k in ['nome', 'email', 'senha', 'data_nascimento']):
        pn.state.notifications.error("Preencha todos os campos obrigatórios!", duration=4000); return False
    try: data['data_nascimento'] = pd.to_datetime(data['data_nascimento']).date()
    except (ValueError, TypeError): pn.state.notifications.error("Formato de data inválido. Use AAAA-MM-DD.", duration=4000); return False
    db = SessionLocal()
    try: db.add(Usuario(**data)); db.commit(); return True
    except: db.rollback(); return False
    finally: db.close()

def update_usuario(id_usuario, campo, valor):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if usuario: 
            if campo == 'data_nascimento': 
                try: valor = pd.to_datetime(valor).date()
                except (ValueError, TypeError): pn.state.notifications.error("Formato de data inválido.", duration=4000); return False
            setattr(usuario, campo, valor); db.commit(); return True
        return False
    except: db.rollback(); return False
    finally: db.close()

def delete_usuarios(ids):
    db = SessionLocal()
    try:
        adm_ids_to_delete = db.query(Adm.id_usuario).filter(Adm.id_usuario.in_(ids)).all()
        adm_ids_to_delete = [id[0] for id in adm_ids_to_delete]
        if adm_ids_to_delete:
            db.query(Adm_Atualiza_Servico).filter(Adm_Atualiza_Servico.id_usuario.in_(adm_ids_to_delete)).delete(synchronize_session=False)
            db.query(Relatorio_Avaliacao).filter(Relatorio_Avaliacao.id_adm.in_(adm_ids_to_delete)).delete(synchronize_session=False)
        db.query(Favorita).filter(Favorita.id_usuario.in_(ids)).delete(synchronize_session=False)
        db.query(Historico_De_Pesquisas).filter(Historico_De_Pesquisas.id_usuario.in_(ids)).delete(synchronize_session=False)
        db.query(Avaliacao).filter(Avaliacao.id_usuario.in_(ids)).delete(synchronize_session=False)
        db.query(Adm).filter(Adm.id_usuario.in_(ids)).delete(synchronize_session=False)
        db.query(Usuario_comum).filter(Usuario_comum.id_usuario.in_(ids)).delete(synchronize_session=False)
        db.query(Usuario).filter(Usuario.id_usuario.in_(ids)).delete(synchronize_session=False)
        db.commit(); return True
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}"); db.rollback(); return False
    finally: db.close()

# =================================================================
# PARTE 4: LÓGICA E INTERFACE GRÁFICA (VIEW)
# =================================================================
pn.extension('tabulator', notifications=True, loading_spinner='dots')

class CrudApp(param.Parameterized):
    df = param.DataFrame()
    selecao = param.List(default=[])
    reload_trigger = param.Event(default=False)
    
    def __init__(self, get_func, add_func, update_func, delete_func, **params):
        self.get_data, self.add_data, self.update_data, self.delete_data = get_func, add_func, update_func, delete_func
        super().__init__(**params)
        self.carregar_dados()

    @param.depends('reload_trigger', watch=True)
    def carregar_dados(self): self.df = self.get_data()
    
    def adicionar(self, data, callback):
        if self.add_data(data): pn.state.notifications.success("Item adicionado!", duration=3000); self.reload_trigger=True; callback()

    def editar(self, event):
        # CORREÇÃO 2: Usar self.df.index[event.row] em vez de event.index
        id_linha = self.df.index[event.row]
        if self.update_data(id_linha, event.column, event.value):
            pn.state.notifications.info(f"Item {id_linha} atualizado.", duration=2000)
        else:
            pn.state.notifications.error(f"Falha ao atualizar item {id_linha}.", duration=4000)
            self.reload_trigger=True

    def remover(self, event):
        # CORREÇÃO 1: Converter os IDs de numpy.int64 para int
        ids = [int(self.df.index[i]) for i in self.selecao]
        if not ids:
            pn.state.notifications.warning("Nenhum item selecionado.", duration=3000)
            return
        if self.delete_data(ids):
            pn.state.notifications.success(f"{len(ids)} item(ns) removido(s)!", duration=3000)
            self.selecao = []
            self.reload_trigger=True
        else:
            pn.state.notifications.error("Falha ao remover item.", duration=5000)

def criar_aba_servicos():
    app = CrudApp(get_servicos_enriquecidos_df, add_servico, update_servico, delete_servicos)
    form_inputs = { 'nome': pn.widgets.TextInput(name='Nome'), 'categoria': pn.widgets.TextInput(name='Categoria'), 'horario_funcionamento': pn.widgets.TextInput(name='Horário'), 'rua': pn.widgets.TextInput(name='Rua'), 'numero': pn.widgets.TextInput(name='Nº'), 'bairro': pn.widgets.TextInput(name='Bairro'), 'cidade': pn.widgets.TextInput(name='Cidade', value='QUIXADA', disabled=True) }
    add_button = pn.widgets.Button(name='Adicionar Serviço', button_type='primary', icon='plus')
    def limpar_form(): [w.param.update(value='') for k, w in form_inputs.items() if k != 'cidade']
    add_button.on_click(lambda e: app.adicionar({k: w.value for k, w in form_inputs.items()}, limpar_form))
    form_card = pn.Card(pn.FlexBox(*form_inputs.values()), title="➕ Adicionar Novo Serviço", collapsed=True, width_policy='max', header_background="#F0F0F0")
    form_card.append(pn.layout.Divider()); form_card.append(pn.Row(add_button, align='center'))
    
    tabulator = pn.widgets.Tabulator.from_param(app.param.df, layout='fit_data_table', show_index=True, selectable='checkbox', height=500, editors={k: {'type': 'input'} for k in form_inputs.keys()}, header_filters=True, pagination='local', page_size=10)
    tabulator.on_edit(app.editar); tabulator.link(app, selection='selecao', bidirectional=True)
    remove_button = pn.widgets.Button(name='Remover Selecionados', button_type='danger', icon='trash')
    remove_button.on_click(app.remover)
    tabela_card = pn.Card(pn.Row(pn.pane.Markdown("Filtre pelos cabeçalhos."), pn.layout.HSpacer(), remove_button), pn.layout.Divider(), tabulator, title="📋 Serviços Cadastrados (com Avaliações)", collapsible=False)
    return pn.Column(form_card, tabela_card, sizing_mode='stretch_width')

def criar_aba_usuarios():
    app = CrudApp(get_all_usuarios_df, add_usuario, update_usuario, delete_usuarios)
    form_inputs = { 'nome': pn.widgets.TextInput(name='Nome Completo'), 'email': pn.widgets.TextInput(name='Email'), 'senha': pn.widgets.PasswordInput(name='Senha'), 'data_nascimento': pn.widgets.TextInput(name='Data Nascimento', placeholder='AAAA-MM-DD') }
    add_button = pn.widgets.Button(name='Adicionar Usuário', button_type='primary', icon='plus')
    def limpar_form(): [w.param.update(value='') for w in form_inputs.values()]
    add_button.on_click(lambda e: app.adicionar({k: w.value for k, w in form_inputs.items()}, limpar_form))
    form_card = pn.Card(pn.FlexBox(*form_inputs.values()), title="➕ Adicionar Novo Usuário", collapsed=True, width_policy='max', header_background="#F0F0F0")
    form_card.append(pn.layout.Divider()); form_card.append(pn.Row(add_button, align='center'))
    
    tabulator = pn.widgets.Tabulator.from_param(app.param.df, layout='fit_data_table', show_index=True, selectable='checkbox', height=500, editors={k: {'type': 'input'} for k in form_inputs.keys()}, header_filters=True, pagination='local', page_size=10)
    tabulator.on_edit(app.editar); tabulator.link(app, selection='selecao', bidirectional=True)
    remove_button = pn.widgets.Button(name='Remover Selecionados', button_type='danger', icon='trash')
    remove_button.on_click(app.remover)
    tabela_card = pn.Card(pn.Row(pn.pane.Markdown("Filtre pelos cabeçalhos."), pn.layout.HSpacer(), remove_button), pn.layout.Divider(), tabulator, title="👥 Usuários Cadastrados", collapsible=False)
    return pn.Column(form_card, tabela_card, sizing_mode='stretch_width')

def create_main_view():
    try:
        if not DB_CONNECTION_OK:
            return pn.pane.Markdown(f"## 🚨 Erro Crítico na Conexão\n\nVerifique a senha e se o PostgreSQL está ativo.\n\n```{DB_CONNECTION_ERROR}```")
        tabs = pn.Tabs(('Serviços', criar_aba_servicos()), ('Usuários', criar_aba_usuarios()), dynamic=True)
        return pn.template.VanillaTemplate(title="🗺️ Mapa de Serviços BR", main=[pn.pane.Markdown("## Mapa de Serviços de Quixadá"), tabs])
    except Exception as e:
        return pn.pane.Markdown(f"## 🚨 Erro Inesperado ao Construir a Interface\n\n```{traceback.format_exc()}```")

create_main_view().servable()
