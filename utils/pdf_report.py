from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def safe(value, suffix=""):
    if value in (None, "", "—"):
        return "—"
    return f"{value}{suffix}"


def generate_consultation_pdf(data: dict) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------
    story.append(Paragraph("CAREASSIST – CONSULTATION REPORT", styles["Title"]))
    story.append(Spacer(1, 14))

    # -------------------------------------------------
    # PATIENT DETAILS
    # -------------------------------------------------
    story.append(Paragraph("Patient Details", styles["Heading2"]))
    story.append(Paragraph(f"Name: {safe(data.get('patient_name'))}", styles["Normal"]))
    story.append(Paragraph(f"Gender: {safe(data.get('gender'))}", styles["Normal"]))
    story.append(Paragraph(f"DOB: {safe(data.get('dob'))}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # -------------------------------------------------
    # DOCTOR DETAILS
    # -------------------------------------------------
    story.append(Paragraph("Doctor Details", styles["Heading2"]))
    story.append(
        Paragraph(
            f"Consulting Doctor: {safe(data.get('doctor_name'))}",
            styles["Normal"]
        )
    )
    story.append(Spacer(1, 12))

    # -------------------------------------------------
    # CHIEF COMPLAINT
    # -------------------------------------------------
    story.append(Paragraph("Chief Complaint", styles["Heading2"]))
    story.append(Paragraph(safe(data.get("chief_complaint")), styles["Normal"]))
    story.append(Spacer(1, 12))

    # -------------------------------------------------
    # VITALS
    # -------------------------------------------------
    story.append(Paragraph("Vitals", styles["Heading2"]))

    vitals = data.get("vitals", {})

    vitals_table = Table([
        ["Height (cm)", safe(vitals.get("height"))],
        ["Weight (kg)", safe(vitals.get("weight"))],
        ["Temperature (°C)", safe(vitals.get("temperature"))],
        ["Blood Pressure", safe(vitals.get("bp"))],
        ["Heart Rate", safe(vitals.get("heart_rate"))],
        ["SpO₂ (%)", safe(vitals.get("spo2"))],
    ])

    story.append(vitals_table)
    story.append(Spacer(1, 12))

    # -------------------------------------------------
    # SYMPTOMS
    # -------------------------------------------------
    story.append(Paragraph("Symptoms", styles["Heading2"]))
    symptoms = data.get("symptoms", [])

    if symptoms:
        for s in symptoms:
            story.append(Paragraph(f"- {s}", styles["Normal"]))
    else:
        story.append(Paragraph("No symptoms reported.", styles["Normal"]))

    story.append(Spacer(1, 12))

    # -------------------------------------------------
    # AI PREDICTION
    # -------------------------------------------------
    story.append(Paragraph("AI Risk Prediction", styles["Heading2"]))
    story.append(Paragraph(safe(data.get("risk_prediction")), styles["Normal"]))
    story.append(Spacer(1, 12))

    # -------------------------------------------------
    # DOCTOR REMARKS
    # -------------------------------------------------
    story.append(Paragraph("Doctor Remarks", styles["Heading2"]))
    story.append(Paragraph(safe(data.get("doctor_remarks")), styles["Normal"]))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
