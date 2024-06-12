import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from helper_functions import extended_describe


@st.cache_data
def get_df():
    return pd.read_csv("data/airline_merged_clean.csv")


@st.cache_data
def load_data():
    data = get_df()
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

    st.subheader("Estadísticas descriptivas")
    st.dataframe(extended_describe(data))


def main():
    st.set_page_config(
        page_title="Satisfaccion del Cliente", page_icon=":airplane:", layout="wide"
    )
    st.title("Satisfaccion del Cliente")

    data = get_df()
    load_data()

    col1, col2 = st.columns(2)

    with col1:
        # Create a bar chart for 'Type Of Travel' using Seaborn
        plt.figure(figsize=(8, 6))
        chart = sns.countplot(x="Type Of Travel", data=data, palette="viridis")
        chart.set_xticklabels(chart.get_xticklabels(), rotation=0)
        chart.set_title("Total de Pasajeros por Tipo de Viaje", weight="bold")
        chart.set_xlabel("Tipo de viaje", weight="bold")
        chart.set_ylabel("Pasajeros", weight="bold")

        # Add count annotations to each bar
        for p in chart.patches:
            chart.annotate(
                format(p.get_height(), ".0f"),
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="center",
                xytext=(0, 5),
                textcoords="offset points",
            )

        # Display the bar chart using Streamlit
        st.pyplot(plt.gcf())


if __name__ == "__main__":
    main()
