from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO


def generate_pdf_report(contract_id: str, analysis_data: dict):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph("ClauseGuard AI Risk Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"Contract ID: {contract_id}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    overall_score = analysis_data.get("overall_risk_score", "N/A")
    elements.append(Paragraph(f"Overall Risk Score: {overall_score}", styles["Heading2"]))
    elements.append(Spacer(1, 0.5 * inch))

    for clause_name, clause_data in analysis_data.items():
        if clause_name == "overall_risk_score":
            continue

        elements.append(Paragraph(clause_name.upper(), styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph(f"Risk Level: {clause_data.get('risk_level')}", styles["Normal"]))
        elements.append(Spacer(1, 0.1 * inch))

        elements.append(Paragraph(f"Clause Text: {clause_data.get('text')}", styles["Normal"]))
        elements.append(Spacer(1, 0.1 * inch))

        elements.append(Paragraph(f"Why Risky: {clause_data.get('why_risky')}", styles["Normal"]))
        elements.append(Spacer(1, 0.1 * inch))

        elements.append(Paragraph(f"Scenario: {clause_data.get('scenario_analysis')}", styles["Normal"]))
        elements.append(Spacer(1, 0.1 * inch))

        elements.append(Paragraph(f"Suggested Rewrite: {clause_data.get('suggested_rewrite')}", styles["Normal"]))
        elements.append(Spacer(1, 0.5 * inch))

    doc.build(elements)
    buffer.seek(0)

    return buffer