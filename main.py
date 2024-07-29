import streamlit as st

# Page configuration
st.set_page_config(page_title="Module Configurator", page_icon=":electric_plug:", layout="centered")

# Header
st.title("Module Configurator")
st.markdown("""
<style>
    .main {
        background-color: #8ab0e6;
        padding: 20px;
        border-radius: 10px;
    }
    .st-selectbox > div > div > div {
        background-color: #e0e0e0;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    .header-icon {
        display: inline;
        font-size: 1.5em;
        vertical-align: middle;
        margin-right: 10px;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
""", unsafe_allow_html=True)

st.markdown('<i class="fas fa-tools header-icon"></i>', unsafe_allow_html=True)
st.subheader("Customize Your Module")

# Constants for the program
MODULE_SIZES = {
    '2M': 2,
    '4M': 4,
    '6M': 6,
    '8M': 8,
    '12M': 12
}

ACCESSORIES = {
    '10 Amp Socket (2M)': 2,
    '16 Amp Socket (2M)': 2,
    'USB (1M)': 1,
    '2 Pin Socket (1M)': 1
}

GLASS_COLORS = ['Black', 'Champagne Gold', 'Space Grey']
BEZEL_COLORS = ['Black', 'Chrome', 'Gold']
AUTOMATION_OPTIONS = ['Yes', 'No']

# Dropdowns for user inputs
module_size_label = st.selectbox('MODULE SIZE', list(MODULE_SIZES.keys()))
selected_module_size = MODULE_SIZES[module_size_label]

accessories_selected = []
remaining_size = selected_module_size

while remaining_size > 0:
    available_accessories = [accessory for accessory, size in ACCESSORIES.items() if size <= remaining_size]

    if not available_accessories:
        st.write("Cannot fully utilize the selected module size with the available accessories.")
        break

    accessory = st.selectbox(f'Select accessory to fill remaining size {remaining_size}M:', available_accessories)
    accessories_selected.append(accessory)
    remaining_size -= ACCESSORIES[accessory]

glass_color = st.selectbox('GLASS COLOUR', GLASS_COLORS)
bezel_color = st.selectbox('BEZEL COLOUR', BEZEL_COLORS)
automation_required = st.selectbox('AUTOMATION REQUIRED', AUTOMATION_OPTIONS)

# Display the selected options
st.markdown('<i class="fas fa-list header-icon"></i>', unsafe_allow_html=True)
st.write("### Selected Options:")
st.markdown(f"**Module Size:** {module_size_label}")
st.markdown(f"**Accessories:** {', '.join(accessories_selected)}")
st.markdown(f"**Glass Colour:** {glass_color}")
st.markdown(f"**Bezel Colour:** {bezel_color}")
st.markdown(f"**Automation Required:** {automation_required}")
