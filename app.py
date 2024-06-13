import pandas as pd
import plotly.express as px
import streamlit as st

from helper_functions import extended_describe


def set_font_size(fig):
    size = 24
    fig.update_layout(
        font=dict(
            size=size,
        ),
        title_font=dict(
            size=size,
        ),
        legend=dict(
            font=dict(
                size=size,
            )
        ),
        xaxis=dict(
            title_font=dict(
                size=size,
            ),
            tickfont=dict(
                size=size,
            ),
        ),
        yaxis=dict(
            title_font=dict(
                size=size,
            ),
            tickfont=dict(
                size=size,
            ),
        ),
    )
    return fig


@st.cache_data
def get_df():
    return pd.read_csv("data/airline_merged_clean.csv")


@st.cache_data
def display_tables(data):
    st.dataframe(data)

    with st.expander("Atributos"):
        st.markdown("""
        | Variable | Description |
        | --- | --- |
        | **Gender** | Género de los pasajeros (Femenino, Masculino) |
        | **Customer Type** | El tipo de cliente (Cliente leal, cliente desleal) |
        | **Age** | La edad actual de los pasajeros |
        | **Type of Travel** | Propósito del vuelo de los pasajeros (Viaje personal, Viaje de negocios) |
        | **Class** | Clase de viaje en el avión de los pasajeros (Negocios, Económica, Económica Plus) |
        | **Flight Distance** | La distancia del vuelo de este viaje |
        | **Inflight Wifi Service** | Nivel de satisfacción con el servicio de wifi a bordo (0: No aplicable; 1-5) |
        | **Departure/Arrival Time Convenient** | Nivel de satisfacción con la comodidad de la hora de salida/llegada |
        | **Ease of Online Booking** | Nivel de satisfacción con la reserva en línea |
        | **Gate Location** | Nivel de satisfacción con la ubicación de la puerta de embarque |
        | **Food and Drink** | Nivel de satisfacción con la comida y bebida |
        | **Online Boarding** | Nivel de satisfacción con el embarque en línea |
        | **Seat Comfort** | Nivel de satisfacción con la comodidad del asiento |
        | **Inflight Entertainment** | Nivel de satisfacción con el entretenimiento a bordo |
        | **On-board Service** | Nivel de satisfacción con el servicio a bordo |
        | **Leg Room Service** | Nivel de satisfacción con el servicio de espacio para las piernas |
        | **Baggage Handling** | Nivel de satisfacción con el manejo del equipaje |
        | **Check-in Service** | Nivel de satisfacción con el servicio de check-in |
        | **Inflight Service** | Nivel de satisfacción con el servicio a bordo |
        | **Cleanliness** | Nivel de satisfacción con la limpieza |
        | **Departure Delay in Minutes** | Minutos de retraso en la salida |
        | **Arrival Delay in Minutes** | Minutos de retraso en la llegada |
        | **Satisfaction** | Nivel de satisfacción con la aerolínea (Satisfacción, neutral o insatisfacción) |
                    """)

    return data


@st.cache_data
def display_descriptive_stats(data):
    st.dataframe(extended_describe(data))


def display_charts(data):
    col1, col2, col3 = st.columns(3)

    with col1:
        # Calculate the counts
        counts = data["Type Of Travel"].value_counts()

        # Convert the counts to a DataFrame
        df_counts = pd.DataFrame(
            {"Type Of Travel": counts.index, "Count": counts.values}
        )

        # Create a bar chart for 'Type Of Travel' using Plotly
        fig = px.bar(
            data_frame=df_counts,
            x="Type Of Travel",
            y="Count",
            color="Type Of Travel",
            color_discrete_map={
                "Personal Travel": "LightSkyBlue",
                "Business travel": "OliveDrab",
            },
            text="Count",
            title="Total de pasajeros por Tipo de Viaje",
            labels={
                "Type Of Travel": "Tipo de Viaje",
                "Count": "Pasajeros",
            },
        )

        fig.update_traces(textposition="auto", textfont_color="white")
        fig = set_font_size(fig)
        st.plotly_chart(fig)

    with col2:
        # Get counts of each gender
        gender_counts = data["Gender"].value_counts()

        # Create a pie chart
        fig = px.pie(
            gender_counts,
            values=gender_counts.values,
            names=gender_counts.index,
            color=gender_counts.index,
            color_discrete_map={"Female": "Orchid", "Male": "CornflowerBlue"},
            title="Distribución de género de los pasajeros",
        )

        # Add percentage and value to the labels
        fig.update_traces(textinfo="label+percent+value", textfont_color="white")
        fig = set_font_size(fig)
        st.plotly_chart(fig)

    with col3:
        fig = (
            data["Satisfaction"]
            .value_counts()
            .reset_index()
            .rename(columns={"Satisfaction": "Satisfaction", "count": "Count"})
            .pipe(
                px.pie,
                names="Satisfaction",
                values="Count",
                color="Satisfaction",
                color_discrete_map={
                    "Neutral or Dissatisfied": "Crimson",
                    "Satisfied": "Chartreuse",
                },
                title="Distribución de satisfacción de los pasajeros",
                labels={
                    "Satisfaction": "Nivel de Satisfacción",
                    "Count": "Pasajeros",
                },
            )
            .update_traces(
                textposition="inside",
                textinfo="percent+label+value",
                textfont_color="white",
            )
        )

        fig = set_font_size(fig)
        st.plotly_chart(fig)

    with col1:
        fig = px.histogram(
            data,
            x="Flight Distance",
            nbins=50,
            title="Distribución de Distancia de Vuelo",
            color_discrete_sequence=["#636EFA"],
            template="plotly_dark",
        )

        fig.update_traces(textposition="inside", texttemplate="%{y}", textfont_size=28)

        fig.update_layout(
            xaxis_title_text="Distancia de Vuelo",
            yaxis_title_text="Vuelos",
            bargap=0.2,
            bargroupgap=0.1,
        )

        fig = set_font_size(fig)
        st.plotly_chart(fig)


def main():
    st.set_page_config(
        page_title="Satisfaccion del Cliente", page_icon=":airplane:", layout="wide"
    )

    st.title("🙋‍♂️ :blue[Satisfaccion del Cliente]")
    data = get_df()
    display_tables(data)

    st.subheader("🔍 :blue[Estadísticas descriptivas]")
    display_descriptive_stats(data)

    st.subheader("🕵️ :blue[Visualizaciones]")
    option_col1, option_col2 = st.columns(2)
    with option_col1:
        plot_type = st.selectbox(
            "Seleccione un tipo de gráfico", ["Histograma", "Linea", "Box Plot"]
        )
    with option_col2:
        column = st.selectbox("Seleccione una columna", data.columns)

    if plot_type == "Histograma":
        fig = px.histogram(data, x=column)
    elif plot_type == "Linea":
        fig = px.line(data, x=column)
    elif plot_type == "Box Plot":
        fig = px.box(data, x=column)
    fig.update_layout(title=f"{plot_type} de {column}")
    fig = set_font_size(fig)
    st.plotly_chart(fig)

    st.subheader("📊 :blue[Gráficos]")
    display_charts(data)


if __name__ == "__main__":
    main()
