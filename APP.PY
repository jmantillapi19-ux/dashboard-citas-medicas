import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página (Debe ser la primera línea de Streamlit)
st.set_page_config(
    page_title="Dashboard Hospital Lima Norte",
    page_icon="🏥",
    layout="wide" # Hace que el contenido ocupe toda la pantalla
)

# Cargar datos
df = pd.read_csv('citas_medicas.csv')

# --- ENCABEZADO PERSONALIZADO ---
st.markdown("<h1 style='text-align: center; color: #0083B0;'>📊 Plataforma Inteligente de Gestión de Citas</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Análisis de rendimiento, demanda y comportamiento de pacientes - Hospital Lima Norte</p>", unsafe_allow_html=True)
st.write("---")

# --- SECCIÓN DE MÉTRICAS CLAVE (KPIs) ---
total_citas = len(df)
porcentaje_canceladas = (df['estado'] == 'Cancelada').sum() / total_citas * 100
edad_promedio = df['edad'].mean()

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="Total Citas Simuladas", value=f"{total_citas:,}")
with col_m2:
    st.metric(label="Tasa de Cancelación", value=f"{porcentaje_canceladas:.1f}%", delta="-1.5% vs mes anterior")
with col_m3:
    st.metric(label="Edad Promedio Pacientes", value=f"{edad_promedio:.1f} años")

st.write("---")

# --- SECCIÓN DE GRÁFICOS (En 2 Columnas) ---
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader('🏢 Demandas por Especialidad Médica')
    # Gráfico de barras ordenado y con paleta de colores continua
    conteo_esp = df['especialidad'].value_counts().reset_index()
    conteo_esp.columns = ['Especialidad', 'Cantidad']
    
    fig1 = px.bar(
        conteo_esp,
        x='Especialidad',
        y='Cantidad',
        color='Cantidad',
        color_continuous_scale='Blues', # Cambia el color plano por un degradado
        text_auto=True # Muestra el número exacto encima de cada barra
    )
    fig1.update_layout(showlegend=False) # Quita leyendas innecesarias
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    st.subheader('🎯 Estado General de las Citas')
    # Gráfico de pastel estilizado (Donut chart) con colores corporativos
    fig2 = px.pie(
        df,
        names='estado',
        hole=0.4, # Convierte el pastel en un anillo/dona moderna
        color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12'] # Verde, Rojo, Amarillo
    )
    fig2.update_traces(textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

# --- SECCIÓN DE TENDENCIA TEMPORAL (Ancho completo abajo) ---
st.write("---")
st.subheader('📈 Evolución y Tendencia de Citas por Mes')

df['fecha'] = pd.to_datetime(df['fecha'])
df['mes'] = df['fecha'].dt.month
citas_mes = df.groupby('mes').size().reset_index(name='cantidad')

fig3 = px.line(
    citas_mes,
    x='mes',
    y='cantidad',
    markers=True,
    line_shape='spline', # Suaviza la línea para que sea curva y estilizada
    color_discrete_sequence=['#0083B0']
)
fig3.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1)) # Asegura meses del 1 al 12
st.plotly_chart(fig3, use_container_width=True)