import pandas as pd
import streamlit as st

# Cargar datos desde el archivo local "rutinas.xlsx"
def cargar_datos_local():
    try:
        datos = pd.read_excel("rutinas.xlsx")
        datos.columns = datos.columns.str.strip()  # Limpia espacios en los nombres de columnas
        print("Columnas en el archivo:", datos.columns)  # Imprime los nombres para debug
        return datos
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío si hay error

# Función para filtrar las rutinas según los criterios seleccionados
def filtrar_rutinas(datos, nivel, dias, objetivo, genero, frecuencia):
    # Filtrar rutinas aplicables a ambos géneros si corresponde
    if genero in ["Masculino", "Femenino"]:
        datos_filtrados = datos[
            (datos["Nivel"] == nivel) &
            (datos["Días/Semana"] == dias) &
            (datos["Objetivo"] == objetivo) &
            ((datos["Género"] == genero) | (datos["Género"] == "Masculino, Femenino")) &
            (datos["Frecuencia"] == frecuencia)
        ]
    else:
        datos_filtrados = pd.DataFrame()  # Manejo de casos no esperados
    return datos_filtrados

# Aplicación principal
def app():
    st.markdown(
        """
        <div style="text-align: center">
            <h1 style="font-size: 3rem; font-weight: bold;">Smart Split</h1>
        </div>

        <div style="text-align: center">
            <p style="font-size: 1.3rem; color: gray;">Sponsored by MEGA GYM</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Cargar datos
    datos = cargar_datos_local()
    if datos.empty:
        st.error("No se pudieron cargar los datos. Revisa el archivo.")
        return

    # Filtrar opciones dinámicamente
    datos_filtrados = datos.copy()  # Declaración inicial para evitar errores si no se filtra nada.

    try:
        # Pregunta nivel
        nivel = st.selectbox("¿Cuál es tu nivel de experiencia?", options=["Selecciona una opción"] + datos_filtrados['Nivel'].unique().tolist())
        if nivel != "Selecciona una opción":
            datos_filtrados = datos_filtrados[datos_filtrados['Nivel'] == nivel]

        # Pregunta días
        dias = st.selectbox("¿Cuántos días a la semana puedes entrenar?", options=["Selecciona una opción"] + datos_filtrados['Días/Semana'].unique().tolist())
        if dias != "Selecciona una opción":
            datos_filtrados = datos_filtrados[datos_filtrados['Días/Semana'] == dias]

        # Pregunta objetivo
        objetivo = st.selectbox("¿Cuál es tu objetivo principal?", options=["Selecciona una opción"] + datos_filtrados['Objetivo'].unique().tolist())
        if objetivo != "Selecciona una opción":
            datos_filtrados = datos_filtrados[datos_filtrados['Objetivo'] == objetivo]

        # Pregunta género
        genero = st.selectbox("¿Cuál es tu género?", options=["Selecciona una opción", "Masculino", "Femenino"])
        if genero != "Selecciona una opción":
            datos_filtrados = datos_filtrados[(datos_filtrados['Género'] == genero) | (datos_filtrados['Género'] == "Masculino, Femenino")]

        # Pregunta frecuencia
        frecuencia_map = {1.0: "Baja", 1.5: "Media", 2.0: "Alta"}
        opciones_frecuencia = ["Selecciona una opción"] + [
            frecuencia_map[freq] for freq in datos_filtrados['Frecuencia'].unique()
            if freq in frecuencia_map
        ]
        frecuencia = st.selectbox("¿Qué frecuencia de entrenamiento prefieres?", options=opciones_frecuencia)
        if frecuencia != "Selecciona una opción":
            # Mapear de vuelta a los valores numéricos
            frecuencia_valor = {v: k for k, v in frecuencia_map.items()}.get(frecuencia)
            datos_filtrados = datos_filtrados[datos_filtrados['Frecuencia'] == frecuencia_valor]

        # Preguntas de personalización
        experiencia_previa = st.selectbox("¿Tienes experiencia previa con algún tipo de entrenamiento?", 
                                          options=["Selecciona una opción", "Ninguno", "Gym", "Entrenamiento en Casa", "Calistenia", "Crossfit", "Running", "Zumba", "Circuitos de Entrenamiento", "Yoga", "Pilates", "Hipopresivos", "Otras Opciones"])
        
        tiempo_disponible = st.selectbox("¿Cuánto tiempo al día dispones para entrenar?", 
                                         options=["Selecciona una opción", "<30 minutos", "30-60 minutos", ">60 minutos"])
        
        grupo_muscular = st.multiselect("¿En qué grupo muscular te quieres enfocar?", 
                                        options=["Pecho", "Espalda", "Brazos", "Hombros", "Piernas", "Glúteos", "Abdomen", "Pantorrillas"])
        
        condicion_medica = st.selectbox("¿Tienes alguna lesión o condición médica que debamos considerar?", 
                                        options=["Selecciona una opción", "No", "Sí"])

        # Validar si todas las preguntas fueron respondidas
        if st.button("Generar rutina"):
            if (
                nivel == "Selecciona una opción" or
                dias == "Selecciona una opción" or
                objetivo == "Selecciona una opción" or
                genero == "Selecciona una opción" or
                frecuencia == "Selecciona una opción" or
                experiencia_previa == "Selecciona una opción" or
                tiempo_disponible == "Selecciona una opción" or
                not grupo_muscular or  # Multiselect vacío
                condicion_medica == "Selecciona una opción"
            ):
                st.markdown(
            """
            <div style="
                background-color: #7a282e;
                color: #fcd7dc;
                padding: 15px 15px;
                border-radius: 5px;
                font-size: 16px;">
                Por favor, responde todas las preguntas antes de generar la rutina.
            </div>
            """,
            unsafe_allow_html=True
        )
            else:
                if not datos_filtrados.empty:
                    splits_recomendados = datos_filtrados['Split Recomendado'].unique().tolist()
                    st.success(f"Rutina generada exitosamente: {', '.join(splits_recomendados)}")
                else:
                    st.warning("No se encontraron rutinas que coincidan exactamente con tus criterios. Por favor ajusta tus respuestas.")

    except KeyError as e:
        st.error(f"Error en los datos: Falta la columna {e}. Verifica el archivo Excel.")

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
