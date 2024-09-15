import datetime

import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from collections import Counter


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

# Ask how many modules to configure
num_modules = st.number_input("Enter number of modules to configure", min_value=1, step=1)
module_data = []

# Loop through the number of modules
for module_index in range(num_modules):
    st.write(f"### Module {module_index + 1}")

    # User selections per module
    module_size = st.selectbox(f"Select Module Size for Module {module_index + 1}", module_sizes,
                               key=f"module_size_{module_index}")
    remaining_space = int(module_size[:-1])  # Extract numeric part from module size (e.g., "12M" -> 12)

    st.write(f"Module Size: {module_size}, Total Space: {remaining_space}M")

    # Accessory selection for each module
    selected_accessories = []
    for accessory, size in accessories.items():
        if st.checkbox(f"Add {accessory} to Module {module_index + 1}", key=f"{accessory}_module_{module_index}"):
            if remaining_space >= size:
                selected_accessories.append(accessory)
                remaining_space -= size
                st.write(f"{accessory} added to Module {module_index + 1}, Remaining Space: {remaining_space}M")
            else:
                st.warning(f"Not enough space for {accessory} in Module {module_index + 1}.")

    # Ensure space management for 1M accessories
    if remaining_space == 1:
        st.warning(f"You must add another 1M accessory for Module {module_index + 1}.")
        for accessory, size in accessories.items():
            if size == 1 and accessory not in selected_accessories:
                if st.checkbox(f"Add {accessory} (1M) to Module {module_index + 1}",
                               key=f"{accessory}_1M_module_{module_index}"):
                    selected_accessories.append(accessory)
                    remaining_space -= size
                    st.write(f"{accessory} added to Module {module_index + 1}, Remaining Space: {remaining_space}M")

    # Circuit selection to fill remaining space
    selected_circuits = []
    if remaining_space > 0:
        st.write(f"Select circuits to fill the remaining {remaining_space}M space for Module {module_index + 1}:")
        while remaining_space > 0:
            available_circuits = [size for size in circuits if int(size[:-1]) <= remaining_space]
            if not available_circuits:
                st.warning(f"Not enough space left for any circuit in Module {module_index + 1}.")
                break
            selected_circuit_size = st.selectbox(f"Select Circuit Size for Module {module_index + 1}",
                                                 available_circuits,
                                                 key=f"circuit_size_{module_index}_{remaining_space}")
            selected_circuit = st.selectbox(f"Select Circuit for Module {module_index + 1}",
                                            circuits[selected_circuit_size],
                                            key=f"option_{module_index}_{remaining_space}")
            selected_circuits.append(f"{selected_circuit} ({selected_circuit_size})")
            remaining_space -= int(selected_circuit_size[:-1])

    # Glass and Bezel Color selection
    glass_color = st.selectbox(f"Select Glass Colour for Module {module_index + 1}", glass_colors,
                               key=f"glass_color_{module_index}")
    bezel_color = st.selectbox(f"Select Bezel Colour for Module {module_index + 1}", bezel_colors,
                               key=f"bezel_color_{module_index}")
    automation = st.selectbox(f"Automation Required for Module {module_index + 1}", automation_required,
                              key=f"automation_{module_index}")

    # Store data for this module
    module_data.append({
        "module_size": module_size,
        "selected_accessories": selected_accessories,
        "selected_circuits": selected_circuits,
        "glass_color": glass_color,
        "bezel_color": bezel_color,
        "automation": automation
    })

# Display summary for each module
st.write("### Summary of All Modules")
for i, module in enumerate(module_data, start=1):
    st.write(f"#### Module {i}")
    st.write(f"Module Size: {module['module_size']}")
    st.write(
        f"Selected Accessories: {', '.join(module['selected_accessories']) if module['selected_accessories'] else 'None'}")
    st.write(f"Selected Circuits: {', '.join(module['selected_circuits']) if module['selected_circuits'] else 'None'}")
    st.write(f"Glass Colour: {module['glass_color']}")
    st.write(f"Bezel Colour: {module['bezel_color']}")
    st.write(f"Automation Required: {module['automation']}")


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

    # Iterate over each word in the phrase
    for word in words:
        # If the word is a number, keep it as is
        if word.isdigit():
            result += word
        else:
            # Otherwise, append the first letter of the word (uppercase)
            result += word[0].upper()

    return result


def generate_pdf_report(modules):
    pdf_filename = f"Alisan_{datetime.date.today()}.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    part_counter = Counter()  # Counter to store total pieces of each part code

    for idx, module in enumerate(modules, 1):
        elements.append(Paragraph(f"Module {idx} Report", styles["Heading2"]))

        data = [["Component", "Details", "Part Code"]]
        module_size = module['module_size']
        glass_color = module['glass_color']
        bezel_color = module['bezel_color']
        automation = module['automation']
        selected_accessories = module['selected_accessories']
        selected_circuits = module['selected_circuits']

        # Front Panel
        front_panel_part_code = f"{module_size}{glass_color[0].upper()}F"
        data.append(["Front Panel", f"Colour: {glass_color}, Size: {module_size}", front_panel_part_code])
        part_counter[front_panel_part_code] += 1  # Increment part counter

        # Back Panel
        back_panel_part_code = f"{module_size}B"
        data.append(["Back Panel", f"Size: {module_size}", back_panel_part_code])
        part_counter[back_panel_part_code] += 1

        # Touch Sense Board
        for circuit in selected_circuits:
            circuit_name, circuit_size = extract_circuit_parts(circuit)
            circuit_name = get_initials(circuit_name)
            part_code = f"{circuit_size}_SEN_{circuit_name.replace(' ', '_').upper()}"
            data.append(["Touch Sense Board", f"{circuit}", part_code])
            part_counter[part_code] += 1

        # Relay Board PCB
        for circuit in selected_circuits:
            circuit_name, circuit_size = extract_circuit_parts(circuit)
            circuit_name = get_initials(circuit_name)
            part_code = f"{circuit_size}_REL_{circuit_name.replace(' ', '_').upper()}"
            data.append(["Relay Board PCB", f"{circuit}", part_code])
            part_counter[part_code] += 1

        # Accessories
        if selected_accessories:
            for accessory in selected_accessories:
                data.append(["Accessory", accessory, ""])
        else:
            data.append(["Accessories", "No accessories selected.", ""])

        # Automation
        if automation == "Yes":
            data.append(["ESP", "Automation Board", "ESP_COMMON"])
            part_counter["ESP_COMMON"] += 1

        # Power Supply
        data.append(["Power Supply", "Compulsory", "F_DUAL_PS"])
        part_counter["F_DUAL_PS"] += 1

        # Bezel
        data.append(["Bezel Colour", bezel_color, "-"])

        # C Section
        c_section_count = int(module_size[:-1]) // 2
        data.append(["C Section", f"Number of C Sections: {c_section_count}", ""])
        part_counter["C_SECTION"] += c_section_count

        # Big Cover
        big_cover_size = "4M" if int(module_size[:-1]) <= 4 else "6M"
        data.append(["Big Cover", f"Size: {big_cover_size}", f"BIG_COVER_{big_cover_size}"])
        part_counter[f"BIG_COVER_{big_cover_size}"] += 1

        # Small Cover
        data.append(["Small Cover", "-", "SMALL_COVER_1PC"])
        part_counter["SMALL_COVER_1PC"] += 1

        # Screws
        screws_required = 2 + 2 * (int(module_size[:-1]) // 2)
        data.append(["Screw", f"Number of Screws: {screws_required}", f"SCREW_{screws_required}PCS"])
        part_counter[f"SCREW_{screws_required}PCS"] += screws_required

        # Add a table for each module
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))

    # Add a second table showing the total pieces for each part code
    elements.append(Paragraph("Total Pieces by Part Code", styles["Heading2"]))

    total_pieces_data = [["Part Code", "Total Pieces"]]
    for part_code, count in part_counter.items():
        total_pieces_data.append([part_code, str(count)])

    total_pieces_table = Table(total_pieces_data)
    total_pieces_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(total_pieces_table)

    doc.build(elements)
    return pdf_filename


if st.button("Generate PDF Report"):
    pdf_filename = generate_pdf_report(module_data)
    with open(pdf_filename, "rb") as pdf_file:
        st.download_button(label="Download PDF", data=pdf_file, file_name=pdf_filename, mime="application/pdf")
