import streamlit as st
import time
import pandas as pd
from joblib import load
from utils import Transformer 


#---------------------------------------------------------------------
#Criando as variáveis necessárias
#lê arquivo com vars categóricas necessárias ao preenchimento
lista_de_campos = load('joblib files/cat_options_a_preencher_2.joblib')

#lê os arquivos com o modelo e as features
model_simula_credito = load('joblib files/pipeline_modelo.joblib')

features_do_model = load('joblib files/features_a_preencher.joblib')

#por conta de algum erro na hora da Joblib salvar, os valores desse dict estavam sem as vírgulas
lista_de_campos['grau_escolaridade'] = ['Ensino superior', 'Ensino medio', 'Ensino superior incompleto',
                                        'Ensino fundamental', 'Pos graduacao']

#cria dicionário de respostas dos clientes
dicionario_de_respostas = dict()

#lista de sim/não para os selectbox's gerais
lista_sim_nao = ['sim', 'não']


def avaliar_tomador(dicionario_de_respostas):
    """Esta função inputa os dados fornecidos pelo cliente no modelo de crédito criado
        e define a aprovação do crédito
        1 é negado e 0 é aprovado
    """
    if dicionario_de_respostas['anos_desempregado'] > 0:
        dicionario_de_respostas['anos_empregado'] = (dicionario_de_respostas['anos_desempregado']*-1)

    dados_cliente = [dicionario_de_respostas[columns] for columns in features_do_model]

    df_dados_cliente = pd.DataFrame(data=[dados_cliente], columns=[features_do_model])

    avaliacao_cliente = model_simula_credito.predict(df_dados_cliente)[0] #para garantir que sempre virá a primeira predição

    return avaliacao_cliente

#configura o layout da página e o "About" do app
st.set_page_config(layout='wide', menu_items={'About':'Construído por Enzo Golfetti em 09/2021'}) #mudar ao final do projeto
#Cor de fundo do listbox
st.markdown('<style>div[role="listbox"] ul{background-color: #eee1f79e};</style>', unsafe_allow_html=True)
#display radio button horizontalmente
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

#------------------------------------------------------------------------
#Construindo a estrutura do Streamlit App

#Logo do banco fake
st.image('images/bytebank_logo.png')

#Título do site
st.title('Simulador de Avaliação de Crédito')

#Criando um CTA para o simulador
st.subheader("Simples, rápido e eficiente:")
st.subheader("Tudo que os tempos modernos exigem para você focar no que importa :)")

#Coletando nome para colocar na aprovação/reprovação
nome_do_cliente = st.text_input("Antes de começarmos, qual seu nome?", value='nome', key=875)
if nome_do_cliente != 'nome': 
    st.write('Bem vinde', nome_do_cliente)
    st.write('Não se preocupe, esse é um simulador, seu nome será apagado ao final da simulação, não armazenamos nenhum dado!')

#expander da categoria de trabalho
    expander_trabalho = st.expander('Primeiro, queremos saber um pouco mais sobre seu trabalho:')
    #Criando os campos de preenchimento no expander de trabalho
    with expander_trabalho:
        coluna_de_trabalho_1, coluna_de_trabalho_2 = st.columns(2) #variáveis das colunas da categoria de trabalho

        #cria chave de categoria de renda no dict de respostas para futuramente ser input para o modelo
        dicionario_de_respostas['categoria_de_renda'] = coluna_de_trabalho_1.selectbox('Preencha sua Categoria de Renda:', 
                                                                                    lista_de_campos['categoria_de_renda'])

        #cria chave de ocupação no dict de respostas de trabalho para futuramente ser input no modelo
        dicionario_de_respostas['ocupacao'] = coluna_de_trabalho_1.selectbox('Sua ocupação?', lista_de_campos['ocupacao'])

        #cria chave de rendimento anual no dict de respostas de trabalho para futuramente ser input para o modelo
        dicionario_de_respostas['rendimento_anual'] = ((coluna_de_trabalho_1.slider("Qual seu salário atual?", min_value=0, max_value=35000,
                                                                                step=500)) * 12) #para fazer a renda anual 
                                                                                                #seguindo como o model está acostumado
        
        #cria chave de anos empregado no dict de respostas de trabalho para futuramente ser input no modelo
        dicionario_de_respostas['anos_empregado'] = coluna_de_trabalho_2.slider("Há quanto tempo você está empregado?",
                                                                                         min_value=0, max_value=44, step=1)
        
        #cria chave de anos desempregado no dict de respostas de trabalho para futuramente ser input no modelo
        dicionario_de_respostas['anos_desempregado'] = coluna_de_trabalho_2.slider("Há quanto tempo você está desempregado?",
                                                                                         min_value=0, max_value=44, step=1)

        #cria chave de telefone de trabalho no dict de respostas de trabalho para futuramente ser input para o modelo
        dicionario_de_respostas['tem_telefone_trabalho'] = 1 if coluna_de_trabalho_2.radio("Você tem um telefone do trabalho?", 
                                                                                                    lista_sim_nao, index=1) == 'sim' else 0
    
#expander da categoria de infos pessoais
    #tentar fazer uma transição da categoria de trabalho para essa!
    expander_pessoal = st.expander('Agora, nos conte um pouco mais sobre você...')
    #Criando os campos de preenchimento no expander de trabalho
    with expander_pessoal:
        coluna_pessoal_1, coluna_pessoal_2 = st.columns(2)

        #cria chave de idade para o dict pessoal para ser input no modelo
        dicionario_de_respostas['idade'] = coluna_pessoal_1.number_input("Qual a sua idade?", min_value=21, max_value=69,
                                                                                step=1, key=569)
        
        #cria chave de grau de escolaridade para o dict pessoal para ser input no modelo
        dicionario_de_respostas['grau_escolaridade'] = coluna_pessoal_1.selectbox("E seu grau de escolaridade?", 
                                                                                            lista_de_campos['grau_escolaridade'])

        #cria chave de estado civil no dict pessoal para ser input no modelo
        dicionario_de_respostas['estado_civil'] = coluna_pessoal_1.selectbox("Seu estado civil:", 
                                                                                lista_de_campos['estado_civil'])

        #cria chave de tem carro no dict pessoal para ser input no modelo
        dicionario_de_respostas['tem_carro'] = 1 if coluna_pessoal_1.radio("Você tem carro?",
                                                                         lista_sim_nao) == 'sim' else 0
        
        #cria chave de casa própria no dict pessoal para ser input no modelo
        dicionario_de_respostas['tem_casa_propria'] = 1 if coluna_pessoal_2.radio("Você tem casa própria?", 
                                                                                    lista_sim_nao) == 'sim' else 0

        #cria chave de moradia no dict pessoal para ser input no modelo
        dicionario_de_respostas['moradia'] = coluna_pessoal_2.selectbox("Selecione sua moradia:",
                                                                         lista_de_campos['moradia'])

        #cria chave de telefone fixo no dict pessoal para ser input no modelo
        dicionario_de_respostas['tem_telefone_fixo'] = 1 if coluna_pessoal_2.radio("Você tem um telefone fixo?", 
                                                                                        lista_sim_nao) == 'sim' else 0
        
        #cria chave de e-mail no dict pessoal para ser input no modelo
        dicionario_de_respostas['tem_email'] = 1 if coluna_pessoal_2.radio("Você tem e-mail?", 
                                                                                        lista_sim_nao) == 'sim' else 0
    
    expander_familia = st.expander('Por fim, você pode nos contar um pouco sobre sua família?')

    with expander_familia:
        coluna_familia1, coluna_familia2 = st.columns(2)
        
        #cria chave de tamanho da família para ser input no modelo
        bool_sozinho = st.radio('Você mora sozinho?', lista_sim_nao, key=3654, index=0)
        if bool_sozinho == 'sim':
            dicionario_de_respostas['tamanho_familia'] = 1
        else:    
            dicionario_de_respostas['tamanho_familia'] = (st.number_input("Com quantas pessoas você mora?", min_value=1,
                                                                            max_value=8, key=7851)) + 1
        
        #cria chave de qtd de filhos para ser input no modelo
        bool_filhos = st.radio('Você tem filhos?', lista_sim_nao, key=3654, index=1) #por comodidade para o cliente, pergunta se tem filhos

        if bool_filhos == 'sim':
            dicionario_de_respostas['qtd_filhos'] = st.number_input("você tem filhos?", min_value=1,
                                                                            max_value=7, key=6921310)
        else:
            dicionario_de_respostas['qtd_filhos'] = 0
    
    #pede confirmação para os dados serem usados na simulação de crédito e faz alerta sobre data security
    confirmacao_simulacao = st.checkbox("""Ao selecionar essa caixa, você concorda em ter essas informações utilizadas 
                                        para uma SIMULAÇÃO de crédito feita por um estudante de Data Science e que nenhum dado 
                                        aqui será armazenado e essa simulação não tem validade prática nem interfere em sua 
                                        capacidade de tomar crédito.""")
    botao_iniciar_simulacao = st.button("Avaliar Crédito")
    if confirmacao_simulacao:
    #se o cliente concordar com as condições autoriza ele a fazer a avaliação   
        if botao_iniciar_simulacao:
            st.write("Muito obrigado por sua contribuição para esse projeto!")
            time.sleep(2)
            st.write("Análise de crédito em andamento...")
            progress_bar = st.progress(0) #cria barra de progresso
            mostra_avaliacao = st.empty() #guarda slot para inputar resultado da análise de crédito

            for i in range(100): #preenche a barra de progresso
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            if avaliar_tomador(dicionario_de_respostas): #avalia o cliente no modelo
                mostra_avaliacao.error("""Infelizmente você não foi aprovado no simulador de crédito :-1:""")
                #negado
            else:
                mostra_avaliacao.success("""Parabéns!!! Você conseguiu crédito em nosso simulador!!! :+1:""")
                st.balloons()
                #aprovado




     






