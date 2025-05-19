import streamlit as st
import pandas as pd
import numpy as np
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

# Configuração visual para gráficos
plt.style.use('ggplot')
sns.set_style("whitegrid")

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

# Função para gerar gráfico e converter para imagem
def plot_to_img(fig, dpi=100):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
    buf.seek(0)
    return buf

# Função para exportar dados
def exportar_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="dados_subregistro.csv">Download CSV</a>'
    return href

# Carregamento dos dados
df_municipios, df_municipios_atual, df_regioes, df_regioes_atual = carregar_dados()

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
    
    # Usando matplotlib em vez de plotly
    fig, ax = plt.subplots(figsize=(10, 6))
    # Ordenar por taxa de subregistro
    df_reg_plot = df_reg_filtrado.sort_values('Taxa_Subregistro', ascending=False)
    
    # Definir uma paleta de cores
    colors = sns.color_palette("Reds", len(df_reg_plot))
    
    # Criar gráfico de barras
    bars = ax.bar(df_reg_plot['Região'], df_reg_plot['Taxa_Subregistro'], color=colors)
    
    # Adicionar rótulos nas barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.1f}%', ha='center', va='bottom')
    
    ax.set_ylabel('Taxa de Subregistro (%)')
    ax.set_title('Taxa de Subregistro por Região')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # Mapa dos municípios do MA (simulado com gráfico de barras horizontal)
    if len(df_mun_filtrado) > 0:
        st.subheader(f"Distribuição do Subregistro nos Municípios do Maranhão - {ano_selecionado}")
        
        # Ordenar por taxa de subregistro
        df_plot = df_mun_filtrado.sort_values('Taxa_Subregistro', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        # Usar a função barh para barras horizontais
        bars = ax.barh(df_plot['Município'], df_plot['Taxa_Subregistro'], 
                     color=sns.color_palette("Reds_r", len(df_plot)))
        
        # Adicionar rótulos nas barras
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                    f'{width:.1f}%', ha='left', va='center')
        
        ax.set_xlabel('Taxa de Subregistro (%)')
        ax.set_title(f'Taxa de Subregistro por Município - {ano_selecionado}')
        plt.tight_layout()
        
        st.pyplot(fig)

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
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df_mun_detalhe['Ano'], df_mun_detalhe['Taxa_Subregistro'], 
                marker='o', linestyle='-', color='darkblue', linewidth=2)
        
        # Adicionar rótulos
        for x, y in zip(df_mun_detalhe['Ano'], df_mun_detalhe['Taxa_Subregistro']):
            ax.text(x, y + 0.2, f'{y:.1f}%', ha='center')
            
        ax.set_ylabel('Taxa de Subregistro (%)')
        ax.set_title(f'Evolução da Taxa de Subregistro em {municipio_detalhado}')
        ax.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # Comparação com média estadual
        st.subheader(f"Comparação com a Média Estadual")
        df_ma_historico = df_regioes[df_regioes['Região'] == 'Maranhão']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df_mun_detalhe['Ano'], df_mun_detalhe['Taxa_Subregistro'], 
                marker='o', linestyle='-', label=municipio_detalhado, color='darkblue')
        ax.plot(df_ma_historico['Ano'], df_ma_historico['Taxa_Subregistro'], 
                marker='s', linestyle='--', label='Média do Maranhão', color='darkred')
        
        ax.set_ylabel('Taxa de Subregistro (%)')
        ax.set_title(f'Comparação da Taxa de Subregistro: {municipio_detalhado} vs. Média Estadual')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        st.pyplot(fig)
        
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
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(top5['Município'], top5['Taxa_Subregistro'], 
                     color=sns.color_palette("Reds", len(top5)))
        
        # Adicionar rótulos nas barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        ax.set_ylabel('Taxa de Subregistro (%)')
        ax.set_title('Top 5 Municípios com Maior Taxa de Subregistro')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)

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
    if not df_serie_regioes.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Criar um mapa de cores para as regiões
        cores = {'Brasil': 'darkblue', 'Nordeste': 'darkgreen', 'Maranhão': 'darkred'}
        
        # Plotar cada região
        for regiao in regioes_selecionadas:
            df_plot = df_serie_regioes[df_serie_regioes['Região'] == regiao]
            ax.plot(df_plot['Ano'], df_plot['Taxa_Subregistro'], 
                    marker='o', linestyle='-', label=regiao, 
                    color=cores.get(regiao, 'gray'))
        
        ax.set_ylabel('Taxa de Subregistro (%)')
        ax.set_title('Evolução Histórica da Taxa de Subregistro')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        st.pyplot(fig)
    
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
        
        # Criar gráfico com dois eixos Y
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # Eixo primário - Taxa de subregistro
        line1 = ax1.plot(df_ma_historico['Ano'], df_ma_historico['Taxa_Subregistro'], 
                         marker='o', linestyle='-', color='darkred', label='Taxa de Subregistro (%)')
        ax1.set_xlabel('Ano')
        ax1.set_ylabel('Taxa de Subregistro (%)', color='darkred')
        ax1.tick_params(axis='y', labelcolor='darkred')
        
        # Eixo secundário - Unidades interligadas
        ax2 = ax1.twinx()
        line2 = ax2.plot(unidades_historico['Ano'], unidades_historico['Unidades_Interligadas'], 
                         marker='s', linestyle='-', color='darkblue', label='Nº de Unidades Interligadas')
        ax2.set_ylabel('Nº de Unidades Interligadas', color='darkblue')
        ax2.tick_params(axis='y', labelcolor='darkblue')
        
        # Adicionar legenda
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper center')
        
        ax1.set_title('Relação entre Unidades Interligadas e Taxa de Subregistro')
        ax1.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        st.pyplot(fig)
    
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
