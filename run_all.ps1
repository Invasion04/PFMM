# Start Flask backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\mkmad\.cursor\PFM\Backend; .\venv\Scripts\Activate.ps1; python app.py"

# Start Streamlit frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\mkmad\.cursor\PFM\frontend; .\venv\Scripts\Activate.ps1; streamlit run app.py"