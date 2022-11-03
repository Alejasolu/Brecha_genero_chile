# ---------------- Importar Paquetes -------------
import streamlit as st # !pip install streamlit 
import pandas as pd
import plotly.express as px #!pip install plotly
import plotly.graph_objects as go
# ---------------- Import packages -------------
import streamlit as st # !pip install streamlit 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geojson # !pip install geojson
import base64
import hydralit_components as hc # Package for create the menu

# -------- Function to download csv fields  -------
def get_table_download_link(df, brecha): # It has as parameters the base and the name of the gap to download
    csv = df.to_csv(index = False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="datos_' + brecha + '.csv">Descargar archivo ' + brecha + ' csv</a>' # The download option appears with the name of the gap and with this name it is downloaded
    return href

# ------------ Page Setup ---------------
st.set_page_config(page_title = 'Brecha de Género', # Name of the page
                   page_icon = ':bar_chart:', # page bar chart icon
                   layout = 'wide') # Use the full page instead of a narrow center column

# -----------  Optimize Performance --------------
@st.cache(persist = True) 

# ------ Function to load the databases ----------
def load_data(url): # It has as a parameter the access path of the database
    df = pd.read_csv(url) # Import base with path
    df ['Anio'] = pd.to_datetime(df['Anio'], format ='%Y') # Convert year to date format
    df['Anio'] = df['Anio'].dt.year # Leave only the year of the date
    df = df[(df['Anio'] >= 2010) & (df['Anio'] <= 2019 )] #Only the data belonging to the years of interest are taken (2010-2019)
    return df # Return the loaded dataframe

# ------------ Import Databases -------------
df = load_data('brecha_des.csv') # Gender gap in unemployment
brecha_des = df.copy() # A copy of the original is created to work

df = load_data('brecha_nac.csv') # Gender gap in adolescent fatherhood and motherhood
brecha_nac = df.copy() # A copy of the original is created to work

df = load_data('brecha_tit.csv') # Gender gap in professional titles
brecha_tit = df.copy() #A copy of the original is created to work

# -------------- Import geojson --------------
with open('regiones.json') as f: # The geojson is loaded with the regions of Chile
  gj_com = geojson.load(f) 
  
# ---------- Import Additional Bases ------------
df = pd.read_csv('brecha_salario.csv', sep = ';') # Gender gap in salary
brecha_sal = df.copy() # A copy of the original is created to work

df = pd.read_csv('poblacion.csv', sep=';') # Population of Chile
poblacion = df.copy() # A copy of the original is created to work

# -------- Database Debugging ----------
#brecha_des.columns
brecha_des = brecha_des.rename(columns={'Tasa_des_mujeres ':'Tasa_des_mujeres'}) # Remove space in column name

#brecha_des['Trimestre'].unique() # January has no space with the '-'
brecha_des['Trimestre'] = brecha_des['Trimestre'].replace({'Ene- Mar':'Ene - Mar'}) #Now they're all spelled the same


# --- Treatment of Missing Data to Correct the Type of Data ---
brecha_tit['Mujeres_tituladas'] = brecha_tit['Mujeres_tituladas'].interpolate().astype(int)

# -------- Data Warehouse Generation ----------
brecha_des1 = brecha_des[['Anio', 'Trimestre', 'Region', # Gender gap in unemployment
                          'Codigo_region','Tasa_desocupacion', 'Tasa_des_hombres',  
                          'Tasa_des_mujeres', 'Brecha_genero']] # The attributes of interest are left

brecha_tit1 = brecha_tit[['Anio', 'Region', 'Codigo_region', 'Tituladas', # Gender gap in professional titles 
                          'Hombres_titulados', 'Mujeres_tituladas', 'Porc_hombres_t', 
                          'Porc_mujeres_t', 'Brecha_genero']] #  The attributes of interest are left

brecha_nac1 = brecha_nac[['Anio', 'Region', 'Codigo_region', 'Tramos_edad', # Gender gap in adolescent fatherhood and motherhood
                        'Nacidos_padres', 'Nacidos_madres', 'Porc_nacidos_padres', 
                        'Porc_nacidos_madres', 'Brecha_genero']] # The attributes of interest are left

# --- Specify Main Menu Definition ---
menu_data = [
        {'icon': "far fa-chart-bar", 'label':"Dashboard"}, # An icon is added to each menu
        {'icon': "fa fa-database", 'label':"Bases"},
        {'icon': "fa fa-play", 'label':"Videos"}]

# -------- Menu Primary Colors ------
over_theme = {'txc_inactive': '#FFFFFF', 'menu_background':'#68BAE3', 'txc_active':'#4811A3', 'option_active':'#A6FAC7'}

# -------- ---Menu Creation ---------------
menu_id = hc.nav_bar(menu_definition = menu_data, home_name = 'Home', override_theme = over_theme, 
                     use_animation = True, sticky_mode = 'pinned')


# -------- Add Color to Page Background -----------
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

# -------- Conditional to Enter the Content to the Start Menu --------
if menu_id == 'Home':
    
    # Partition the page to fit the image
    col1, col2, col3 = st.columns((1,3,1))
    
    with col1:
        st.write(' ')
    with col2:
        st.image('inicio1.jpg', use_column_width=True) # Cover image is inserted       
        # Text that accompanies the Start image
        st.markdown('<div style="text-align: justify;">Gender inequality gaps are a statistical measure that accounts for the distance between women and men with respect to the same indicator. The quantification of the gaps has stimulated the development of statistics and the formulation of indicators to understand the dimensions of inequality and monitor the effects of policies on its eradication, as well as progress in eliminating inequality comparatively over time..</div>', unsafe_allow_html=True)
    with col3:
        st.write(' ')        

# -------- Conditional to Enter the Content to the Dashboard Menu --------
if menu_id == 'Dashboard':
    
# --------- Page Partition ----------    
    c1, c2, c3, c4, c5 = st.columns((0.4,1,1,1,1))
    

# ----------------- Metrics -------------------- 

    # -------- Top Unemployment Gap---------
    c2.markdown("<h3 style ='text-align: left; color: #169AA3;'>Top Unemployment </h3>", unsafe_allow_html =True)
    
    bd = brecha_des1.groupby(['Region'])[['Brecha_genero']].max().sort_values(by='Brecha_genero', ascending = False).head(1)
    
    
    top_perp_name = bd['Brecha_genero'][0]

    top_region = bd.index[0]  
    
    c2.metric('Gap', value = top_perp_name, delta = top_region)
    

    # -------- Top Title Gap ---------    
    c3.markdown("<h3 style ='text-align: left; color: #169AA3;'>Top Titles</h3>", unsafe_allow_html =True)
    
    bd = brecha_tit1.groupby(['Region'])[['Brecha_genero']].max().sort_values(by='Brecha_genero').head(1)    
        
    top_perp_name = bd['Brecha_genero'][0]

    top_region = bd.index[0]  
       
    c3.metric('Gap', value = top_perp_name, delta = top_region)
    
    # -------- Top Brecha de Maternidad y Paternidad ---------  
    c4.markdown("<h3 style ='text-align: left; color: #169AA3;'>Top Births</h3>", unsafe_allow_html =True)
    
    bd = brecha_nac1.groupby(['Region'])[['Brecha_genero']].max().sort_values(by='Brecha_genero', ascending = False)
    
    top_perp_name = bd['Brecha_genero'][0]

    top_region = bd.index[0]  
       
    c4.metric('Gap', value = top_perp_name, delta = top_region)
    
    # -------- Top Salary Gap ---------  
    
    brechas = brecha_sal.columns[brecha_sal.columns.str.contains('^Brecha')]
    salario1 = brecha_sal[brechas]
    salario1['region'] = brecha_sal.iloc[:,0]
    salario1['Brecha_promedio'] = salario1.iloc[:,:8].mean(axis = 1)
    salario1 = salario1[['region','Brecha_promedio']].sort_values(by='Brecha_promedio', ascending = False)
    
    bd = salario1.groupby(['region'])[['Brecha_promedio']].max().sort_values(by='Brecha_promedio', ascending = True).head(1)
    
    top_perp_name = round(bd['Brecha_promedio'][0],2)

    top_region = bd.index[0]  
    
    c5.markdown("<h3 style ='text-align: left; color: #169AA3;'>Top Salary</h3>", unsafe_allow_html =True)
    
    c5.metric('Gap', value = top_perp_name, delta = top_region)
    
    st.markdown('---')    

# --------------------------------- Gender Gaps Evolution -----------------------------------------

    # ------ Title ------ 
    st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Gender Gaps Evolution</h3>", unsafe_allow_html = True)
    
    # The unemployment gap is grouped by year
    bgdes = brecha_des1.groupby(['Anio'])[['Brecha_genero']].mean().rename(columns={'Brecha_genero':'unemployment gap'}).reset_index() 
    
    # The percentages of adolescent mothers and fathers are grouped by year and region, as it was by age groups
    bgnac = brecha_nac1.groupby(['Anio', 'Region'])[['Porc_nacidos_padres', 'Porc_nacidos_madres']].sum().reset_index()
    
    # The difference between percentages by gender and region is calculated to calculate the gap
    bgnac['brecha_genero'] = bgnac['Porc_nacidos_madres'] - bgnac['Porc_nacidos_padres']
    
    # The gap between mothers and fathers is grouped by year
    bgnac = bgnac.groupby(['Anio'])[['brecha_genero']].mean().rename(columns={'brecha_genero':'fathers gap'}).reset_index()
    
    # The title gaps is grouped by year
    bgtit = brecha_tit1.groupby(['Anio'])[['Brecha_genero']].mean().rename(columns={'Brecha_genero':'titles gap'}).reset_index()
    
    # The gender gaps are merged by year
    bgseries = pd.merge(bgnac, bgdes, how = 'outer', on = ['Anio'])
    bgseries1 = pd.merge(bgseries, bgtit, how = 'outer', on = ['Anio'])
    
    # A line graph is made to visualize the time series
    
    # ---- Gaph ------
    fig = px.line(bgseries1, x = 'Anio', y = ['fathers gap',	'unemployment gap', 'titles gap'], width = 1000, height = 450,
                  color_discrete_sequence = ['#A6FAC7','#68BAE3','#169AA3'], markers = True
                  )
    
    # --- Details ---
    fig.update_layout(
        template = 'simple_white',
        legend_title = 'Type:',
        xaxis_title = '<b>Year<b>',
        yaxis_title = '<b>Gap<b>',
        plot_bgcolor='rgba(0,0,0,0)',
        
        legend = dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor = "right",
            x = 0.7)
        )
    
    # ---- Show graph -----
    st.plotly_chart(fig, use_container_width = True)

# --------- Position of the page ----------
    c1, c2 = st.columns((4,5))
    
# ---------------------------------- Relationship between Graduates with Adolescent Mothers -----------------------------------
   
    # ------ Title ------ 
    c1.markdown("<h3 style ='text-align: center; color:#169AA3;'>Relationship between Graduates with Adolescent Mothers</h3>", unsafe_allow_html =True)
    
    # We create two dataframes from the 'brecha_tit1' data warehouse, grouping for each year the number of women graduates and teenage mothers
    tituladas1 = brecha_tit1.groupby(['Anio'])[['Mujeres_tituladas']].sum().rename(columns={'Mujeres_tituladas':'cantidad'}).reset_index()
    tituladas1['tipo'] = 'Titled women' # A column with the type 'Titles' is added
    madres1 = brecha_nac1.groupby(['Anio'])[['Nacidos_madres']].sum().rename(columns={'Nacidos_madres':'cantidad'}).reset_index()
    madres1['tipo'] = 'Teenage mothers' # A column with the type 'Teen Mothers' is added

    # We join the two previous dataframes
    tm = pd.merge(tituladas1, madres1, how = 'outer', on = ['Anio','cantidad','tipo'])
    
    # We created a bar chart where the relationship of graduates with teenage mothers per year can be visualized
    
    # ---- Graph ------
    fig = px.bar(tm, x = 'Anio', y = 'cantidad', color = 'tipo', barmode = 'group', width = 580, height = 350,
             color_discrete_sequence = ['#A6FAC7','#68BAE3']
             )
    
    # --- Details ---
    fig.update_layout(
        template = 'simple_white',
        legend_title = 'Evolution in the year according to:',
        xaxis_title = '<b>Region<b>',
        yaxis_title = '<b>Quantity<b>',
        plot_bgcolor = 'rgba(0,0,0,0)',
        
        legend=dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor = "right",
            x = 0.8)
    )
    
    # ---- Show Graph -----
    c1.plotly_chart(fig)

# ---------------------------------- Historical Regional Unemployment Rate by Gender -----------------------------------    
    
    # ------ Title ------ 
    c2.markdown("<h3 style ='text-align: center; color:#169AA3;'>Historical Regional Unemployment Rate by Gender</h3>", unsafe_allow_html =True)
    
    # We create two dataframes where each unemployment rate of each gender is grouped by region in order to obtain a column that contains information on the gender
    # Each gender rate is renamed by quantity so that we can create a column that is in common and we will call it rate
    desocupados = brecha_des1.groupby(['Region'])[['Tasa_des_hombres']].mean().rename(columns={'Tasa_des_hombres':'tasa'}).reset_index()
    desocupados['tipo'] = 'Men'
    desocupadas = brecha_des1.groupby(['Region'])[['Tasa_des_mujeres']].mean().rename(columns={'Tasa_des_mujeres':'tasa'}).reset_index()
    desocupadas['tipo'] = 'Women'
    
    # We join the two dataframes and obtain a table that contains the unemployment rate of each region and to which gender it belongs
    des = pd.merge(desocupados, desocupadas, how = 'outer', on = ['Region','tasa','tipo']).sort_values(by="tasa", ascending= False)
   
    # ---- Graph ------
    fig = px.bar(des, x ='Region', y = 'tasa', color = 'tipo', barmode = 'group', width = 750, height = 350,
             color_discrete_sequence = ['#A6FAC7','#68BAE3']
             ) 
    
    # --- Details ---
    fig.update_layout(
        template = 'simple_white',
        legend_title = 'Evolution in the year according to:',
        xaxis_title = '<b>Region<b>',
        yaxis_title = '<b>Quantity<b>',
        plot_bgcolor = 'rgba(0,0,0,0)',
        
        legend=dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor="right",
            x = 0.8)
    )
    
    # ---- Show Graphic -----
    c2.plotly_chart(fig)

# --------- Page Partition----------  
    c3, c4 = st.columns((1,1))

# ---------------------------------- Variation in the Relationship between Mothers and Graduates of the Year 2019 Compared to 2018 -----------------------------------    
    
    # ------ Title ------ 
    c3.markdown("<h3 style ='text-align: center; color:#169AA3;'>Variation in the Relationship between Mothers and Graduates of the Year 2019 Compared to 2018</h3>", unsafe_allow_html =True)
    
    # Filtered by year 2018 and grouped by year and region for women graduates and for teenage mothers
    brecha2018t = brecha_tit1[brecha_tit1['Anio'] == 2018].groupby(['Anio', 'Region'])[['Mujeres_tituladas']].sum().reset_index()
    brecha2018n = brecha_nac1[brecha_nac1['Anio'] == 2018].groupby(['Anio', 'Region'])[['Nacidos_madres']].sum().reset_index()
    
    # Filtered by year 2019 and grouped by year and region for women graduates and for teenage mothers
    brecha2019t = brecha_tit1[brecha_tit1['Anio'] == 2019].groupby(['Anio', 'Region'])[['Mujeres_tituladas']].sum().reset_index()
    brecha2019n = brecha_nac1[brecha_nac1['Anio'] == 2019].groupby(['Anio', 'Region'])[['Nacidos_madres']].sum().reset_index()
    
    # The merge is done for the dataframes of each year
    brecha2018 = pd.merge(brecha2018t, brecha2018n, how = 'outer', on = ['Anio', 'Region'])
    brecha2019 = pd.merge(brecha2019t, brecha2019n, how = 'outer', on = ['Anio', 'Region'])
        
    # Proportion between teenage mothers and women graduates for each year
    brecha2018['Prop2018'] = brecha2018['Nacidos_madres']/brecha2018['Mujeres_tituladas']
    brecha2019['Prop2019'] = brecha2019['Nacidos_madres']/brecha2019['Mujeres_tituladas']
    
    # Percentage change
    brecha2019['var_prop'] = round((brecha2019['Prop2019'] - brecha2018['Prop2018'])/brecha2018['Prop2018'], 2)*100
    
    # The dataframe is filtered with the proportion difference for each region 
    bdiff = brecha2019[['Region', 'var_prop']].sort_values(by = 'var_prop')   
    
    # ---- Graph ------
    fig = px.bar(bdiff, x = 'Region', y = 'var_prop',                 
                 barmode = 'group',
                 color_discrete_sequence = ['#A6FAC7'], 
                 width = 640, height = 450)

    # --- Detalles ---
    fig.update_layout(
        template = 'simple_white',
        xaxis_title = '<b>Region<b>',
        yaxis_title = '<b>Percentage change<b>',
        plot_bgcolor = 'rgba(0,0,0,0)'
        )    
    
    # ---- Show Graph -----
    c3.plotly_chart(fig)

# ---------------------------------- % Maximum Gender Gap per Year -----------------------------------       
    
    # ------ Title ------
    c4.markdown("<h3 style ='text-align: center; color:#169AA3;'>% Maximum Gender Gap per Year</h3>", unsafe_allow_html = True)
    
    # The gender gap is grouped by year, taking the maximum value for each year
    bd = brecha_des1.groupby(['Anio'])[['Brecha_genero']].max().reset_index()
    
    # ---- Graph ------
    fig = px.pie(bd, values = 'Brecha_genero', names = 'Anio',
                 width = 520, height = 520,
                 color_discrete_sequence = ['#1b4f72','#21618c','#2874a6','#2e86c1','#3498db','#5dade2','#85c1e9','#aed6f1','#d6eaf8','#ebf5fb'])
    
    # --- Detalles ---
    fig.update_layout(
        template = 'simple_white',
        legend_title = '<b> Year<b>',
        title_x = 0.5,
        
    legend=dict(
        yanchor = "bottom",
        y = 0.2,
        xanchor = "right",
        x = 1.4))
    
    c4.plotly_chart(fig)
    
# --------- Page Division ---------- 
    c1, c2 = st.columns((1,1))
    
# ---------------------------------- Behavior of Paternity Regarding Unemployed Men -----------------------------------        
    
    # ------ Title ------
    c1.markdown("<h3 style ='text-align: center; color:#169AA3;'>Behavior of Paternity Regarding Unemployed Men</h3>", unsafe_allow_html =True)
    
    # How is the behavior of fatherhood with regard to unemployed men?    
    brecha_nac2 = brecha_nac1[brecha_nac1['Tramos_edad'] == '15 a 19 años']
    desocupados = brecha_des1.groupby(['Anio'])[['Tasa_des_hombres']].mean()
    padres = brecha_nac2.groupby(['Anio'])[['Porc_nacidos_padres']].mean()
    tabla = pd.DataFrame()
    tabla['Tasa_des_hombres'] = desocupados['Tasa_des_hombres']
    tabla['Porc_nacidos_padres'] = padres['Porc_nacidos_padres']
    tabla['Relacion'] = (round(tabla['Porc_nacidos_padres']/tabla['Tasa_des_hombres'],2)*100)
    tabla = tabla.reset_index()
    
    # ---- Graph ------
    fig = px.line(tabla, x = 'Anio', y = ['Relacion'],
                  color_discrete_sequence = px.colors.qualitative.G10, width = 650, height = 450,labels=False)
    
    # --- Details ---
    fig.update_layout(
        template = 'simple_white',
        xaxis_title = '<b>Date<b>',
        yaxis_title = '<b>Teen Parents Rate / Male Unemployment Rate<b>',
        plot_bgcolor = 'rgba(0,0,0,0)',
        
         
    )

    c1.plotly_chart(fig)
    
# ---------------------------------- Maternity Behavior Regarding Unemployed Mothers -----------------------------------   
    
    # ------ Title ------
    c2.markdown("<h3 style ='text-align: center; color:#169AA3;'>Maternity Behavior Regarding Unemployed Women</h3>", unsafe_allow_html =True)
    
        #How is the behavior of motherhood with respect to unemployed women in 2019?
    brecha_nac2=brecha_nac1[brecha_nac1['Tramos_edad']=='15 a 19 años']
    desocupados=brecha_des1.groupby(['Anio'])[['Tasa_des_mujeres']].mean()
    padres=brecha_nac2.groupby(['Anio'])[['Porc_nacidos_madres']].mean()
    tabla=pd.DataFrame()
    tabla['Tasa_des_mujeres']=desocupados['Tasa_des_mujeres']
    tabla['Porc_nacidos_madres']=padres['Porc_nacidos_madres']
    tabla['Relacion']=(round(tabla['Porc_nacidos_madres']/tabla['Tasa_des_mujeres'],2)*100)
    tabla= tabla.reset_index()
    
    # ---- Graph ------
    fig = px.line(tabla, x='Anio', y =['Relacion'], 
                  color_discrete_sequence=px.colors.qualitative.G10, width =650, height=450)
    
    # --- Details ---
    fig.update_layout(
        template = 'simple_white',
        xaxis_title = '<b>Date<b>',
        yaxis_title = '<b>Teenage mothers rate / Female unemployment rate<b>',
        plot_bgcolor='rgba(0,0,0,0)',
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.8)
        )
    
    c2.plotly_chart(fig)

# --------- Page Division ----------     
    c1, c2 = st.columns((1,1))
    
# ---------------------------------- Regions with the most Adolescent Mothers and Fathers in 2019 -----------------------------------   
        
    # ------ Title ------
    c1.markdown("<h3 style ='text-align: center; color:#169AA3;'>Regions with the most Adolescent Mothers and Fathers in 2019</h3>", unsafe_allow_html =True)
    
    # The three regions with the most teenage mothers and fathers in 2019 are filtered on an individual bases
    madres2019 = brecha_nac1[brecha_nac1['Anio'] == 2019][['Anio', 'Region', 'Tramos_edad', 'Nacidos_madres']].rename(columns = {'Nacidos_madres':'quantity'}).sort_values(by = 'quantity', ascending = False).head(3)
    padres2019 = brecha_nac1[brecha_nac1['Anio'] == 2019][['Anio', 'Region', 'Tramos_edad', 'Nacidos_padres']].rename(columns = {'Nacidos_padres':'quantity'}).sort_values(by = 'quantity', ascending = False).head(3)
    
    # Columns with gender are added
    madres2019['genero'] = 'Mothers'
    padres2019['genero'] = 'Fathers'
    
    # The merge between the bases of mothers and fathers is done
    pm = pd.merge(madres2019, padres2019, how = 'outer', on = ['Anio',	'Region', 'Tramos_edad', 'quantity', 'genero'])
    
    # ---- Graph ------
    fig = px.bar(pm, x = 'Region', y = 'quantity', color = 'genero',
                 barmode = 'group',
                 hover_data =['Tramos_edad'],
                 color_discrete_sequence = ['#A6FAC7','#68BAE3'])
    
    # --- Detalles ---
    fig.update_layout(
        template = 'simple_white',
        title_x = 0.5,
        legend_title = 'Evolution in the year according to:',
        xaxis_title = '<b>Region<b>',
        yaxis_title = '<b>Quantity<b>',
        plot_bgcolor = 'rgba(0,0,0,0)',
        
        legend = dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor = "right",
            x = 0.8)
        )
    
    c1.plotly_chart(fig, use_container_width = True)
    
# -------------------- Historical Percentage of Titles by Gender in the 3 Regions with the Most Persons Graduated ----------------------     
    
    # ------ Title ------
    c2.markdown("<h3 style ='text-align: center; color:#169AA3;'>Historical Percentage of Titles by Gender in the 3 Regions with the Most Persons Graduated</h3>", unsafe_allow_html =True)
    
    #We created two dataframes from the data warehouse ofbrecca_tit1, grouping the number of female graduates and teenage mothers for each year.
    tituladas1 = brecha_tit1.groupby(['Region'])[['Tituladas']].sum().rename(columns={'Tituladas':'cantidad'}).reset_index().sort_values(by = "cantidad", ascending = False)
    tituladas1['tipo'] = 'Tituladas'
    madres1 = brecha_nac1.groupby(['Anio'])[['Nacidos_madres']].sum().rename(columns={'Nacidos_madres':'cantidad'}).reset_index()
    madres1['tipo'] = 'Madres Adolescentes'
    tone = tituladas1.head(3)
        
    #We create two dataframes that have the number of graduates of each gender grouped by region and we add a column whose values indicate what gender it is
    porch = brecha_tit1.groupby(['Region'])[['Porc_hombres_t']].mean().reset_index().rename(columns = {'Porc_hombres_t':'Porc'})
    porch['genero'] = 'Man' 
    porch['Porc'] = round(porch['Porc'],2)
    porcm = brecha_tit1.groupby(['Region'])[['Porc_mujeres_t']].mean().reset_index().rename(columns = {'Porc_mujeres_t':'Porc'})
    porcm['genero'] = 'Woman'
    porcm['Porc'] = round(porcm['Porc'], 2)
    
    porc = pd.merge(porch, porcm, how = 'outer', on = ['Region','genero','Porc'])
    porcg = pd.merge(porc, tone, how = 'inner', on = ['Region'])
    
    #We create a sunray graph to represent the previous dataframe
    fig = px.sunburst(porcg, path=['Region','Porc',], color='genero', color_discrete_sequence=['#A6FAC7','#1AB3EC','#A0FEFF'], values='Porc')
    
    #Legend    
    D = porc['genero'].unique() # We generate the list of genera shown in the diagram
    colors = [ '#1AB3EC', # the color of mens
             '#A6FAC7'] # The color of womens
    for i, m in enumerate(D):  # We create the legend
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

# -------------------- Average Salary Gap by Region ----------------------
    # ------ Title ------ 
    st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Average Salary Gap by Region</h3>", unsafe_allow_html =True)      
    
    # ---- Graph ------
    fig = px.bar(salario1, x = 'region', y='Brecha_promedio', barmode = 'group', width =650, height=500)
                 
    # --- Details ---
    fig.update_layout(
        xaxis_title = 'Region',
        yaxis_title = 'Percentage gap',
        template = 'simple_white',
        title_x = 0.5,
        plot_bgcolor='rgba(0,0,0,0)')
    
    st.plotly_chart(fig, use_container_width = True)
        
    st.markdown('---') # Division Line

    # ------ Title ------    
    st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Relationship between Titles and Population</h3>", unsafe_allow_html =True)
    
    poblacion = poblacion.sort_values(by='Region') # Regions are arranged in alphabetical order.
    
    # Selectbox de lo que se mostrará en el mapa
    genero_map = st.selectbox('Seleccione el género:', options = ['Titled Women', 'Titled Men', 'Titled Women/Population', 'Titled Men/Population'])
    
    # Crear bases con el código de región para hacer el join con el geojson
    base1 = brecha_tit1.groupby(['Region', 'Codigo_region'])[['Mujeres_tituladas']].sum().reset_index().rename(columns = {'Codigo_region':'codregion','Mujeres_tituladas':'Indicador'})
    base2 = brecha_tit1.groupby(['Region', 'Codigo_region'])[['Hombres_titulados']].sum().reset_index().rename(columns = {'Codigo_region':'codregion','Hombres_titulados':'Indicador'})
    
    
    # Condicional en función del selectbox
    if genero_map == 'Titled Women':
        st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Titled women</h3>", unsafe_allow_html =True)
        base = base1   # Women graduates are shown by region
    elif genero_map == 'Titled Men':
        st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Titled Men</h3>", unsafe_allow_html =True)
        base = base1  # The Titled Men by region are showing 
    elif genero_map == 'Titled Women/Population':
        st.markdown("<h3 style ='text-align: center; color:#169AA3;'>Mujeres Tituladas/Población</h3>", unsafe_allow_html =True)
        base = base1 
        base['Indicador'] = base1['Indicador']/poblacion['Total'] # Women graduates are shown by region/total population
    elif genero_map == 'Titled Men/Population':
        st.markdown("<h3 style ='text-align: center; color:#169AA3;'>'Titled Men/Population'</h3>", unsafe_allow_html =True)
        base = base2
        base['Indicador'] = base2['Indicador']/poblacion['Total'] # Se muestra las hombres titulados por región/población total  
     
    # ---- Graph ------
    min = base['Indicador'].min() # generate minimum of color range
    max = base['Indicador'].max() # generate maximum of color range
    
    fig = px.choropleth_mapbox( base, # dataframe that has the indicator
                  geojson = gj_com, # json file with the shape
                  color = 'Indicador', # column containing the indicator: value on which the color tone will be given
                  locations = 'codregion', # key of the dataframe to do the join with the shape
                  featureidkey = 'properties.codregion', # key of the shape to do the join with the dataframe
                  color_continuous_scale = 'Viridis', # color scale to be used
                  range_color =(max, min), # ranges between which the color will vary
                  hover_name = 'Region', # information to be observed when the cursor is passed over the polygon
                  center = {'lat':	-39.675147, 'lon': -71.542969}, # centro en el cual se va ubicar el mapa, ubicado a conveniencia
                  zoom = 3.5, # zoom of the image
                  mapbox_style = "carto-positron", height = 950) # map style
    
    fig.update_geos(fitbounds = 'locations', visible = False) # adjust to shape bounds
    
    st.plotly_chart(fig, use_container_width = True)  

# -------- Conditional to Enter the Content to the Bases Menu --------    
if menu_id == 'Bases':

# -------- Gender Gap between Adolescent Paternity and Maternity --------     
    # ------ Title ------ 
    st.markdown("<h3 style ='text-align: center; color: #169AA3;'>Gender Gap in Adolescent Paternity and Maternity</h3>", unsafe_allow_html =True)

    # Dataframe to display
    df1 = brecha_nac1    
    
    # Multiselect to filter by year
    anio1 = st.multiselect(
        "Select the year here:",
        options = df1['Anio'].unique(),
        default = df1['Anio'].unique())
    
    # Regions by which you can filter
    region_list = ['Todas','Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama',
       'Coquimbo', 'Valparaíso', 'Metropolitana', "O'Higgins", 'Maule',
       'Ñuble', 'Biobío', 'La Araucanía', 'Los Ríos', 'Los Lagos',
       'Aysén', 'Magallanes']
    
    # Regions Selectbox
    region1 = st.selectbox('Select the region here:', region_list, key = '1')
    
    # Conditional depending on the chosen possibilities
    if  region1 == 'Todas':
        df_selection = df1.query(
            "Anio == @anio1")
    else:
        df_selection = df1.query(
            "Anio == @anio1 & Region == @region1")
    
    # Dataframe with filters to display
    df1 = df_selection
    
    # Organize Table
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
    

# -------- Gender Gap in Unemployment--------
    
    # ------ Title ------
    st.markdown("<h3 style = 'text-align: center; color: #169AA3;'>Gender Gap in Unemployment</h3>", unsafe_allow_html = True)
    
    # Dataframe to display
    df2 = brecha_des1
    
    # Multiselect for filter by year
    anio2 = st.multiselect(
        "Select the year here:",
        options = df2['Anio'].unique(),
        default = df2['Anio'].unique(), key = '2')
    
    # Regions by which you can filter
    region_list = ['Todas','Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama',
       'Coquimbo', 'Valparaíso', 'Metropolitana', "O'Higgins", 'Maule',
       'Ñuble', 'Biobío', 'La Araucanía', 'Los Ríos', 'Los Lagos',
       'Aysén', 'Magallanes']
    
    # Selectbox of the regions
    region2 = st.selectbox('Select the regions here:', region_list, key = '3')
    
    # Conditional depending on the chosen possibilities
    if  region2 == 'Todas':
        df_selection = df2.query(
            "Anio == @anio2")
    else:
        df_selection = df2.query(
            "Anio == @anio2 & Region == @region2")

    # Dataframe with filters to show
    df2 = df_selection
    
    # Organize Table
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
    
# -------- Gender Gap in Professional Degrees --------
    
    # ------ Title ------
    st.markdown("<h3 style ='text-align: center; color: #169AA3;'>Gender Gap in Professional Degrees</h3>", unsafe_allow_html =True)
    
    # Dataframe to display
    df3 = brecha_tit1
    
    # Multiselect for filter by year
    anio3 = st.multiselect(
        "Seleccione el año aquí:",
        options = df3['Anio'].unique(),
        default = df3['Anio'].unique(), key = '5')
    
    # Regions by which you can filter
    region_list = ['Todas','Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama',
       'Coquimbo', 'Valparaíso', 'Metropolitana', "O'Higgins", 'Maule',
       'Ñuble', 'Biobío', 'La Araucanía', 'Los Ríos', 'Los Lagos',
       'Aysén', 'Magallanes']
    
    # Selectbox of the regions
    region3 = st.selectbox('Select the region here:', region_list, key = '4')
    
    # Conditional depending on the chosen possibilities
    if  region3 == 'Todas':
        df_selection = df3.query(
            "Anio == @anio3")
    else:
        df_selection = df3.query(
            "Anio == @anio3 & Region == @region3")

    # Dataframe with filters to display
    df3 = df_selection

    # Organize Tabla
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
    
    
    # ------ Download the files in CSV format -------
    st.markdown(get_table_download_link(df1,'brecha_paternidad_maternidad'), unsafe_allow_html=True)
    st.markdown(get_table_download_link(df2,'brecha_desocupacion'), unsafe_allow_html=True)
    st.markdown(get_table_download_link(df3,'brecha_titulos'), unsafe_allow_html=True)


if menu_id == 'Videos':
    
    # ------ Video 1 -------
    c1, c2 = st.columns((1,1))
    c1.markdown("<h3 style ='text-align: center; color:#169AA3;'>Challenges for Gender Equality</h3>", unsafe_allow_html =True)   
    c1.video("https://youtu.be/KSwJQrhxH14")
    c1.markdown('<div style="text-align: justify;">In this context, there are cultural, educational and family democracy challenges that are priorities, the sources agree. One is the great social barrier that inhibits womens participation: they continue to be the main people in charge of the household and the care of people who require attention: children, the sick or the elderly.</div>', unsafe_allow_html=True)
    
    # ------ Video 2 -------
    c2.markdown("<h3 style ='text-align: center; color:#169AA3;'>More Women in Science</h3>", unsafe_allow_html =True)
    c2.video("https://youtu.be/Yuki-g9sgLw")
    c2.markdown('<div style="text-align: justify;">Encourage, promote and encourage more young women to choose careers focused on science, technology, engineering and mathematics, not only to increase female labor participation, but also to increase the participation of women in historically masculinized careers. Until now, there has been a low participation of women in STEM careers due to a series of gaps resulting from stereotypes that are reproduced from childhood.</div>', unsafe_allow_html=True)

    # ------ Video 3 -------
    c3, c4 = st.columns((1,1))
    c3.markdown("<h3 style ='text-align: center; color:#169AA3;'>Gender in the Financial System</h3>", unsafe_allow_html =True)
    c3.video("https://youtu.be/9INYaVbHiCY")
    c3.markdown('<div style="text-align: justify;">The Report on Gender in the Financial System 2021, with a statistical close as of March this year, revealed sustained progress in closing gender gaps associated with the use of financial services.</div>', unsafe_allow_html=True)
    
    # ------ Video 4 -------    
    c4.markdown("<h3 style ='text-align: center; color:#169AA3;'>Gap's evaluation in the investigation trayectory</h3>", unsafe_allow_html =True)
    c4.video("https://www.youtube.com/watch?v=9OUiga-9VuI&feature=emb_imp_woyt")
    c4.markdown('<div style="text-align: justify;">Gender study that evaluates and quantifies the possible existence of barriers that women beneficiaries of public programs in Chile may have during their research trajectories.</div>', unsafe_allow_html=True)