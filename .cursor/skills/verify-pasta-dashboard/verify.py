#!/usr/bin/env python3
"""Verification runner for PastaDashboard. See SKILL.md."""
import json, os, re, subprocess, sys, time
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]
CHROME = os.environ.get('CHROME_PATH', '/usr/bin/google-chrome')
failures = []
def check(name, ok, detail=''):
    print(('PASS' if ok else 'FAIL'), name, (':: ' + str(detail))[:400] if detail else '')
    if not ok: failures.append(name)
def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=900, **kw)
def render(url, markers):
    proc = subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu',
                           '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1',
                           '--virtual-time-budget=9000', '--window-size=1280,900',
                           '--dump-dom', url], capture_output=True, text=True, timeout=120)
    dom = proc.stdout
    check('render: app boots', all(m in dom for m in markers), dom[:200])
    errs = [l for l in proc.stderr.splitlines() if 'console' in l.lower() and 'error' in l.lower()
            and not re.search(r'dbus|gpu|vulkan|ozone|fontconfig', l, re.I)]
    check('render: no js console errors', not errs, errs[:3])
def main():
    proc = run([sys.executable, '-m', 'py_compile', 'pasta_dashboard.py'])
    check('py_compile', proc.returncode == 0, proc.stderr[-200:])
    for jf in ['pasta_data.json', 'nutritional_info.json']:
        try:
            json.load(open(REPO / jf))
            check('json valid: ' + jf, True)
        except Exception as e:
            check('json valid: ' + jf, False, str(e))
    env = dict(os.environ, STREAMLIT_BROWSER_GATHER_USAGE_STATS='false')
    server = subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'pasta_dashboard.py',
                               '--server.headless', 'true', '--server.port', '4234', '--server.address', '127.0.0.1'],
                              cwd=REPO, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
    try:
        import urllib.request
        ok = False
        for _ in range(45):
            try:
                body = urllib.request.urlopen('http://127.0.0.1:4234/', timeout=2).read().decode('utf-8', 'replace')
                ok = 'Pasta' in body or 'streamlit' in body.lower()
                if ok: break
            except Exception:
                time.sleep(1)
        check('streamlit serves app', ok)
    finally:
        server.terminate()

    print('FAILURES=%d' % len(failures))
    with open(REPO / '.cursor/skills/verify-pasta-dashboard/evidence.json', 'w') as f:
        json.dump({'repo': 'PastaDashboard', 'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'failures': failures}, f, indent=2)
    return 1 if failures else 0
if __name__ == '__main__':
    sys.exit(main())
