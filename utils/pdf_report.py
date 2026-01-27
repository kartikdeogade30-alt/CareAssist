from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def generate_consultation_pdf(data: dict) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x = 50
    y = height - 50
    line_gap = 16

    def draw(text):
        nonlocal y
        c.drawString(x, y, text)
        y -= line_gap

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------
    c.setFont("Helvetica-Bold", 16)
    draw("CareAssist – Consultation Report")
    y -= 20

    c.setFont("Helvetica", 10)
    draw(f"Patient Name: {data.get('patient_name', '-')}")
    draw(f"Gender: {data.get('gender', '-')}")
    draw(f"DOB: {data.get('dob', '-')}")
    draw(f"Doctor: {data.get('doctor_name', '-')}")
    y -= 20

    # -------------------------------------------------
    # CHIEF COMPLAINT
    # -------------------------------------------------
    c.setFont("Helvetica-Bold", 12)
    draw("Chief Complaint")
    c.setFont("Helvetica", 10)
    draw(data.get("chief_complaint", "-"))
    y -= 20

    # -------------------------------------------------
    # VITALS
    # -------------------------------------------------
    c.setFont("Helvetica-Bold", 12)
    draw("Vitals")
    c.setFont("Helvetica", 10)

    vitals = data.get("vitals", {})
    draw(f"Height: {vitals.get('height', '-')}")
    draw(f"Weight: {vitals.get('weight', '-')}")
    draw(f"Temperature: {vitals.get('temperature', '-')}")
    draw(f"Blood Pressure: {vitals.get('bp', '-')}")
    draw(f"Heart Rate: {vitals.get('heart_rate', '-')}")
    draw(f"SpO2: {vitals.get('spo2', '-')}")
    y -= 20

    # -------------------------------------------------
    # SYMPTOMS
    # -------------------------------------------------
    c.setFont("Helvetica-Bold", 12)
    draw("Reported Symptoms")
    c.setFont("Helvetica", 10)

    symptoms = data.get("symptoms", [])
    if symptoms:
        for s in symptoms:
            draw(f"- {s}")
    else:
        draw("No symptoms reported")
    y -= 20

    # -------------------------------------------------
    # AI INSIGHTS (HUMAN READABLE)
    # -------------------------------------------------
    c.setFont("Helvetica-Bold", 12)
    draw("AI Clinical Insights")
    c.setFont("Helvetica", 10)

    prediction = data.get("risk_prediction", {})

    # ---- VITALS RISK ----
    vitals_risk = prediction.get("vitals_risk", {})
    if vitals_risk.get("status") == "AVAILABLE":
        draw(f"Vitals Risk Level: {vitals_risk.get('risk_level')}")
    else:
        draw("Vitals Risk Level: Not Available")

    y -= 10

    # ---- DISEASE PREDICTION ----
    disease = prediction.get("disease_prediction", {})
    if disease.get("status") == "AVAILABLE":
        draw(f"Primary Condition: {disease.get('primary_disease')}")

        preds = disease.get("predictions", [])
        if preds:
            draw("Other Possible Conditions:")
            for p in preds:
                conf = round(p["confidence"] * 100, 2)
                draw(f"- {p['disease']} ({conf}%)")
    else:
        draw("Disease Prediction: Not Available")

    y -= 20

    # -------------------------------------------------
    # DOCTOR REMARKS
    # -------------------------------------------------
    c.setFont("Helvetica-Bold", 12)
    draw("Doctor Remarks")
    c.setFont("Helvetica", 10)
    draw(data.get("doctor_remarks", "— No remarks added —"))

    # -------------------------------------------------
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.getvalue()
