#!/usr/bin/env python
# coding: utf-8

# # pandas e csv
# 
# ## Resumo
# 
# Quase sempre quando formos "ler" um arquivo csv, vamos usar o pandas. É prático e bem eficiente.
# 
# ## Funcionamento

# In[1]:


import pandas as pd

Forma mais básica: (muitas vezes não usaremos a forma mais básica)
dataframe = pd.read_csv(arquivo_com_extensao)
# - Vamos ler um arquivo real, com a Base de Dados de Vendas da Empresa "Contoso"

# In[2]:


path = r'C:\Users\Caroline\OneDrive\Documentos\Meus estudos\PYTHON\HASHTAG\data'


# In[3]:


vendas_df = pd.read_csv(path+'\Contoso - Vendas - 2017.csv', sep=';')

vendas_df


# # Comparando, Tratando e Mesclando DataFrames
# 
# ## Objetivo
# 
# Vamos modificar os IDs para os nomes dos produtos, dos clientes e das lojas, para nossas análises ficarem mais intuitivas futuramente. Para isso, vamos criar um data frame com todos os detalhes.
# 
# - Usaremos o método merge para isso e, depois se quisermos, podemos pegar apenas as colunas que queremos do dataframe final.

# ### Criando nossos dataframes

# In[4]:


import pandas as pd

#às vezes precisaremos mudar o encoding. Possiveis valores para testar:
#encoding='latin1', encoding='ISO-8859-1', encoding='utf-8' ou então encoding='cp1252'
produtos_df = pd.read_csv(path+'\Contoso - Cadastro Produtos.csv', sep=';')
lojas_df = pd.read_csv(path+'\Contoso - Lojas.csv', sep=';')
clientes_df = pd.read_csv(path+'\Contoso - Clientes.csv', sep=';')


# In[5]:


#usaremos o display para ver todos os dataframes
#display(vendas_df)
display(produtos_df)
display(lojas_df)
display(clientes_df)


# ### Vamos tirar as colunas inúteis do clientes_df ou pegar apenas as colunas que quisermos
.drop([coluna1, coluna2, coluna3]) -> retira as colunas: coluna1, coluna2, coluna3
# In[6]:


clientes_df = clientes_df[['ID Cliente', 'E-mail']]
produtos_df_ajus = produtos_df[['ID Produto', 'Nome do Produto']]
lojas_df = lojas_df[['ID Loja', 'Nome da Loja']]
display(produtos_df)


# ### Agora vamos juntar os dataframes para ter 1 único dataframe com tudo "bonito"
novo_dataframe = dataframe1.merge(dataframe2, on='coluna')dataframe.rename({'coluna1': 'novo_coluna_1'})
# In[7]:


#juntando os dataframes

# default do merge é inner

vendas_df = vendas_df.merge(produtos_df_ajus, on='ID Produto')
vendas_df = vendas_df.merge(lojas_df, on='ID Loja')
vendas_df = vendas_df.merge(clientes_df, on='ID Cliente')


# In[8]:


#exibindo o dataframe final
display(vendas_df)


# In[9]:


#vamos renomear o e-mail para ficar claro que é do cliente
vendas_df = vendas_df.rename(columns={'E-mail': 'E-mail do Cliente'})
display(vendas_df)


# # Resumos e um pouco de Visualização no pandas
# 
# 
# ## Resumo
# 
# Vamos ver alguns métodos para analisar nossas tabelas (dataframes)
# 
# Além disso, vamos usar os plot de gráfico padrões do pandas, mas no projeto de DataScience veremos outras mais bonitas e também muito práticas.
# 
# OBS: O pandas usa o matplotlib (que vimos na seção de "módulos e bibliotecas") para plotar gráficos.<br>
# Se quiser personalizar mais do que o padrão do pandas, importe o matplotlib e use os métodos do matplotlib

# ### Qual cliente que comprou mais vezes?
# 
# - Usaremos o método .value_counts() para contar quantas vezes cada valor do Dataframe aparece
# - Usaremos o método .plot() para exibir um gráfico

# In[10]:


clientes_mais = vendas_df['E-mail do Cliente'].value_counts()


# In[11]:


clientes_mais[:5].plot(figsize = (14,3))


# ### Qual a Loja que mais vendeu?
# 
# - Usaremos o .groupby para agrupar o nosso dataframe, de acordo com o que queremos (somando as quantidades de vendas, por exemplo)

# In[12]:


loja_mais = vendas_df[['Nome da Loja', 'Quantidade Vendida']].groupby(['Nome da Loja']).sum()


# In[13]:


loja_mais


# - Agora precisamos pegar o maior valor. Temos 2 formas:
#     1. Ordenar o dataframe em ordem decrescente de Quantidade Vendida
#         - Método .sort_values
#     2. Pegar o Maior valor diretamente
#         - Métodos .max() e .idxmax()

# In[14]:


loja_mais.sort_values(by = 'Quantidade Vendida', ascending= False)[:1]


# In[15]:


loja_mais.max()


# In[16]:


loja_mais.idxmax()


# ### Qual produto que menos vendeu?
# 
# - Já temos uma lista criada para isso, basta verificarmos o final da lista (já que ela está ordenada) ou então usarmos os métodos:
#     1. min()
#     2. idxmin()

# In[17]:


print(loja_mais.min(), loja_mais.idxmin(), sep = "\n")


# ### Primeiro, vamos aplicar uma função normalmente. Qual o % das vendas que foi devolvido?
# 
# - Para isso vamos somar as quantidades nas colunas correspondentes. Lembrando, o % vai ser: Total Devolvido / Total Vendido.

# In[18]:


vendas_df.columns


# In[19]:


perc_devol = sum(vendas_df['Quantidade Devolvida'])/sum(vendas_df['Quantidade Vendida'])
print('Total devolvido {:.2%}'.format(perc_devol))


# ### Agora, se quisermos fazer a mesma análise apenas para 1 loja. Queremos filtrar apenas os itens da Loja Contoso Europe Online e saber o % de devolução dessa loja.
# 
# - Para isso, vamos precisar filtrar. A forma de filtrar nos dataframes é uma "simples" comparação

# In[20]:


perc_devol_espic = sum(vendas_df[vendas_df['Nome da Loja'] == 'Loja Contoso Europe Online ']['Quantidade Devolvida'])/sum(vendas_df[vendas_df['Nome da Loja'] == 'Loja Contoso Europe Online ']['Quantidade Vendida'])
print('Total devolvido {:.1%}'.format(perc_devol_espic))


# ### Desafio: e se eu quisesse criar uma tabela apenas com as vendas da Loja Contoso Europe Online e que não tiveram nenhuma devolução. Quero criar essa tabela e saber quantas vendas são.
# 
# - Repare que nesse caso são 2 condições, como fazemos isso?

# In[21]:


vendas_df[(vendas_df['Nome da Loja'] == 'Loja Contoso Europe Online ') & (vendas_df['Quantidade Devolvida'] == 0)].head()


# # Adicionando Colunas, Modificando Colunas e Valores

# ### Agora, e se quisermos acrescentar uma coluna com o mês, o dia e o ano de cada venda (e não só a data completa)

# In[22]:


vendas_df['Data da Venda']


# #### pd.to_datetime()

# In[23]:


vendas_df['Data da Venda'] = pd.to_datetime(vendas_df['Data da Venda'], format= '%d/%m/%Y')


# #### extracting dates from datetime

# In[24]:


vendas_df['ano_venda'] = vendas_df['Data da Venda'].dt.year
vendas_df['mes_venda' ] = vendas_df['Data da Venda'].dt.month
vendas_df['dia_venda'] = vendas_df['Data da Venda'].dt.day


# In[25]:


vendas_df.head()


# ### E agora, caso a gente queira modificar 1 valor específico, como fazemos? Vamos importar novamente a base de produtos

# In[26]:


novo_produtos_df = pd.read_csv(path+'\Contoso - Cadastro Produtos.csv', sep=';')


# In[27]:


novo_produtos_df = novo_produtos_df.set_index('Nome do Produto')
display(novo_produtos_df.head())


# ### Antes de entrar no próximo exemplo, precisamos falar de 2 métodos:
#     1. loc - permite pegar uma linha de acordo com o índice dela. Ele dá erro caso não encontre o índice. Isso é interessante principalmente quando o índice é uma informação relevante ao invés só do número do índice ou quando queremos pegar alguma linha específica do dataframe (ao invés de ir do início do dataframe até a linha 5, por exemplo).
#         Também podemos usar como loc[índice_linha, índice_coluna] para acessar um valor específico e modificá-lo.
#     2. iloc - enxerga o dataframe como linhas e colunas e consegue pegar o valor com um número de linha e um número de coluna. Repara que ele não analisa o valor do índice da linha e da coluna, apenas a posição importa.
#         Uso: iloc[num_linha, num_coluna]
#         
# - Vendo na prática

# In[28]:


#vamos pegar o preço produto Contoso Optical Wheel OEM PS/2 Mouse E60 Black
#por loc
novo_produtos_df.loc['Contoso Optical Wheel OEM PS/2 Mouse E60 Black', 'Preco Unitario']

# o index é nome do produto


# In[29]:


#por iloc
novo_produtos_df.iloc[2, 5]

# use numeros


# ### A empresa decidiu aumentar o preço do produto ID 873 (Contoso Wireless Laser Mouse E50 Grey) para 23 reais. Como fazemos, para modificar isso na nossa base?

# In[30]:


novo_produtos_df.loc['Contoso Wireless Laser Mouse E50 Grey','Preco Unitario']


# In[31]:


novo_produtos_df.loc['Contoso Wireless Laser Mouse E50 Grey','Preco Unitario'] = '23,00'


# In[32]:


novo_produtos_df.loc['Contoso Wireless Laser Mouse E50 Grey','Preco Unitario']


# In[33]:


# se tivesse que usar o .iloc

#descobrimos qual eh o index da linha
produtos_df[produtos_df['Nome do Produto'] == 'Contoso Optical Wheel OEM PS/2 Mouse E60 Black'].index


# In[34]:


# sabendo qual eh o index da coluna produto
# se quisermos modificar o produto 'Contoso Optical Wheel OEM PS/2 Mouse E60 Black' para 69

# original
produtos_df.iloc[2]


# In[ ]:





# In[35]:


produtos_df.head()


# In[36]:


produtos_df.iloc[2, 5] 


# In[37]:


# atualizado
produtos_df.iloc[2, 5] = 69


# In[38]:


produtos_df.iloc[2]


# # Exportando do DataFrame para um csv
# 
# ### Depois de modificar um DataFrame, ou até criar um, muitas vezes podemos exportar esse dataframe para um csv
# 
# No pandas, isso é bem simples:
# 
# dataframe.to_csv('nome_do_arquivo.csv', sep=',')

# ### Criando um dicionário, transformando o dicionário em um DataFrame e Exportando para csv

# In[39]:


vendas_produtos = {'iphone': [558147, 951642], 'galaxy': [712350, 244295], 'ipad': [573823, 26964], 'tv': [405252, 787604], 'máquina de café': [718654, 867660], 'kindle': [531580, 78830], 'geladeira': [973139, 710331], 'adega': [892292, 646016], 'notebook dell': [422760, 694913], 'notebook hp': [154753, 539704], 'notebook asus': [887061, 324831], 'microsoft surface': [438508, 667179], 'webcam': [237467, 295633], 'caixa de som': [489705, 725316], 'microfone': [328311, 644622], 'câmera canon': [591120, 994303]}


# In[40]:


vendas_produtos_df = pd.DataFrame.from_dict(vendas_produtos, orient='index')
display(vendas_produtos_df)


# In[41]:


vendas_produtos_df = vendas_produtos_df.rename(columns={0: 'Vendas 2019', 1: 'Vendas 2020'})
display(vendas_produtos_df)


# In[ ]:


vendas_produtos_df.to_csv(r'Novo Vendas Produtos.csv', sep=',', encoding='latin1')

