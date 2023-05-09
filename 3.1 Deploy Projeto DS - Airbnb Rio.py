#!/usr/bin/env python
# coding: utf-8

# # Context
# Após ter feito o deploy do melhor modelo em 3. Projeto DS - Airbnb Rio, iniciamos neste notebook o passo 3 do passo-a-passo do deploy de um projeto,

# # Deploy do projeto
# 
# * Passo 1 -> Criar arquivo do Modelo (joblib)
# * Passo 2 -> Escolher a forma do deploy
# 
#     - Arquivo executável + Tkinter
#     - Deploy em um Microsite (Flask)
#     - Deploy apenas para uso direto (Streamlit)
# 
# * Passo 3 -> Outro arquivo Python (jupyter ou PyCharm) <font color= 'green'> > Estamos aqui!</font>
# * Passo 4 -> Importar streamlit e criar código
# * Passo 5 -> Atribuir ao botã

# # Import de bibliotecas

# In[1]:


import pandas as pd
import streamlit as st
import joblib


# # Separando os tipos das variáveis

# In[2]:


x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'ano': 0, 'mes': 0, 'n_amenities': 0, 'host_listings_count': 0}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancelation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
            }


# In[12]:


dicionario = {}
dic_list = []
for key, item in x_listas.items():
    for value in item:
        dic_list.append(str(key)+'_'+str(value))
        dicionario[f'{key}_{value}'] = 0


# In[15]:


for item in x_numericos:
    if item == 'latitude' or item == 'longitude':
        valor = st.number_input(f'{item}', step=0.00001, value=0.0, format="%.5f")
    elif item == 'extra_people':
        valor = st.number_input(f'{item}', step=0.01, value=0.0)
    else:
        valor = st.number_input(f'{item}', step=1, value=0)
    x_numericos[item] = valor

for item in x_tf:
    valor = st.selectbox(f'{item}', ('Sim', 'Não'))
    if valor == "Sim":
        x_tf[item] = 1
    else:
        x_tf[item] = 0
    
    
for item in x_listas:
    valor = st.selectbox(f'{item}', x_listas[item])
    dicionario[f'{item}_{valor}'] = 1
    
botao = st.button('Prever Valor do Imóvel')

if botao:
    dicionario.update(x_numericos)
    dicionario.update(x_tf)
    valores_x = pd.DataFrame(dicionario, index=[0])
    modelo = joblib.load( r'../../PYTHON/HASHTAG/data/m_extra_trees.joblib')
    preco = modelo.predict(valores_x)
    st.write(preco[0])


# In[ ]:




