import streamlit as st
import json

# 1. Define Data
# Load pasta data from JSON file
with open("pasta_data.json", "r") as f:
    pasta_data = json.load(f)

# Load nutritional info from JSON file
with open("nutritional_info.json", "r") as f:
    nutritional_info_notes = json.load(f)

# 2. Dashboard Layout & Theming
st.set_page_config(
    page_title="Pasta Paradise Dashboard",
    page_icon="🍝",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help', # Placeholder
        'Report a bug': "https://www.extremelycoolapp.com/bug", # Placeholder
        'About': "# Pasta Paradise Dashboard\nYour go-to source for pasta info!"
    }
)

# Apply Custom CSS
st.markdown("""
<style>
    /* General App Styling */
    .stApp {
        /* background-color: #f0f2f6; /* Light gray background for the app */
    }
    body {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        line-height: 1.6;
    }

    /* Main Title */
    .stTitle { /* Targets st.title() */
        font-size: 2.5em;
        color: #2c3e50; /* Dark blue-gray */
        text-align: center;
        padding-bottom: 20px;
    }

    /* Headers */
    /* st.header() uses h2 internally by default */
    h2 { /* Targets st.header() */
        color: #e67e22; /* Carrot orange */
        border-bottom: 2px solid #e67e22;
        padding-bottom: 10px;
        margin-top: 30px;
    }

    /* Subheaders for pasta names */
    /* st.subheader() uses h3 internally by default */
    h3 { /* Targets st.subheader() */
        color: #FF6347; /* Tomato color */
        font-size: 1.75em;
        margin-top: 20px;
    }

    /* Sidebar Styling */
    .css-1d391kg { /* Specific class for Streamlit sidebar content area */
        padding: 15px;
        /* background-color: #ffffff; */ /* Optional: if you want sidebar to have different bg */
    }
    .st-emotion-cache-10oheav { /* Class for sidebar header (st.sidebar.header) */
         font-size: 1.5em;
         color: #2980b9; /* Peter River blue */
    }


    /* Markdown text styling */
    .stMarkdown p {
        font-size: 1.05em;
        color: #34495e; /* Wet Asphalt (dark gray) */
    }
    .stMarkdown strong {
        color: #2c3e50; /* Slightly darker for emphasis */
    }
    .stMarkdown em {
        color: #555;
    }
    .stMarkdown ul {
        padding-left: 20px;
    }
    .stMarkdown li {
        margin-bottom: 5px;
    }
    .stMarkdown code {
        background-color: #ecf0f1; /* Clouds (light gray) */
        padding: 3px 6px;
        border-radius: 4px;
        color: #c0392b; /* Pomegranate (reddish) */
        font-family: 'Courier New', Courier, monospace;
    }

    /* Image styling */
    .stImage img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Divider */
    .stDivider {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

</style>
""", unsafe_allow_html=True)


st.title("Pasta Paradise: An Informative Dashboard")
st.markdown("""
Welcome to the **Pasta Paradise**! This dashboard provides a quick look at various types of pasta,
their origins, and common uses. You can also find general nutritional insights about pasta.
Use the filter on the left to explore different pasta types.
""")

# Image - Updated Placeholder
st.image("https://via.placeholder.com/800x200.png?text=Pasta+Showcase+Banner", caption="A delightful assortment of pasta")


# 3. Display Pasta Information
st.sidebar.header("Filter Pasta")
pasta_types = ["All"] + sorted(list(set([p["type"] for p in pasta_data])))
selected_type = st.sidebar.selectbox("Select Pasta Type", pasta_types, help="Choose a pasta category to display.")

st.header("Pasta Showcase")

if selected_type == "All":
    filtered_pasta = pasta_data
else:
    filtered_pasta = [p for p in pasta_data if p["type"] == selected_type]

if filtered_pasta:
    # Using columns for a more structured layout, e.g., 2 columns
    cols = st.columns(2)
    col_idx = 0
    for pasta in filtered_pasta:
        with cols[col_idx % 2]: # Cycle through columns
            st.subheader(pasta["name"])
            if "image_url" in pasta and pasta["image_url"]:
                st.image(pasta["image_url"], caption=f"Image of {pasta['name']}")
            st.markdown(f"**Type:** `{pasta['type']}`") # Using backticks for type
            st.markdown(f"**Description:** {pasta['description']}")
            st.markdown(f"**Origin:** {pasta['origin']}")
            st.markdown(f"**Translation:** _{pasta['translation']}_")
            st.markdown(f"**Common Uses:** {pasta['common_uses']}")
        # Add a visual separator within the column before the next item in the same column
        # Or a full divider if we are not using columns or after each full row of columns
        if col_idx % 2 == 1 or col_idx == len(filtered_pasta) -1 : # after second column or if it's the last item
             st.divider() # This will be a full-width divider
        col_idx += 1

else:
    st.warning("No pasta found for the selected type. Try another filter!")

# 4. Display Nutritional Information
st.header("General Nutritional Insights")
st.markdown("Here are some general notes on the nutritional aspects of pasta. Remember, the overall healthiness of a pasta dish is greatly influenced by its sauce and accompaniments!")
for note in nutritional_info_notes:
    st.markdown(f"- {note}")

st.sidebar.markdown("---")
st.sidebar.info("🍝 Pasta Paradise Dashboard | Built with Streamlit.")
st.sidebar.markdown("Enjoy exploring the world of pasta!")
