from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
import json
from fpdf import FPDF
import subprocess
import sys


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/api/patients")
async def get_patients():
    with open("output.json") as f:
        data = json.load(f)
    return data

@app.get("/api/patients/{patient_id}/report")
async def get_patient_report(patient_id: str):
    # 1. Get patient data
    with open("output.json") as f:
        all_patients_data = json.load(f)
    
    patient_data = all_patients_data.get(patient_id)

    if not patient_data:
        return Response(content="Patient not found", status_code=404)

    # 2. Generate PDF in memory
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', size=20)
    pdf.cell(0, 15, 'Patient Risk Report', 0, 1, 'C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Patient ID: {patient_id}", 0, 1)
    pdf.cell(0, 10, f"Risk Score: {patient_data['risk_score']:.2f}", 0, 1)
    
    # Color-coded risk category
    risk_category = patient_data['risk_category']
    if risk_category == 'High':
        pdf.set_text_color(217, 83, 79) # red
    elif risk_category == 'Medium':
        pdf.set_text_color(240, 173, 78) # orange
    else: # Low
        pdf.set_text_color(92, 184, 92) # green
        
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(0, 10, f"Risk Category: {risk_category}", 0, 1)
    pdf.set_text_color(0, 0, 0) # reset to black
    pdf.ln(10)
    
    # Add some explanation for the patient
    pdf.set_font("Arial", '', size=11)
    pdf.cell(0, 10, "What this means for you:", 0, 1)
    
    pdf.set_font("Arial", 'I', size=10)
    if risk_category == 'High':
        explanation = "A high risk score indicates a significant likelihood of the condition. It is very important to consult with your doctor for further evaluation and guidance."
    elif risk_category == 'Medium':
        explanation = "A medium risk score indicates a moderate likelihood of the condition. It is advisable to discuss these results with your healthcare provider to determine next steps."
    else: # Low
        explanation = "A low risk score indicates a reduced likelihood of the condition. Please continue with your regular health check-ups and maintain a healthy lifestyle."
        
    pdf.multi_cell(0, 5, explanation)
    
    # 3. Return PDF as a response
    pdf_output = pdf.output(dest='S').encode('latin-1')
    
    headers = {
        'Content-Disposition': f'attachment; filename="patient_report_{patient_id}.pdf"'
    }
    return Response(content=pdf_output, media_type='application/pdf', headers=headers)

@app.post("/api/run-script")
async def run_script():
    try:
        python_executable = sys.executable
        result = subprocess.run([python_executable, "risk_score_categorizer.py"], check=True, capture_output=True, text=True)
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr}
