from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO


def generate_consultation_pdf(data: dict) -> bytes:
    """
    Generates a consultation PDF and returns bytes.
    """

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------
    elements.append(Paragraph(
        "<b>CAREASSIST – CONSULTATION REPORT</b>",
        styles["Title"]
    ))
    elements.append(Spacer(1, 12))

    # -------------------------------------------------
    # PATIENT DETAILS
    # -------------------------------------------------
    patient_table = Table([
        ["Patient Name", data["patient_name"]],
        ["Gender", data["gender"]],
        ["Date of Birth", data["dob"]],
        ["Consultation ID", str(data["consultation_id"])],
        ["Consultation Date", data["date"]],
    ])

    patient_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
    ]))

    elements.append(Paragraph("<b>Patient Information</b>", styles["Heading2"]))
    elements.append(patient_table)
    elements.append(Spacer(1, 12))

    # -------------------------------------------------
    # CHIEF COMPLAINT
    # -------------------------------------------------
    elements.append(Paragraph("<b>Chief Complaint</b>", styles["Heading2"]))
    elements.append(Paragraph(data["chief_complaint"], styles["Normal"]))
    elements.append(Spacer(1, 12))

    # -------------------------------------------------
    # VITALS
    # -------------------------------------------------
    vitals_table = Table([
        ["Height (cm)", data["vitals"]["height"]],
        ["Weight (kg)", data["vitals"]["weight"]],
        ["Temperature (°C)", data["vitals"]["temperature"]],
        ["Blood Pressure", data["vitals"]["bp"]],
        ["Heart Rate", data["vitals"]["heart_rate"]],
        ["SpO₂ (%)", data["vitals"]["spo2"]],
    ])

    vitals_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(Paragraph("<b>Vitals</b>", styles["Heading2"]))
    elements.append(vitals_table)
    elements.append(Spacer(1, 12))

    # -------------------------------------------------
    # SYMPTOMS
    # -------------------------------------------------
    elements.append(Paragraph("<b>Symptoms</b>", styles["Heading2"]))

    if data["symptoms"]:
        for s in data["symptoms"]:
            elements.append(Paragraph(f"- {s}", styles["Normal"]))
    else:
        elements.append(Paragraph("No symptoms reported.", styles["Italic"]))

    elements.append(Spacer(1, 12))

    # -------------------------------------------------
    # AI RISK
    # -------------------------------------------------
    elements.append(Paragraph("<b>AI Risk Assessment</b>", styles["Heading2"]))
    elements.append(Paragraph(
        data["risk_prediction"],
        styles["Normal"]
    ))

    elements.append(Spacer(1, 12))

    # -------------------------------------------------
    # DOCTOR REMARKS
    # -------------------------------------------------
    elements.append(Paragraph("<b>Doctor Remarks</b>", styles["Heading2"]))
    elements.append(Paragraph(data["doctor_remarks"], styles["Normal"]))

    elements.append(Spacer(1, 20))

    # -------------------------------------------------
    # FOOTER
    # -------------------------------------------------
    elements.append(Paragraph(
        "<i>This report is generated for clinical reference only.</i>",
        styles["Italic"]
    ))

    doc.build(elements)
    buffer.seek(0)

    return buffer.read()
