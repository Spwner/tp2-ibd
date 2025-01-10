import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


# Importando os dados
# Carregar os arquivos de uma vez
dados_candidatos_partes = [
    pd.read_csv(f'consulta_cand_2024_BRASIL.csv.part{i}', delimiter=';', encoding='latin1') 
    for i in range(1, 25)
]

# Concatenar os arquivos
dados_candidatos = pd.concat(dados_candidatos_partes, ignore_index=True)

# Para dados de bens
dados_bens_partes = [
    pd.read_csv(f'bem_candidato_2024_BRASIL.csv.part{i}', delimiter=';', encoding='latin1')
    for i in range(1, 25)
]

# Concatenar os arquivos
dados_bens = pd.concat(dados_bens_partes, ignore_index=True)

# Para dados de redes sociais
dados_redes_partes = [
    pd.read_csv(f'rede_social_candidato_BRASIL.csv.part{i}', delimiter=';', encoding='latin1')
    for i in range(1, 9)
]

# Concatenar os arquivos
dados_redes = pd.concat(dados_redes_partes, ignore_index=True)

#dados_candidatos = pd.read_csv('consulta_cand_2024_BRASIL.csv', delimiter=';', encoding='latin1')
#dados_bens = pd.read_csv('bem_candidato_2024_BRASIL.csv', delimiter=';', encoding='latin1')
#dados_redes = pd.read_csv('rede_social_candidato_2024_BRASIL.csv', delimiter=';', encoding='latin1')


def exibir_tabelas(base_escolhida):
    """Exibe e permite filtrar as tabelas candidatos, bens e rede sociais."""
    if base_escolhida == 'Candidatos':
        dataframe = dados_candidatos.copy()
        filtros_disponiveis = ['Município', 'Estado', 'Cargo','Partido','Raça/Cor', 'Gênero']
    elif base_escolhida == 'Bens':
        dataframe = dados_bens.copy()
        filtros_disponiveis = ['Município', 'Estado', 'Tipo do Bem']  
    elif base_escolhida == 'Redes Sociais':
        dataframe = dados_redes.copy()
        filtros_disponiveis = ['Estado']  

    # Filtros disponíveis
    filtro_opcoes = st.multiselect(
        'Escolha os filtros que deseja aplicar:',
        filtros_disponiveis
    )

    if 'Município' in filtro_opcoes:
        municipios = dataframe['NM_UE'].dropna().unique()
        municipio_selecionado = st.selectbox('Selecione o município:', sorted(municipios))
        dataframe = dataframe[dataframe['NM_UE'] == municipio_selecionado]

    if 'Estado' in filtro_opcoes:
        estados = dataframe['SG_UF'].dropna().unique()
        estado_selecionado = st.selectbox('Selecione o estado:', sorted(estados))
        dataframe = dataframe[dataframe['SG_UF'] == estado_selecionado]

    if 'Cargo' in filtro_opcoes:
        cargos = dataframe['DS_CARGO'].dropna().unique()
        cargo_selecionado = st.selectbox('Selecione o cargo:', sorted(cargos))
        dataframe = dataframe[dataframe['DS_CARGO'] == cargo_selecionado]

    if 'Situação da Candidatura' in filtro_opcoes:
        situacao = dataframe['DS_SITUACAO_CANDIDATURA'].dropna().unique()
        situacao_selecionado = st.selectbox('Selecione a situação:', sorted(situacao))
        dataframe = dataframe[dataframe['DS_SITUACAO_CANDIDATURA'] == situacao_selecionado]

    if 'Partido' in filtro_opcoes:
        partido = dataframe['SG_PARTIDO'].dropna().unique()
        partido_selecionado = st.selectbox('Selecione o Partido:', sorted(partido))
        dataframe = dataframe[dataframe['SG_PARTIDO'] == partido_selecionado]

    if 'Raça/Cor' in filtro_opcoes:
        etnia = dataframe['DS_COR_RACA'].dropna().unique()
        etnia_selecionado = st.selectbox('Selecione a Cor/Raça:', sorted(etnia))
        dataframe = dataframe[dataframe['DS_COR_RACA'] == etnia_selecionado]

    if 'Gênero' in filtro_opcoes:
        genero = dataframe['DS_GENERO'].dropna().unique()
        genero_selecionado = st.selectbox('Selecione o Gênero', sorted(genero))
        dataframe = dataframe[dataframe['DS_GENERO'] == genero_selecionado]

    if 'Tipo do Bem' in filtro_opcoes:
        bem = dataframe['DS_TIPO_BEM_CANDIDATO'].dropna().unique()
        bem_selecionado = st.selectbox('Selecione o Tipo de Bem', sorted(bem))
        dataframe = dataframe[dataframe['DS_TIPO_BEM_CANDIDATO'] == bem_selecionado]



    # Opção para remover colunas
    colunas_remover = st.multiselect(
        'Escolha as colunas que deseja remover:',
        dataframe.columns
    )
    dataframe = dataframe.drop(columns=colunas_remover)

    # Mostrar tabela com slider para quantidade de linhas
    qtd_linhas = st.slider(
        'Quantidade de linhas para exibir:',
        min_value=1, max_value=len(dataframe), value=min(10, len(dataframe))
    )
    st.write(dataframe.head(qtd_linhas))

    # Botão para download
    csv = dataframe.to_csv(index=False)
    st.download_button(
        label="Baixar tabela filtrada como CSV",
        data=csv,
        file_name=f'{base_escolhida.lower()}_filtrada.csv',
        mime='text/csv'
    )

def grafico_candidatos(filtro_tipo, filtro_valor):

    """Gera um gráfico com a quantidade de candidatos por Estado, Raça/Cor ou Partido."""
    # Agrupamento baseado no filtro escolhido
    if filtro_tipo == 'Estados':
        dataframe = dados_candidatos.groupby('SG_UF')['SQ_CANDIDATO'].nunique().reset_index()
        eixo_x = 'SG_UF'
        titulo = f'Candidatos por Estado - {filtro_valor}'
        max_slider = 27  # Limite máximo para Estados
        usar_slider = True
    elif filtro_tipo == 'Raça/Cor':
        dataframe = dados_candidatos.groupby('DS_COR_RACA')['SQ_CANDIDATO'].nunique().reset_index()
        eixo_x = 'DS_COR_RACA'
        titulo = f'Candidatos por Raça/Cor - {filtro_valor}'
        usar_slider = False
    elif filtro_tipo == 'Partido':
        dataframe = dados_candidatos.groupby('NM_PARTIDO')['SQ_CANDIDATO'].nunique().reset_index()
        eixo_x = 'NM_PARTIDO'
        titulo = f'Candidatos por Partido - {filtro_valor}'
        max_slider = 35
        usar_slider = True
    else:
        st.error("Filtro inválido. Escolha entre 'Estados', 'Raça/Cor' ou 'Partido'.")
        return

    # Renomear a coluna para facilitar a manipulação
    dataframe = dataframe.rename(columns={'SQ_CANDIDATO': 'quantidade'})
    
    # Ordenar os dados pelo número de candidatos
    dataframe = dataframe.sort_values(by='quantidade', ascending=False)
    
    # Aplicar o slider apenas quando necessário
    if usar_slider:
        num_candidatos = st.slider(
            'Selecione o número de colunas para o gráfico', 
            min_value=10, 
            max_value=max_slider, 
            step=1
        )
        dataframe = dataframe.head(num_candidatos)

    # Gerar o gráfico
    plt.figure(figsize=(12, 6))
    sns.barplot(data=dataframe, x=eixo_x, y='quantidade', palette='RdBu')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel(filtro_tipo)
    plt.ylabel('Quantidade de Candidatos')
    plt.title(titulo)
    plt.tight_layout()

    # Renderizar no Streamlit
    st.pyplot(plt)


    """Gera um gráfico comparando os gêneros dos candidatos por estado."""
    # Filtrar e organizar os dados
    dataframe = dados_candidatos.groupby(['SG_UF', 'DS_GENERO'])['SQ_CANDIDATO'].nunique().reset_index()
    dataframe = dataframe.rename(columns={'SQ_CANDIDATO': 'quantidade'})

    # Criar um gráfico de barras agrupadas
    plt.figure(figsize=(14, 7))
    sns.barplot(
        data=dataframe, 
        x='SG_UF', 
        y='quantidade', 
        hue='DS_GENERO', 
        palette='Set2'
    )
    
    # Configuração do gráfico
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Estados')
    plt.ylabel('Quantidade de Candidatos')
    plt.title('Comparação de Gêneros dos Candidatos por Estado')
    plt.legend(title='Gênero')
    plt.tight_layout()

    # Renderizar no Streamlit
    st.pyplot(plt)

def gerar_grafico_pizza(dados, estado=None, municipio= None):
    """
    Gera um gráfico de pizza baseado na coluna de generos, com filtros opcionais para municipio e estado.
    """
    # Filtrando por estado
    if estado:
        dados = dados[dados['SG_UF'] == estado]

    #Filtrando por municipio
    if municipio:
        dados = dados[dados['NM_UE'] == municipio]

    # Verificando se há dados após os filtros
    if dados.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    # Contagem por genero
    modalidade_counts = dados['DS_GENERO'].value_counts()

    # Gerar o gráfico
    fig, ax = plt.subplots(figsize=(3, 4))
    ax.pie(
        modalidade_counts.values,
        labels=modalidade_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Paired.colors
    )
    ax.set_title("Distribuição de Candidatos por Genero")
    st.pyplot(fig)
# Título da página
st.title('Trabalho Pratico: Introducação a Banco de Dados - Candidatos-2024 ')
st.write('PLACEHOLDER.')



# Permitir exibição das tabelas, independente do tipo de análise
st.sidebar.subheader("Exibir tabelas")
base_tabelas = st.sidebar.radio(
    'Escolha a base de dados para exibir:',
    ['Candidatos', 'Bens', 'Redes Sociais']
)
if st.sidebar.checkbox('Mostrar tabela com filtros'):
    exibir_tabelas(base_tabelas)


# Escolha do tipo de análise
tipo_analise = st.sidebar.radio('Escolha o tipo de análise:', ['Candidatos'])

if tipo_analise == 'Candidatos':
    # Filtro para candidatos
    filtro_tipo = st.sidebar.radio('Filtrar por:', ['Estados', 'Raça/Cor', 'Partido'])
    filtro_valor = 'Brasil'  # Para indicar uma visão geral nacional

    if st.sidebar.checkbox('Mostrar gráfico de candidatos'):
        grafico_candidatos(filtro_tipo, filtro_valor)
    st.sidebar.header('Análise da distribuição de generos')

    if st.sidebar.checkbox('Mostrar gráfico de generos'):
        municipio = st.sidebar.selectbox(
            'Selecione o municipio:', 
            options=['Todas'] + list(dados_candidatos['NM_UE'].dropna().unique())
        )
        estado = st.sidebar.selectbox(
            'Selecione o estado:', 
            options=['Todos'] + list(dados_candidatos['SG_UF'].dropna().unique())
        )

        municipio_selecionado = None if municipio == 'Todas' else municipio
        estado_selecionado = None if estado == 'Todos' else estado

        # Gerar o gráfico de pizza para a base "Candidatos"
        gerar_grafico_pizza(dados_candidatos, municipio=municipio_selecionado, estado=estado_selecionado)


    

