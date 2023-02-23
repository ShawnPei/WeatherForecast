import streamlit as st
import plotly.express as px

from backend import get_data

# Add title, text input, slider, selectbox, and subheader
st.title("Weather forecast for the following days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")

try:
    if place:
        # Get the temperature
        filtered_data = get_data(place, days)

        if option == "Temperature":
            # Generate temperature plot
            temperature = [dict["main"]["temp"] for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            figure = px.line(x=dates, y=[temp-273.15 for temp in temperature], labels={"x": "Date", "Y": "Temperature (C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]['main'] for dict in filtered_data]
            image_path = [images[condition] for condition in sky_conditions]
            days_per_page = 1
            for i in range(0, len(filtered_data), 8 * days_per_page):
                page_data = filtered_data[i:i + 8 * days_per_page]
                page_images = image_path[i:i + 8 * days_per_page]
                st.write(f"Data for {page_data[0]['dt_txt'].split(' ')[0]}")
                row = st.container()
                with row:
                    for j, path in enumerate(page_images):
                        col1, col3 = st.columns([3, 3])
                        with col1:
                            st.image(path, width=150)
                        with col3:
                            st.write(f"Date and Time: {page_data[j]['dt_txt']}")
                st.write('\n')
                st.write('---')

except KeyError:
    st.warning("This place does not exist, please check your spelling")

