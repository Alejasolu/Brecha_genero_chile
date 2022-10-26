# ---------------- Importar Paquetes -------------
import streamlit as st # !pip install streamlit 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geojson # !pip install geojson
import base64
import hydralit_components as hc # Paquete para crear el menú

# -------- Función para Descargar Archivos csv -------
def get_table_download_link(df, brecha): # Tiene cómo parámetros la base y el nombre de la brecha a descargar
    csv = df.to_csv(index = False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="datos_' + brecha + '.csv">Descargar archivo ' + brecha + ' csv</a>' # Apararece la opción de descarga con el nombre de la brecha y con este nombre se descarga 
    return href

# ------------ Configuración de Página ---------------
st.set_page_config(page_title = 'Brecha de Género', # Nombre de la página 
                   page_icon = ':bar_chart:', # Ícono de gráfico de barras de la página
                   layout = 'wide') # Utilizar la página completa en lugar de una columna central estrecha

# -----------  Optimizar el Rendimiento --------------
@st.cache(persist = True) 

# ------ Función para cargar las bases de datos ----------
def load_data(url): # Tiene cómo parámetro la ruta de acceso de la base de datos
    df = pd.read_csv(url) # Importar la base con la ruta de acceso
    df ['Anio'] = pd.to_datetime(df['Anio'], format ='%Y') # Pasar el año a formato fecha
    df['Anio'] = df['Anio'].dt.year # Dejar solo el año de la fecha
    df = df[(df['Anio'] >= 2010) & (df['Anio'] <= 2019 )] #Se toman solo los datos pertenecientes a los años de interes(2010-2019)
    return df # Retorna el dataframe cargado 

# ------------ Importar Bases de Datos -------------
df = load_data('brecha_des.csv') # Brecha de género en la desocupación
brecha_des = df.copy() # Se crea una copia del original para trabajar

df = load_data('brecha_nac.csv') # Brecha de género en paternidad y maternidad adolescentes
brecha_nac = df.copy() # Se crea una copia del original para trabajar

df = load_data('brecha_tit.csv') # Brecha de género en titulos profesionales
brecha_tit = df.copy() # Se crea una copia del original para trabajar

# -------------- Importar geojson --------------
with open('regiones.json') as f: # Se carga el geojson con la regiones de Chile
  gj_com = geojson.load(f) 
  
# ---------- Importar Bases Adicionales ------------
df = pd.read_csv('brecha_salario.csv', sep = ';') # Brecha de género en salario
brecha_sal = df.copy() # Se crea una copia del original para trabajar

df = pd.read_csv('poblacion.csv', sep=';') # Población de Chile
poblacion = df.copy() # Se crea una copia del original para trabajar

# -------- Depuración de Bases de Datos ----------
#brecha_des.columns
brecha_des = brecha_des.rename(columns={'Tasa_des_mujeres ':'Tasa_des_mujeres'}) # Quitar espacio en nombre de columna

#brecha_des['Trimestre'].unique() # Enero no tiene espacio con el '-'
brecha_des['Trimestre'] = brecha_des['Trimestre'].replace({'Ene- Mar':'Ene - Mar'}) #Ahora todos están escritos de la misma forma


# --- Tratamiento de Datos Faltantes para Corregir el Tipo de Dato ---
brecha_tit['Mujeres_tituladas'] = brecha_tit['Mujeres_tituladas'].interpolate().astype(int)

# -------- Generación Bodegas de Datos ----------
brecha_des1 = brecha_des[['Anio', 'Trimestre', 'Region', # Brecha de género en la desocupación
                          'Codigo_region','Tasa_desocupacion', 'Tasa_des_hombres',  
                          'Tasa_des_mujeres', 'Brecha_genero']] # Se dejan los atributos de interes

brecha_tit1 = brecha_tit[['Anio', 'Region', 'Codigo_region', 'Tituladas', # Brecha de género en titulos profesionales 
                          'Hombres_titulados', 'Mujeres_tituladas', 'Porc_hombres_t', 
                          'Porc_mujeres_t', 'Brecha_genero']] # Se dejan los atributos de interes

brecha_nac1 = brecha_nac[['Anio', 'Region', 'Codigo_region', 'Tramos_edad', # Brecha de género en paternidad y maternidad adolescentes
                        'Nacidos_padres', 'Nacidos_madres', 'Porc_nacidos_padres', 
                        'Porc_nacidos_madres', 'Brecha_genero']] # Se dejan los atributos de interes

# --- Especificar la Definición del Menú Principal ---
menu_data = [
        {'icon': "far fa-chart-bar", 'label':"Dashboard"}, # Se agrega un ícono a cada menú
        {'icon': "fa fa-database", 'label':"Bases"},
        {'icon': "fa fa-play", 'label':"Videos"}]

# -------- Colores Primarios del Menú ------
over_theme = {'txc_inactive': '#FFFFFF', 'menu_background':'#68BAE3', 'txc_active':'#4811A3', 'option_active':'#A6FAC7'}

# -------- ---Creación del Menú ---------------
menu_id = hc.nav_bar(menu_definition = menu_data, home_name = 'Inicio', override_theme = over_theme, 
                     use_animation = True, sticky_mode = 'pinned')


# -------- Agregar Color a Background de la Página -----------
st.markdown(
    """
<style>
span[data-baseweb="tag"] {
  background-color: #A6FAC7 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# -------- Condicional para Ingresar el Contenido al Menú Inicio --------
if menu_id == 'Inicio':
    
    # Partición de la página para ajustar la imagen
    col1, col2, col3 = st.columns((1,3,1))
    
    with col1:
        st.write(' ')
    with col2:
        st.image('inicio1.jpg', use_column_width=True) # Se inserta la imagen de la portada        
        # Texto que acompaña la imagen de Inicio
        st.markdown('<div style="text-align: justify;">Las brechas de desigualdad de género son una medida estadística que da cuenta de la distancia de mujeres y hombres con respecto a un mismo indicador. La cuantificación de las brechas ha estimulado el desarrollo de estadísticas y la formulación de indicadores para comprender las dimensiones de la desigualdad y monitorear los efectos de las políticas sobre su erradicación, así como los avances en la eliminación de la desigualdad comparativamente a través del tiempo.</div>', unsafe_allow_html=True)
    with col3:
        st.write(' ')        

# -------- Condicional para Ingresar el Contenido al Menú Dashboard --------
if menu_id == 'Dashboard':
    
# --------- Partición de la Página ----------    
    c1, c2, c3, c4, c5 = st.columns((0.4,1,1,1,1))
    

# ----------------- Métricas -------------------- 

    # -------- Top Brecha de Desocupación ---------
    c2.markdown("<h3 style ='text-align: left; color: #169AA3;'>Top Desocupación </h3>", unsafe_allow_html =True)
    
    bd = brecha_des1.groupby(['Region'])[['Brecha_genero']].max().sort_values(by='Brecha_genero', ascending = False).head(1)
    
    top_perp_name = bd['Brecha_genero'][0]

    top_region = bd.index[0]  
    
    c2.metric('Brecha', value = top_perp_name, delta = top_region)
    

    # -------- Top Brecha de Títulos ---------    
    c3.markdown("<h3 style ='text-align: left; color: #169AA3;'>Top Títulos</h3>", unsafe_allow_html =True)
    
    bd = brecha_tit1.groupby(['Region'])[['Brecha_genero']].max().sort_values(by='Brecha_genero').head(1)    
        
    top_perp_name = bd['Brecha_genero'][0]

    top_region = bd.index[0]  
       
    c3.metric('Brecha', value = top_perp_name, delta = top_region)
    
    # -------- Top Brecha de Maternidad y Paternidad ---------  
    c4.markdown("<h3 style ='text-align: left; color: #169AA3;'>Top Nacimientos</h3>", unsafe_allow_html =True)
    
    bd = brecha_nac1.groupby(['Region'])[['Brecha_genero']].max().sort_values(by='Brecha_genero', ascending = False)
    
    top_perp_name = bd['Brecha_genero'][0]

    top_region = bd.index[0]  
       
    c4.metric('Brecha', value = top_perp_name, delta = top_region)
    
    # -------- Top Brecha de Salario ---------  
    
    brechas = brecha_sal.columns[brecha_sal.columns.str.contains('^Brecha')]
    salario1 = brecha_sal[brechas]
    salario1['region'] = brecha_sal.iloc[:,0]
    salario1['Brecha_promedio'] = salario1.iloc[:,:8].mean(axis = 1)
    salario1 = salario1[['region','Brecha_promedio']].sort_values(by='Brecha_promedio', ascending = False)
    
    bd = salario1.groupby(['region'])[['Brecha_promedio']].max().sort_values(by='Brecha_promedio', ascending = True).head(1)
    
    top_perp_name = round(bd['Brecha_promedio'][0],2)

    top_region = bd.index[0]  
    
    c5.markdown("<h3 style ='text-align: left; color: #169AA3;'>Top Salario</h3>", unsafe_allow_html =True)
    
    c5.metric('Brecha', value = top_perp_name, delta = top_region)
    
    st.markdown('---')    

# --------------------------------- Evolución de las Brechas de Género -----------------------------------------

    # ------ Título ------ 
    st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Evolución de las Brechas de Género</h3>", unsafe_allow_html = True)
    
    # Se agrupa la brecha de desocupación por año
    bgdes = brecha_des1.groupby(['Anio'])[['Brecha_genero']].mean().rename(columns={'Brecha_genero':'brecha desocupación'}).reset_index() 
    
    # Se agrupa los porcentajes de madres y padres adolescentes por año y región, ya que estaba por tramos de edad
    bgnac = brecha_nac1.groupby(['Anio', 'Region'])[['Porc_nacidos_padres', 'Porc_nacidos_madres']].sum().reset_index()
    
    # Se calcula la diferencia entre porcentajes por género y región, para calcular la brecha
    bgnac['brecha_genero'] = bgnac['Porc_nacidos_madres'] - bgnac['Porc_nacidos_padres']
    
    # Se agrupa la brecha entre madres y padres por año
    bgnac = bgnac.groupby(['Anio'])[['brecha_genero']].mean().rename(columns={'brecha_genero':'brecha padres'}).reset_index()
    
    # Se agrupa la brecha de titulos por año
    bgtit = brecha_tit1.groupby(['Anio'])[['Brecha_genero']].mean().rename(columns={'Brecha_genero':'brecha titulos'}).reset_index()
    
    # Se hace el merge de las brechas de género por año
    bgseries = pd.merge(bgnac, bgdes, how = 'outer', on = ['Anio'])
    bgseries1 = pd.merge(bgseries, bgtit, how = 'outer', on = ['Anio'])
    
    # Se hace un gráfico de líneas para visulizar las series de tiempo
    
    # ---- Gráfica ------
    fig = px.line(bgseries1, x = 'Anio', y = ['brecha padres',	'brecha desocupación', 'brecha titulos'], width = 1000, height = 450,
                  color_discrete_sequence = ['#A6FAC7','#68BAE3','#169AA3'], markers = True
                  )
    
    # --- Detalles ---
    fig.update_layout(
        template = 'simple_white',
        legend_title = 'Tipo:',
        xaxis_title = '<b>Año<b>',
        yaxis_title = '<b>Brecha<b>',
        plot_bgcolor='rgba(0,0,0,0)',
        
        legend = dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor = "right",
            x = 0.7)
        )
    
    # ---- Mostrar Gráfica -----
    st.plotly_chart(fig, use_container_width = True)

# --------- Partición de la Página ----------
    c1, c2 = st.columns((4,5))
    
# ---------------------------------- Relación Tituladas con Madres Adolescentes -----------------------------------
   
    # ------ Título ------ 
    c1.markdown("<h3 style ='text-align: center; color:#169AA3;'>Relación Tituladas con Madres Adolescentes</h3>", unsafe_allow_html =True)
    
    # Creamos dos dataframes apartir de la bodega de datos brecha_tit1 agrupando por cada año la cantidad de mujeres tituladas y las madres adolescentes
    tituladas1 = brecha_tit1.groupby(['Anio'])[['Mujeres_tituladas']].sum().rename(columns={'Mujeres_tituladas':'cantidad'}).reset_index()
    tituladas1['tipo'] = 'Tituladas' # Se agrega una columna con el tipo 'Tituladas'
    madres1 = brecha_nac1.groupby(['Anio'])[['Nacidos_madres']].sum().rename(columns={'Nacidos_madres':'cantidad'}).reset_index()
    madres1['tipo'] = 'Madres Adolescentes' # Se agrega una columna con el tipo 'Madres Adolescentes'

    # Unimos los dos dataframes anteriores
    tm = pd.merge(tituladas1, madres1, how = 'outer', on = ['Anio','cantidad','tipo'])
    
    # Creamos un gráfico de barras dónde se pueda visualizar la relación de las tituladas con las madres adolescentes por año
    
    # ---- Gráfica ------
    fig = px.bar(tm, x = 'Anio', y = 'cantidad', color = 'tipo', barmode = 'group', width = 580, height = 350,
             color_discrete_sequence = ['#A6FAC7','#68BAE3']
             )
    
    # --- Detalles ---
    fig.update_layout(
        template = 'simple_white',
        legend_title = 'Evolución en el año según:',
        xaxis_title = '<b>Región<b>',
        yaxis_title = '<b>Cantidad<b>',
        plot_bgcolor = 'rgba(0,0,0,0)',
        
        legend=dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor = "right",
            x = 0.8)
    )
    
    # ---- Mostrar Gráfica -----
    c1.plotly_chart(fig)

# ---------------------------------- Tasa Regional de Desocupación Histórica por Género -----------------------------------    
    
    # ------ Título ------ 
    c2.markdown("<h3 style ='text-align: center; color:#169AA3;'>Tasa Regional de Desocupación Histórica por Género</h3>", unsafe_allow_html =True)
    
    # Creamos dos dataframes dónde cada tasa de desocupación de cada género se agrupe por region para así obtener una columna que contenga información del género
    # Se renombra cada tasa de genero por cantidad para que podamos crear una columna que sea en común y la llamaremos tasa
    desocupados = brecha_des1.groupby(['Region'])[['Tasa_des_hombres']].mean().rename(columns={'Tasa_des_hombres':'tasa'}).reset_index()
    desocupados['tipo'] = 'Hombres'
    desocupadas = brecha_des1.groupby(['Region'])[['Tasa_des_mujeres']].mean().rename(columns={'Tasa_des_mujeres':'tasa'}).reset_index()
    desocupadas['tipo'] = 'Mujeres'
    
    # Juntamos los dos dataframes y obtenemos una tabla que contiene la tasa de desocupación de cada región y a que género pertenece
    des = pd.merge(desocupados, desocupadas, how = 'outer', on = ['Region','tasa','tipo']).sort_values(by="tasa", ascending= False)
   
    # ---- Gráfica ------
    fig = px.bar(des, x ='Region', y = 'tasa', color = 'tipo', barmode = 'group', width = 750, height = 350,
             color_discrete_sequence = ['#A6FAC7','#68BAE3']
             ) 
    
    # --- Detalles ---
    fig.update_layout(
        template = 'simple_white',
        legend_title = 'Evolución en el año según:',
        xaxis_title = '<b>Región<b>',
        yaxis_title = '<b>Cantidad<b>',
        plot_bgcolor = 'rgba(0,0,0,0)',
        
        legend=dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor="right",
            x = 0.8)
    )
    
    # ---- Mostrar Gráfica -----
    c2.plotly_chart(fig)

# --------- Partición de la Página ----------  
    c3, c4 = st.columns((1,1))

# ---------------------------------- Variación de la Relación entre Madres y Tituladas del Año 2019 Respecto a 2018 -----------------------------------    
    
    # ------ Título ------ 
    c3.markdown("<h3 style ='text-align: center; color:#169AA3;'>Variación de la Relación entre Madres y Tituladas del Año 2019 Respecto a 2018</h3>", unsafe_allow_html =True)
    
    # Filtra por año 2018 y se agrupa por año y región las mujeres tituladas y para las madres adolescentes
    brecha2018t = brecha_tit1[brecha_tit1['Anio'] == 2018].groupby(['Anio', 'Region'])[['Mujeres_tituladas']].sum().reset_index()
    brecha2018n = brecha_nac1[brecha_nac1['Anio'] == 2018].groupby(['Anio', 'Region'])[['Nacidos_madres']].sum().reset_index()
    
    # Filtra por año 2019 y se agrupa por año y región las mujeres tituladas y para las madres adolescentes
    brecha2019t = brecha_tit1[brecha_tit1['Anio'] == 2019].groupby(['Anio', 'Region'])[['Mujeres_tituladas']].sum().reset_index()
    brecha2019n = brecha_nac1[brecha_nac1['Anio'] == 2019].groupby(['Anio', 'Region'])[['Nacidos_madres']].sum().reset_index()
    
    # Se hace el merge para los dataframes de cada año
    brecha2018 = pd.merge(brecha2018t, brecha2018n, how = 'outer', on = ['Anio', 'Region'])
    brecha2019 = pd.merge(brecha2019t, brecha2019n, how = 'outer', on = ['Anio', 'Region'])
        
    # Proporción entre las madres adolescentes y mujeres tituladas para cada año
    brecha2018['Prop2018'] = brecha2018['Nacidos_madres']/brecha2018['Mujeres_tituladas']
    brecha2019['Prop2019'] = brecha2019['Nacidos_madres']/brecha2019['Mujeres_tituladas']
    
    # Variación porcentual
    brecha2019['var_prop'] = round((brecha2019['Prop2019'] - brecha2018['Prop2018'])/brecha2018['Prop2018'], 2)*100
    
    # Se filtra el dataframe con la diferencia de proporción para cada región 
    bdiff = brecha2019[['Region', 'var_prop']].sort_values(by = 'var_prop')   
    
    # ---- Gráfica ------
    fig = px.bar(bdiff, x = 'Region', y = 'var_prop',                 
                 barmode = 'group',
                 color_discrete_sequence = ['#A6FAC7'], 
                 width = 640, height = 450)

    # --- Detalles ---
    fig.update_layout(
        template = 'simple_white',
        xaxis_title = '<b>Región<b>',
        yaxis_title = '<b>Variación porcentual<b>',
        plot_bgcolor = 'rgba(0,0,0,0)'
        )    
    
    # ---- Mostrar Gráfica -----
    c3.plotly_chart(fig)

# ---------------------------------- % Brecha Máxima de Género por Año -----------------------------------       
    
    # ------ Título ------
    c4.markdown("<h3 style ='text-align: center; color:#169AA3;'>% Brecha Máxima de Género por Año</h3>", unsafe_allow_html = True)
    
    # Se agrupa por año la brecha de género tomando el valor máximo para cada año
    bd = brecha_des1.groupby(['Anio'])[['Brecha_genero']].max().reset_index()
    
    # ---- Gráfica ------
    fig = px.pie(bd, values = 'Brecha_genero', names = 'Anio',
                 width = 520, height = 520,
                 color_discrete_sequence = ['#1b4f72','#21618c','#2874a6','#2e86c1','#3498db','#5dade2','#85c1e9','#aed6f1','#d6eaf8','#ebf5fb'])
    
    # --- Detalles ---
    fig.update_layout(
        template = 'simple_white',
        legend_title = '<b> Año<b>',
        title_x = 0.5,
        
    legend=dict(
        yanchor = "bottom",
        y = 0.2,
        xanchor = "right",
        x = 1.4))
    
    c4.plotly_chart(fig)
    
# --------- Partición de la Página ---------- 
    c1, c2 = st.columns((1,1))
    
# ---------------------------------- Comportamiento de la Paternidad con Respecto a los Hombres Desocupados -----------------------------------        
    
    # ------ Título ------
    c1.markdown("<h3 style ='text-align: center; color:#169AA3;'>Comportamiento de la Paternidad con Respecto a los Hombres Desocupados</h3>", unsafe_allow_html =True)
    
    # ¿Cómo es el comportamiento de la paternidad con respecto a los hombres desocupados?
    brecha_nac2 = brecha_nac1[brecha_nac1['Tramos_edad'] == '15 a 19 años']
    desocupados = brecha_des1.groupby(['Anio'])[['Tasa_des_hombres']].mean()
    padres = brecha_nac2.groupby(['Anio'])[['Porc_nacidos_padres']].mean()
    tabla = pd.DataFrame()
    tabla['Tasa_des_hombres'] = desocupados['Tasa_des_hombres']
    tabla['Porc_nacidos_padres'] = padres['Porc_nacidos_padres']
    tabla['Relacion'] = (round(tabla['Porc_nacidos_padres']/tabla['Tasa_des_hombres'],2)*100)
    tabla = tabla.reset_index()
    
    # ---- Gráfica ------
    fig = px.line(tabla, x = 'Anio', y = ['Relacion'],
                  color_discrete_sequence = px.colors.qualitative.G10, width = 650, height = 450)
    
    # --- Detalles ---
    fig.update_layout(
        template = 'simple_white',
        xaxis_title = '<b>Fecha<b>',
        yaxis_title = '<b>Tasa de Padres adolescentes / Tasa de desocupación masculina<b>',
        plot_bgcolor = 'rgba(0,0,0,0)',
        
        legend=dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor = "right",
            x = 0.8)
    )

    c1.plotly_chart(fig)
    
# ---------------------------------- Comportamiento de la Maternidad con Respecto a las Madres Desocupadas -----------------------------------   
    
    # ------ Título ------
    c2.markdown("<h3 style ='text-align: center; color:#169AA3;'>Comportamiento de la Maternidad con Respecto a las Mujeres Desocupadas</h3>", unsafe_allow_html =True)
    
        #¿Cómo es el comportamiento de la maternidad con respecto a las mujeres desocupadas en el 2019?
    brecha_nac2=brecha_nac1[brecha_nac1['Tramos_edad']=='15 a 19 años']
    desocupados=brecha_des1.groupby(['Anio'])[['Tasa_des_mujeres']].mean()
    padres=brecha_nac2.groupby(['Anio'])[['Porc_nacidos_madres']].mean()
    tabla=pd.DataFrame()
    tabla['Tasa_des_mujeres']=desocupados['Tasa_des_mujeres']
    tabla['Porc_nacidos_madres']=padres['Porc_nacidos_madres']
    tabla['Relacion']=(round(tabla['Porc_nacidos_madres']/tabla['Tasa_des_mujeres'],2)*100)
    tabla= tabla.reset_index()
    
    # ---- Gráfica ------
    fig = px.line(tabla, x='Anio', y =['Relacion'], 
                  color_discrete_sequence=px.colors.qualitative.G10, width =650, height=450)
    
    # --- Detalles ---
    fig.update_layout(
        template = 'simple_white',
        xaxis_title = '<b>Fecha<b>',
        yaxis_title = '<b>Tasa de Madres adolescentes / Tasa de desocupación femenina<b>',
        plot_bgcolor='rgba(0,0,0,0)',
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.8)
        )
    
    c2.plotly_chart(fig)

# --------- Partición de la Página ----------     
    c1, c2 = st.columns((1,1))
    
# ---------------------------------- Regiones con más Madres y Padres Adolescentes en 2019 -----------------------------------   
        
    # ------ Título ------
    c1.markdown("<h3 style ='text-align: center; color:#169AA3;'>Regiones con más Madres y Padres Adolescentes en 2019</h3>", unsafe_allow_html =True)
    
    # Se filtran las tres regiones con más madres y padres adolescentes en el año 2019 en bases individules
    madres2019 = brecha_nac1[brecha_nac1['Anio'] == 2019][['Anio', 'Region', 'Tramos_edad', 'Nacidos_madres']].rename(columns = {'Nacidos_madres':'cantidad'}).sort_values(by = 'cantidad', ascending = False).head(3)
    padres2019 = brecha_nac1[brecha_nac1['Anio'] == 2019][['Anio', 'Region', 'Tramos_edad', 'Nacidos_padres']].rename(columns = {'Nacidos_padres':'cantidad'}).sort_values(by = 'cantidad', ascending = False).head(3)
    
    # Se agregan columnas con el genero
    madres2019['genero'] = 'Madres'
    padres2019['genero'] = 'Padres'
    
    # Se hace el merge entre las bases de madres y padres
    pm = pd.merge(madres2019, padres2019, how = 'outer', on = ['Anio',	'Region', 'Tramos_edad', 'cantidad', 'genero'])
    
    # ---- Gráfica ------
    fig = px.bar(pm, x = 'Region', y = 'cantidad', color = 'genero',
                 barmode = 'group',
                 hover_data =['Tramos_edad'],
                 color_discrete_sequence = ['#A6FAC7','#68BAE3'])
    
    # --- Detalles ---
    fig.update_layout(
        template = 'simple_white',
        title_x = 0.5,
        legend_title = 'Evolución en el año según:',
        xaxis_title = '<b>Región<b>',
        yaxis_title = '<b>Cantidad<b>',
        plot_bgcolor = 'rgba(0,0,0,0)',
        
        legend = dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor = "right",
            x = 0.8)
        )
    
    c1.plotly_chart(fig, use_container_width = True)
    
# -------------------- Porcentaje Histórico de Títulos por Género en las 3 Regiones con más Personas Tituladas ----------------------     
    
    # ------ Título ------
    c2.markdown("<h3 style ='text-align: center; color:#169AA3;'>Porcentaje Histórico de Títulos por Género en las 3 Regiones con más Personas Tituladas</h3>", unsafe_allow_html =True)
    
    #Creamos dos dataframes apartir de la bodega de datos brecha_tit1 agrupando por cada año la cantidad de mujeres tituladas y las madres adolescentes
    tituladas1 = brecha_tit1.groupby(['Region'])[['Tituladas']].sum().rename(columns={'Tituladas':'cantidad'}).reset_index().sort_values(by = "cantidad", ascending = False)
    tituladas1['tipo'] = 'Tituladas'
    madres1 = brecha_nac1.groupby(['Anio'])[['Nacidos_madres']].sum().rename(columns={'Nacidos_madres':'cantidad'}).reset_index()
    madres1['tipo'] = 'Madres Adolescentes'
    tone = tituladas1.head(3)
        
    #Creamos dos dataframes que tengan la cantidad de titulados de cada genero agrupados por región y le agregamos una columna cuyos valores indiquen de que género es
    porch = brecha_tit1.groupby(['Region'])[['Porc_hombres_t']].mean().reset_index().rename(columns = {'Porc_hombres_t':'Porc'})
    porch['genero'] = 'Hombre' 
    porch['Porc'] = round(porch['Porc'],2)
    porcm = brecha_tit1.groupby(['Region'])[['Porc_mujeres_t']].mean().reset_index().rename(columns = {'Porc_mujeres_t':'Porc'})
    porcm['genero'] = 'Mujer'
    porcm['Porc'] = round(porcm['Porc'], 2)
    
    porc = pd.merge(porch, porcm, how = 'outer', on = ['Region','genero','Porc'])
    porcg = pd.merge(porc, tone, how = 'inner', on = ['Region'])
    
    #Creamos un gráfico de rayos de sol para representar el dataframe anterior
    fig = px.sunburst(porcg, path=['Region','Porc',], color='genero', color_discrete_sequence=['#A6FAC7','#1AB3EC','#A0FEFF'], values='Porc')
    
    #Crearemos legend a mano    
    D = porc['genero'].unique() # Generamos la lista de los generos que se muestran en el diagrama
    colors = [ '#1AB3EC', # El color de los hombres
             '#A6FAC7'] # El color de las Mujeres
    for i, m in enumerate(D):  # Creamos la leyenda
        fig.add_annotation(dict(font = dict(color = colors[i],size = 14),
                                            x = 0.8,
                                            y = 1-(i/10),
                                            showarrow = False,
                                            text = D[i],
                                            textangle = 0,
                                            xanchor = 'left',
                                            xref = "paper",
                                            yref = "paper",
                                            ))
    
    c2.plotly_chart(fig)  

# -------------------- Brecha Salarial Promedio por Región ----------------------
    # ------ Título ------ 
    st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Brecha Salarial Promedio por Región</h3>", unsafe_allow_html =True)      
    
    # ---- Gráfica ------
    fig = px.bar(salario1, x = 'region', y='Brecha_promedio', barmode = 'group', width =650, height=500)
                 
    # --- Detalles ---
    fig.update_layout(
        xaxis_title = 'Región',
        yaxis_title = 'Brecha porcentual',
        template = 'simple_white',
        title_x = 0.5,
        plot_bgcolor='rgba(0,0,0,0)')
    
    st.plotly_chart(fig, use_container_width = True)
        
    st.markdown('---') # Línea de división

    # ------ Título ------    
    st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Relación entre Títulos y Población</h3>", unsafe_allow_html =True)
    
    poblacion = poblacion.sort_values(by='Region') # Se ordena las regiones en orden alfabetico
    
    # Selectbox de lo que se mostrará en el mapa
    genero_map = st.selectbox('Seleccione el género:', options = ['Tituladas', 'Titulados', 'Tituladas/Población', 'Titulados/Población'])
    
    # Crear bases con el código de región para hacer el join con el geojson
    base1 = brecha_tit1.groupby(['Region', 'Codigo_region'])[['Mujeres_tituladas']].sum().reset_index().rename(columns = {'Codigo_region':'codregion','Mujeres_tituladas':'Indicador'})
    base2 = brecha_tit1.groupby(['Region', 'Codigo_region'])[['Hombres_titulados']].sum().reset_index().rename(columns = {'Codigo_region':'codregion','Hombres_titulados':'Indicador'})
    
    
    # Condicional en función del selectbox
    if genero_map == 'Tituladas':
        st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Mujeres Tituladas</h3>", unsafe_allow_html =True)
        base = base1   # Se muestra las mujeres tituladas por región
    elif genero_map == 'Titulados':
        st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Hombres Titulados</h3>", unsafe_allow_html =True)
        base = base1  # Se muestra las hombres titulados por región
    elif genero_map == 'Tituladas/Población':
        st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Mujeres Tituladas/Población</h3>", unsafe_allow_html =True)
        base = base1 
        base['Indicador'] = base1['Indicador']/poblacion['Total'] # Se muestra las mujeres tituladas por región/población total
    elif genero_map == 'Titulados/Población':
        st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Hombres Titulados/Población</h3>", unsafe_allow_html =True)
        base = base2
        base['Indicador'] = base2['Indicador']/poblacion['Total'] # Se muestra las hombres titulados por región/población total  
     
    # ---- Gráfica ------
    min = base['Indicador'].min() # generar mínimo del rango del color
    max = base['Indicador'].max() # generar máximo del rango del color
    
    fig = px.choropleth_mapbox( base, # dataframe que tiene el indicador
                  geojson = gj_com, # archivo json con el shape
                  color = 'Indicador', # columna que contiene el indicador: valor sobre el cual se va dar la tonalidad del color
                  locations = 'codregion', # llave del dataframe para hacer el join con el shape
                  featureidkey = 'properties.codregion', # llave del shape para hacer el join con el dataframe
                  color_continuous_scale = 'Viridis', # escala de color que se va usar
                  range_color =(max, min), # rangos entre los cuales va variar el color
                  hover_name = 'Region', # información que se va a observar cuando se pase el cursor por el poligono
                  center = {'lat':	-39.675147, 'lon': -71.542969}, # centro en el cual se va ubicar el mapa, ubicado a conveniencia
                  zoom = 3.5, # zoom de la imagen
                  mapbox_style = "carto-positron", height = 950) # estilo del mapa
    
    fig.update_geos(fitbounds = 'locations', visible = False) # ajustar a los limites del shape
    
    st.plotly_chart(fig, use_container_width = True)  

# -------- Condicional para Ingresar el Contenido al Menú Bases --------    
if menu_id == 'Bases':

# -------- Brecha de Género en Paternidad y Maternidad Adolescente --------     
    # ------ Título ------ 
    st.markdown("<h3 style ='text-align: center; color: #169AA3;'>Brecha de Género en Paternidad y Maternidad Adolescente</h3>", unsafe_allow_html =True)

    # Dataframe a mostrar
    df1 = brecha_nac1    
    
    # Multiselect para filtrar por año
    anio1 = st.multiselect(
        "Seleccione el año aquí:",
        options = df1['Anio'].unique(),
        default = df1['Anio'].unique())
    
    # Regiones por las cuales se puede filtrar
    region_list = ['Todas','Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama',
       'Coquimbo', 'Valparaíso', 'Metropolitana', "O'Higgins", 'Maule',
       'Ñuble', 'Biobío', 'La Araucanía', 'Los Ríos', 'Los Lagos',
       'Aysén', 'Magallanes']
    
    # Selectbox de las regiones
    region1 = st.selectbox('Seleccione la región aquí:', region_list, key = '1')
    
    # Condicional en función de las posibilidades escogidas
    if  region1 == 'Todas':
        df_selection = df1.query(
            "Anio == @anio1")
    else:
        df_selection = df1.query(
            "Anio == @anio1 & Region == @region1")
    
    # Dataframe con filtros a mostrar
    df1 = df_selection
    
    # Organizar Tabla
    fig1=go.Figure(data = [go.Table(
        
        header = dict(values = list(df1.columns),
        fill_color = '#A6FAC7',
        line_color = 'darkslategray'),
        cells = dict(values = [df1.Anio, df1.Region, df1.Codigo_region, df1.Tramos_edad, df1.Nacidos_padres,
               df1.Nacidos_madres, df1.Porc_nacidos_padres, df1.Porc_nacidos_madres,
               df1.Brecha_genero],
            fill_color = 'white',
            line_color = 'lightgrey'))
        ])
    
    fig1.update_layout(width = 1200, height = 450)
    
    st.write(fig1)
    

# -------- Brecha de Género en Desocupación --------
    
    # ------ Título ------
    st.markdown("<h3 style = 'text-align: center; color: #169AA3;'>Brecha de Género en Desocupación</h3>", unsafe_allow_html = True)
    
    # Dataframe a mostrar
    df2 = brecha_des1
    
    # Multiselect para filtrar por año
    anio2 = st.multiselect(
        "Seleccione el año aquí:",
        options = df2['Anio'].unique(),
        default = df2['Anio'].unique(), key = '2')
    
    # Regiones por las cuales se puede filtrar
    region_list = ['Todas','Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama',
       'Coquimbo', 'Valparaíso', 'Metropolitana', "O'Higgins", 'Maule',
       'Ñuble', 'Biobío', 'La Araucanía', 'Los Ríos', 'Los Lagos',
       'Aysén', 'Magallanes']
    
    # Selectbox de las regiones
    region2 = st.selectbox('Seleccione la región aquí:', region_list, key = '2')
    
    # Condicional en función de las posibilidades escogidas
    if  region2 == 'Todas':
        df_selection = df2.query(
            "Anio == @anio2")
    else:
        df_selection = df2.query(
            "Anio == @anio2 & Region == @region2")

    # Dataframe con filtros a mostrar
    df2 = df_selection
    
    # Organizar Tabla
    fig = go.Figure(data = [go.Table(
        
        header = dict(values = list(df2.columns),
        fill_color = '#A6FAC7',
        line_color = 'darkslategray'),
        cells = dict(values = [df2.Anio, df2.Trimestre, df2.Region, df2.Codigo_region, df2.Tasa_desocupacion,
               df2.Tasa_des_hombres, df2.Tasa_des_mujeres, df2.Brecha_genero],
            fill_color = 'white',
            line_color = 'lightgrey'))
        ])
    fig.update_layout(width =1200, height=450)
    
    st.write(fig)
    
# -------- Brecha de Género en Titulos Profesionales --------
    
    # ------ Título ------
    st.markdown("<h3 style ='text-align: center; color: #169AA3;'>Brecha de Género en Titulos Profesionales</h3>", unsafe_allow_html =True)
    
    # Dataframe a mostrar
    df3 = brecha_tit1
    
    # Multiselect para filtrar por año
    anio3 = st.multiselect(
        "Seleccione el año aquí:",
        options = df3['Anio'].unique(),
        default = df3['Anio'].unique(), key = '3')
    
    # Regiones por las cuales se puede filtrar
    region_list = ['Todas','Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama',
       'Coquimbo', 'Valparaíso', 'Metropolitana', "O'Higgins", 'Maule',
       'Ñuble', 'Biobío', 'La Araucanía', 'Los Ríos', 'Los Lagos',
       'Aysén', 'Magallanes']
    
    # Selectbox de las regiones
    region3 = st.selectbox('Seleccione la región aquí:', region_list, key = '3')
    
    # Condicional en función de las posibilidades escogidas
    if  region3 == 'Todas':
        df_selection = df3.query(
            "Anio == @anio3")
    else:
        df_selection = df3.query(
            "Anio == @anio3 & Region == @region3")

    # Dataframe con filtros a mostrar
    df3 = df_selection

    # Organizar Tabla
    fig=go.Figure(data = [go.Table(
        
        header = dict(values = list(df3.columns),
        fill_color = '#A6FAC7',
        line_color = 'darkslategray'),
        cells = dict(values = [df3.Anio, df3.Region, df3.Codigo_region, df3.Tituladas,
               df3.Hombres_titulados, df3.Mujeres_tituladas , df3.Porc_hombres_t, df3.Porc_mujeres_t,
               df3.Brecha_genero],
            fill_color = 'white',
            line_color = 'lightgrey'))
        ])
    fig.update_layout(width = 1200, height = 450)
    
    st.write(fig)
    
    
    # ------ Descargar los archivos en formato csv -------
    st.markdown(get_table_download_link(df1,'brecha_paternidad_maternidad'), unsafe_allow_html=True)
    st.markdown(get_table_download_link(df2,'brecha_desocupacion'), unsafe_allow_html=True)
    st.markdown(get_table_download_link(df3,'brecha_titulos'), unsafe_allow_html=True)


if menu_id == 'Videos':
    
    # ------ Vídeo 1 -------
    c1, c2 = st.columns((1,1))
    c1.markdown("<h3 style ='text-align: center; color:#169AA3;'>Desafíos para la Igualdad de Género</h3>", unsafe_allow_html =True)   
    c1.video("https://youtu.be/KSwJQrhxH14")
    c1.markdown('<div style="text-align: justify;">En este contexto, hay retos culturales, educacionales y de democracia familiar que son prioritarios, coinciden las fuentes. Uno es la gran barrera social que inhibe la participación femenina: ellas se mantienen como las principales encargadas de lo doméstico y del cuidado de personas que requieren atención: hijos, enfermos o ancianos.</div>', unsafe_allow_html=True)
    
    # ------ Vídeo 2 -------
    c2.markdown("<h3 style ='text-align: center; color:#169AA3;'>Más Mujeres en Ciencias</h3>", unsafe_allow_html =True)
    c2.video("https://youtu.be/Yuki-g9sgLw")
    c2.markdown('<div style="text-align: justify;">Fomentar, promover e incentivar a más mujeres jóvenes a elegir carreras enfocadas en la ciencia, tecnología, ingeniería y matemáticas, no solo para aumentar la participación laboral femenina, sino también para elevar la participación de mujeres en carreras históricamente masculinizadas. Hasta ahora existe una baja participación de mujeres en carreras STEM por una serie de brechas producto de estereotipos que se reproducen desde la infancia.</div>', unsafe_allow_html=True)

    # ------ Vídeo 3 -------
    c3, c4 = st.columns((1,1))
    c3.markdown("<h3 style ='text-align: center; color:#169AA3;'>Género en el Sistema Financiero</h3>", unsafe_allow_html =True)
    c3.video("https://youtu.be/9INYaVbHiCY")
    c3.markdown('<div style="text-align: justify;">El Informe de Género en el Sistema Financiero 2021, con cierre estadístico a marzo de este año, reveló sostenidos avances en el cierre de brechas de género asociadas al uso de servicios financieros.</div>', unsafe_allow_html=True)
    
    # ------ Vídeo 4 -------    
    c4.markdown("<h3 style ='text-align: center; color:#169AA3;'>Evaluación de Brechas en la Trayectoria de Investigación</h3>", unsafe_allow_html =True)
    c4.video("https://www.youtube.com/watch?v=9OUiga-9VuI&feature=emb_imp_woyt")
    c4.markdown('<div style="text-align: justify;">Estudio de género que evalúa y cuantifica la posible existencia de barreras que puedan tener las mujeres beneficiarias de programas públicos en Chile durante sus trayectorias de investigación.</div>', unsafe_allow_html=True)