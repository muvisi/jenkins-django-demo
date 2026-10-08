from django.http import HttpResponse, JsonResponse


def home(request):
    return HttpResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>CI/CD Pipeline | Samuel Mwangangi</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            min-height: 100vh;
            font-family: Inter, "Segoe UI", Arial, sans-serif;
            color: #e8eefb;
            background:
                radial-gradient(ellipse at 15% 5%, #193d69 0%, transparent 40%),
                radial-gradient(ellipse at 90% 85%, #1c2859 0%, transparent 40%),
                #080f1f;
        }
        .shell { max-width: 1100px; margin: auto; padding: 35px 24px 65px; }
        nav { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
        .brand { font-size: 17px; font-weight: 800; letter-spacing: 1px; }
        .brand span { color: #59c9ff; }
        .pill {
            padding: 10px 16px; border-radius: 30px;
            background: #123a32; color: #7af5bd;
            border: 1px solid #276a56; font-size: 13px;
        }
        .hero { text-align: center; padding: 88px 0 50px; }
        .eyebrow { color: #66cfff; font-size: 13px; letter-spacing: 3px; font-weight: 800; }
        h1 {
            font-size: clamp(42px, 7vw, 76px);
            line-height: 1.08; letter-spacing: -2px;
            margin: 22px 0;
        }
        h1 span {
            background: linear-gradient(90deg, #59c9ff, #aa88ff);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        .subtitle { color: #a8b7d2; font-size: 18px; line-height: 1.8; }
        .chips { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-top: 30px; }
        .chip {
            background: #16243d; border: 1px solid #30435e;
            padding: 10px 17px; border-radius: 9px;
            color: #dce8ff; font-size: 14px;
        }
        .panel {
            background: rgba(19, 32, 55, .9);
            border: 1px solid #30415d;
            border-radius: 20px; padding: 28px; margin-top: 25px;
        }
        .panel h2 { margin: 0 0 24px; font-size: 20px; }
        .flow { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }
        .step {
            background: #0c1930; border: 1px solid #31435e;
            padding: 22px 12px; text-align: center; border-radius: 12px;
        }
        .step .symbol { font-size: 30px; margin-bottom: 12px; }
        .step strong { display: block; font-size: 15px; }
        .step small { display: block; color: #90a4c3; margin-top: 8px; line-height: 1.5; }
        .metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 22px; }
        .metric { padding: 22px; background: #0c1930; border-radius: 12px; border: 1px solid #30415d; }
        .metric .label { color: #91a6c5; font-size: 13px; }
        .metric .value { font-size: 22px; font-weight: 800; margin-top: 10px; }
        .green { color: #75f0b4; }
        .blue { color: #67ccff; }
        .footer { text-align: center; margin-top: 55px; color: #91a4c1; line-height: 1.8; }
        .footer strong { color: white; }
        a { color: #7ed8ff; text-decoration: none; }
        @media (max-width: 750px) {
            .hero { padding-top: 65px; }
            .flow { grid-template-columns: repeat(2, 1fr); }
            .metrics { grid-template-columns: 1fr; }
        }
        @media (max-width: 420px) {
            .flow { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
<div class="shell">
    <nav>
        <div class="brand">⚡ DEVOPS<span> / PIPELINE</span></div>
        <div class="pill" id="status">● Checking application...</div>
    </nav>

    <section class="hero">
        <div class="eyebrow">AUTOMATED SOFTWARE DELIVERY</div>
        <h1>From Code to <span>Production.</span></h1>
        <p class="subtitle">
            CI/CD Pipeline Demonstration<br>
            Automated Django deployment using Jenkins, Ansible and Nginx.
        </p>
        <div class="chips">
            <div class="chip">GitHub</div>
            <div class="chip">Jenkins</div>
            <div class="chip">Ansible</div>
            <div class="chip">Python / Django</div>
            <div class="chip">Gunicorn</div>
            <div class="chip">Nginx</div>
        </div>
    </section>

    <section class="panel">
        <h2>🚀 Deployment Pipeline</h2>
        <div class="flow">
            <div class="step">
                <div class="symbol">📦</div>
                <strong>GitHub</strong>
                <small>Source control</small>
            </div>
            <div class="step">
                <div class="symbol">⚙️</div>
                <strong>Jenkins</strong>
                <small>Build &amp; test</small>
            </div>
            <div class="step">
                <div class="symbol">🔧</div>
                <strong>Ansible</strong>
                <small>Provision &amp; deploy</small>
            </div>
            <div class="step">
                <div class="symbol">🖥️</div>
                <strong>Ubuntu VPS</strong>
                <small>Gunicorn service</small>
            </div>
            <div class="step">
                <div class="symbol">🌐</div>
                <strong>Nginx</strong>
                <small>Public HTTP access</small>
            </div>
        </div>
    </section>

    <section class="panel">
        <h2>📊 Deployment Overview</h2>
        <div class="metrics">
            <div class="metric">
                <div class="label">Application Health</div>
                <div class="value green" id="health">Checking...</div>
            </div>
            <div class="metric">
                <div class="label">Deployment Method</div>
                <div class="value blue">Jenkins + Ansible</div>
            </div>
            <div class="metric">
                <div class="label">Environment</div>
                <div class="value">Ubuntu VPS</div>
            </div>
        </div>
    </section>

    <div class="footer">
        <p>Designed &amp; Presented by <strong>Samuel Mwangangi</strong></p>
        <p>CI/CD Pipeline Demonstration • DevOps Automation</p>
        <p><a href="/health/" target="_blank" rel="noopener">View Application Health API ↗</a></p>
    </div>
</div>
<script>
    fetch('/health/', {cache: 'no-store'})
        .then(response => {
            if (!response.ok) throw new Error('Health check failed');
            return response.json();
        })
        .then(data => {
            if (data.status !== 'healthy') throw new Error('Unhealthy');
            document.getElementById('status').textContent = '● Application Online';
            document.getElementById('health').textContent = 'Healthy ✓';
        })
        .catch(() => {
            document.getElementById('status').textContent = '● Health Check Failed';
            document.getElementById('health').textContent = 'Unavailable';
        });
</script>
</body>
</html>
    """)


def health(request):
    return JsonResponse({
        "status": "healthy",
        "application": "jenkins-django-demo"
    })
