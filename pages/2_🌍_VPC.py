import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Calculadora VPC Endpoint', layout='wide')

st.title('Calculadora de Costos VPC Endpoint')

st.image("vpcdp.jpg", caption="EndPoints summary")

with st.sidebar.form('vpc_calculator'):
    tarifa_hora = st.number_input('Tarifa por hora por AZ ($)', min_value=0.0, value=0.01, step=0.01)
    num_az = st.number_input('Número de AZ', min_value=1, value=1, step=1)
    num_horas = st.number_input('Número de horas en el mes', min_value=1, value=730, step=1)
    tarifa_gb = st.number_input('Tarifa por GB ($)', min_value=0.0, value=0.01, step=0.01)
    gb_procesados = st.number_input('Cantidad de GB procesados', min_value=0.0, value=0.0, step=0.1)
    submitted = st.form_submit_button('Calcular')

if submitted:
    # Cálculos
    costo_hora = tarifa_hora * num_az
    costo_mensual_az = costo_hora * num_horas
    costo_datos = tarifa_gb * gb_procesados
    total = costo_mensual_az + costo_datos
    
    # Mostrar resultados
    st.header('Resultados del Cálculo')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric('Costo por hora', f'${costo_hora:.2f}')
        st.metric('Costo mensual por AZ', f'${costo_mensual_az:.2f}')
        st.metric('Costo por datos', f'${costo_datos:.2f}')
        st.metric('Total mensual', f'${total:.2f}', delta=None)
    
    with col2:
        # Crear datos para el gráfico
        data = pd.DataFrame({
            'Concepto': ['Costo mensual por AZ', 'Costo por datos'],
            'Monto': [costo_mensual_az, costo_datos]
        })
        
        # Crear gráfico de barras
        fig = px.bar(
            data,
            x='Concepto',
            y='Monto',
            title='Desglose de Costos',
            labels={'Monto': 'Costo ($)', 'Concepto': ''},
            color='Concepto'
        )
        st.plotly_chart(fig)

# Agregar información adicional
with st.expander('Información sobre el cálculo'):
    st.write("""
    ### Fórmulas utilizadas:
    
    1. **Costo por hora**: 
       - Costo por hora = Tarifa por hora por AZ × Número de AZ
    
    2. **Costo mensual por AZ**:
       - Costo mensual = Costo por hora × Número de horas en un mes
    
    3. **Costo por procesamiento de datos**:
       - Costo por datos = Tarifa por GB × Cantidad de GB procesados
    
    4. **Total mensual**:
       - Total = Costo mensual por AZ + Costo por datos
    """)