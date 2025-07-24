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
pn.extension('tabulator', template='fast') 

# --- Funções de Interação com o Banco de Dados (CRUD - READ) ---

def get_all_servicos():
    """Busca todos os serviços do banco de dados e retorna como lista de dicionários."""
    db = next(get_db()) # Obtém uma sessão do banco de dados
    try:
        servicos = db.query(Servico).all() # Busca todos os objetos Servico
        
        data_for_panel = []
        for s in servicos:
            # Pegamos os dados do objeto Servico e criamos um dicionário limpo
            servico_dict = {
                "ID_servico": s.id_servico,
                "Nome": s.nome,
                "Horario": s.horario_funcionamento,
                "Categoria": s.categoria,
                "Rua": s.rua,
                "Cidade": s.cidade,
                "Numero": s.numero if s.numero is not None else "", # Exibe vazio se for NULO
                "Bairro": s.bairro
            }
            data_for_panel.append(servico_dict)
        
        print("Dados retornados de get_all_servicos():", data_for_panel) 
        return data_for_panel
    finally:
        db.close() 

# --- Função que cria o layout da aplicação (para ser chamada no __main__) ---
def create_app_layout():
    titulo_app = pn.pane.Markdown("# Gerenciamento Simples de Serviços")
    # Este texto de teste é crucial para depurar se o Panel está renderizando algo.
    test_markdown = pn.pane.Markdown("## Se você vê este texto, o Panel está renderizando! E logo abaixo, a tabela.")

    servicos_table_data = get_all_servicos()

    servicos_tabulator = pn.widgets.Tabulator(
        pd.DataFrame(servicos_table_data), # Passar como DataFrame
        layout='fit_columns', # Ajusta automaticamente as colunas
        show_index=False,    # Não mostra o índice numérico padrão
        selectable=True,     # Permite selecionar linhas
        height=400, # Altura fixa para garantir visibilidade
        widths={ # Define larguras para melhor visualização
            'ID_servico': 0.08, 'Nome': 0.15, 'Horario': 0.12, 'Categoria': 0.10,
            'Rua': 0.15, 'Cidade': 0.10, 'Numero': 0.08, 'Bairro': 0.12
        }
    )

    main_layout = pn.Column(
        titulo_app,
        test_markdown, 
        pn.pane.Markdown("## Lista de Serviços Cadastrados"),
        servicos_tabulator,
        pn.pane.Markdown("---"),
        pn.pane.Markdown("Este é um protótipo básico. Funcionalidades de filtragem, edição, inclusão e remoção serão adicionadas em próximas iterações.")
    )
    return main_layout

# --- Configuração para tornar a aplicação servível ---
if __name__ == '__main__':
    # Cria a instância do layout
    app_layout_instance = create_app_layout() 
    
    # --- PONTO CRÍTICO DE PUBLICAÇÃO: FORÇAR ADIÇÃO AO DOCUMENTO BOKEH MANUALMENTE ---
    # Este é o comando para contornar o erro "aplicativo não publicou nenhum conteúdo"
    doc = bokeh.io.curdoc() # Obtém o documento Bokeh atual (o que o servidor está servindo)
    doc.add_root(app_layout_instance) # Adiciona o layout ao documento Bokeh
    doc.title = "App Mapeamento de Serviços" # Define o título da aba do navegador
    # Não é necessário .servable() quando se usa doc.add_root() diretamente.