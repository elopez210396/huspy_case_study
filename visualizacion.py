import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px

st.set_page_config(page_title="Case Study Huspy", page_icon='icono.jpeg',layout="wide",initial_sidebar_state='collapsed')

st.image('Logo.png', width=200)

@st.cache_data
def leer_datos():
    propiedades = pd.read_excel("Huspy Case.xlsx", sheet_name='Props')
    estadisticas = pd.read_excel("Huspy Case.xlsx", sheet_name='Estadisticas')
    clientes = pd.read_excel("Huspy Case.xlsx", sheet_name='Clientes', header=1)

    propiedades = propiedades[['Nombre de la calle','Planta','Zona','Localidad','Venta o Alquiler',
             'Precio','Codigo de la propiedad','Tipo','Dorm','Baños','m²','Fecha alta']]
    propiedades.drop_duplicates(subset='Codigo de la propiedad', keep='first', inplace=True)
    propiedades['Venta o Alquiler'].replace({'Enta':'Venta'}, inplace=True)
    propiedades['Precio'] = propiedades['Precio'].astype(str).str.replace(r'\.', '', regex=True)  # Elimina los puntos
    propiedades['Precio'] = propiedades['Precio'].str.replace('€/mes', '', regex=True).str.replace('€', '', regex=True).str.strip()
    propiedades['Precio'] = propiedades['Precio'].astype(int)
    return propiedades, estadisticas, clientes

propiedades, estadisticas, clientes = leer_datos()
propiedades_madrid = propiedades[propiedades['Localidad'] == 'Madrid']
menu = option_menu('',options=['Propiedades','Estadísticas','Clientes'],orientation='horizontal',
                    styles={'container':{'background-color':'#020c0f'},'icon':{'color':'white'},
                                'icon':{'color':'white'},
                                'nav-link':{'color':'white'},
                                'nav-link-selected':{'background-color':'#919ca1'}})

if menu == 'Propiedades':
    col1, col2, col3, col4, col5 = st.columns([1,0.7,1.3,1,1])
    with col1:
        st.metric('Total de propiedades', propiedades.shape[0])
    
    with col3:
        st.metric('Total de propiedades Madrid', propiedades_madrid.shape[0])
    col10, col11, col12 = st.columns([1,1,1])
    with col10:
        zonas_count = propiedades['Localidad'].value_counts().reset_index()
        zonas_count.columns = ['Localidad', 'Cantidad']
        top_n = 3
        zonas_count['Categoria'] = zonas_count.apply(lambda row: row['Localidad'] if row.name < top_n else 'Otros', axis=1)

        # Reagrupar datos
        zonas_agrupadas = zonas_count.groupby('Categoria')['Cantidad'].sum().reset_index()
        fig = px.pie(zonas_count, names="Categoria", values="Cantidad", title="Propiedades por Localidad")

        # Mostrar en Streamlit
        st.plotly_chart(fig)
    
    with col12:
        ventas_madrid = propiedades_madrid[propiedades_madrid['Venta o Alquiler'] == 'Venta']
        fig = px.histogram(ventas_madrid, x="Precio", nbins=30, title="Precios de venta en Madrid")

        # Mostrar en Streamlit
        st.plotly_chart(fig)
    with col11:
        
        zonas_count = propiedades_madrid['Zona'].value_counts().reset_index()
        zonas_count.columns = ['Zona', 'Cantidad']
        top_n = 5
        zonas_count['Categoria'] = zonas_count.apply(lambda row: row['Zona'] if row.name < top_n else 'Otros', axis=1)

        # Reagrupar datos
        zonas_agrupadas = zonas_count.groupby('Categoria')['Cantidad'].sum().reset_index()
        fig = px.pie(zonas_count, names="Categoria", values="Cantidad", title="Propiedades por zona de Madrid")

        # Mostrar en Streamlit
        st.plotly_chart(fig)


if menu == 'Estadísticas':
    ids_propiedades = propiedades_madrid['Codigo de la propiedad'].unique()
    estadisticas_madrid = estadisticas[estadisticas['REFERENCIA INTERNA'].isin(ids_propiedades)]
    estadisticas_madrid = pd.merge(propiedades_madrid, estadisticas_madrid, left_on='Codigo de la propiedad', right_on='REFERENCIA INTERNA', how='left')
    zonas_count = estadisticas_madrid.groupby(['Zona']).agg({'VISITAS EN DETALLE':'mean'}).sort_values(by='VISITAS EN DETALLE', ascending=False).reset_index()
    top_n = 5
    zonas_count['Categoria'] = zonas_count.apply(lambda row: row['Zona'] if row.name < top_n else 'Otros', axis=1)

    # Reagrupar datos
    zonas_agrupadas = zonas_count.groupby('Categoria')['VISITAS EN DETALLE'].sum().reset_index()
    fig = px.pie(zonas_count, names="Categoria", values="VISITAS EN DETALLE", title="Zonas de Madrid con más visitas")

    # Mostrar en Streamlit
    st.plotly_chart(fig)

if menu == 'Clientes':
    clientes_count = clientes['LEAD_ORIGIN'].value_counts().reset_index()
    clientes_count.columns = ['LEAD_ORIGIN', 'Cantidad']
    top_n = 5
    clientes_count['Categoria'] = clientes_count.apply(lambda row: row['LEAD_ORIGIN'] if row.name < top_n else 'Otros', axis=1)

    # Reagrupar datos
    zonas_agrupadas = clientes_count.groupby('Categoria')['Cantidad'].sum().reset_index()
    fig = px.pie(clientes_count, names="Categoria", values="Cantidad", title="# de clientes por fuente")

    # Mostrar en Streamlit
    st.plotly_chart(fig)
