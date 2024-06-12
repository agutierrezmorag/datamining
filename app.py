import pandas as pd
import streamlit as st

from helper_functions import extended_describe


def main():
    st.set_page_config(
        page_title="Satisfaccion del Cliente", page_icon=":airplane:", layout="wide"
    )
    st.title("Satisfaccion del Cliente")

    data = pd.read_csv("data/airline_merged_clean.csv")
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


if __name__ == "__main__":
    main()
