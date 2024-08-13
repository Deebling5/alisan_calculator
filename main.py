import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

# Define available options
module_sizes = ["2M", "4M", "6M", "8M", "12M"]
circuits = {
    "2M": ["2 Switch (1 - HD)", "4 Switch", "1 Fan", "1 Light Dimmer", "1 Curtain", "2 Curtain", "Bell Switch"],
    "4M": ["4 Switch", "1 Fan", "4 Switch 1 Dimmer", "2 Switch 1 Fan (1 - HD)", "6 Switch (1 - HD)",
           "8 Switch (1 - HD)", "2 Dimmer"],
    "6M": ["4 Switch 2 Fan", "4 Switch 2 Dimmer", "6 Switch 1 Fan (1 - HD)", "4 Switch 1 Fan 1 Dimmer",
           "8 Switch 1 Dimmer (1 - HD)", "10 Switch (2 - HD)", "8 Switch 1 Fan"],
}
accessories = {"10 Amp Socket(2M)": 2, "16 Amp Socket(2M)": 2, "USB (1M)": 1, "2 Pin Socket(1M)": 1}
glass_colors = ["Black", "Champagne Gold", "Space Grey"]
bezel_colors = ["Black", "Chrome", "Gold"]
automation_required = ["Yes", "No"]
# Part codes for different components
part_codes = {
    "touch_sense_board": {
        "2 Switch (1 - HD)": "2_SEN_S2",
        "4 Switch": "2_SEN_S4",
        "1 Fan": "2_SEN_F1",
        "1 Light Dimmer": "2_SEN_F1",
        "1 Curtain": "2_SEN_C1",
        "2 Curtain": "2_SEN_C2",
        "Bell Switch": "2_SEN_B",
        "4 switch 1 fan": "4_SEN_S4F1",
        "4 switch 1 dimmer": "4_SEN_S4F1",
        "2 switch 1 fan (1 - HD)": "4_SEN_S2F1",
        "6 switch (1 - HD)": "4_SEN_S6",
        "8 Switch (1 - HD)": "4_SEN_S8",
        "2 Dimmer": "4_SEN_F2",
        "4 switch 2 fan": "6_SEN_S4F2",
        "4 switch 2 dimmer": "6_SEN_S4F2",
        "4 switch 1 fan 1 dimmer": "6_SEN_S4F2",
        "6 switch 1 fan (1 - HD)": "6_SEN_S6F1",
        "8 switch 1 dimmer (1 - HD)": "6_SEN_S8F1",
        "8 switch 1 Fan (1 - HD)": "6_SEN_S8F1",
        "10 Switch (2 - HD)": "6_SEN_S10"
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

# Generate PDF Report
def generate_pdf_report(front_panel_color, module_size, selected_circuits, accessories, automation_required):
    # Create a PDF document
    pdf_filename = "report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    # Front Panel
    front_panel_part_code = f"{module_size}{front_panel_color[0].upper()}F"
    elements.append(Paragraph("Front Panel", styles["Heading2"]))
    elements.append(Paragraph(f"Colour: {front_panel_color}, Size: {module_size}, Part Code: {front_panel_part_code}",
                              styles["Normal"]))

    # Back Panel
    back_panel_part_code = f"{module_size}B"
    elements.append(Paragraph("Back Panel", styles["Heading2"]))
    elements.append(Paragraph(f"Size: {module_size}, Part Code: {back_panel_part_code}", styles["Normal"]))

    # Touch Sense Board
    elements.append(Paragraph("Touch Sense Board", styles["Heading2"]))
    for circuit in selected_circuits:
        circuit_name, circuit_size = extract_circuit_parts(circuit)
        part_code = f"{circuit_size}_SEN_{circuit_name.replace(' ', '_').upper()}"
        # part_code = part_codes["touch_sense_board"].get(circuit, "Unknown")
        elements.append(Paragraph(f"Circuit: {circuit}, Part Code: {part_code}", styles["Normal"]))

    # Relay Board PCB
    elements.append(Paragraph("Relay Board PCB", styles["Heading2"]))
    for circuit in selected_circuits:
        circuit_name, circuit_size = extract_circuit_parts(circuit)
        part_code = f"{circuit_size}_REL_{circuit_name.replace(' ', '_').upper()}"
        # part_code = part_codes["relay_board_pcb"].get(circuit, "Unknown")
        elements.append(Paragraph(f"Circuit: {circuit}, Part Code: {part_code}", styles["Normal"]))

    # Power Supply (Compulsory)
    elements.append(Paragraph("Power Supply", styles["Heading2"]))
    elements.append(Paragraph("Part Code: F_DUAL_PS", styles["Normal"]))

    # ESP (for Automation)
    if automation_required == "Yes":
        elements.append(Paragraph("ESP (Automation Board)", styles["Heading2"]))
        elements.append(Paragraph("Part Code: ESP_COMMON", styles["Normal"]))

    # C Section
    elements.append(Paragraph("C Section", styles["Heading2"]))
    # c_section_count = sum(int(circuit.split(" (")[1].rstrip(")")[0]) // 2 for circuit in selected_circuits)
    c_section_count = int(module_size[:-1]) // 2
    elements.append(Paragraph(f"Number of C Sections: {c_section_count}", styles["Normal"]))

    # Big Cover
    elements.append(Paragraph("Big Cover", styles["Heading2"]))
    big_cover_size = "4M" if int(module_size[:-1]) <= 4 else "6M"
    elements.append(Paragraph(f"Size: {big_cover_size}, Part Code: BIG_COVER_{big_cover_size}", styles["Normal"]))

    # Small Cover
    elements.append(Paragraph("Small Cover", styles["Heading2"]))
    elements.append(Paragraph("Part Code: SMALL_COVER_1PC", styles["Normal"]))

    # Screw
    elements.append(Paragraph("Screw", styles["Heading2"]))
    screws_required = 2 + 2 * (int(module_size[:-1]) // 2)
    elements.append(
        Paragraph(f"Number of Screws: {screws_required}, Part Code: SCREW_{screws_required}PCS", styles["Normal"]))

    # Accessories
    elements.append(Paragraph("Accessories", styles["Heading2"]))
    if accessories:
        for accessory in accessories:
            elements.append(Paragraph(f"Accessory: {accessory}", styles["Normal"]))
    else:
        elements.append(Paragraph("No accessories selected.", styles["Normal"]))

    # Build PDF
    doc.build(elements)

    return pdf_filename


# Button to generate the PDF
if st.button("Generate PDF Report"):
    pdf_filename = generate_pdf_report(glass_color, module_size, selected_circuits, selected_accessories, automation)
    with open(pdf_filename, "rb") as pdf_file:
        st.download_button(label="Download PDF", data=pdf_file, file_name=pdf_filename, mime="application/pdf")
