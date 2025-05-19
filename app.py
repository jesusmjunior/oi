import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import base64
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Subregistro Civil - COGEX-MA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para importar os dados reais dos arquivos Excel
@st.cache_data
def carregar_dados():
    try:
        # Importando dados sobre municípios
        df_municipios = pd.read_excel("IBGE_Subregistro_Posicao_Municipios.xls")
        
        # Importando dados regionais/nacionais
        df_regioes = pd.read_excel("IBGE_Subregistro_Posicao_BR_NE.xls")
        
        # Exibir informações sobre os dataframes carregados
        print("DataFrame Municípios:")
        print(df_municipios.info())
        print("\nDataFrame Regiões:")
        print(df_regioes.info())
        
        return df_municipios, df_regioes
    
    except Exception as e:
        st.error(f"Erro ao carregar os arquivos: {e}")
        
        # Criar dados simulados para demonstração se houver erro
        # Dados simulados para municípios do Maranhão
        municipios = [
            'São Luís', 'Imperatriz', 'São José de Ribamar', 'Timon', 
            'Caxias', 'Codó', 'Bacabeira', 'Raposa', 'Paço do Lumiar',
            'Balsas', 'Santa Inês', 'Açailândia', 'Buriticupu', 'Barra do Corda'
        ]
        
        dados_simulados_municipios = {
            'Município': municipios,
            'UF': ['MA'] * len(municipios),
            'População_2023': [
                1115932, 260526, 177687, 170222, 164880, 123116, 
                16014, 30761, 148427, 95929, 89489, 113121, 72380, 88492
            ],
            'Nascidos_Vivos_2023': [
                16852, 3687, 2654, 2557, 2463, 1840, 
                241, 462, 2231, 1447, 1354, 1694, 1092, 1320
            ],
            'Registros_Civil_2023': [
                16431, 3540, 2458, 2442, 2280, 1710, 
                218, 423, 2113, 1374, 1259, 1593, 984, 1208
            ],
            'Taxa_Subregistro_2023': [
                2.5, 4.0, 7.4, 4.5, 7.4, 7.1, 
                9.5, 8.4, 5.3, 5.0, 7.0, 6.0, 9.9, 8.5
            ],
            'Ano': [2023] * len(municipios)
        }
        
        # Dados simulados regionais
        dados_simulados_regioes = {
            'Região': ['Brasil', 'Nordeste', 'Norte', 'Sudeste', 'Sul', 'Centro-Oeste', 'Maranhão'],
            'População_2023': [203062512, 57667842, 18430980, 89012756, 30192370, 16758564, 7153262],
            'Nascidos_Vivos_2023': [2805901, 868204, 322542, 1096275, 339958, 178922, 107537],
            'Registros_Civil_2023': [2749783, 834676, 308528, 1078831, 336559, 176190, 102160],
            'Taxa_Subregistro_2023': [2.0, 3.8, 4.3, 1.6, 1.0, 1.5, 5.0],
            'Ano': [2023] * 7
        }
        
        st.warning("Usando dados simulados para demonstração. Por favor, verifique os arquivos Excel.")
        
        return pd.DataFrame(dados_simulados_municipios), pd.DataFrame(dados_simulados_regioes)

# Função para processar os dados
def processar_dados(df_municipios, df_regioes):
    # Processar dados dos municípios
    # Adapte esta função conforme a estrutura real dos seus dados
    
    # Verificar se a coluna de taxa de subregistro existe ou precisa ser calculada
    if 'Taxa_Subregistro' not in df_municipios.columns:
        # Verificar se temos colunas de nascidos vivos e registros civis
        colunas = df_municipios.columns
        col_nascidos = [col for col in colunas if 'nasc' in col.lower() or 'vivo' in col.lower()]
        col_registros = [col for col in colunas if 'regis' in col.lower() or 'civil' in col.lower()]
        
        if col_nascidos and col_registros:
            df_municipios['Taxa_Subregistro'] = 100 * (1 - df_municipios[col_registros[0]] / df_municipios[col_nascidos[0]])
    
    # Processar dados das regiões
    # Adapte esta função conforme a estrutura real dos seus dados
    
    # Verificar se a coluna de taxa de subregistro existe ou precisa ser calculada
    if 'Taxa_Subregistro' not in df_regioes.columns:
        # Verificar se temos colunas de nascidos vivos e registros civis
        colunas = df_regioes.columns
        col_nascidos = [col for col in colunas if 'nasc' in col.lower() or 'vivo' in col.lower()]
        col_registros = [col for col in colunas if 'regis' in col.lower() or 'civil' in col.lower()]
        
        if col_nascidos and col_registros:
            df_regioes['Taxa_Subregistro'] = 100 * (1 - df_regioes[col_registros[0]] / df_regioes[col_nascidos[0]])
    
    return df_municipios, df_regioes

# Função para exportar dados como CSV
def exportar_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="dados_subregistro.csv">Download CSV</a>'
    return href

# Função para criar um gráfico de barras para taxa de subregistro por região
def grafico_subregistro_regiao(df_regioes, ano_selecionado=None):
    if ano_selecionado:
        df_plot = df_regioes[df_regioes['Ano'] == ano_selecionado].copy()
    else:
        # Se não tiver o ano selecionado, usa o ano mais recente
        ano_max = df_regioes['Ano'].max()
        df_plot = df_regioes[df_regioes['Ano'] == ano_max].copy()
    
    # Ordenar por taxa de subregistro decrescente
    df_plot = df_plot.sort_values('Taxa_Subregistro', ascending=False)
    
    # Criar o gráfico
    fig = px.bar(
        df_plot,
        x='Região',
        y='Taxa_Subregistro',
        color='Taxa_Subregistro',
        color_continuous_scale='Reds',
        text_auto='.1f',
        title=f'Taxa de Subregistro por Região - {df_plot["Ano"].iloc[0]}'
    )
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Taxa de Subregistro (%)",
        coloraxis_showscale=False,
        height=500
    )
    
    return fig

# Função para criar um gráfico de barras para taxa de subregistro por município
def grafico_subregistro_municipio(df_municipios, ano_selecionado=None, municipios_selecionados=None):
    if ano_selecionado:
        df_plot = df_municipios[df_municipios['Ano'] == ano_selecionado].copy()
    else:
        # Se não tiver o ano selecionado, usa o ano mais recente
        ano_max = df_municipios['Ano'].max()
        df_plot = df_municipios[df_municipios['Ano'] == ano_max].copy()
    
    # Filtrar por municípios selecionados, se houver
    if municipios_selecionados:
        df_plot = df_plot[df_plot['Município'].isin(municipios_selecionados)]
    
    # Ordenar por taxa de subregistro decrescente
    df_plot = df_plot.sort_values('Taxa_Subregistro', ascending=False)
    
    # Se houver muitos municípios, limitar a exibição aos 15 primeiros
    if len(df_plot) > 15 and not municipios_selecionados:
        df_plot = df_plot.head(15)
    
    # Criar o gráfico
    fig = px.bar(
        df_plot,
        x='Município',
        y='Taxa_Subregistro',
        color='Taxa_Subregistro',
        color_continuous_scale='Reds',
        text_auto='.1f',
        title=f'Taxa de Subregistro por Município - {df_plot["Ano"].iloc[0]}'
    )
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Taxa de Subregistro (%)",
        coloraxis_showscale=False,
        height=500
    )
    
    # Ajustar orientação dos rótulos do eixo x se houver muitos municípios
    if len(df_plot) > 8:
        fig.update_layout(xaxis_tickangle=-45)
    
    return fig

# Função para criar um gráfico de dispersão relacionando população e taxa de subregistro
def grafico_dispersao_populacao_subregistro(df_municipios, ano_selecionado=None):
    if ano_selecionado:
        df_plot = df_municipios[df_municipios['Ano'] == ano_selecionado].copy()
    else:
        # Se não tiver o ano selecionado, usa o ano mais recente
        ano_max = df_municipios['Ano'].max()
        df_plot = df_municipios[df_municipios['Ano'] == ano_max].copy()
    
    # Identificar a coluna de população
    col_populacao = [col for col in df_plot.columns if 'popul' in col.lower()]
    if not col_populacao:
        # Se não encontrar coluna específica, assumir que a coluna 'População' existe
        col_populacao = 'População'
    else:
        col_populacao = col_populacao[0]
    
    # Criar o gráfico
    fig = px.scatter(
        df_plot,
        x=col_populacao,
        y='Taxa_Subregistro',
        size='Taxa_Subregistro',
        color='Taxa_Subregistro',
        hover_name='Município',
        color_continuous_scale='Reds',
        title=f'Relação entre População e Taxa de Subregistro - {df_plot["Ano"].iloc[0]}'
    )
    
    fig.update_layout(
        xaxis_title="População",
        yaxis_title="Taxa de Subregistro (%)",
        height=500
    )
    
    # Usar escala logarítmica para população se houver grande variação
    if df_plot[col_populacao].max() / df_plot[col_populacao].min() > 100:
        fig.update_xaxes(type='log')
    
    return fig

# Função para criar um gráfico de evolução histórica da taxa de subregistro
def grafico_evolucao_historica(df, coluna_regiao='Região', coluna_ano='Ano', regioes_selecionadas=None):
    # Identificar regiões disponíveis
    regioes_disponiveis = df[coluna_regiao].unique()
    
    # Filtrar regiões selecionadas, se houver
    if regioes_selecionadas:
        regioes_plot = [r for r in regioes_selecionadas if r in regioes_disponiveis]
    else:
        # Priorizar Brasil e Maranhão se disponíveis
        regioes_plot = []
        if 'Brasil' in regioes_disponiveis:
            regioes_plot.append('Brasil')
        if 'Maranhão' in regioes_disponiveis:
            regioes_plot.append('Maranhão')
        if 'Nordeste' in regioes_disponiveis and 'Nordeste' not in regioes_plot:
            regioes_plot.append('Nordeste')
    
    # Se não houver regiões para plotar, usar as duas primeiras disponíveis
    if not regioes_plot and len(regioes_disponiveis) > 0:
        regioes_plot = list(regioes_disponiveis[:min(2, len(regioes_disponiveis))])
    
    # Filtrar o dataframe
    df_plot = df[df[coluna_regiao].isin(regioes_plot)]
    
    # Criar o gráfico
    fig = px.line(
        df_plot,
        x=coluna_ano,
        y='Taxa_Subregistro',
        color=coluna_regiao,
        markers=True,
        title='Evolução Histórica da Taxa de Subregistro'
    )
    
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Taxa de Subregistro (%)",
        height=500
    )
    
    return fig

# Função para criar um gráfico de evolução histórica para um município específico
def grafico_evolucao_municipio(df_municipios, municipio, coluna_ano='Ano'):
    # Filtrar dados do município
    df_plot = df_municipios[df_municipios['Município'] == municipio].copy()
    
    # Ordenar por ano
    df_plot = df_plot.sort_values(coluna_ano)
    
    # Criar o gráfico
    fig = px.line(
        df_plot,
        x=coluna_ano,
        y='Taxa_Subregistro',
        markers=True,
        title=f'Evolução da Taxa de Subregistro em {municipio}'
    )
    
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Taxa de Subregistro (%)",
        height=500
    )
    
    # Adicionar anotações com os valores em cada ponto
    for i, row in df_plot.iterrows():
        fig.add_annotation(
            x=row[coluna_ano],
            y=row['Taxa_Subregistro'],
            text=f"{row['Taxa_Subregistro']:.1f}%",
            showarrow=False,
            yshift=10
        )
    
    return fig

# Função para criar um gráfico de comparação entre município e média estadual
def grafico_comparacao_municipio_estado(df_municipios, df_regioes, municipio, coluna_ano='Ano'):
    # Filtrar dados do município
    df_municipio = df_municipios[df_municipios['Município'] == municipio].copy()
    
    # Filtrar dados do estado (Maranhão)
    df_estado = df_regioes[df_regioes['Região'] == 'Maranhão'].copy()
    
    # Verificar anos disponíveis em ambos os dataframes
    anos_municipio = set(df_municipio[coluna_ano])
    anos_estado = set(df_estado[coluna_ano])
    anos_comuns = list(anos_municipio.intersection(anos_estado))
    
    # Filtrar por anos comuns
    df_municipio = df_municipio[df_municipio[coluna_ano].isin(anos_comuns)]
    df_estado = df_estado[df_estado[coluna_ano].isin(anos_comuns)]
    
    # Ordenar por ano
    df_municipio = df_municipio.sort_values(coluna_ano)
    df_estado = df_estado.sort_values(coluna_ano)
    
    # Criar o gráfico
    fig = go.Figure()
    
    # Adicionar linha para o município
    fig.add_trace(go.Scatter(
        x=df_municipio[coluna_ano],
        y=df_municipio['Taxa_Subregistro'],
        mode='lines+markers',
        name=municipio,
        line=dict(color='#1a237e', width=3)
    ))
    
    # Adicionar linha para o estado
    fig.add_trace(go.Scatter(
        x=df_estado[coluna_ano],
        y=df_estado['Taxa_Subregistro'],
        mode='lines+markers',
        name='Média do Maranhão',
        line=dict(color='#d32f2f', width=3, dash='dash')
    ))
    
    fig.update_layout(
        title=f'Comparação entre {municipio} e Média Estadual',
        xaxis_title="Ano",
        yaxis_title="Taxa de Subregistro (%)",
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

# Função principal do app
def main():
    # Título e descrição
    st.title("📊 Dashboard de Análise de Subregistro Civil - COGEX-MA")
    st.markdown("""
    Este dashboard analisa os dados de subregistro civil no Maranhão, comparando com médias regionais e nacionais.
    Utilize os filtros à esquerda para personalizar a visualização.
    """)
    
    # Carregar dados
    df_municipios, df_regioes = carregar_dados()
    
    # Processar dados
    df_municipios, df_regioes = processar_dados(df_municipios, df_regioes)
    
    # Sidebar com filtros
    st.sidebar.title("Filtros")
    
    # Obter anos disponíveis nos dados
    if 'Ano' in df_municipios.columns:
        anos_disponiveis = sorted(df_municipios['Ano'].unique(), reverse=True)
        ano_selecionado = st.sidebar.selectbox(
            "Selecione o ano:",
            anos_disponiveis
        )
    else:
        st.sidebar.warning("Coluna 'Ano' não encontrada nos dados. Usando dados sem filtro de ano.")
        ano_selecionado = None
    
    # Obter municípios disponíveis
    municipios_disponiveis = sorted(df_municipios['Município'].unique())
    
    # Filtro de município para análise detalhada
    municipio_detalhado = st.sidebar.selectbox(
        "Selecione um município para análise detalhada:",
        ['Todos os Municípios'] + municipios_disponiveis
    )
    
    # Filtro para seleção múltipla de municípios
    municipios_selecionados = st.sidebar.multiselect(
        "Selecione municípios para comparação (opcional):",
        municipios_disponiveis
    )
    
    # Filtro para seleção de regiões na evolução histórica
    if 'Região' in df_regioes.columns:
        regioes_disponiveis = sorted(df_regioes['Região'].unique())
        regioes_selecionadas = st.sidebar.multiselect(
            "Selecione regiões para evolução histórica:",
            regioes_disponiveis,
            default=['Brasil', 'Maranhão'] if 'Brasil' in regioes_disponiveis and 'Maranhão' in regioes_disponiveis else []
        )
    else:
        regioes_selecionadas = []
    
    # Opções de visualização
    st.sidebar.title("Opções de Visualização")
    mostrar_unidades_interligadas = st.sidebar.checkbox("Mostrar informações sobre unidades interligadas", value=True)
    mostrar_info_cogex = st.sidebar.checkbox("Mostrar informações sobre COGEX", value=True)
    
    # Botão para exportar dados
    st.sidebar.title("Exportar Dados")
    st.sidebar.markdown(exportar_csv(df_municipios), unsafe_allow_html=True)
    
    # Dividir o layout em abas
    tab1, tab2, tab3 = st.tabs(["Panorama Geral", "Análise por Município", "Séries Históricas"])
    
    with tab1:
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        # Métrica 1: Taxa de Subregistro (MA)
        with col1:
            try:
                # Obter dados do Maranhão e Brasil para o ano selecionado
                if ano_selecionado:
                    taxa_ma = df_regioes[(df_regioes['Região'] == 'Maranhão') & (df_regioes['Ano'] == ano_selecionado)]['Taxa_Subregistro'].values[0]
                    taxa_br = df_regioes[(df_regioes['Região'] == 'Brasil') & (df_regioes['Ano'] == ano_selecionado)]['Taxa_Subregistro'].values[0]
                else:
                    # Se não houver ano selecionado, usar o ano mais recente
                    ano_max = df_regioes['Ano'].max()
                    taxa_ma = df_regioes[(df_regioes['Região'] == 'Maranhão') & (df_regioes['Ano'] == ano_max)]['Taxa_Subregistro'].values[0]
                    taxa_br = df_regioes[(df_regioes['Região'] == 'Brasil') & (df_regioes['Ano'] == ano_max)]['Taxa_Subregistro'].values[0]
                
                # Calcular diferença
                diff = taxa_ma - taxa_br
                
                # Exibir métrica
                st.metric(
                    "Taxa de Subregistro (MA)",
                    f"{taxa_ma:.1f}%",
                    f"{diff:+.1f}% vs Brasil"
                )
            except:
                st.metric("Taxa de Subregistro (MA)", "N/A")
        
        # Métrica 2: Nascidos Vivos (MA)
        with col2:
            try:
                # Identificar coluna de nascidos vivos
                col_nascidos = [col for col in df_regioes.columns if 'nasc' in col.lower() or 'vivo' in col.lower()]
                if col_nascidos:
                    col_nascidos = col_nascidos[0]
                    
                    # Obter dados do Maranhão para o ano selecionado
                    if ano_selecionado:
                        nascidos_ma = df_regioes[(df_regioes['Região'] == 'Maranhão') & (df_regioes['Ano'] == ano_selecionado)][col_nascidos].values[0]
                    else:
                        # Se não houver ano selecionado, usar o ano mais recente
                        ano_max = df_regioes['Ano'].max()
                        nascidos_ma = df_regioes[(df_regioes['Região'] == 'Maranhão') & (df_regioes['Ano'] == ano_max)][col_nascidos].values[0]
                    
                    # Exibir métrica
                    st.metric("Nascidos Vivos (MA)", f"{int(nascidos_ma):,}".replace(',', '.'))
                else:
                    st.metric("Nascidos Vivos (MA)", "N/A")
            except:
                st.metric("Nascidos Vivos (MA)", "N/A")
        
        # Métrica 3: Registros Civis (MA)
        with col3:
            try:
                # Identificar coluna de registros civis
                col_registros = [col for col in df_regioes.columns if 'regis' in col.lower() or 'civil' in col.lower()]
                if col_registros:
                    col_registros = col_registros[0]
                    
                    # Obter dados do Maranhão para o ano selecionado
                    if ano_selecionado:
                        registros_ma = df_regioes[(df_regioes['Região'] == 'Maranhão') & (df_regioes['Ano'] == ano_selecionado)][col_registros].values[0]
                    else:
                        # Se não houver ano selecionado, usar o ano mais recente
                        ano_max = df_regioes['Ano'].max()
                        registros_ma = df_regioes[(df_regioes['Região'] == 'Maranhão') & (df_regioes['Ano'] == ano_max)][col_registros].values[0]
                    
                    # Exibir métrica
                    st.metric("Registros Civis (MA)", f"{int(registros_ma):,}".replace(',', '.'))
                else:
                    st.metric("Registros Civis (MA)", "N/A")
            except:
                st.metric("Registros Civis (MA)", "N/A")
        
        # Métrica 4: Unidades Interligadas
        with col4:
            if mostrar_unidades_interligadas:
                st.metric("Unidades Interligadas", "125")
        
        # Gráfico de taxa de subregistro por região
        st.subheader("Comparativo de Taxa de Subregistro por Região")
        fig_regioes = grafico_subregistro_regiao(df_regioes, ano_selecionado)
        st.plotly_chart(fig_regioes, use_container_width=True)
        
        # Gráfico de taxa de subregistro por município (top 15)
        st.subheader(f"Distribuição do Subregistro nos Municípios do Maranhão")
        fig_municipios = grafico_subregistro_municipio(df_municipios, ano_selecionado)
        st.plotly_chart(fig_municipios, use_container_width=True)
        
        # Gráfico de dispersão: população vs taxa de subregistro
        st.subheader("Relação entre População e Taxa de Subregistro")
        fig_dispersao = grafico_dispersao_populacao_subregistro(df_municipios, ano_selecionado)
        st.plotly_chart(fig_dispersao, use_container_width=True)
        
        # Alerta sobre riscos de subregistro
        st.warning("""
        ### Alerta de Subregistro
        
        A partir de janeiro/2025, o ON-RCPN adotou entendimento pelo qual apenas delegatários, interinos ou prepostos 
        de serventias extrajudiciais podem emitir certidões, afetando o acesso nas maternidades e criando risco de 
        aumento do subregistro.
        """)
    
    with tab2:
        if municipio_detalhado != 'Todos os Municípios':
            # Análise detalhada do município selecionado
            st.subheader(f"Análise Detalhada: {municipio_detalhado}")
            
            # Métricas do município
            col1, col2, col3 = st.columns(3)
            
            # Métrica 1: Taxa de Subregistro
            with col1:
                try:
                    # Obter taxa de subregistro do município para o ano selecionado
                    if ano_selecionado:
                        taxa_mun = df_municipios[(df_municipios['Município'] == municipio_detalhado) & (df_municipios['Ano'] == ano_selecionado)]['Taxa_Subregistro'].values[0]
                    else:
                        # Se não houver ano selecionado, usar o ano mais recente
                        ano_max = df_municipios['Ano'].max()
                        taxa_mun = df_municipios[(df_municipios['Município'] == municipio_detalhado) & (df_municipios['Ano'] == ano_max)]['Taxa_Subregistro'].values[0]
                    
                    # Exibir métrica
                    st.metric("Taxa de Subregistro", f"{taxa_mun:.1f}%")
                except:
                    st.metric("Taxa de Subregistro", "N/A")
            
            # Métrica 2: Nascidos Vivos
            with col2:
                try:
                    # Identificar coluna de nascidos vivos
                    col_nascidos = [col for col in df_municipios.columns if 'nasc' in col.lower() or 'vivo' in col.lower()]
                    if col_nascidos:
                        col_nascidos = col_nascidos[0]
                        
                        # Obter dados do município para o ano selecionado
                        if ano_selecionado:
                            nascidos_mun = df_municipios[(df_municipios['Município'] == municipio_detalhado) & (df_municipios['Ano'] == ano_selecionado)][col_nascidos].values[0]
                        else:
                            # Se não houver ano selecionado, usar o ano mais recente
                            ano_max = df_municipios['Ano'].max()
                            nascidos_mun = df_municipios[(df_municipios['Município'] == municipio_detalhado) & (df_municipios['Ano'] == ano_max)][col_nascidos].values[0]
                        
                        # Exibir métrica
                        st.metric("Nascidos Vivos", f"{int(nascidos_mun):,}".replace(',', '.'))
                    else:
                        st.metric("Nascidos Vivos", "N/A")
                except:
                    st.metric("Nascidos Vivos", "N/A")
            
            # Métrica 3: Registros Civis
            with col3:
                try:
                    # Identificar coluna de registros civis
                    col_registros = [col for col in df_municipios.columns if 'regis' in col.lower() or 'civil' in col.lower()]
                    if col_registros:
                        col_registros = col_registros[0]
                        
                        # Obter dados do município para o ano selecionado
                        if ano_selecionado:
                            registros_mun = df_municipios[(df_municipios['Município'] == municipio_detalhado) & (df_municipios['Ano'] == ano_selecionado)][col_registros].values[0]
                        else:
                            # Se não houver ano selecionado, usar o ano mais recente
                            ano_max = df_municipios['Ano'].max()
                            registros_mun = df_municipios[(df_municipios['Município'] == municipio_detalhado) & (df_municipios['Ano'] == ano_max)][col_registros].values[0]
                        
                        # Exibir métrica
                        st.metric("Registros Civis", f"{int(registros_mun):,}".replace(',', '.'))
                    else:
                        st.metric("Registros Civis", "N/A")
                except:
                    st.metric("Registros Civis", "N/A")
            
            # Gráfico de evolução da taxa de subregistro no município
            st.subheader(f"Evolução da Taxa de Subregistro em {municipio_detalhado}")
            fig_evolucao = grafico_evolucao_municipio(df_municipios, municipio_detalhado)
            st.plotly_chart(fig_evolucao, use_container_width=True)
            
            # Gráfico de comparação com a média estadual
            st.subheader("Comparação com a Média Estadual")
            fig_comparacao = grafico_comparacao_municipio_estado(df_municipios, df_regioes, municipio_detalhado)
            st.plotly_chart(fig_comparacao, use_container_width=True)
            
        else:
            # Visão geral de todos os municípios
            st.subheader("Análise de Todos os Municípios")
            
            # Tabela com dados de todos os municípios
            if ano_selecionado:
                df_tabela = df_municipios[df_municipios['Ano'] == ano_selecionado].copy()
            else:
                # Se não houver ano selecionado, usar o ano mais recente
                ano_max = df_municipios['Ano'].max()
                df_tabela = df_municipios[df_municipios['Ano'] == ano_max].copy()
            
            # Selecionar colunas relevantes
            colunas_relevantes = ['Município', 'Taxa_Subregistro']
            
            # Adicionar colunas de nascidos vivos e registros civis, se existirem
            col_nascidos = [col for col in df_tabela.columns if 'nasc' in col.lower() or 'vivo' in col.lower()]
            col_registros = [col for col in df_tabela.columns if 'regis' in col.lower() or 'civil' in col.lower()]
            
            if col_nascidos:
                colunas_relevantes.append(col_nascidos[0])
            if col_registros:
                colunas_relevantes.append(col_registros[0])
            
            # Ordenar por taxa de subregistro decrescente
            df_tabela = df_tabela[colunas_relevantes].sort_values('Taxa_Subregistro', ascending=False)
            
            # Adicionar coluna de status
            df_tabela['Status'] = pd.cut(
                df_tabela['Taxa_Subregistro'],
                bins=[0, 3, 7, 100],
                labels=['Baixo', 'Médio', 'Alto']
            )
            
            # Exibir tabela
            st.dataframe(df_tabela, use_container_width=True)
            
            # Gráfico dos municípios com maior taxa de subregistro
            st.subheader("Top 5 Municípios com Maior Taxa de Subregistro")
            fig_top5 = grafico_subregistro_municipio(df_municipios, ano_selecionado, municipios_selecionados=df_tabela.head(5)['Município'].tolist())
            st.plotly_chart(fig_top5, use_container_width=True)
            
            # Gráfico de municípios selecionados, se houver
            if municipios_selecionados:
                st.subheader("Comparativo dos Municípios Selecionados")
                fig_selecionados = grafico_subregistro_municipio(df_municipios, ano_selecionado, municipios_selecionados=municipios_selecionados)
                st.plotly_chart(fig_selecionados, use_container_width=True)
    
    with tab3:
        # Evolução histórica da taxa de subregistro
        st.subheader("Evolução Histórica da Taxa de Subregistro")
        fig_historico = grafico_evolucao_historica(df_regioes, regioes_selecionadas=regioes_selecionadas)
        st.plotly_chart(fig_historico, use_container_width=True)
        
        # Informações adicionais sobre unidades interligadas
        if mostrar_unidades_interligadas:
            st.subheader("Unidades Interligadas em Hospitais")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total de Unidades Interligadas", "125")
                st.metric("Unidades com Problemas de Acesso", "119")
            
            with col2:
                st.metric("Unidades Operacionais", "119")
                st.metric("Risco de Aumento do Subregistro", "Alto")
            
            st.info("""
            ### Impacto das Unidades Interligadas
            
            As unidades interligadas são essenciais para o registro civil de nascimento nas maternidades, 
            contribuindo significativamente para a redução do subregistro. A política recente do ON-RCPN 
            pode comprometer esse avanço.
            """)
        
        # Informações sobre a COGEX
        if mostrar_info_cogex:
            st.subheader("Informações sobre a COGEX")
            
            st.markdown("""
            A Corregedoria Geral do Foro Extrajudicial (COGEX) foi criada pela Lei Complementar n.º 271, 
            de 25 de junho de 2024, com competência para fiscalizar os serviços extrajudiciais do Estado do Maranhão.
            
            **Principais desafios relacionados ao registro civil:**
            
            - Ressarcimentos não integrais pelo FERC aos registradores civis
            - A partir de janeiro/2025, o ON-RCPN adotou entendimento pelo qual apenas delegatários, interinos ou 
              prepostos podem emitir certidões em papel nas unidades interligadas
            - Risco de aumento do subregistro devido à preferência da população por certidões em papel
            """)
            
            # Tabela de problemas e ações
            st.markdown("### Principais Ações Recomendadas")
            
            acoes = pd.DataFrame({
                'Problema': [
                    'Ressarcimentos não integrais pelo FERC',
                    'Limitação na emissão de certidões em unidades interligadas',
                    'Falta de capacitação em LGPD e PLD/FT'
                ],
                'Ação Recomendada': [
                    'Regularizar fluxo de ressarcimentos e garantir pagamento integral aos registradores',
                    'Implementar campanha de conscientização sobre validade da certidão digital',
                    'Estabelecer programa institucional de capacitação'
                ],
                'Prazo': ['30 dias', '60 dias', '90 dias']
            })
            
            st.dataframe(acoes, use_container_width=True)

# Executar o aplicativo
if __name__ == "__main__":
    main()
