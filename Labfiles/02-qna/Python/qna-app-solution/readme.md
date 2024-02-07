# QnA App Solution Python
This is solution of QnA code of python

## How to run?
1. Create and activate Virtual Environment
    ```
    python -m venv .venv
    ```
    Activate Virtual Environment

    Windows :
    ```
    .venv/Scripts/activate
    ```
    Linux :
    ```
    .venv/bin/activate
    ```
2. Install dependencies
    ```
    pip install -r requirements.txt
    ```

3. Add API Credential in `.env` file.
    ```
    AI_SERVICE_ENDPOINT=<YOUR_AI_SERVICES_ENDPOINT
    AI_SERVICE_KEY=YOUR_AI_SERVICES_KEY
    QA_PROJECT_NAME=LearnFAQ
    QA_DEPLOYMENT_NAME=production
    ```

4. Run the Program
    ```
    python ana-app.py
    ```


