from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO


def generate_pdf_report(contract_id: str, analysis_data: dict):
    # --------------------------------------------
    # Create an in-memory buffer to store PDF
    # --------------------------------------------
    buffer = BytesIO()

    # Create PDF document object
    doc = SimpleDocTemplate(buffer)

    # List that will hold all PDF elements
    elements = []

    # Load default ReportLab styles
    styles = getSampleStyleSheet()

    # --------------------------------------------
    # Title Section
    # --------------------------------------------
    elements.append(Paragraph("ClauseGuard AI Risk Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Show Contract ID
    elements.append(Paragraph(f"Contract ID: {contract_id}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # --------------------------------------------
    # Overall Risk Score Section
    # --------------------------------------------
    overall_score = analysis_data.get("overall_risk_score", "N/A")

    elements.append(
        Paragraph(f"Overall Risk Score: {overall_score}", styles["Heading2"])
    )
    elements.append(Spacer(1, 0.5 * inch))

    # --------------------------------------------
    # Clause Details Section
    # --------------------------------------------
    for clause_name, clause_data in analysis_data.items():

        # Skip the overall score key
        if clause_name == "overall_risk_score":
            continue

        # 🚨 Skip if clause is None (clause not found in contract)
        if clause_data is None:
            continue

        # 🚨 Extra safety: ensure clause_data is a dictionary
        if not isinstance(clause_data, dict):
            continue

        # Clause Title
        elements.append(
            Paragraph(clause_name.upper(), styles["Heading2"])
        )
        elements.append(Spacer(1, 0.2 * inch))

        # Risk Level
        elements.append(
            Paragraph(
                f"Risk Level: {clause_data.get('risk_level', 'N/A')}",
                styles["Normal"]
            )
        )
        elements.append(Spacer(1, 0.1 * inch))

        # Clause Text
        elements.append(
            Paragraph(
                f"Clause Text: {clause_data.get('text', 'Not available')}",
                styles["Normal"]
            )
        )
        elements.append(Spacer(1, 0.1 * inch))

        # Why Risky
        elements.append(
            Paragraph(
                f"Why Risky: {clause_data.get('why_risky', 'Not available')}",
                styles["Normal"]
            )
        )
        elements.append(Spacer(1, 0.1 * inch))

        # Scenario Analysis
        elements.append(
            Paragraph(
                f"Scenario: {clause_data.get('scenario_analysis', 'Not available')}",
                styles["Normal"]
            )
        )
        elements.append(Spacer(1, 0.1 * inch))

        # Suggested Rewrite
        elements.append(
            Paragraph(
                f"Suggested Rewrite: {clause_data.get('suggested_rewrite', 'Not available')}",
                styles["Normal"]
            )
        )
        elements.append(Spacer(1, 0.5 * inch))

    # --------------------------------------------
    # Build PDF document
    # --------------------------------------------
    doc.build(elements)

    # Move cursor to beginning of buffer
    buffer.seek(0)

    # Return PDF as file-like object
    return buffer