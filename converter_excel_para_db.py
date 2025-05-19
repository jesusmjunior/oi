import pandas as pd
import sqlite3
import os
import json

def converter_excel_para_sqlite():
    """
    Converte os arquivos Excel IBGE para um banco de dados SQLite.
    Também exporta os dados para JSON para consumo direto no frontend.
    """
    print("Iniciando conversão dos arquivos Excel para SQLite e JSON...")
    
    # Verificar se os arquivos existem
    if not os.path.exists("IBGE_Subregistro_Posicao_Municipios.xls"):
        print("Erro: Arquivo IBGE_Subregistro_Posicao_Municipios.xls não encontrado.")
        return False
        
    if not os.path.exists("IBGE_Subregistro_Posicao_BR_NE.xls"):
        print("Erro: Arquivo IBGE_Subregistro_Posicao_BR_NE.xls não encontrado.")
        return False
    
    # Carregar os dados dos arquivos Excel
    try:
        print("Lendo arquivo de municípios...")
        df_municipios = pd.read_excel("IBGE_Subregistro_Posicao_Municipios.xls")
        
        print("Lendo arquivo de regiões...")
        df_regioes = pd.read_excel("IBGE_Subregistro_Posicao_BR_NE.xls")
        
        # Processar e limpar dados se necessário
        print("Processando dados...")
        
        # Verificar se a coluna de taxa de subregistro existe ou calculá-la
        if 'Taxa_Subregistro' not in df_municipios.columns:
            # Identificar colunas de nascidos vivos e registros
            colunas_municipios = df_municipios.columns
            col_nascidos_municipios = [col for col in colunas_municipios if 'nasc' in col.lower() or 'vivo' in col.lower()]
            col_registros_municipios = [col for col in colunas_municipios if 'regis' in col.lower() or 'civil' in col.lower()]
            
            if col_nascidos_municipios and col_registros_municipios:
                print(f"Calculando taxa de subregistro para municípios usando colunas {col_nascidos_municipios[0]} e {col_registros_municipios[0]}...")
                df_municipios['Taxa_Subregistro'] = 100 * (1 - df_municipios[col_registros_municipios[0]] / df_municipios[col_nascidos_municipios[0]])
        
        if 'Taxa_Subregistro' not in df_regioes.columns:
            # Identificar colunas de nascidos vivos e registros
            colunas_regioes = df_regioes.columns
            col_nascidos_regioes = [col for col in colunas_regioes if 'nasc' in col.lower() or 'vivo' in col.lower()]
            col_registros_regioes = [col for col in colunas_regioes if 'regis' in col.lower() or 'civil' in col.lower()]
            
            if col_nascidos_regioes and col_registros_regioes:
                print(f"Calculando taxa de subregistro para regiões usando colunas {col_nascidos_regioes[0]} e {col_registros_regioes[0]}...")
                df_regioes['Taxa_Subregistro'] = 100 * (1 - df_regioes[col_registros_regioes[0]] / df_regioes[col_nascidos_regioes[0]])
        
        # Criar banco de dados SQLite
        print("Criando banco de dados SQLite...")
        conn = sqlite3.connect("subregistro_data.db")
        
        # Salvar dados no SQLite
        df_municipios.to_sql("municipios", conn, if_exists="replace", index=False)
        df_regioes.to_sql("regioes", conn, if_exists="replace", index=False)
        
        # Fechar conexão
        conn.close()
        
        # Exportar para JSON para uso direto no frontend
        print("Exportando dados para JSON...")
        
        # Converter para JSON com tratamento de NaN
        municipios_json = df_municipios.to_json(orient="records", date_format="iso")
        regioes_json = df_regioes.to_json(orient="records", date_format="iso")
        
        # Salvar arquivos JSON
        with open("data/municipios.json", "w", encoding="utf-8") as f:
            f.write(municipios_json)
            
        with open("data/regioes.json", "w", encoding="utf-8") as f:
            f.write(regioes_json)
        
        # Criar arquivo de metadados para uso no frontend
        metadados = {
            "colunas_municipios": df_municipios.columns.tolist(),
            "colunas_regioes": df_regioes.columns.tolist(),
            "anos_disponiveis": sorted(df_municipios["Ano"].unique().tolist() if "Ano" in df_municipios.columns else []),
            "municipios_disponiveis": sorted(df_municipios["Município"].unique().tolist() if "Município" in df_municipios.columns else []),
            "regioes_disponiveis": sorted(df_regioes["Região"].unique().tolist() if "Região" in df_regioes.columns else []),
            "data_atualizacao": pd.Timestamp.now().isoformat()
        }
        
        with open("data/metadados.json", "w", encoding="utf-8") as f:
            json.dump(metadados, f, ensure_ascii=False, indent=2)
        
        print("Conversão concluída com sucesso!")
        print(f"Banco de dados SQLite criado: subregistro_data.db")
        print(f"Arquivos JSON criados na pasta data/")
        
        # Mostrar algumas estatísticas
        print("\nEstatísticas dos dados:")
        print(f"Municípios: {len(df_municipios)} registros")
        print(f"Regiões: {len(df_regioes)} registros")
        
        return True
    
    except Exception as e:
        print(f"Erro durante a conversão: {e}")
        return False

if __name__ == "__main__":
    # Garantir que a pasta data/ exista
    if not os.path.exists("data"):
        os.makedirs("data")
        
    # Executar a conversão
    converter_excel_para_sqlite()
