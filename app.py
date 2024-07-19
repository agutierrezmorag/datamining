import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from helper_functions import extended_describe


def set_font_size(fig, size=36):
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
                "Personal Travel": "SandyBrown",  # Vibrant orange for personal travel
                "Business Travel": "#34495E",  # Navy blue for business travel
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
        fig.update_layout(showlegend=False)
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

        fig.update_traces(textinfo="percent+value", textfont_color="white")
        fig.update_layout(legend_title_text="Género", separators=",.")

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
                textinfo="percent+value",
                textfont_color="white",
            )
        )

        fig.update_layout(legend_title_text="Nivel de Satisfacción", separators=",.")

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
            xaxis_title_text="Distancia de Vuelo (km)",
            yaxis_title_text="Vuelos",
            bargap=0.2,
            bargroupgap=0.1,
        )

        fig = set_font_size(fig)
        st.plotly_chart(fig)

    with col2:
        fig = px.histogram(
            data,
            x="Age",
            title="Distribución de Edad",
            color_discrete_sequence=["#636EFA"],
            template="plotly_dark",
            range_x=[0, 90],  # Adjusted to start from 0 and cover up to 90
            nbins=9,  # Adjusted to create 9 bins, which will cover the range 0-90 in steps of 10
        )

        fig.update_traces(textposition="inside", texttemplate="%{y}", textfont_size=28)

        fig.update_layout(
            xaxis_title_text="Edad",
            yaxis_title_text="Pasajeros",
            bargap=0.2,
            bargroupgap=0.1,
        )

        fig = set_font_size(fig)
        st.plotly_chart(fig)

    with col3:
        class_counts = data["Class"].value_counts()

        fig = px.pie(
            class_counts,
            values=class_counts.values,
            names=class_counts.index,
            color=class_counts.index,
            color_discrete_map={
                "Business": "LightBlue",
                "Eco": "DarkSeaGreen",
                "Eco Plus": "GreenYellow",
            },
            title="Distribución de clase de los pasajeros",
        )

        fig.update_traces(textinfo="percent+value", textfont_color="white")
        fig.update_layout(legend_title_text="Clase", separators=",.")

        fig = set_font_size(fig)
        st.plotly_chart(fig)

    with col1:
        customer_counts = data["Customer Type"].value_counts()

        fig = px.pie(
            customer_counts,
            values=customer_counts.values,
            names=customer_counts.index,
            color=customer_counts.index,
            color_discrete_map={
                "Loyal Customer": "LightGreen",
                "Disloyal Customer": "LightCoral",
            },
            title="Distribución de tipo de cliente",
        )

        fig.update_traces(textinfo="percent+value", textfont_color="white")
        fig.update_layout(legend_title_text="Tipo de cliente", separators=",.")

        fig = set_font_size(fig)
        st.plotly_chart(fig)

    with col2:
        fig = px.histogram(
            data_frame=data,
            x="Gate Location",
            title="Distribución de Satisfacción de Ubicación de Puerta",
            labels={"Gate Location": "Nivel de Satisfacción"},
            color_discrete_sequence=["#636EFA"],
            category_orders={"Gate Location": [1, 2, 3, 4, 5]},
        )
        fig.update_layout(
            xaxis_title_text="Nivel de Satisfacción",
            yaxis_title_text="Frecuencia",
            xaxis=dict(
                tickmode="array",
                tickvals=[1, 2, 3, 4, 5],
                ticktext=["1", "2", "3", "4", "5"],
                range=[
                    0.5,
                    5.5,
                ],  # Sets the range of the x-axis to start from 1 and end at 5
            ),
            bargap=0.2,  # Adjusts the gap between bars
        )

        fig.update_traces(textposition="inside", texttemplate="%{y}", textfont_size=28)
        fig = set_font_size(fig)
        st.plotly_chart(fig)

    with col3:
        # Define the columns to include
        columns_to_include = [
            "Inflight Wifi Service",
            "Departure/Arrival Time Convenient",
            "Ease Of Online Booking",
            "Gate Location",
            "Food And Drink",
            "Online Boarding",
            "Seat Comfort",
            "Inflight Entertainment",
            "On-Board Service",
            "Leg Room Service",
            "Baggage Handling",
            "Checkin Service",
            "Inflight Service",
            "Cleanliness",
        ]

        # Filter the DataFrame to include only the specified columns
        filtered_data = data[columns_to_include]

        data_long = pd.melt(filtered_data, var_name="Servicio", value_name="Rating")
        rating_counts = (
            data_long.groupby(["Servicio", "Rating"])
            .size()
            .reset_index(name="Pasajeros")
        )

        pivot_table = rating_counts.pivot(
            index="Servicio", columns="Rating", values="Pasajeros"
        )

        pivot_table = pivot_table.reindex(columns=[0, 1, 2, 3, 4, 5], fill_value=0)

        fig = px.imshow(
            pivot_table,
            labels=dict(x="Rating", y="Servicio", color="Pasajeros"),
            x=[str(i) for i in range(0, 6)],
            aspect="auto",
            title="Service Satisfaction Heatmap",
            color_continuous_scale="Viridis",
        )

        fig.update_layout(
            title_text="Satisfacción de los pasajeros por servicio",
            title_x=0.5,
            title_font=dict(size=24),
            xaxis=dict(tickfont=dict(size=12)),
            yaxis=dict(tickfont=dict(size=12), title=""),
            autosize=False,
            width=1000,
            height=800,
            coloraxis_colorbar=dict(
                title="Pasajeros",
                titleside="right",
                titlefont=dict(size=12),
                tickfont=dict(size=10),
            ),
        )

        max_values_per_rating = pivot_table.max()
        # Add annotations for each cell as before
        for y in range(pivot_table.shape[0]):
            for x in range(pivot_table.shape[1]):
                value = pivot_table.iloc[y, x]
                if pd.notnull(value) and value == max_values_per_rating[x]:
                    # Highlight maximum values with bold text and attempt to draw a border
                    text_color = "red"
                    font_weight = "bold"
                    text_value = "{:,}".format(int(value)).replace(",", ".")
                    # Draw a red border around the cell
                    fig.add_shape(
                        type="rect",
                        x0=x - 0.5,
                        y0=y - 0.5,
                        x1=x + 0.5,
                        y1=y + 0.5,
                        line=dict(color="red", width=2),
                        fillcolor="rgba(0,0,0,0)",
                    )  # Transparent fill
                elif pd.notnull(value):
                    # Normal color and weight for other values
                    text_color = "white"
                    font_weight = "normal"
                    text_value = "{:,}".format(int(value)).replace(",", ".")
                else:
                    # Handle NaN values
                    text_color = "white"
                    font_weight = "normal"
                    text_value = "N/A"

                fig.add_annotation(
                    x=x,
                    y=y,
                    text=text_value,
                    showarrow=False,
                    font=dict(color=text_color, weight=font_weight),
                )

        fig = set_font_size(fig, 30)
        st.plotly_chart(fig)

    with col1:
        # Add 'Satisfaction' to the columns to include for filtering
        columns_to_include.append("Satisfaction")

        # The 'Satisfaction' column has two unique values: 'Neutral or Dissatisfied' and 'Satisfied'
        # Loop through each unique satisfaction level
        for satisfaction_level in ["Neutral or Dissatisfied", "Satisfied"]:
            # Filter data for the current satisfaction level
            filtered_data = data[data["Satisfaction"] == satisfaction_level][
                columns_to_include
            ]

            # Melt, count, and pivot as before
            data_long = pd.melt(
                filtered_data,
                id_vars=["Satisfaction"],
                var_name="Servicio",
                value_name="Rating",
            )
            rating_counts = (
                data_long.groupby(["Servicio", "Rating"])
                .size()
                .reset_index(name="Pasajeros")
            )
            pivot_table = rating_counts.pivot(
                index="Servicio", columns="Rating", values="Pasajeros"
            ).reindex(columns=[0, 1, 2, 3, 4, 5], fill_value=0)

            # Create heatmap
            fig = px.imshow(
                pivot_table,
                labels=dict(x="Rating", y="Servicio", color="Pasajeros"),
                x=[str(i) for i in range(0, 6)],
                aspect="auto",
                title=f"Service Satisfaction Heatmap for {satisfaction_level}",
                color_continuous_scale="Viridis",
            )

            # Update layout with satisfaction level in title and remove y-axis label
            fig.update_layout(
                title_text=f"Satisfacción de los pasajeros por servicio <br>{satisfaction_level}",
                title_x=0.5,
                title_font=dict(size=24),
                xaxis=dict(
                    tickfont=dict(size=12), title="Rating"
                ),  # Ensure x-axis is labeled
                yaxis=dict(tickfont=dict(size=12), title=""),  # Remove y-axis label
                autosize=False,
                width=1000,
                height=800,
                coloraxis_colorbar=dict(
                    title="Pasajeros",
                    titleside="right",
                    titlefont=dict(size=12),
                    tickfont=dict(size=10),
                ),
            )

            max_values_per_rating = pivot_table.max()
            # Add annotations for each cell as before
            for y in range(pivot_table.shape[0]):
                for x in range(pivot_table.shape[1]):
                    value = pivot_table.iloc[y, x]
                    if pd.notnull(value) and value == max_values_per_rating[x]:
                        # Highlight maximum values with bold text and attempt to draw a border
                        text_color = "red"
                        font_weight = "bold"
                        text_value = "{:,}".format(int(value)).replace(",", ".")
                        # Draw a red border around the cell
                        fig.add_shape(
                            type="rect",
                            x0=x - 0.5,
                            y0=y - 0.5,
                            x1=x + 0.5,
                            y1=y + 0.5,
                            line=dict(color="red", width=2),
                            fillcolor="rgba(0,0,0,0)",
                        )  # Transparent fill
                    elif pd.notnull(value):
                        # Normal color and weight for other values
                        text_color = "white"
                        font_weight = "normal"
                        text_value = "{:,}".format(int(value)).replace(",", ".")
                    else:
                        # Handle NaN values
                        text_color = "white"
                        font_weight = "normal"
                        text_value = "N/A"

                    fig.add_annotation(
                        x=x,
                        y=y,
                        text=text_value,
                        showarrow=False,
                        font=dict(color=text_color, weight=font_weight),
                    )

            # Adjust font size and display the plot
            fig = set_font_size(fig, 30)
            st.plotly_chart(fig)

    with col2:
        # Step 1: Create a list of the column names you want to select
        selected_columns = [
            "Inflight Wifi Service",
            "Departure/Arrival Time Convenient",
            "Ease Of Online Booking",
            "Gate Location",
            "Food And Drink",
            "Online Boarding",
            "Seat Comfort",
            "Inflight Entertainment",
            "On-Board Service",
            "Leg Room Service",
            "Baggage Handling",
            "Checkin Service",
            "Inflight Service",
            "Cleanliness",
        ]

        # Step 2: Use this list to select the specified columns from your DataFrame
        selected_df = data[selected_columns]

        # Step 3: Calculate the average for each of the selected columns
        averages = selected_df.mean()

        # Step 4: Convert these averages into a format suitable for plotting
        avg_df = pd.DataFrame(
            {"Service": averages.index, "Average Rating": averages.values}
        )

        # Display each average rating with st.metric for a more appealing presentation
        for index, row in avg_df.iterrows():
            st.metric(label=row["Service"], value=f"{row['Average Rating']:.2f}")

        st.table(avg_df)


def main():
    st.set_page_config(
        page_title="Satisfaccion del Cliente", page_icon=":airplane:", layout="wide"
    )

    st.title("🙋‍♂️ :blue[Satisfaccion del Cliente]")
    data = get_df()
    display_tables(data)

    st.markdown(
        """
        <style>
        .legendtitletext {
            font-size: 26px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("🔍 :blue[Estadísticas descriptivas]")
    display_descriptive_stats(data)

    st.subheader("🕵️ :blue[Visualizaciones]")
    option_col1, option_col2, option_col3 = st.columns(3)
    with option_col1:
        plot_type = st.selectbox(
            "Seleccione un tipo de gráfico", ["Histograma", "Linea", "Box Plot"]
        )
    with option_col2:
        column = st.selectbox("Seleccione una columna", data.columns)
    with option_col3:
        color_input = st.text_input(
            "Ingrese una secuencia de colores (separados por comas)"
        )

    color_sequences = (
        px.colors.qualitative.Plotly if not color_input else color_input.split(",")
    )

    if plot_type == "Histograma":
        fig = px.histogram(
            data, x=column, color=column, color_discrete_sequence=color_sequences
        )
    elif plot_type == "Linea":
        fig = px.line(data, x=column, template="plotly_dark")
    elif plot_type == "Box Plot":
        fig = px.box(data, x=column, template="plotly_dark")
    fig.update_layout(title=f"{plot_type} de {column}")
    fig = set_font_size(fig)
    st.plotly_chart(fig)

    st.subheader("📊 :blue[Gráficos]")
    display_charts(data)


if __name__ == "__main__":
    main()
