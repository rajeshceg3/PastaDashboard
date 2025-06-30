import streamlit as st
import json
import pandas as pd
import pydeck as pdk
import altair as alt

# 1. Define Data
# Load pasta data from JSON file
try:
    with open("pasta_data.json", "r") as f:
        pasta_data = json.load(f)
except FileNotFoundError:
    st.error("Critical error: `pasta_data.json` not found. The application cannot start without this file.")
    st.stop()

# Load nutritional info from JSON file
try:
    with open("nutritional_info.json", "r") as f:
        nutritional_info_notes = json.load(f)
except FileNotFoundError:
    st.error("Warning: `nutritional_info.json` not found. Nutritional information will be unavailable.")
    nutritional_info_notes = []

# 2. Dashboard Layout & Theming
st.set_page_config(
    page_title="Pasta Paradise Dashboard",
    page_icon="🍝",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Pasta Paradise Dashboard\nYour go-to source for pasta info!"
    }
)

# Apply Custom CSS
try:
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("static/style.css not found. Using default Streamlit styling.")


st.title("Pasta Paradise: An Informative Dashboard")
st.markdown("""
Welcome to the **Pasta Paradise**! This dashboard provides a quick look at various types of pasta,
their origins, and common uses. You can also find general nutritional insights about pasta.
Use the filter on the left to explore different pasta types.
""")

# Image - Updated Placeholder
st.image("https://images.unsplash.com/photo-1598866594240-a71619160648?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60", caption="A delightful assortment of pasta", alt="A vibrant collage of various pasta types")


# 3. Display Pasta Information
st.sidebar.header("Filter Pasta")
pasta_types = ["All"] + sorted(list(set([p.get("type") for p in pasta_data if p.get("type") is not None])))
selected_type = st.sidebar.selectbox("Select Pasta Type", pasta_types, help="Choose a pasta category to display.")
sort_option = st.sidebar.selectbox("Sort Pasta By", ["None", "Name (Ascending)", "Name (Descending)"], help="Choose how to sort the pasta items.")

# Create a list of pasta types, filtering out None or missing types
types_list = [p.get("type", "Unknown") for p in pasta_data if p.get("type")]
if types_list:
    types_df = pd.DataFrame(types_list, columns=['type'])
    type_counts = types_df['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']

    # Create the Altair chart
    chart_title = "Pasta Types Distribution"
    chart = alt.Chart(type_counts).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        color='#E67E22' # Use the primary orange color
    ).encode(
        x=alt.X('count:Q', title='Number of Pastas'),
        y=alt.Y('type:N', sort='-x', title='Pasta Type'), # Sort by count descending
        tooltip=['type:N', 'count:Q']
    ).properties(
        title=alt.TitleParams(text=chart_title, anchor='middle', color='#2c3e50')
    ).configure_axis(
        labelColor='#34495e',
        titleColor='#34495e'
    ).configure_title(
        color='#2c3e50'
    )

    st.sidebar.markdown("---") # Add a separator
    st.sidebar.altair_chart(chart, use_container_width=True)
else:
    st.sidebar.markdown("---")
    st.sidebar.info("Not enough type data to display distribution chart.")

st.header("Pasta Showcase")
search_term = st.text_input("Search Pasta by Name or Description", "")

if selected_type == "All":
    filtered_pasta = pasta_data
else:
    filtered_pasta = [p for p in pasta_data if p.get("type") == selected_type]

if search_term: # If search_term is not empty
    search_term_lower = search_term.lower()
    # Further filter the already type-filtered list
    filtered_pasta = [
        p for p in filtered_pasta
        if search_term_lower in p.get("name", "").lower() or \
           search_term_lower in p.get("description", "").lower()
    ]

# Apply sorting based on user selection
if sort_option == "Name (Ascending)":
    filtered_pasta = sorted(filtered_pasta, key=lambda p: p.get("name", "").lower())
elif sort_option == "Name (Descending)":
    filtered_pasta = sorted(filtered_pasta, key=lambda p: p.get("name", "").lower(), reverse=True)
# If sort_option is "None", no sorting is applied, maintaining the original order from filtering.

if filtered_pasta:
    # Using columns for a more structured layout, e.g., 2 columns
    cols = st.columns(2)
    col_idx = 0
    for pasta in filtered_pasta:
        with cols[col_idx % 2]: # Cycle through columns
            st.markdown('<div class="pasta-card">', unsafe_allow_html=True)
            st.subheader(pasta.get("name", "N/A"))
            image_url = pasta.get("image_url")
            if image_url:
                st.image(image_url, caption=f"Image of {pasta.get('name', 'N/A')}", alt=f"Image of {pasta.get('name', 'N/A')}")
            else:
                st.image("https://images.unsplash.com/photo-1613634326309-7fe54ed25ffa?auto=format&fit=crop&w=300&q=80", caption=f"Image of {pasta.get('name', 'N/A')}", alt=f"Placeholder image for {pasta.get('name', 'N/A')}")

            st.markdown(f"**Type:** `{pasta.get('type', 'N/A')}`")
            st.markdown(f"**Description:** {pasta.get('description', 'N/A')}")
            st.markdown(f"**Origin:** {pasta.get('origin', 'N/A')}")
            st.markdown(f"**Translation:** _{pasta.get('translation', 'N/A')}_")
            st.markdown(f"**Common Uses:** {pasta.get('common_uses', 'N/A')}")
            st.markdown('</div>', unsafe_allow_html=True)

        # Divider logic (remains outside the card, but after the column content)
        if col_idx % 2 == 1 or col_idx == len(filtered_pasta) -1 :
             st.divider()
        col_idx += 1

else:
    st.warning("No pasta found for the selected type. Try another filter!")

# New Section: Pasta Origins Map
st.header("Pasta Origins Map")
map_data_list = []
for pasta in pasta_data:
    if "latitude" in pasta and "longitude" in pasta:
        map_data_list.append({
            "latitude": pasta["latitude"],
            "longitude": pasta["longitude"],
            "name": pasta.get("name", "Unnamed Pasta Location") # Include name for potential future use or if map supports tooltips
        })

if map_data_list:
    map_df = pd.DataFrame(map_data_list)
    # Ensure column names are 'lat' or 'latitude', 'lon' or 'longitude'
    # Streamlit's st.map expects columns named 'latitude'/'lat' and 'longitude'/'lon'.
    # Our current 'latitude' and 'longitude' are fine.
    # st.map(map_df, key="pasta_origin_map") # Old map rendering

    if not map_df.empty:
        # Define a PyDeck layer
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position=["longitude", "latitude"],
            get_radius=10000,  # Radius in meters, adjust as needed
            get_fill_color=[230, 126, 34, 180],  # Carrot orange, semi-transparent: [R, G, B, Alpha]
            pickable=True  # Enable tooltips
        )

        # Set the initial view state for the map
        # Use the mean of lat/lon for the initial view, or a sensible default
        initial_view_state = pdk.ViewState(
            latitude=map_df["latitude"].mean(),
            longitude=map_df["longitude"].mean(),
            zoom=3, # Adjust zoom level as needed
            pitch=30 # Adjust pitch for a slight 3D effect
        )

        # Define the tooltip content
        tooltip = {
            "html": "<b>{name}</b>", # Display the 'name' field from map_df in bold
            "style": {
                "backgroundColor": "rgba(44, 62, 80, 0.8)", # Dark background for tooltip
                "color": "white",
                "padding": "5px",
                "borderRadius": "3px"
            }
        }

        # Render the PyDeck chart
        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=initial_view_state,
            tooltip=tooltip,
            map_style='mapbox://styles/mapbox/light-v9' # Optional: use a specific map style
        ))
    else:
        st.write("No location data available to display on the map.")

st.divider() # Add a visual separator

# 4. Display Nutritional Information
st.header("General Nutritional Insights")
with st.expander("View General Nutritional Insights", expanded=False): # Set expanded=False by default
    st.markdown("Here are some general notes on the nutritional aspects of pasta. Remember, the overall healthiness of a pasta dish is greatly influenced by its sauce and accompaniments!")
    for note in nutritional_info_notes:
        st.markdown(f"- {note}")

st.sidebar.markdown("---")
st.sidebar.info("🍝 Pasta Paradise Dashboard | Built with Streamlit.")
st.sidebar.markdown("Enjoy exploring the world of pasta!")
