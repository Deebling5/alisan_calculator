import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Define available options
module_sizes = ["2M", "4M", "6M", "8M", "12M"]
circuits = {
    "2M": ["2 Switch (1-HD)", "4 Switch", "1 Fan", "1 Light Dimmer", "1 Curtain", "2 Curtain", "Bell Switch"],
    "4M": ["4 Switch", "1 Fan", "4 Switch 1 Dimmer", "2 Switch 1 Fan (1-HD)", "6 Switch (1-HD)",
           "8 Switch (1-HD)", "2 Dimmer"],
    "6M": ["4 Switch 2 Fan", "4 Switch 2 Dimmer", "6 Switch 1 Fan (1-HD)", "4 Switch 1 Fan 1 Dimmer",
           "8 Switch 1 Dimmer (1-HD)", "10 Switch (2-HD)", "8 Switch 1 Fan"],
}
accessories = {"10 Amp Socket(2M)": 2, "16 Amp Socket(2M)": 2, "USB (1M)": 1, "2 Pin Socket(1M)": 1}
glass_colors = ["Black", "Champagne Gold", "Space Grey"]
bezel_colors = ["Black", "Chrome", "Gold"]
automation_required = ["Yes", "No"]
# Part codes for different components
part_codes = {
    "touch_sense_board": {
        "2 Switch (1-HD)": "2_SEN_S2",
        "4 Switch": "2_SEN_S4",
        "1 Fan": "2_SEN_F1",
        "1 Light Dimmer": "2_SEN_F1",
        "1 Curtain": "2_SEN_C1",
        "2 Curtain": "2_SEN_C2",
        "Bell Switch": "2_SEN_B",
        "4 switch 1 fan": "4_SEN_S4F1",
        "4 switch 1 dimmer": "4_SEN_S4F1",
        "2 switch 1 fan (1-HD)": "4_SEN_S2F1",
        "6 switch (1-HD)": "4_SEN_S6",
        "8 Switch (1-HD)": "4_SEN_S8",
        "2 Dimmer": "4_SEN_F2",
        "4 switch 2 fan": "6_SEN_S4F2",
        "4 switch 2 dimmer": "6_SEN_S4F2",
        "4 switch 1 fan 1 dimmer": "6_SEN_S4F2",
        "6 switch 1 fan (1-HD)": "6_SEN_S6F1",
        "8 switch 1 dimmer (1-HD)": "6_SEN_S8F1",
        "8 switch 1 Fan (1-HD)": "6_SEN_S8F1",
        "10 Switch (2-HD)": "6_SEN_S10"
    },
    "relay_board_pcb": {
        "2 Switch (1 - HD)": "2_REL_S2",
        "4 Switch": "2_REL_S4",
        "1 Fan": "2_REL_F1",
        "1 Light Dimmer": "2_REL_D1",
        "1 Curtain": "2_REL_C1",
        "2 Curtain": "2_REL_C2",
        "Bell Switch": "2_REL_B",
        "4 switch 1 fan": "4_REL_S4F1",
        "4 switch 1 dimmer": "4_REL_S4D1",
        "2 switch 1 fan (1 - HD)": "4_REL_S2F1",
        "6 switch (1 - HD)": "4_REL_S6",
        "8 Switch (1 - HD)": "4_REL_S8",
        "2 Dimmer": "4_REL_F2",
        "4 switch 2 fan": "4_REL_S4F2",
        "4 switch 2 dimmer": "4_REL_S4D2",
        "6 switch 1 fan (1 - HD)": "6_REL_S6F1",
        "4 switch 1 fan 1 dimmer": "6_REL_S4F1D1",
        "8 switch 1 dimmer (1 - HD)": "6_REL_S8D1",
        "10 Switch (2 - HD)": "6_REL_S10",
        "8 switch 1 Fan": "6_REL_S8F1"
    },
    "power_supply": "F_DUAL_PS",
    "esp": "FTT_ESP",
    "big_cover": {
        "4M": "4M Cover Part Number",
        "6M": "6M Cover Part Number"
    },
    "small_cover": "Small Cover Part Number",
    "screw": {
        "2M": "4 Screws",
        "4M": "6 Screws",
        "6M": "8 Screws"
    }
}

# User selections
module_size = st.selectbox("Select Module Size", module_sizes)
remaining_space = int(module_size[:-1])  # Extract numeric part from module size (e.g., "12M" -> 12)

st.write(f"Module Size: {module_size}, Total Space: {remaining_space}M")

# Accessory selection
selected_accessories = []
for accessory, size in accessories.items():
    if st.checkbox(f"Add {accessory}"):
        if remaining_space >= size:
            selected_accessories.append(accessory)
            remaining_space -= size
            st.write(f"{accessory} added, Remaining Space: {remaining_space}M")
        else:
            st.warning(f"Not enough space for {accessory}.")

# Ensure space management for 1M accessories
if remaining_space == 1:
    st.warning("You must add another 1M accessory.")
    for accessory, size in accessories.items():
        if size == 1 and accessory not in selected_accessories:
            if st.checkbox(f"Add {accessory}", key=f"{accessory}_1M"):
                selected_accessories.append(accessory)
                remaining_space -= size
                st.write(f"{accessory} added, Remaining Space: {remaining_space}M")

# Circuit selection to fill remaining space
selected_circuits = []
if remaining_space > 0:
    st.write(f"Select circuits to fill the remaining {remaining_space}M space:")
    while remaining_space > 0:
        available_circuits = [size for size in circuits if int(size[:-1]) <= remaining_space]
        if not available_circuits:
            st.warning("Not enough space left for any circuit.")
            break
        selected_circuit_size = st.selectbox("Select Circuit Size", available_circuits,
                                             key=f"circuit_{remaining_space}")
        selected_circuit = st.selectbox("Select Circuit", circuits[selected_circuit_size],
                                        key=f"option_{remaining_space}")
        selected_circuits.append(f"{selected_circuit} ({selected_circuit_size})")
        remaining_space -= int(selected_circuit_size[:-1])

# Glass and Bezel Color selection
glass_color = st.selectbox("Select Glass Colour", glass_colors)
bezel_color = st.selectbox("Select Bezel Colour", bezel_colors)
automation = st.selectbox("Automation Required", automation_required)

# Display summary
st.write("### Summary")
st.write(f"Module Size: {module_size}")
st.write(f"Selected Accessories: {', '.join(selected_accessories) if selected_accessories else 'None'}")
st.write(f"Selected Circuits: {', '.join(selected_circuits) if selected_circuits else 'None'}")
st.write(f"Glass Colour: {glass_color}")
st.write(f"Bezel Colour: {bezel_color}")
st.write(f"Automation Required: {automation}")


def extract_circuit_parts(circuit):
    # Split by the last occurrence of " (" to separate the circuit name from its size
    circuit_name, circuit_size = circuit.rsplit(" (", 1)
    circuit_size = circuit_size.rstrip(")")  # Remove the trailing ")"
    return circuit_name.strip(), circuit_size.strip()


def get_initials(phrase):
    # Split the phrase into words
    words = phrase.split()

    # Initialize an empty string to store the result
    result = ""

    # Iterate over pairs of numbers and words
    for i in range(0, len(words), 2):
        # First, handle the word (non-numeric)
        word = words[i + 1]
        # Get the corresponding number (numeric word)
        number = words[i]

        # Append the initial of the word and the corresponding number
        result += word[0].upper() + number

    return result


# Generate PDF Report
def generate_pdf_report(front_panel_color, module_size, selected_circuits, accessories, automation_required):
    # Create a PDF document
    pdf_filename = "report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    elements = []

    # Table Data (first row as headers)
    data = [["Component", "Details", "Part Code"]]

    # Front Panel
    front_panel_part_code = f"{module_size}{front_panel_color[0].upper()}F"
    data.append(["Front Panel", f"Colour: {front_panel_color}, Size: {module_size}", front_panel_part_code])

    # Back Panel
    back_panel_part_code = f"{module_size}B"
    data.append(["Back Panel", f"Size: {module_size}", back_panel_part_code])

    # Touch Sense Board
    for circuit in selected_circuits:
        circuit_name, circuit_size = extract_circuit_parts(circuit)
        circuit_name = get_initials(circuit_name)
        part_code = f"{circuit_size}_SEN_{circuit_name.replace(' ', '_').upper()}"
        data.append(["Touch Sense Board", f"Circuit: {circuit}", part_code])

    # Relay Board PCB
    for circuit in selected_circuits:
        circuit_name, circuit_size = extract_circuit_parts(circuit)
        circuit_name = get_initials(circuit_name)
        part_code = f"{circuit_size}_REL_{circuit_name.replace(' ', '_').upper()}"
        data.append(["Relay Board PCB", f"Circuit: {circuit}", part_code])

    # Power Supply
    data.append(["Power Supply", "Compulsory", "F_DUAL_PS"])

    # ESP (for Automation)
    if automation_required == "Yes":
        data.append(["ESP", "Automation Board", "ESP_COMMON"])

    # C Section
    c_section_count = int(module_size[:-1]) // 2
    data.append(["C Section", f"Number of C Sections: {c_section_count}", ""])

    # Big Cover
    big_cover_size = "4M" if int(module_size[:-1]) <= 4 else "6M"
    data.append(["Big Cover", f"Size: {big_cover_size}", f"BIG_COVER_{big_cover_size}"])

    # Small Cover
    data.append(["Small Cover", "", "SMALL_COVER_1PC"])

    # Screws
    screws_required = 2 + 2 * (int(module_size[:-1]) // 2)
    data.append(["Screw", f"Number of Screws: {screws_required}", f"SCREW_{screws_required}PCS"])

    # Accessories
    if accessories:
        for accessory in accessories:
            data.append(["Accessory", accessory, ""])
    else:
        data.append(["Accessories", "No accessories selected.", ""])

    # Create the table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align text center
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Body background color
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Add gridlines
    ]))

    # Add the table to the elements
    elements.append(table)

    # Build the PDF
    doc.build(elements)

    return pdf_filename


# Button to generate the PDF
if st.button("Generate PDF Report"):
    pdf_filename = generate_pdf_report(glass_color, module_size, selected_circuits, selected_accessories, automation)
    with open(pdf_filename, "rb") as pdf_file:
        st.download_button(label="Download PDF", data=pdf_file, file_name=pdf_filename, mime="application/pdf")
