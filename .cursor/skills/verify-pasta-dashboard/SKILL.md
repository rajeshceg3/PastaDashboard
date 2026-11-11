# Verify PastaDashboard
Pasta Dashboard - streamlit dashboard of pasta types with nutritional info (pandas, altair).
## Launch
pip install streamlit pandas altair, then streamlit run pasta_dashboard.py.
## Doctor
`python3 .cursor/skills/verify-pasta-dashboard/verify.py`
## Drive
Compiles pasta_dashboard.py, validates both JSON data files, boots the streamlit server headless and asserts it serves the app.
## Evidence
`.cursor/skills/verify-pasta-dashboard/evidence.json`
## Cleanup
Static/streamlit server terminated after the render.
## Known boundaries
Render smoke only; scene quality unverified. Playwright e2e configs are not exercised (chromium-only sandbox).
