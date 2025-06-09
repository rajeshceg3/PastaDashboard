import streamlit as st

# 1. Define Data
pasta_data = [
    {
        "name": "Spaghetti",
        "type": "Long",
        "description": "A long, thin, cylindrical pasta.",
        "origin": "Sicily",
        "translation": "Little strings",
        "common_uses": "Often served with tomato sauces, meat, or vegetables."
    },
    {
        "name": "Penne",
        "type": "Short-cut",
        "description": "Medium length tubes with ridges, cut diagonally at both ends.",
        "origin": "Liguria",
        "translation": "Pens (after a quill pen)",
        "common_uses": "Good with chunky sauces, in salads, or baked dishes."
    },
    {
        "name": "Fettuccine",
        "type": "Long",
        "description": "Ribbon of pasta approximately 6.5 millimeters wide.",
        "origin": "Rome",
        "translation": "Little ribbons",
        "common_uses": "Often paired with rich and creamy sauces like Alfredo."
    },
    {
        "name": "Farfalle",
        "type": "Short-cut",
        "description": "Bow tie- or butterfly-shaped pasta.",
        "origin": "Northern Italy",
        "translation": "Butterflies",
        "common_uses": "Versatile for various sauces, salads, and baked dishes."
    },
    {
        "name": "Lasagne",
        "type": "Sheet",
        "description": "Square or rectangle sheets of pasta.",
        "origin": "Emilia-Romagna (disputed)",
        "translation": "Cooking pot (possibly from Latin/Greek)",
        "common_uses": "Layered with sauces and cheese in baked dishes."
    },
    {
        "name": "Ravioli",
        "type": "Filled",
        "description": "Square or circular pockets of pasta, filled with cheese, meat, or vegetables.",
        "origin": "Italy (general)",
        "translation": "Possibly from 'to wrap' or 'turnip'",
        "common_uses": "Served with light butter or oil sauces, or in broth."
    },
    {
        "name": "Bucatini",
        "type": "Long",
        "description": "Thick spaghetti-like pasta with a hole running through the center.",
        "origin": "Lazio",
        "translation": "Hollow straws",
        "common_uses": "Excellent with rich, buttery sauces or Amatriciana."
    },
    {
        "name": "Rigatoni",
        "type": "Short-cut",
        "description": "Medium-Large tube with square-cut ends, always grooved.",
        "origin": "Lazio",
        "translation": "Lined ones",
        "common_uses": "Perfect for capturing sauces in its ridges; good for baking."
    },
    {
        "name": "Orecchiette",
        "type": "Stretched",
        "description": "Irregular disc with a central dome and a slightly thicker crown.",
        "origin": "Apulia",
        "translation": "Little ears",
        "common_uses": "Typically served with broccoli rabe or chunky vegetable sauces."
    },
    {
        "name": "Cannelloni",
        "type": "Filled",
        "description": "Rolls of pasta with various fillings, usually cooked in an oven.",
        "origin": "Central Italy",
        "translation": "Large reeds",
        "common_uses": "Stuffed with ricotta, spinach, or meat, and baked with sauce."
    }
]

nutritional_info_notes = [
    "Nutritional values can vary based on ingredients (e.g., whole wheat vs. refined flour, egg content) and portion size.",
    "A typical serving of cooked pasta (about 1 cup, or 140g) can range from 180-220 calories for plain pasta.",
    "Generally, pasta is a good source of carbohydrates, providing energy. It also contains some protein and fiber.",
    "Whole wheat pasta offers more fiber (typically 5-7g per serving vs 2-3g for refined) which aids digestion and can help manage blood sugar levels.",
    "Pasta itself is relatively low in fat and sodium; the overall nutritional profile of a pasta dish heavily depends on the sauce and accompaniments.",
    "The Harvard School of Public Health recommends choosing whole grain pasta as part of a healthy diet.",
    "Enriched pasta often contains added folic acid and iron."
]

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
