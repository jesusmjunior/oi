import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# Configurações da página
st.set_page_config(
    page_title="Análise de Subregistro Civil - COGEX-MA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para criar dados simulados (substitua pela leitura real dos arquivos Excel)
@st.cache_data
def carregar_dados():
    # Dados simulados para municípios do Maranhão
    dados_municipios = {
        'Município': [
            'São Luís', 'Imperatriz', 'São José de Ribamar', 'Timon', 
            'Caxias', 'Codó', 'Bacabeira', 'Raposa', 'Paço do Lumiar',
            'Balsas', 'Santa Inês', 'Açailândia', 'Buriticupu', 'Barra do Corda'
        ],
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
        'Unidades_Interligadas': [
            8, 3, 1, 2, 2, 1, 
            0, 0, 1, 1, 1, 1, 0, 1
        ],
        'Possui_COGEX': [
            'Sim', 'Sim', 'Sim', 'Sim', 
            'Sim', 'Não', 'Sim', 'Sim', 'Não',
            'Não', 'Não', 'Não', 'Não', 'Não'
        ]
    }
    
    # Dados históricos simulados
    anos = [2018, 2019, 2020, 2021, 2022, 2023]
    historico = []
    
    for municipio_idx, municipio in enumerate(dados_municipios['Município']):
        for ano in anos:
            # Taxa de subregistro diminuindo ao longo dos anos
            fator_historico = max(0.8, (2024 - ano) / 10)
            taxa_base = dados_municipios['Taxa_Subregistro_2023'][municipio_idx]
            taxa = taxa_base * fator_historico * (1 + np.random.normal(0, 0.1))
            
            # População aumentando levemente
            pop_base = dados_municipios['População_2023'][municipio_idx]
            pop_fator = (ano - 2018) / (2023 - 2018) if ano < 2023 else 1
            populacao = int(pop_base * (0.9 + 0.1 * pop_fator))
            
            # Nascidos vivos proporcional à população
            nasc_base = dados_municipios['Nascidos_Vivos_2023'][municipio_idx]
            nascidos = int(nasc_base * (0.9 + 0.1 * pop_fator) * (1 + np.random.normal(0, 0.05)))
            
            # Registros com base na taxa de subregistro
            registros = int(nascidos * (1 - taxa/100))
            
            historico.append({
                'Município': municipio,
                'Ano': ano,
                'População': populacao,
                'Nascidos_Vivos': nascidos,
                'Registros_Civil': registros,
                'Taxa_Subregistro': max(0, min(15, taxa))
            })
    
    # Dados regionais/nacionais simulados
    dados_regioes = {
        'Região': ['Brasil', 'Nordeste', 'Norte', 'Sudeste', 'Sul', 'Centro-Oeste', 'Maranhão'],
        'População_2023': [203062512, 57667842, 18430980, 89012756, 30192370, 16758564, 7153262],
        'Nascidos_Vivos_2023': [2805901, 868204, 322542, 1096275, 339958, 178922, 107537],
        'Registros_Civil_2023': [2749783, 834676, 308528, 1078831, 336559, 176190, 102160],
        'Taxa_Subregistro_2023': [2.0, 3.8, 4.3, 1.6, 1.0, 1.5, 5.0]
    }
    
    # Histórico regional
    historico_regioes = []
    for regiao_idx, regiao in enumerate(dados_regioes['Região']):
        for ano in anos:
            # Taxa de subregistro diminuindo ao longo dos anos
            fator_historico = max(0.8, (2024 - ano) / 10)
            taxa_base = dados_regioes['Taxa_Subregistro_2023'][regiao_idx]
            taxa = taxa_base * fator_historico * (1 + np.random.normal(0, 0.1))
            
            # População aumentando levemente
            pop_base = dados_regioes['População_2023'][regiao_idx]
            pop_fator = (ano - 2018) / (2023 - 2018) if ano < 2023 else 1
            populacao = int(pop_base * (0.9 + 0.1 * pop_fator))
            
            # Nascidos vivos proporcional à população
            nasc_base = dados_regioes['Nascidos_Vivos_2023'][regiao_idx]
            nascidos = int(nasc_base * (0.9 + 0.1 * pop_fator) * (1 + np.random.normal(0, 0.05)))
            
            # Registros com base na taxa de subregistro
            registros = int(nascidos * (1 - taxa/100))
            
            historico_regioes.append({
                'Região': regiao,
                'Ano': ano,
                'População': populacao,
                'Nascidos_Vivos': nascidos,
                'Registros_Civil': registros,
                'Taxa_Subregistro': max(0, min(15, taxa))
            })
    
    # Criar DataFrames
    df_municipios = pd.DataFrame(historico)
    df_municipios_atual = pd.DataFrame(dados_municipios)
    df_regioes = pd.DataFrame(historico_regioes)
    df_regioes_atual = pd.DataFrame(dados_regioes)
    
    return df_municipios, df_municipios_atual, df_regioes, df_regioes_atual

# Carregamento dos dados
df_municipios, df_municipios_atual, df_regioes, df_regioes_atual = carregar_dados()

# Função para exportar dados
def exportar_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="dados_subregistro.csv">Download CSV</a>'
    return href

# INTERFACE DO USUÁRIO

# Título principal e descrição
st.title("📊 Análise de Subregistro Civil - COGEX-MA")
st.markdown("""
Este aplicativo mostra a análise dos dados de subregistro civil no Estado do Maranhão,
comparados com dados nacionais e regionais. O dashboard permite filtrar e visualizar
informações sobre a efetividade do registro civil de nascimento.
""")

# Sidebar para filtros
st.sidebar.title("Filtros")

# Seleção de ano
anos_disponiveis = sorted(df_municipios['Ano'].unique())
ano_selecionado = st.sidebar.selectbox(
    "Selecione o ano:",
    anos_disponiveis,
    index=len(anos_disponiveis)-1  # Seleciona o último ano por padrão
)

# Filtrar dados pelo ano selecionado
df_mun_filtrado = df_municipios[df_municipios['Ano'] == ano_selecionado]
df_reg_filtrado = df_regioes[df_regioes['Ano'] == ano_selecionado]

# Filtro de municípios
municipios = sorted(df_mun_filtrado['Município'].unique())
municipios_selecionados = st.sidebar.multiselect(
    "Selecione os municípios (vazio = todos):",
    municipios,
    default=[]
)

# Aplicar filtro de municípios
if municipios_selecionados:
    df_mun_filtrado = df_mun_filtrado[df_mun_filtrado['Município'].isin(municipios_selecionados)]

# Outras opções
mostrar_unidades_interligadas = st.sidebar.checkbox("Mostrar informações sobre unidades interligadas", value=True)
mostrar_info_cogex = st.sidebar.checkbox("Mostrar informações sobre COGEX", value=True)

# Botão para exportar dados
st.sidebar.markdown("### Exportar Dados")
st.sidebar.markdown(exportar_csv(df_mun_filtrado), unsafe_allow_html=True)

# LAYOUT PRINCIPAL

# Dividing the layout into tabs
tab1, tab2, tab3 = st.tabs(["Panorama Geral", "Análise por Município", "Séries Históricas"])

with tab1:
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Taxa de Subregistro (MA)", 
            f"{df_reg_filtrado[df_reg_filtrado['Região'] == 'Maranhão']['Taxa_Subregistro'].values[0]:.1f}%",
            f"{df_reg_filtrado[df_reg_filtrado['Região'] == 'Maranhão']['Taxa_Subregistro'].values[0] - df_reg_filtrado[df_reg_filtrado['Região'] == 'Brasil']['Taxa_Subregistro'].values[0]:.1f}%"
        )
    
    with col2:
        st.metric(
            "Nascidos Vivos (MA)", 
            f"{int(df_reg_filtrado[df_reg_filtrado['Região'] == 'Maranhão']['Nascidos_Vivos'].values[0]):,}".replace(',', '.')
        )
    
    with col3:
        st.metric(
            "Registros Civis (MA)", 
            f"{int(df_reg_filtrado[df_reg_filtrado['Região'] == 'Maranhão']['Registros_Civil'].values[0]):,}".replace(',', '.')
        )
    
    with col4:
        if mostrar_unidades_interligadas:
            st.metric("Unidades Interligadas", "125")
    
    # Gráfico comparativo entre regiões
    st.subheader("Comparativo de Taxa de Subregistro por Região")
    fig_regioes = px.bar(
        df_reg_filtrado,
        x='Região',
        y='Taxa_Subregistro',
        color='Taxa_Subregistro',
        text_auto='.1f',
        color_continuous_scale=px.colors.sequential.Reds,
        height=400
    )
    fig_regioes.update_layout(xaxis_title="", yaxis_title="Taxa de Subregistro (%)")
    st.plotly_chart(fig_regioes, use_container_width=True)
    
    # Mapa dos municípios do MA (simulado com gráfico de dispersão)
    if len(df_mun_filtrado) > 0:
        st.subheader(f"Distribuição do Subregistro nos Municípios do Maranhão - {ano_selecionado}")
        
        fig_mapa = px.scatter(
            df_mun_filtrado,
            x='Município',
            y='Taxa_Subregistro',
            size='Nascidos_Vivos',
            color='Taxa_Subregistro',
            hover_name='Município',
            color_continuous_scale=px.colors.sequential.Reds,
            height=500
        )
        fig_mapa.update_layout(
            xaxis_title="", 
            yaxis_title="Taxa de Subregistro (%)",
            xaxis={'categoryorder':'total descending'}
        )
        st.plotly_chart(fig_mapa, use_container_width=True)

with tab2:
    # Filtro adicional para análise detalhada
    municipio_detalhado = st.selectbox(
        "Selecione um município para análise detalhada:",
        ['Todos os Municípios'] + sorted(df_municipios['Município'].unique())
    )
    
    if municipio_detalhado != 'Todos os Municípios':
        # Dados do município selecionado para todos os anos
        df_mun_detalhe = df_municipios[df_municipios['Município'] == municipio_detalhado]
        
        # Métricas do município
        st.subheader(f"Estatísticas de {municipio_detalhado} - {ano_selecionado}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Taxa de Subregistro", 
                f"{df_mun_detalhe[df_mun_detalhe['Ano'] == ano_selecionado]['Taxa_Subregistro'].values[0]:.1f}%"
            )
        
        with col2:
            st.metric(
                "Nascidos Vivos", 
                f"{int(df_mun_detalhe[df_mun_detalhe['Ano'] == ano_selecionado]['Nascidos_Vivos'].values[0]):,}".replace(',', '.')
            )
        
        with col3:
            st.metric(
                "Registros Civis", 
                f"{int(df_mun_detalhe[df_mun_detalhe['Ano'] == ano_selecionado]['Registros_Civil'].values[0]):,}".replace(',', '.')
            )
        
        # Evolução histórica do município
        st.subheader(f"Evolução da Taxa de Subregistro em {municipio_detalhado}")
        fig_evolucao = px.line(
            df_mun_detalhe,
            x='Ano',
            y='Taxa_Subregistro',
            markers=True,
            height=400
        )
        fig_evolucao.update_layout(yaxis_title="Taxa de Subregistro (%)")
        st.plotly_chart(fig_evolucao, use_container_width=True)
        
        # Comparação com média estadual
        st.subheader(f"Comparação com a Média Estadual")
        df_ma_historico = df_regioes[df_regioes['Região'] == 'Maranhão']
        
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Scatter(
            x=df_mun_detalhe['Ano'],
            y=df_mun_detalhe['Taxa_Subregistro'],
            mode='lines+markers',
            name=municipio_detalhado
        ))
        fig_comp.add_trace(go.Scatter(
            x=df_ma_historico['Ano'],
            y=df_ma_historico['Taxa_Subregistro'],
            mode='lines+markers',
            name='Média do Maranhão',
            line=dict(dash='dash')
        ))
        fig_comp.update_layout(
            height=400,
            yaxis_title="Taxa de Subregistro (%)"
        )
        st.plotly_chart(fig_comp, use_container_width=True)
        
    else:
        # Tabela de todos os municípios
        st.subheader(f"Dados de Todos os Municípios - {ano_selecionado}")
        
        # Definir colunas a serem exibidas
        colunas_exibir = ['Município', 'Nascidos_Vivos', 'Registros_Civil', 'Taxa_Subregistro']
        
        # Ordenar por taxa de subregistro
        df_tabela = df_mun_filtrado[colunas_exibir].sort_values('Taxa_Subregistro', ascending=False)
        
        # Formatação da tabela
        df_formatado = df_tabela.copy()
        df_formatado['Taxa_Subregistro'] = df_formatado['Taxa_Subregistro'].round(1).astype(str) + '%'
        df_formatado['Nascidos_Vivos'] = df_formatado['Nascidos_Vivos'].astype(int)
        df_formatado['Registros_Civil'] = df_formatado['Registros_Civil'].astype(int)
        
        st.dataframe(
            df_formatado,
            hide_index=True,
            use_container_width=True
        )
        
        # Top 5 municípios com maior taxa de subregistro
        st.subheader("Top 5 Municípios com Maior Taxa de Subregistro")
        top5 = df_mun_filtrado.sort_values('Taxa_Subregistro', ascending=False).head(5)
        
        fig_top5 = px.bar(
            top5,
            x='Município',
            y='Taxa_Subregistro',
            color='Taxa_Subregistro',
            text_auto='.1f',
            color_continuous_scale=px.colors.sequential.Reds,
            height=400
        )
        fig_top5.update_layout(yaxis_title="Taxa de Subregistro (%)")
        st.plotly_chart(fig_top5, use_container_width=True)

with tab3:
    # Evolução histórica da taxa de subregistro
    st.subheader("Evolução Histórica da Taxa de Subregistro")
    
    # Opções de visualização
    regioes_disponiveis = ['Brasil', 'Nordeste', 'Maranhão']
    regioes_selecionadas = st.multiselect(
        "Selecione as regiões:",
        regioes_disponiveis,
        default=['Brasil', 'Maranhão']
    )
    
    # Filtrar dados
    df_serie_regioes = df_regioes[df_regioes['Região'].isin(regioes_selecionadas)]
    
    # Gráfico de linha para evolução histórica
    fig_historico = px.line(
        df_serie_regioes,
        x='Ano',
        y='Taxa_Subregistro',
        color='Região',
        markers=True,
        height=400
    )
    fig_historico.update_layout(yaxis_title="Taxa de Subregistro (%)")
    st.plotly_chart(fig_historico, use_container_width=True)
    
    # Taxa de subregistro x Unidades interligadas (simulado)
    if mostrar_unidades_interligadas:
        st.subheader("Impacto das Unidades Interligadas no Subregistro")
        
        # Dados simulados de evolução das unidades interligadas
        unidades_historico = pd.DataFrame({
            'Ano': [2018, 2019, 2020, 2021, 2022, 2023],
            'Unidades_Interligadas': [65, 78, 90, 105, 120, 125]
        })
        
        # Taxa de subregistro do Maranhão
        df_ma_historico = df_regioes[df_regioes['Região'] == 'Maranhão']
        
        # Criando gráfico com dois eixos Y
        fig_impacto = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Adicionando taxa de subregistro
        fig_impacto.add_trace(
            go.Scatter(
                x=df_ma_historico['Ano'],
                y=df_ma_historico['Taxa_Subregistro'],
                name="Taxa de Subregistro (%)",
                mode="lines+markers",
                line=dict(color='red')
            ),
            secondary_y=False,
        )
        
        # Adicionando unidades interligadas
        fig_impacto.add_trace(
            go.Scatter(
                x=unidades_historico['Ano'],
                y=unidades_historico['Unidades_Interligadas'],
                name="Nº de Unidades Interligadas",
                mode="lines+markers",
                line=dict(color='blue')
            ),
            secondary_y=True,
        )
        
        # Configurando títulos dos eixos
        fig_impacto.update_layout(
            title_text="Relação entre Unidades Interligadas e Taxa de Subregistro",
            height=400
        )
        fig_impacto.update_xaxes(title_text="Ano")
        fig_impacto.update_yaxes(title_text="Taxa de Subregistro (%)", secondary_y=False)
        fig_impacto.update_yaxes(title_text="Nº de Unidades Interligadas", secondary_y=True)
        
        st.plotly_chart(fig_impacto, use_container_width=True)
    
    # Informações da COGEX
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
        
        st.dataframe(acoes, hide_index=True, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 14px;'>
        © 2025 Corregedoria Geral do Foro Extrajudicial do TJMA. Dados simulados para demonstração.
    </div>
    """, 
    unsafe_allow_html=True
)
