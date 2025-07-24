import panel as pn
from sqlalchemy.orm import Session
from database.db_connection import get_db
from database.models import Servico 
import datetime 
import pandas as pd 

# IMPORTS ADICIONAIS NECESSÁRIOS PARA O PANEL PUBLICAR O CONTEÚDO CORRETAMENTE
import bokeh.io 
import bokeh.document

# --- AQUI É CRÍTICO: pn.extension() deve ser o primeiro comando Panel executável ---
# Carrega as extensões do Panel (como 'tabulator') e define o template.
pn.extension('tabulator', template='fast') 

# --- Funções de Interação com o Banco de Dados (CRUD - READ) ---

def get_all_servicos():
    """
    Busca todos os serviços do banco de dados e retorna uma lista de dicionários.
    Cada dicionário representa um serviço e será usado para popular a tabela no Panel.
    """
    db = next(get_db()) # Obtém uma nova sessão de banco de dados
    try:
        servicos = db.query(Servico).all() # Busca todos os objetos Servico do BD
        
        data_for_panel = []
        for s in servicos:
            # Converte o objeto Servico em um dicionário, tratando a coluna 'Numero' que pode ser NULA.
            servico_dict = {
                "ID_servico": s.id_servico,
                "Nome": s.nome,
                "Horario": s.horario_funcionamento,
                "Categoria": s.categoria,
                "Rua": s.rua,
                "Cidade": s.cidade,
                "Numero": s.numero if s.numero is not None else "", # Se 'numero' for None, exibe string vazia
                "Bairro": s.bairro
            }
            data_for_panel.append(servico_dict)
        
        # Opcional: Imprime os dados no terminal para depuração. Remove em produção.
        print("Dados retornados de get_all_servicos():", data_for_panel) 
        return data_for_panel
    finally:
        db.close() # Garante que a sessão do banco de dados seja fechada após o uso

# --- Função que cria e organiza o layout da aplicação ---
def create_app_layout():
    """
    Cria todos os componentes da interface do usuário (widgets) e os organiza em um layout.
    """
    titulo_app = pn.pane.Markdown("# Gerenciamento Simples de Serviços")
    
    # Este texto de teste é crucial para depurar: se ele aparecer, o Panel está renderizando.
    test_markdown = pn.pane.Markdown("## Se você vê este texto, o Panel está renderizando! E logo abaixo, a tabela.")

    # Obtém os dados do banco de dados para a tabela
    servicos_table_data = get_all_servicos()

    # Cria a tabela interativa usando pn.widgets.Tabulator
    # Passamos os dados como um Pandas DataFrame para compatibilidade e recursos extras.
    servicos_tabulator = pn.widgets.Tabulator(
        pd.DataFrame(servicos_table_data), # Dados para a tabela, convertidos em DataFrame
        layout='fit_columns', # Ajusta as colunas automaticamente para preencher o espaço disponível
        show_index=False,    # Não mostra a coluna de índice numérico padrão do Pandas
        selectable=True,     # Permite a seleção de linhas na tabela
        height=400, # Define uma altura fixa para a tabela em pixels
        widths={ # Define as larguras relativas das colunas para melhor visualização
            'ID_servico': 0.08, 'Nome': 0.15, 'Horario': 0.12, 'Categoria': 0.10,
            'Rua': 0.15, 'Cidade': 0.10, 'Numero': 0.08, 'Bairro': 0.12
        }
        # editors={'Numero': None} pode ser adicionado se quiser desabilitar a edição de colunas específicas.
    )

    # Organiza todos os componentes em uma coluna vertical (pn.Column)
    main_layout = pn.Column(
        titulo_app,
        test_markdown, # O texto de depuração
        pn.pane.Markdown("## Lista de Serviços Cadastrados"),
        servicos_tabulator,
        pn.pane.Markdown("---"), # Separador visual
        pn.pane.Markdown("Este é um protótipo básico. Funcionalidades de filtragem, edição, inclusão e remoção serão adicionadas em próximas iterações.")
    )
    return main_layout

# --- Ponto de Entrada da Aplicação e Publicação (CRÍTICO PARA A TELA BRANCA) ---
if __name__ == '__main__':
    # 1. Cria a instância do layout da aplicação
    app_layout_instance = create_app_layout() 
    
    # 2. Obtém o documento Bokeh atual. Este é o objeto que representa a página web.
    doc = bokeh.io.curdoc() 
    
    # 3. Adiciona o layout da sua aplicação como o elemento raiz do documento Bokeh.
    # Esta é a ação que publica o conteúdo para o navegador.
    doc.add_root(app_layout_instance) 
    
    # 4. Define o título da aba do navegador.
    doc.title = "App Mapeamento de Serviços" 

    # Para rodar no navegador, use o comando no terminal do VS Code (na pasta raiz do projeto):
    # panel serve app.py --show