import streamlit as st
import json
import pandas as pd
import altair as alt
import math
import html

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
    layout="centered",
    initial_sidebar_state="auto",
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


st.title("Pasta Paradise")
st.markdown("Explore ten shapes, from long strands to filled parcels. Find a shape by name, compare its uses, then see the places associated with it.")
st.caption("Original shape studies · a small pasta collection")

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
    chart_title = "Shape families"
    chart = alt.Chart(type_counts).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
        color='#9b6b39' # Warm ink
    ).encode(
        x=alt.X('count:Q', title='Number of Pastas'),
        y=alt.Y('type:N', sort='-x', title='Pasta Type'), # Sort by count descending
        tooltip=['type:N', 'count:Q']
    ).properties(
        title=alt.TitleParams(text=chart_title, anchor='middle', color='#5a5a5a')
    ).configure_axis(
        labelColor='#5a5a5a',
        titleColor='#5a5a5a'
    ).configure_title(
        color='#5a5a5a'
    )

    st.sidebar.markdown("---") # Add a separator
    st.sidebar.altair_chart(chart, width="stretch")
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
    col_idx = 0
    for pasta in filtered_pasta:
        if col_idx % 2 == 0:
            cols = st.columns(2)
        with cols[col_idx % 2]: # Cycle through columns
            with st.container(border=True):
                st.subheader(pasta.get("name", "N/A"))
                st.image(f"static/specimens/{pasta['name'].lower()}.svg", width="stretch")
                st.caption("Illustrated shape study")
                st.markdown(f"**Type:** `{pasta.get('type', 'N/A')}`")
                st.markdown(pasta.get('description', ''))
                st.markdown(f"**Associated place:** {pasta.get('origin', 'N/A')}")
                st.markdown(f"**Name meaning:** _{pasta.get('translation', 'N/A')}_")
                st.markdown(f"**At the table:** {pasta.get('common_uses', 'N/A')}")

        # Divider logic (remains outside the card, but after the column content)
        if col_idx % 2 == 1 or col_idx == len(filtered_pasta) -1 :
             st.divider()
        col_idx += 1

else:
    st.warning("No pasta found for the selected type. Try another filter!")

# Local geographic context does not need a map-provider key.
st.header("Places in the collection")
st.caption("Representative catalog locations, not verified birthplaces. Traditions and origin claims can cross regions.")
with open("static/natural-earth-context.geojson") as f:
    context = json.load(f)
places = pd.DataFrame([{"longitude":p["longitude"],"latitude":p["latitude"],"name":p["name"]} for p in filtered_pasta if "latitude" in p and "longitude" in p])
if not places.empty:
    # A local, responsive SVG has a fixed geographic extent and no token/tile dependency.
    def project(lon, lat):
        return ((lon-6)/14*600, (math.asinh(math.tan(math.radians(48)))-math.asinh(math.tan(math.radians(lat))))*2450)
    paths = []
    for feature in context["features"]:
        geometry = feature["geometry"]
        polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
        for polygon in polygons:
            points = [project(lon,lat) for lon,lat in polygon[0]]
            d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x,y in points) + " Z"
            paths.append(f'<path d="{d}"/>')
    dots = []
    point_groups = {}
    for _,place in places.iterrows():
        key = (place.longitude, place.latitude)
        point_groups.setdefault(key, []).append(place["name"])
    for number,((lon,lat),names) in enumerate(point_groups.items(), start=1):
        x,y = project(lon,lat)
        dots.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="12" fill="#86452d"><title>{html.escape(", ".join(names))}</title></circle><text x="{x:.2f}" y="{y+4:.2f}" fill="#fff8e8" font-size="13" font-family="sans-serif" text-anchor="middle">{number}</text>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="650" viewBox="0 0 600 650" role="img" aria-label="Simplified Italy and surrounding countries, catalog locations marked as dots"><rect width="600" height="650" fill="#f7f1e4"/><g fill="#e7d8b5" stroke="#958267" stroke-width="1">' + ''.join(paths) + '</g>' + ''.join(dots) + '</svg>'
    st.image(svg, width=600)
    for number,((lon,lat),names) in enumerate(point_groups.items(), start=1):
        st.markdown(f"**{number}.** {', '.join(names)}")
    st.dataframe(places.rename(columns={"name":"Pasta","latitude":"Latitude","longitude":"Longitude"}), hide_index=True, width="stretch")
else:
    st.info("No matching shapes to place on the map.")
st.caption("Map context: Natural Earth, public domain. Simplified educational geography.")

st.divider() # Add a visual separator

# 4. Display Nutritional Information
st.header("A note on nutrition")
with st.expander("View General Nutritional Insights", expanded=False): # Set expanded=False by default
    st.markdown("Here are some general notes on the nutritional aspects of pasta. Remember, the overall healthiness of a pasta dish is greatly influenced by its sauce and accompaniments!")
    st.markdown("Ingredients, portion size and accompaniments change the nutritional profile. This catalog is not dietary advice. The inherited numeric serving claims have not been independently checked and are not presented as measured values.")

st.sidebar.markdown("---")
st.sidebar.caption("10 shapes · 5 families")
