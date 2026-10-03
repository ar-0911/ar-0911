"""Generates the animated SVG assets for the ar-0911 profile README."""
import math, os, re

ICONS = os.environ.get('SIMPLE_ICONS_DIR', 'node_modules/simple-icons/icons')
OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

BG = '#0d1117'
PANEL = '#111826'
STROKE = '#1f2a3d'
TEXT = '#e6edf3'
MUTED = '#8b98a9'
CYAN = '#22d3ee'
VIOLET = '#a78bfa'
GREEN = '#34d399'
AMBER = '#fbbf24'
SANS = "'Segoe UI', Ubuntu, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"


def icon_path(name):
    s = open(f'{ICONS}/{name}.svg').read()
    return re.search(r'<path d="([^"]+)"', s).group(1)


def defs_common():
    return f'''
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" fill="none" stroke="{STROKE}" stroke-width="1" opacity=".55"/>
  </pattern>
  <radialGradient id="glowC" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{CYAN}" stop-opacity=".35"/>
    <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowV" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity=".28"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="brand" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="{CYAN}"/>
    <stop offset="1" stop-color="{VIOLET}"/>
  </linearGradient>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3"/>
  </filter>'''


def frame(w, h, body, extra_defs='', style=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
<defs>{defs_common()}{extra_defs}
  <clipPath id="round"><rect width="{w}" height="{h}" rx="18"/></clipPath>
</defs>
<style>
  .sans {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
{style}
</style>
<g clip-path="url(#round)">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
{body}
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" stroke="{STROKE}"/>
</svg>
'''


# ---------------------------------------------------------------- header
def header():
    W, H = 1200, 360
    hx, hy = 905, 182
    labels = ['Teleport', 'WARP', 'VyOS', 'Grafana', 'Bedrock', 'Terraform', 'Wazuh', 'ECS']
    colors = [VIOLET, CYAN, GREEN, AMBER, VIOLET, CYAN, GREEN, AMBER]
    nodes = []
    for i, lab in enumerate(labels):
        a = -math.pi / 2 + i * 2 * math.pi / len(labels) + 0.2
        nodes.append((hx + 215 * math.cos(a), hy + 128 * math.sin(a), lab, colors[i]))

    links, packets, dots = [], [], []
    for i, (x, y, lab, c) in enumerate(nodes):
        d = f'M{x:.1f},{y:.1f} L{hx},{hy}'
        links.append(f'<path id="l{i}" d="{d}" stroke="{c}" stroke-opacity=".28" stroke-width="1.4" stroke-dasharray="4 6">'
                     f'<animate attributeName="stroke-dashoffset" values="0;-20" dur="1.6s" repeatCount="indefinite"/></path>')
        dur = 2.4 + (i % 3) * 0.5
        for k, (kp, kt) in enumerate((('0;1', '0;1'), ('1;0', '0;1'))):
            begin = f'{(i * 0.37 + k * dur / 2) % dur:.2f}s'
            packets.append(
                f'<circle r="3.2" fill="{c}"><animateMotion dur="{dur}s" begin="{begin}" repeatCount="indefinite" '
                f'keyPoints="{kp}" keyTimes="{kt}" calcMode="linear"><mpath href="#l{i}"/></animateMotion>'
                f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur}s" begin="{begin}" repeatCount="indefinite"/></circle>')
        tx = x + (14 if x >= hx else -14)
        anchor = 'start' if x >= hx else 'end'
        dots.append(f'''<g>
    <circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="{c}" opacity=".12">
      <animate attributeName="r" values="9;17;9" dur="3s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values=".25;0;.25" dur="3s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{BG}" stroke="{c}" stroke-width="2"/>
    <text x="{tx:.1f}" y="{y+4:.1f}" text-anchor="{anchor}" class="mono" font-size="12" fill="{MUTED}">{lab}</text>
  </g>''')

    roles = ['infrastructure engineer', 'zero-trust networking', 'cloud security &amp; compliance', 'AI developer platforms']
    cycle = 3.0 * len(roles)
    role_els = []
    cvals, ckts = [], []
    for i, r in enumerate(roles):
        n = len(re.sub('&amp;', '&', r))
        w = n * 10.85
        t0 = i / len(roles)
        t1 = (i + 1) / len(roles)
        span = t1 - t0
        kt = [0, t0, t0 + span * .3, t0 + span * .85, t0 + span * .97, 1]
        for k, v in zip(kt[1:5], (0, w, w, 0)):
            ckts.append(k); cvals.append(172 + v)
        kt = ';'.join(f'{min(max(k,0),1):.4f}' for k in kt)
        role_els.append(f'''<clipPath id="rc{i}"><rect x="170" y="196" height="30" width="0">
      <animate attributeName="width" values="0;0;{w:.0f};{w:.0f};0;0" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/>
    </rect></clipPath>
  <text x="170" y="218" class="mono" font-size="18" fill="{TEXT}" clip-path="url(#rc{i})">{r}</text>''')

    caret_kts = ';'.join(f'{k:.4f}' for k in [0] + ckts + [1])
    caret_vals = ';'.join(f'{v:.0f}' for v in [172] + cvals + [172])
    body = f'''
  <circle cx="{hx}" cy="{hy}" r="190" fill="url(#glowC)"/>
  <circle cx="160" cy="40" r="260" fill="url(#glowV)"/>
  {''.join(links)}
  {''.join(packets)}
  {''.join(dots)}
  <g>
    <circle cx="{hx}" cy="{hy}" r="40" fill="none" stroke="{CYAN}" stroke-opacity=".5">
      <animate attributeName="r" values="34;58" dur="2.4s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values=".6;0" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{hx}" cy="{hy}" r="34" fill="{PANEL}" stroke="url(#brand)" stroke-width="2.5"/>
    <text x="{hx}" y="{hy-2}" text-anchor="middle" class="sans" font-size="15" font-weight="700" fill="{TEXT}">adi</text>
    <text x="{hx}" y="{hy+14}" text-anchor="middle" class="mono" font-size="9.5" fill="{CYAN}">hub</text>
  </g>

  <g class="fade">
    <rect x="64" y="72" width="168" height="26" rx="13" fill="{CYAN}" fill-opacity=".1" stroke="{CYAN}" stroke-opacity=".4"/>
    <circle cx="80" cy="85" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
    <text x="92" y="89.5" class="mono" font-size="12" fill="{CYAN}">online · Bangalore</text>
    <text x="62" y="160" class="sans" font-size="54" font-weight="800" fill="url(#brand)" letter-spacing="-1">Aditya Ramguru</text>
    <text x="64" y="218" class="mono" font-size="18" fill="{GREEN}">$ whoami</text>
    {''.join(role_els)}
    <rect x="172" y="202" width="10" height="20" fill="{CYAN}" opacity=".9">
      <animate attributeName="opacity" values="1;0;1" dur="1s" calcMode="discrete" repeatCount="indefinite"/>
      <animate attributeName="x" values="{caret_vals}" keyTimes="{caret_kts}" dur="{cycle}s" repeatCount="indefinite"/>
    </rect>
    <text x="64" y="276" class="sans" font-size="16" fill="{MUTED}">Software Engineer @ Aurm · sole infrastructure engineer, reporting to the CTO</text>
    <text x="64" y="302" class="sans" font-size="16" fill="{MUTED}">AWS · GCP · Cloudflare Zero Trust · WireGuard · Teleport · Terraform</text>
  </g>
'''
    # The caret should follow the text; keep it simple by placing it after the prompt.
    style = '''  .fade { animation: rise .9s ease-out both; }
  @keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }'''
    return frame(W, H, body, style=style)


# ---------------------------------------------------------------- stats
def stats():
    W, H = 1200, 190
    cards = [
        ('30+', 'edge nodes on a', 'WireGuard / VyOS mesh', CYAN, .78),
        ('120', 'internal apps behind', 'Teleport + Cloudflare WARP', VIOLET, .9),
        ('96%', 'fewer critical/high', 'Trivy findings (83 → 3)', GREEN, .96),
        ('100%', 'of PRs agent-driven', 'via Claude Code skills', AMBER, 1.0),
    ]
    cw, gap, x0 = 264, 24, 36
    out = []
    for i, (num, l1, l2, c, frac) in enumerate(cards):
        x = x0 + i * (cw + gap)
        d = i * .18
        bar = (cw - 48) * frac
        out.append(f'''<g class="card" style="animation-delay:{d:.2f}s">
    <rect x="{x}" y="28" width="{cw}" height="134" rx="14" fill="{PANEL}" stroke="{STROKE}"/>
    <rect x="{x}" y="28" width="{cw}" height="3" rx="1.5" fill="{c}" opacity=".85"/>
    <text x="{x+24}" y="86" class="sans" font-size="40" font-weight="800" fill="{c}">{num}</text>
    <text x="{x+24}" y="112" class="sans" font-size="14" fill="{TEXT}">{l1}</text>
    <text x="{x+24}" y="131" class="sans" font-size="14" fill="{MUTED}">{l2}</text>
    <rect x="{x+24}" y="144" width="{cw-48}" height="5" rx="2.5" fill="{STROKE}"/>
    <rect x="{x+24}" y="144" width="0" height="5" rx="2.5" fill="{c}">
      <animate attributeName="width" from="0" to="{bar:.1f}" dur="1.4s" begin="{.4+d:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/>
    </rect>
    <circle cx="{x+cw-28}" cy="58" r="4" fill="{c}">
      <animate attributeName="opacity" values="1;.2;1" dur="2s" begin="{d:.2f}s" repeatCount="indefinite"/>
    </circle>
  </g>''')
    style = '''  .card { animation: pop .7s cubic-bezier(.2,.8,.2,1) both; transform-box: fill-box; transform-origin: center; }
  @keyframes pop { from { opacity: 0; transform: translateY(14px) scale(.97); } to { opacity: 1; transform: none; } }'''
    return frame(W, H, '\n'.join(out), style=style)


# ---------------------------------------------------------------- stack
def text_icon(label, color):
    return ('text', label, color)


STACK = [
    ('Cloud &amp; IaC', [
        ('AWS', ('text', 'aws', '#FF9900')),
        ('Google Cloud', ('icon', 'googlecloud', '#4285F4')),
        ('Terraform', ('icon', 'terraform', '#844FBA')),
        ('Docker', ('icon', 'docker', '#2496ED')),
        ('Linux', ('icon', 'linux', '#FCC624')),
        ('GitHub Actions', ('icon', 'githubactions', '#2088FF')),
    ]),
    ('Networking &amp; Security', [
        ('Cloudflare', ('icon', 'cloudflare', '#F38020')),
        ('WireGuard', ('icon', 'wireguard', '#E5484D')),
        ('Teleport', ('text', 'tp', '#A78BFA')),
        ('VyOS', ('text', 'vy', '#34D399')),
        ('Trivy', ('icon', 'trivy', '#1904DA')),
        ('Wazuh', ('text', 'wz', '#3595F9')),
    ]),
    ('Observability, Code &amp; AI', [
        ('Grafana', ('icon', 'grafana', '#F46800')),
        ('Prometheus', ('icon', 'prometheus', '#E6522C')),
        ('Python', ('icon', 'python', '#3776AB')),
        ('Node.js', ('icon', 'nodedotjs', '#5FA04E')),
        ('Bash', ('icon', 'gnubash', '#4EAA25')),
        ('Claude Code', ('icon', 'claude', '#D97757')),
    ]),
]


def lighten(hexc):
    # Brand colours that are too dark on the dark panel get lifted.
    r, g, b = (int(hexc[i:i+2], 16) for i in (1, 3, 5))
    lum = .2126 * r + .7152 * g + .0722 * b
    if lum < 90:
        r, g, b = (int(v + (255 - v) * .45) for v in (r, g, b))
    return f'#{r:02x}{g:02x}{b:02x}'


def stack():
    W = 1200
    tile, gapx = 96, 18
    row_h = 158
    H = 40 + row_h * len(STACK) + 10
    out = []
    n = 0
    for r, (title, items) in enumerate(STACK):
        y0 = 40 + r * row_h
        out.append(f'<text x="48" y="{y0+14}" class="mono" font-size="13" fill="{CYAN}" letter-spacing="1.5">{title.upper().replace("&AMP;", "&amp;")}</text>')
        out.append(f'<rect x="48" y="{y0+24}" width="1104" height="1" fill="{STROKE}"/>')
        total = len(items) * tile + (len(items) - 1) * gapx
        x0 = 48
        for i, (name, (kind, val, col)) in enumerate(items):
            x = x0 + i * (tile + gapx + 75)
            y = y0 + 42
            col = lighten(col)
            d = n * .07
            fl = (n % 4) * .45
            if kind == 'icon':
                glyph = f'<g transform="translate({x+tile/2-18},{y+20}) scale(1.5)"><path d="{icon_path(val)}" fill="{col}"/></g>'
            else:
                glyph = f'<text x="{x+tile/2}" y="{y+50}" text-anchor="middle" class="sans" font-size="24" font-weight="800" fill="{col}">{val}</text>'
            out.append(f'''<g class="tile" style="animation-delay:{d:.2f}s"><g class="float" style="animation-delay:{fl:.2f}s">
    <rect x="{x}" y="{y}" width="{tile+75}" height="96" rx="14" fill="{PANEL}" stroke="{STROKE}"/>
    <rect x="{x}" y="{y}" width="{tile+75}" height="96" rx="14" fill="none" stroke="{col}" stroke-opacity="0">
      <animate attributeName="stroke-opacity" values="0;.7;0" dur="6s" begin="{1+n*.33:.2f}s" repeatCount="indefinite"/>
    </rect>
    {glyph.replace(f'translate({x+tile/2-18}', f'translate({x+(tile+75)/2-18}').replace(f'x="{x+tile/2}"', f'x="{x+(tile+75)/2}"')}
    <text x="{x+(tile+75)/2}" y="{y+84}" text-anchor="middle" class="sans" font-size="12.5" fill="{MUTED}">{name}</text>
  </g></g>''')
            n += 1
    style = '''  .tile { animation: pop .6s cubic-bezier(.2,.8,.2,1) both; transform-box: fill-box; transform-origin: center; }
  .float { animation: float 4s ease-in-out infinite; }
  @keyframes pop { from { opacity: 0; transform: scale(.85); } to { opacity: 1; transform: scale(1); } }
  @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }'''
    return frame(W, H, '\n'.join(out), style=style)


# ---------------------------------------------------------------- work cards
def work():
    W, H = 1200, 430
    cw, gap, x0, y0, ch = 360, 24, 36, 36, 358
    cards = []

    # 1. Zero-trust access: request passes two shields to an app
    x = x0
    zt = f'''
    <text x="{x+24}" y="{y0+40}" class="mono" font-size="12" fill="{CYAN}" letter-spacing="1.5">01 · ZERO-TRUST ACCESS</text>
    <text x="{x+24}" y="{y0+68}" class="sans" font-size="20" font-weight="700" fill="{TEXT}">Edge mesh + identity access</text>
    <g transform="translate({x+24},{y0+96})">
      <rect width="312" height="128" rx="10" fill="{BG}" stroke="{STROKE}"/>
      <path id="ztp" d="M30,64 H282" stroke="{STROKE}" stroke-width="2"/>
      <circle cx="30" cy="64" r="12" fill="{PANEL}" stroke="{MUTED}"/><text x="30" y="96" text-anchor="middle" class="mono" font-size="10" fill="{MUTED}">user</text>
      <rect x="96" y="44" width="40" height="40" rx="8" fill="{PANEL}" stroke="{AMBER}"/><text x="116" y="69" text-anchor="middle" class="mono" font-size="10" fill="{AMBER}">WARP</text>
      <rect x="176" y="44" width="40" height="40" rx="8" fill="{PANEL}" stroke="{VIOLET}"/><text x="196" y="69" text-anchor="middle" class="mono" font-size="10" fill="{VIOLET}">TP</text>
      <rect x="258" y="48" width="36" height="32" rx="6" fill="{PANEL}" stroke="{GREEN}"/><text x="276" y="68" text-anchor="middle" class="mono" font-size="10" fill="{GREEN}">app</text>
      <text x="116" y="104" text-anchor="middle" class="mono" font-size="9.5" fill="{MUTED}">device</text>
      <text x="196" y="104" text-anchor="middle" class="mono" font-size="9.5" fill="{MUTED}">identity</text>
      <circle r="5" fill="{CYAN}"><animateMotion dur="3s" repeatCount="indefinite" keyPoints="0;.3;.33;.6;.63;1" keyTimes="0;.25;.4;.6;.75;1" calcMode="linear"><mpath href="#ztp"/></animateMotion></circle>
      <circle cx="116" cy="30" r="5" fill="{GREEN}" opacity="0"><animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;.3;.38;.5;1" dur="3s" repeatCount="indefinite"/></circle>
      <circle cx="196" cy="30" r="5" fill="{GREEN}" opacity="0"><animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;.6;.68;.8;1" dur="3s" repeatCount="indefinite"/></circle>
    </g>
    <text x="{x+24}" y="{y0+256}" class="sans" font-size="14" fill="{MUTED}">WireGuard/VyOS hub-and-spoke for 30+ nodes,</text>
    <text x="{x+24}" y="{y0+276}" class="sans" font-size="14" fill="{MUTED}">HA Teleport for 120 apps, Cloudflare WARP</text>
    <text x="{x+24}" y="{y0+296}" class="sans" font-size="14" fill="{MUTED}">in front for defense in depth.</text>
    <text x="{x+24}" y="{y0+330}" class="mono" font-size="11.5" fill="{CYAN}">wireguard · vyos · teleport · terraform</text>'''

    # 2. AI platform: requests from devs through gateway to Bedrock with budget bar
    x = x0 + cw + gap
    devs = ''.join(
        f'<circle cx="30" cy="{24+i*40}" r="9" fill="{PANEL}" stroke="{MUTED}"/>'
        f'<path id="ai{i}" d="M40,{24+i*40} C 90,{24+i*40} 90,64 128,64 L 270,64" stroke="{STROKE}" stroke-width="1.6"/>'
        f'<circle r="4" fill="{VIOLET}"><animateMotion dur="2.6s" begin="{i*.8:.1f}s" repeatCount="indefinite"><mpath href="#ai{i}"/></animateMotion></circle>'
        for i in range(3))
    ai = f'''
    <text x="{x+24}" y="{y0+40}" class="mono" font-size="12" fill="{VIOLET}" letter-spacing="1.5">02 · AI DEV PLATFORM</text>
    <text x="{x+24}" y="{y0+68}" class="sans" font-size="20" font-weight="700" fill="{TEXT}">Claude Code for 50 engineers</text>
    <g transform="translate({x+24},{y0+96})">
      <rect width="312" height="128" rx="10" fill="{BG}" stroke="{STROKE}"/>
      {devs}
      <rect x="128" y="44" width="70" height="40" rx="8" fill="{PANEL}" stroke="{VIOLET}"/>
      <text x="163" y="68" text-anchor="middle" class="mono" font-size="10" fill="{VIOLET}">LiteLLM</text>
      <rect x="236" y="44" width="62" height="40" rx="8" fill="{PANEL}" stroke="{AMBER}"/>
      <text x="267" y="68" text-anchor="middle" class="mono" font-size="10" fill="{AMBER}">Bedrock</text>
      <text x="128" y="106" class="mono" font-size="9.5" fill="{MUTED}">budget</text>
      <rect x="170" y="99" width="128" height="7" rx="3.5" fill="{STROKE}"/>
      <rect x="170" y="99" width="0" height="7" rx="3.5" fill="{GREEN}">
        <animate attributeName="width" values="0;92;92;0" keyTimes="0;.7;.92;1" dur="5s" repeatCount="indefinite"/>
        <animate attributeName="fill" values="{GREEN};{AMBER};{AMBER};{GREEN}" keyTimes="0;.7;.92;1" dur="5s" repeatCount="indefinite"/>
      </rect>
    </g>
    <text x="{x+24}" y="{y0+256}" class="sans" font-size="14" fill="{MUTED}">LiteLLM gateway on ECS Fargate routing to</text>
    <text x="{x+24}" y="{y0+276}" class="sans" font-size="14" fill="{MUTED}">AWS Bedrock with org and per-user budgets;</text>
    <text x="{x+24}" y="{y0+296}" class="sans" font-size="14" fill="{MUTED}">skills + subagents drive 100% of PRs.</text>
    <text x="{x+24}" y="{y0+330}" class="mono" font-size="11.5" fill="{VIOLET}">litellm · ecs · bedrock · claude code</text>'''

    # 3. Security & observability: Trivy bars drop, live sparkline
    x = x0 + 2 * (cw + gap)
    pts = [(i * 26, 60 - 30 * math.sin(i * .9) * (0.5 + 0.5 * math.cos(i * .37))) for i in range(13)]
    spark = 'M' + ' L'.join(f'{px:.1f},{py:.1f}' for px, py in pts)
    sec = f'''
    <text x="{x+24}" y="{y0+40}" class="mono" font-size="12" fill="{GREEN}" letter-spacing="1.5">03 · SECURITY &amp; OBSERVABILITY</text>
    <text x="{x+24}" y="{y0+68}" class="sans" font-size="20" font-weight="700" fill="{TEXT}">Audit-ready, fully observed</text>
    <g transform="translate({x+24},{y0+96})">
      <rect width="312" height="128" rx="10" fill="{BG}" stroke="{STROKE}"/>
      <text x="16" y="24" class="mono" font-size="9.5" fill="{MUTED}">trivy crit+high</text>
      <rect x="16" y="34" width="22" height="80" rx="3" fill="#f87171" opacity=".85">
        <animate attributeName="height" values="80;80;3;3;80" keyTimes="0;.2;.5;.9;1" dur="6s" repeatCount="indefinite"/>
        <animate attributeName="y" values="34;34;111;111;34" keyTimes="0;.2;.5;.9;1" dur="6s" repeatCount="indefinite"/>
        <animate attributeName="fill" values="#f87171;#f87171;{GREEN};{GREEN};#f87171" keyTimes="0;.2;.5;.9;1" dur="6s" repeatCount="indefinite"/>
      </rect>
      <text x="48" y="64" class="sans" font-size="22" font-weight="800" fill="{TEXT}">83<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;.45;.5;.9;1" dur="6s" repeatCount="indefinite"/></text>
      <text x="48" y="64" class="sans" font-size="22" font-weight="800" fill="{GREEN}" opacity="0">3<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.45;.5;.9;1" dur="6s" repeatCount="indefinite"/></text>
      <text x="48" y="84" class="mono" font-size="9.5" fill="{MUTED}">findings</text>
      <text x="120" y="24" class="mono" font-size="9.5" fill="{MUTED}">grafana · edge fleet</text>
      <g transform="translate(120,36)">
        <clipPath id="sc"><rect width="176" height="80"/></clipPath>
        <g clip-path="url(#sc)">
          <g>
            <path d="{spark}" stroke="{CYAN}" stroke-width="2" fill="none"/>
            <path d="{spark}" stroke="{CYAN}" stroke-width="2" fill="none" transform="translate(312,0)"/>
            <animateTransform attributeName="transform" type="translate" from="0 0" to="-312 0" dur="8s" repeatCount="indefinite"/>
          </g>
        </g>
        <path d="M0,79 H176" stroke="{STROKE}"/>
      </g>
    </g>
    <text x="{x+24}" y="{y0+256}" class="sans" font-size="14" fill="{MUTED}">Cleared a third-party cloud security audit,</text>
    <text x="{x+24}" y="{y0+276}" class="sans" font-size="14" fill="{MUTED}">automated Security Hub remediation, Wazuh</text>
    <text x="{x+24}" y="{y0+296}" class="sans" font-size="14" fill="{MUTED}">SIEM and a self-hosted LGTM stack.</text>
    <text x="{x+24}" y="{y0+330}" class="mono" font-size="11.5" fill="{GREEN}">trivy · security hub · wazuh · grafana</text>'''

    for i, inner in enumerate((zt, ai, sec)):
        x = x0 + i * (cw + gap)
        cards.append(f'''<g class="card" style="animation-delay:{i*.15:.2f}s">
    <rect x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="16" fill="{PANEL}" stroke="{STROKE}"/>
    {inner}
  </g>''')
    style = '''  .card { animation: pop .7s cubic-bezier(.2,.8,.2,1) both; }
  @keyframes pop { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }'''
    return frame(W, H, '\n'.join(cards), style=style)


# ---------------------------------------------------------------- section titles
def title(label, sub, color, fname):
    W, H = 1200, 64
    body = f'''
  <rect x="0" y="0" width="1200" height="64" fill="{BG}"/>
  <text x="36" y="40" class="mono" font-size="15" fill="{color}">~/</text>
  <text x="60" y="40" class="sans" font-size="22" font-weight="700" fill="{TEXT}">{label}</text>
  <text x="{60 + len(label)*12.6 + 18:.0f}" y="40" class="mono" font-size="13" fill="{MUTED}">{sub}</text>
  <rect x="36" y="54" width="0" height="2" rx="1" fill="url(#brand)">
    <animate attributeName="width" from="0" to="1128" dur="1.6s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/>
  </rect>
  <circle cx="36" cy="55" r="3.5" fill="{color}">
    <animate attributeName="cx" values="36;1164" dur="5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="5s" repeatCount="indefinite"/>
  </circle>'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
<defs>{defs_common()}</defs>
<style>.sans {{ font-family: {SANS}; }} .mono {{ font-family: {MONO}; }}</style>
<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>
{body}
</svg>
'''
    open(f'{OUT}/{fname}', 'w').write(svg)


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1200, 150
    waves = []
    for i, (c, op, dur, amp) in enumerate(((CYAN, .35, 9, 14), (VIOLET, .3, 12, 18), (GREEN, .18, 15, 10))):
        def wave(phase):
            pts = []
            for k in range(0, 2401, 40):
                pts.append(f'{k},{90 + amp*math.sin(k/1200*4*math.pi + phase):.1f}')
            return 'M' + ' L'.join(pts) + f' V{H} H0 Z'
        waves.append(f'''<path d="{wave(i)}" fill="{c}" fill-opacity="{op*.35:.2f}" stroke="{c}" stroke-opacity="{op}">
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-1200 0" dur="{dur}s" repeatCount="indefinite"/>
    </path>''')
    body = f'''
  {''.join(waves)}
  <text x="600" y="52" text-anchor="middle" class="sans" font-size="22" font-weight="700" fill="{TEXT}">Let's build something reliable.</text>
  <text x="600" y="78" text-anchor="middle" class="mono" font-size="13" fill="{MUTED}">$ ping adi · aditya.ramguru@gmail.com</text>
'''
    return frame(W, H, body)


open(f'{OUT}/header.svg', 'w').write(header())
open(f'{OUT}/stats.svg', 'w').write(stats())
open(f'{OUT}/stack.svg', 'w').write(stack())
open(f'{OUT}/work.svg', 'w').write(work())
open(f'{OUT}/footer.svg', 'w').write(footer())
title('impact', '# numbers from production', CYAN, 'title-impact.svg')
title('what-i-build', '# the systems I own', VIOLET, 'title-build.svg')
title('stack', '# tools I use daily', GREEN, 'title-stack.svg')
title('activity', '# contributions', AMBER, 'title-activity.svg')
print('ok')
