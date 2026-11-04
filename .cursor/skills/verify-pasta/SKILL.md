---
name: verify-pasta
description: Run PastaDashboard's actual Streamlit browser journeys for filtering, sorting, search and nutrition while preserving external image/map failures as separate blockers.
---
# Verify Pasta Dashboard
## Surface and isolation
Streamlit web dashboard with local JSON data, remote images and external Mapbox map. No user data/auth/database. Use an owned local server, not an unknown shared port. External media failure is not a passing whole-app result even if text journeys pass.
## Launch
Create a Python virtualenv and install this directory's requirements.txt. Use Node22.12+ and npm ci --prefix .cursor/skills/verify-pasta for the pinned browser helper. From repo root run `python -m streamlit run pasta_dashboard.py --server.address 127.0.0.1 --server.port 8503 --server.headless true --browser.gatherUsageStats false`. Choose a free port and pass its URL to the helper. Keep exact PID for teardown. Ready requires the real rendered10entry app, not only /_stcore/health.
## Doctor
`node .cursor/skills/verify-pasta/helpers/drive.mjs doctor --base http://127.0.0.1:8503/ --width 390 --out .verification-evidence/doctor`
Checks actual heading,10entries, no Streamlit exception and no browser pageerror.
## Drive
`node .cursor/skills/verify-pasta/helpers/drive.mjs drive --base http://127.0.0.1:8503/ --width 390 --out .verification-evidence/mobile`
Repeat with --width 1365 and a separate evidence directory. Uses actual combobox options, typed search/Enter, sidebar close and expander clicks. Asserts Long membership, both exact sort orders, Ravioli match, no-results message, clear restoration and nutrition expansion. Streamlit rerenders controls, so resolve fresh handles and wait for resulting state. No internal setters or AppTest-only UI claims.
## Evidence
JSON and screenshots survive cleanup. Inspect actual pixels. JSON separately records each external image's loaded state and map canvas size; text-journey ok does not certify these media. Current browser run reported all11remote images unloaded and unrendered base map; whole-app media acceptance blocked. Nutrition facts and exact geographic origin claims are inherited content, not independently validated by this workflow.
## Cleanup
Helper closes only its browser. Stop/reap the exact Streamlit PID you started, including failed iterations. Never kill by name/delete evidence. No account settings, deployment, paid provider or source data mutations.
## Helpers
Executable helpers/drive.mjs, pinned package.json/package-lock.json and Python requirements.txt in this directory. See features/README.md. Maintain source maps and real journeys as app changes.
