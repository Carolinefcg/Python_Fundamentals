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
               'minimum_nights': 0, 'ano': 0, 'mes': 0, 'nr_amenities': 0, 'host_listings_count': 0}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Other', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period'],
            'bed_type': ['Others', 'Real Bed']}


# In[3]:


dicionario = {}
dic_list = []
for key, item in x_listas.items():
    for value in item:
        dic_list.append(str(key)+'_'+str(value))
        dicionario[f'{key}_{value}'] = 0


# In[4]:


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


# In[5]:


ordem_colunas = ['host_is_superhost',
 'host_listings_count',
 'latitude',
 'longitude',
 'accommodates',
 'bathrooms',
 'bedrooms',
 'beds',
 #'price',
 'extra_people',
 'minimum_nights',
 'instant_bookable',
 'ano',
 'mes',
 'nr_amenities',
 'property_type_Apartment',
 'property_type_Bed and breakfast',
 'property_type_Condominium',
 'property_type_Guest suite',
 'property_type_Guesthouse',
 'property_type_Hostel',
 'property_type_House',
 'property_type_Loft',
 'property_type_Other',
 'property_type_Serviced apartment',
 'room_type_Entire home/apt',
 'room_type_Hotel room',
 'room_type_Private room',
 'room_type_Shared room',
 'bed_type_Others',
 'bed_type_Real Bed',
 'cancellation_policy_flexible',
 'cancellation_policy_moderate',
 'cancellation_policy_strict',
 'cancellation_policy_strict_14_with_grace_period']


# In[4]:


botao = st.button('Prever Valor do Imóvel')

if botao:
    dicionario.update(x_numericos)
    dicionario.update(x_tf)
    valores_x = pd.DataFrame(dicionario, index=[0])
    # ordenando conforme os dados de model.fit
    valores_x = valores_x[ordem_colunas]
    modelo = joblib.load( r'../../PYTHON/HASHTAG/data/m_extra_trees_v2.joblib')
    preco = modelo.predict(valores_x)
    st.write(preco[0])


# In[ ]:




