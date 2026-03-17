# Mirxes Clinical Risk Dashboard

## Features (TASK 1)
# Required
* Load and display the JSON summary from Task 1
* Show a table of Patient ID, Risk Score, and Risk Category
* Visually distinguish the three risk categories (e.g. colour coding)

# Optional (encouraged)
* Summary statistics or a chart showing distribution across risk categories
* Filtering or sorting by risk category or score
* A downloadable patient-facing report (PDF or DOCX)
* Any other feature you think adds clinical or operational value

# Final Features
*   View a list of patients with their risk scores and categories.
*   Filter patients by risk category and search by patient ID.
*   Visualize risk distribution with a pie chart.
*   Download a PDF report for each patient.
*   Update the patient data by re-running the risk categorization script.

## Technology Stack
*   **Frontend:** HTML, Bootstrap, JavaScript, Chart.js
*   **Backend:** Python, FastAPI, Pandas, FPDF

## Installation & Setup (TASK 2)
1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Mirxes_OA
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install the dependencies:**
    ```
    pip install -r requirements.txt
    ```

### Running the Application
1.  **Run Python Script for Risk Categorization:**
    ```bash
    python risk_score_categorizer.py
    ```

2.  **Start the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
3.  **Open your browser and navigate to:**
    ```bash
    http://127.0.0.1:8000
    ```

## API Endpoints
*   `GET /`: Serves the main HTML page.
*   `GET /api/patients`: Returns a JSON object of all patients and their risk data.
*   `GET /api/patients/{patient_id}/report`: Generates and downloads a PDF report for a specific patient.
*   `POST /api/run-script`: Executes the `risk_score_categorizer.py` script to update the patient data from `patients.xlsx`.

---

# Project Write-up (TASK 3)

## Why did you choose that layout and technology stack?
|#|Tech Stack|Description|
|---|---|---|
|1|Python|Python is a versatile language with a strong data science ecosystem.|
|2|FastAPI|FastAPI is one of the fastest python framework which is best to serve real-time data processing|
|3|Pandas|Pandas is used for data manipulation and reading CSV/Excel file.|
|4|FPDF|FPDF is used to generate PDF reports for each patient.|
|5|HTML/CSS/JavaScript|HTML/CSS/JavaScript is standard web technologies for the frontend.|
|6|Bootstrap|Bootstrap is a popular CSS framework for creating responsive and clean layouts.|
|7|Chart.js|Chart.js is a simple JavaScript library charting for visualization.|

## What did you assume about the data, the users, or the clinical context?
## Assumptions
*   **Data (Constrains):**
    *   The data is assumed to be cleaned and well-formatted, with patient_id and risk_score columns provided.
    *   Patient IDs are assumed to be unique.
    *   Risk scores are assumed to be numeric between 0 and 1.
*   **Users:**
    *   The users (clinicians or lab operators) want to quickly identify high-risk patients.
    *   Users are assumed to use the latest data with filter for research purposes.
*   **Clinical Context:**
    *   The primary need is to easily visualize and report the existing risk scores.
    *   To provide safe and effective care from looking at doctor to patient ratio.

## What would need to change if the dataset grew to 100,000 patients or multiple concurrent users?
## Scalability (100,000 Patients or Multiple Users)
*   **Data Loading:** 
    * If the dataset grew to 100,000 patients, Loading the Excel file directly into memory with Pandas would be very slow and the output would be very large everytime the script is run. To handle this, I would use a relational database such as Oracles Database, PostgreSQL or MySQL to store the patient data. Then the script would populate the database, and then API would then query the database instead of reading a JSON file.

*   **Concurrent Users:**
    *   While FastAPI is asynchronous and can handle multiple concurrent users much better than other python frameworks like Flask, performance can still be improved by deploying the application using a production web server like Gunicorn, which can manage multiple worker processes. Which then the process can be run using process manager 2 (PM2) for stability. Then you would typically run multiple worker processes behind a reverse proxy like Nginx.

## Known limitations, future improvements, or anything you want to flag.
*   **Authentication:** The dashboard is currently public and no safety features are implemented. A production system would require user authentication and authorization to access to patient data.
*   **PDF Generation:** The PDF report is very basic. It can be improved with better formatting, and with more data, it can provide a more comprehensive patient information.
*   **Testing:** The application lacks automated tests. Unit tests for integration tests for the API endpoints would improve robustness.
*   **Configuration:** Hardcoded values like file the paths or risk thresholds could be moved to a separate configuration file.