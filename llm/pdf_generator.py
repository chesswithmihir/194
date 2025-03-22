from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

def generate_fonar_pdf(data, output_filename="FONAR_Report.pdf"):
    """
    Generates a PDF report similar to the draft FONAR form, using the data provided.
    
    :param data: A dictionary containing all relevant fields for the FONAR form.
    :param output_filename: The name of the output PDF file.
    """
    
    # Create a PDF document using A4 size
    doc = SimpleDocTemplate(output_filename, pagesize=A4,
                            rightMargin=30, leftMargin=30,
                            topMargin=30, bottomMargin=30)
    
    # Get a default style set
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_heading = styles["Heading1"]
    
    # A list to hold all the flowable elements (paragraphs, tables, etc.)
    flowables = []
    
    # 1. Title / Heading
    flowables.append(Paragraph("IMO Compliant Fuel Oil Non-Availability Report (FONAR)", style_heading))
    flowables.append(Spacer(1, 12))
    
    # 2. Intro Paragraph
    intro_text = """
    <b>This form shall be used for reporting non-availability of 0.50% m/m or 0.10% m/m sulphur fuels where applicable.</b><br/>
    It provides documentation if a ship is unable to obtain fuel oil compliant with MARPOL Annex VI. 
    A copy of this report and all supporting documents shall be kept on board for inspection for at least 12 months.
    """
    flowables.append(Paragraph(intro_text, style_normal))
    flowables.append(Spacer(1, 12))
    
    # 3. Basic Ship Info
    ship_info = f"""
    <b>Name of Ship:</b> {data.get("ship_name", "")} <br/>
    <b>Flag:</b> {data.get("flag", "")} <br/>
    <b>IMO Number:</b> {data.get("imo_number", "")} <br/>
    <b>Port of registry:</b> {data.get("port_of_registry", "")} <br/>
    <b>Gross Tonnage:</b> {data.get("gross_tonnage", "")} <br/>
    <b>Other Registration #:</b> {data.get("other_registration", "")} <br/>
    """
    flowables.append(Paragraph(ship_info, style_normal))
    flowables.append(Spacer(1, 12))
    
    # 4. Voyage Plan & Fuel Details
    voyage_info = f"""
    <b>Voyage Plan Description:</b> {data.get("voyage_plan", "")}<br/>
    <b>Last Port of Departure:</b> {data.get("last_port_of_departure", "")} <br/>
    <b>Date of Departure:</b> {data.get("date_departure_last_port", "")} <br/>
    <b>First Port of Call:</b> {data.get("first_port_of_call", "")} <br/>
    <b>Date of Arrival (First Port):</b> {data.get("date_arrival_first_port", "")} <br/>
    <b>Expected Departure from Port:</b> {data.get("date_expected_departure", "")} <br/>
    <b>Sulphur Content of Fuel in Use (BDN):</b> {data.get("sulphur_content_bdn", "")} <br/>
    """
    flowables.append(Paragraph(voyage_info, style_normal))
    flowables.append(Spacer(1, 12))
    
    # 5. ECA Info (If applicable)
    eca_info = f"""
    <b>E1. Date vessel first received notice of ECA transit:</b> {data.get("eca_notice_date", "")} <br/>
    <b>E2. Vessel's location at the time of notice:</b> {data.get("eca_notice_location", "")} <br/>
    <b>E3. Expected ECA Entry (Date/Time):</b> {data.get("eca_entry_datetime", "")} <br/>
    <b>E4. Expected ECA Exit (Date/Time):</b> {data.get("eca_exit_datetime", "")} <br/>
    <b>E5. Projected days main engines in operation within ECA:</b> {data.get("eca_projected_days", "")} <br/>
    <b>E6. Sulphur content of fuel when entering ECA (BDN):</b> {data.get("eca_sulphur_content", "")} <br/>
    """
    flowables.append(Paragraph("<b>If ship is to enter an Emissions Control Area (ECA):</b>", style_normal))
    flowables.append(Paragraph(eca_info, style_normal))
    flowables.append(Spacer(1, 12))
    
    # 6. Description of Actions Taken to Achieve Compliance
    compliance_actions = data.get("compliance_actions", "No data provided.")
    flowables.append(Paragraph("<b>Actions Taken to Attempt Compliance:</b>", style_normal))
    flowables.append(Paragraph(compliance_actions, style_normal))
    flowables.append(Spacer(1, 12))
    
    # 7. Suppliers Contacted - create a small table
    suppliers = data.get("suppliers_contacted", [])
    
    # Table Header
    table_data = [["Name of Supplier", "Address", "Date of Contact"]]
    for supplier in suppliers:
        table_data.append([
            supplier.get("name", ""),
            supplier.get("address", ""),
            supplier.get("date_of_contact", "")
        ])
    
    suppliers_table = Table(table_data, colWidths=[150, 200, 100])
    suppliers_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    
    flowables.append(Paragraph("<b>Suppliers Contacted:</b>", style_normal))
    flowables.append(suppliers_table)
    flowables.append(Spacer(1, 12))
    
    # 8. Disruption Info
    disruption_info = f"""
    <b>Port where compliant fuel was scheduled:</b> {data.get("scheduled_port_for_fuel", "")} <br/>
    <b>Supplier that reported non-availability:</b> {data.get("non_available_supplier", "")} <br/>
    <b>Operational Constraints:</b> {data.get("operational_constraints", "")} <br/>
    <b>Steps to Resolve Constraints:</b> {data.get("steps_to_resolve_constraints", "")} <br/>
    """
    flowables.append(Paragraph("<b>In case of fuel oil supply disruption:</b>", style_normal))
    flowables.append(Paragraph(disruption_info, style_normal))
    flowables.append(Spacer(1, 12))
    
    # 9. Availability & Next Steps
    availability_info = f"""
    <b>Availability of compliant fuel at first port-of-call:</b> {data.get("availability_first_port", "")} <br/>
    <b>Lowest sulphur content available (if no compliant fuel):</b> {data.get("lowest_sulphur_content", "")} <br/>
    <b>Fuel Quality Issues (if any):</b> {data.get("fuel_quality_issues", "")} <br/>
    """
    flowables.append(Paragraph("<b>Fuel Availability & Next Steps:</b>", style_normal))
    flowables.append(Paragraph(availability_info, style_normal))
    flowables.append(Spacer(1, 12))
    
    # 10. Previous FONAR Reports
    prev_fonars = data.get("previous_fonars", [])
    prev_table_data = [["Report Date", "Port", "Type of Fuel", "Comments"]]
    for fonar in prev_fonars:
        prev_table_data.append([
            fonar.get("report_date", ""),
            fonar.get("port", ""),
            fonar.get("fuel_type", ""),
            fonar.get("comments", "")
        ])
    
    prev_fonars_table = Table(prev_table_data, colWidths=[80, 80, 100, 180])
    prev_fonars_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    
    flowables.append(Paragraph("<b>Previous FONAR Reports (last 12 months):</b>", style_normal))
    flowables.append(prev_fonars_table)
    flowables.append(Spacer(1, 12))
    
    # 11. Signatures
    signature_info = f"""
    <b>Name of Master:</b> {data.get("name_of_master", "")} <br/>
    <b>Vessel Operator Name:</b> {data.get("vessel_operator_name", "")} <br/>
    <b>Local Agent(s) & Tel:</b> {data.get("local_agent_info", "")} <br/>
    <b>Name of Company (ISM Document):</b> {data.get("ism_company_name", "")} <br/>
    <b>Name of Designated Person Ashore (DPA) & Tel:</b> {data.get("dpa_info", "")} <br/>
    <b>Address:</b> {data.get("address", "")} <br/>
    <b>Date:</b> {data.get("report_date", "")} <br/>
    """
    flowables.append(Paragraph(signature_info, style_normal))
    
    # Build the PDF
    doc.build(flowables)
    print(f"PDF generated: {output_filename}")


# --------------- TEST CASE ---------------
if __name__ == "__main__":
    # Example data dictionary simulating what the LLM might provide
    example_data = {
        "ship_name": "SS AI Explorer",
        "flag": "Panama",
        "imo_number": "1234567",
        "port_of_registry": "Panama City",
        "gross_tonnage": "50000",
        "other_registration": "REG-XYZ-2023",
        "voyage_plan": "Transit from Port A to Port B, passing through ECA Region.",
        "last_port_of_departure": "Port A",
        "date_departure_last_port": "2025-03-15",
        "first_port_of_call": "Port B",
        "date_arrival_first_port": "2025-03-20",
        "date_expected_departure": "2025-03-22",
        "sulphur_content_bdn": "0.47%",
        "eca_notice_date": "2025-03-10",
        "eca_notice_location": "Gulf of Mexico",
        "eca_entry_datetime": "2025-03-18 06:00",
        "eca_exit_datetime": "2025-03-19 23:00",
        "eca_projected_days": "2",
        "eca_sulphur_content": "0.47%",
        "compliance_actions": (
            "1. Checked multiple suppliers at Port A.\n"
            "2. Attempted to deviate slightly to find compliant fuel.\n"
            "3. Found partial availability but insufficient quantity."
        ),
        "suppliers_contacted": [
            {"name": "FuelCorp Ltd.", "address": "123 Dock Road", "date_of_contact": "2025-03-10"},
            {"name": "Marine Fuel Inc.", "address": "456 Harbor Lane", "date_of_contact": "2025-03-11"},
        ],
        "scheduled_port_for_fuel": "Port A",
        "non_available_supplier": "Marine Fuel Inc.",
        "operational_constraints": "Fuel system compatibility issues with high-blend biofuel.",
        "steps_to_resolve_constraints": "Ship-wide retrofit planned for Q2 2025.",
        "availability_first_port": "Limited availability at 0.80% sulfur.",
        "lowest_sulphur_content": "0.80%",
        "fuel_quality_issues": "High water content detected during sampling.",
        "previous_fonars": [
            {
                "report_date": "2024-12-01",
                "port": "Port X",
                "fuel_type": "0.50% LSFO",
                "comments": "Supplier shortage"
            },
            {
                "report_date": "2024-10-15",
                "port": "Port Y",
                "fuel_type": "0.10% ULSFO",
                "comments": "Supply chain delay"
            }
        ],
        "name_of_master": "Captain Nemo",
        "vessel_operator_name": "Oceanic Ventures",
        "local_agent_info": "Agent Co. (555-1234)",
        "ism_company_name": "Global Shipping Corp.",
        "dpa_info": "John Smith (555-5678)",
        "address": "123 Maritime Way, Panama City, Panama",
        "report_date": "2025-03-19"
    }
    
    generate_fonar_pdf(example_data, "Test_FONAR_Report.pdf")
