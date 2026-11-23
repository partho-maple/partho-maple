#!/usr/bin/env python3
"""Generate the animated SVGs used by the profile README.

Every asset is written twice, assets/<name>-dark.svg and assets/<name>-light.svg,
and the README picks one with <picture> + prefers-color-scheme.

Edit the DATA section below (numbers, jobs, repos), then run:
    python3 scripts/build_assets.py
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# ----------------------------------------------------------------------------- DATA
ROLES = [
    "Mobile Engineering @ Amazon Fire TV, Berlin",
    "iOS, Android & React Native at scale",
    "designs systems from app to AWS",
    "builds SDKs used by tens of millions",
]

IMPACT = [
    ("14+", "years", "building software"),
    ("20M+", "daily users", "Amazon Fire TV app"),
    ("80M", "users", "on Zalando sign-in I built"),
    ("99.99%", "availability", "AWS services I run"),
    ("-70%", "build time", "after modularising"),
]

# (year, company, role, what it is, why it mattered)
JOURNEY = [
    ("2013", "BizMotion", "Mobile Engineer", "VoIP calling apps", "iOS & Android, own SDK"),
    ("2014", "IPVision", "Senior Engineer", "Live voice, video & chat", "ringID app, 5M users"),
    ("2017", "Aurea", "Software Architect", "Enterprise CRM & team apps", "rewrite, 2x faster start"),
    ("2021", "Zalando", "Mobile Foundation", "Base of Zalando's apps", "sign-in for 80M users"),
    ("2022", "Amazon", "Mobile Engineering", "Fire TV org, phone remote", "20M+ daily users"),
]

REPOS = [
    ("coding-interview-gym", "LeetCode & AlgoExpert solutions in Python and Swift, sorted by pattern.",
     "Python", "#3572A5", 839, 461),
    ("PBTreeView", "The UITreeView Apple never shipped: a tree view built on UITableView, pure Swift.",
     "Swift", "#F05138", 140, 11),
    ("Java-Remote-Control", "A TeamViewer-style remote desktop app built with Java RMI and Swing.",
     "Java", "#B07219", 51, 21),
    ("object-oriented-design-interview-gym", "Object-oriented design patterns and principles, in Swift.",
     "Swift", "#F05138", 9, 6),
]

# ----------------------------------------------------------------------------- THEMES
THEMES = {
    "dark": dict(bg="#0d1117", card="#161b22", line="#30363d", text="#e6edf3", muted="#8b949e",
                 accent="#f05138", accent2="#ffa657", cool="#58a6ff", glow="0.55", dot="#21262d"),
    "light": dict(bg="#ffffff", card="#f6f8fa", line="#d0d7de", text="#1f2328", muted="#59636e",
                  accent="#e0442b", accent2="#d4760a", cool="#0969da", glow="0.25", dot="#eaeef2"),
}

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
REDUCED = ("@media (prefers-reduced-motion: reduce){*{animation:none!important}"
           ".in,.card,.node,.role0{opacity:1!important}.track{stroke-dashoffset:0!important}.bar{transform:none!important}}")


def svg(w, h, body, css, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
            f'<style>{css}{REDUCED}</style>{body}</svg>\n')


# ----------------------------------------------------------------------------- HERO
def hero(t):
    W, H = 1000, 300
    slot, n = 4, len(ROLES)
    cycle = slot * n
    fs, cw = 22, 22 * 0.602  # mono glyph width ~0.6em
    tx, ty = 60, 196

    css = f"""
    .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
    .glow{{animation:drift 14s ease-in-out infinite alternate;transform-origin:780px 150px}}
    @keyframes drift{{from{{transform:translate(-40px,10px) scale(1)}}to{{transform:translate(30px,-10px) scale(1.15)}}}}
    .role{{opacity:0;animation:show {cycle}s linear infinite}}
    @keyframes show{{0%,{100/n - 0.01:.2f}%{{opacity:1}}{100/n:.2f}%,100%{{opacity:0}}}}
    .blink{{animation:blink 1s steps(1) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    .in{{opacity:0;animation:up .9s cubic-bezier(.2,.8,.2,1) forwards}}
    @keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
    .wave{{fill:none;stroke:{t['accent']};stroke-width:2.5;stroke-linecap:round;opacity:0;
           transform-box:fill-box;transform-origin:left center;animation:wave 2.4s ease-out infinite}}
    @keyframes wave{{0%{{opacity:0;transform:scale(.6)}}25%{{opacity:1}}100%{{opacity:0;transform:scale(1.25)}}}}
    .beam{{fill:none;stroke:{t['accent2']};stroke-width:2;stroke-dasharray:4 10;animation:flow 1.2s linear infinite}}
    @keyframes flow{{to{{stroke-dashoffset:-28}}}}
    .screen{{animation:tv 4.8s ease-in-out infinite}}
    @keyframes tv{{0%,40%{{fill:{t['card']}}}55%,90%{{fill:{t['accent']};fill-opacity:.18}}100%{{fill:{t['card']}}}}}
    .play{{opacity:0;animation:play 4.8s ease-in-out infinite}}
    @keyframes play{{0%,45%{{opacity:0}}55%,90%{{opacity:1}}100%{{opacity:0}}}}
    """
    roles, clips = [], []
    for i, r in enumerate(ROLES):
        delay = -((n - i) % n) * slot
        # typing: reveal one character per step during the first 35% of the slot (SMIL, discrete)
        k = len(r)
        typing = slot * 0.35 / cycle
        widths = [round(j * cw, 1) for j in range(k + 1)]
        times = [round(j * typing / k, 4) for j in range(k + 1)]
        vals = ";".join(map(str, widths + [widths[-1]]))
        kt = ";".join(map(str, times + [1]))
        xs = ";".join(str(round(tx + w, 1)) for w in widths + [widths[-1]])
        anim = f'dur="{cycle}s" begin="{delay}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}"'
        clips.append(f'<clipPath id="t{i}"><rect x="{tx}" y="{ty - 26}" width="0" height="36">'
                     f'<animate attributeName="width" values="{vals}" {anim}/></rect></clipPath>')
        roles.append(
            f'<g class="role role{i}" style="animation-delay:{delay}s">'
            f'<text class="mono" x="{tx}" y="{ty}" font-size="{fs}" fill="{t["text"]}" clip-path="url(#t{i})">{escape(r)}</text>'
            f'<rect class="blink" x="{tx}" y="{ty - 19}" width="11" height="24" fill="{t["accent"]}">'
            f'<animate attributeName="x" values="{xs}" {anim}/></rect></g>')
    roles.insert(0, f"<defs>{''.join(clips)}</defs>")

    dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="{t["dot"]}"/>'
                   for x in range(20, W, 28) for y in range(18, H, 28))

    phone = (f'<g transform="translate(640 92)">'
             f'<rect width="62" height="118" rx="12" fill="{t["card"]}" stroke="{t["text"]}" stroke-width="2.5"/>'
             f'<rect x="22" y="7" width="18" height="5" rx="2.5" fill="{t["text"]}"/>'
             f'<rect x="8" y="22" width="46" height="8" rx="3" fill="{t["accent"]}" opacity=".9"/>'
             f'<rect x="8" y="36" width="32" height="6" rx="3" fill="{t["muted"]}" opacity=".6"/>'
             f'<rect x="8" y="48" width="40" height="6" rx="3" fill="{t["muted"]}" opacity=".6"/>'
             f'<rect x="8" y="66" width="46" height="38" rx="6" fill="{t["cool"]}" opacity=".25"/></g>')
    waves = "".join(f'<path class="wave" style="animation-delay:{i * 0.8}s" d="M712 {120 - i*0} q 16 31 0 62"/>'
                    for i in range(3))
    tv = (f'<g transform="translate(790 80)">'
          f'<rect class="screen" width="160" height="100" rx="8" fill="{t["card"]}" stroke="{t["text"]}" stroke-width="2.5"/>'
          f'<path class="play" d="M70 34 L96 50 L70 66 Z" fill="{t["accent"]}"/>'
          f'<path d="M60 116 h40 M80 100 v16" stroke="{t["text"]}" stroke-width="2.5" stroke-linecap="round"/></g>')
    beam = (f'<path class="beam" d="M736 151 C 760 151, 765 130, 788 130"/>'
            f'<path class="beam" style="animation-duration:1.6s" d="M671 88 C 671 60, 700 46, 724 46"/>'
            f'<path class="beam" style="animation-duration:1.6s" d="M810 46 C 840 46, 860 60, 860 78"/>'
            f'<g transform="translate(728 22)"><path d="M14 40 a14 14 0 0 1 2-28 a20 20 0 0 1 38-4 a16 16 0 0 1 10 32 Z" '
            f'fill="{t["card"]}" stroke="{t["text"]}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<text class="mono" x="35" y="33" font-size="11" font-weight="700" text-anchor="middle" fill="{t["accent2"]}">AWS</text></g>')
    cap = (f'<text class="mono" x="795" y="226" font-size="12" fill="{t["muted"]}">app · TV · AWS, end to end</text>'
           f'<text class="mono" x="795" y="244" font-size="12" fill="{t["accent2"]}">80% faster connections</text>')

    body = f"""
    <rect width="{W}" height="{H}" rx="16" fill="{t['bg']}"/>
    <defs><radialGradient id="g" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="{t['glow']}"/>
      <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/></radialGradient>
      <clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>
    <g clip-path="url(#c)">{dots}<ellipse class="glow" cx="780" cy="150" rx="260" ry="170" fill="url(#g)"/></g>
    <rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{t['line']}"/>
    <g class="in"><text class="mono" x="{tx}" y="78" font-size="14" fill="{t['accent']}" letter-spacing="1">
      ~/berlin $ whoami</text></g>
    <g><text class="sans" x="{tx - 3}" y="140" font-size="60"
      font-weight="800" fill="{t['text']}" letter-spacing="-1.5">Partho Biswas</text></g>
    {''.join(roles)}
    <g class="in" style="animation-delay:.35s"><text class="sans" x="{tx}" y="246" font-size="15" fill="{t['muted']}">
      iOS · Android · React Native · AWS · infrastructure · system design</text></g>
    {phone}{waves}{beam}{tv}{cap}
    """
    return svg(W, H, body, css, "Partho Biswas, Mobile Engineering at Amazon Fire TV, Berlin")


# ----------------------------------------------------------------------------- IMPACT
def impact(t):
    W, H, n, gap = 1000, 150, len(IMPACT), 14
    cw = (W - gap * (n - 1)) / n
    css = f"""
    .sans{{font-family:{SANS}}}
    .card{{opacity:0;animation:up .8s cubic-bezier(.2,.8,.2,1) forwards}}
    @keyframes up{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:none}}}}
    .bar{{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:fill 1.4s cubic-bezier(.2,.8,.2,1) forwards}}
    @keyframes fill{{to{{transform:scaleX(1)}}}}
    .shine{{animation:shine 7s ease-in-out infinite}}
    @keyframes shine{{0%{{transform:translateX(-300px)}}35%,100%{{transform:translateX({W + 300}px)}}}}
    """
    cards = []
    for i, (num, unit, label) in enumerate(IMPACT):
        x = i * (cw + gap)
        d = i * 0.12
        cards.append(f"""
        <g class="card" style="animation-delay:{d}s"><g transform="translate({x:.1f} 0)">
          <rect x=".5" y=".5" width="{cw - 1:.1f}" height="{H - 1}" rx="12" fill="{t['card']}" stroke="{t['line']}"/>
          <text class="sans" x="20" y="62" font-size="40" font-weight="800" fill="{t['text']}" letter-spacing="-1">{escape(num)}</text>
          <text class="sans" x="20" y="88" font-size="14" font-weight="600" fill="{t['accent']}">{escape(unit)}</text>
          <text class="sans" x="20" y="110" font-size="13" fill="{t['muted']}">{escape(label)}</text>
          <rect class="bar" style="animation-delay:{d + .3}s" x="20" y="128" width="{cw - 40:.1f}" height="3" rx="1.5" fill="{t['accent2']}"/>
        </g></g>""")
    body = f"""
    <defs><linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
      <clipPath id="c">{''.join(f'<rect x="{i*(cw+gap):.1f}" width="{cw:.1f}" height="{H}" rx="12"/>' for i in range(n))}</clipPath></defs>
    {''.join(cards)}
    <g clip-path="url(#c)"><rect class="shine" x="0" y="0" width="220" height="{H}" fill="url(#s)" transform="skewX(-20)"/></g>
    """
    return svg(W, H, body, css, "Impact: 14+ years, 20M+ daily users, 80M users, 99.99% availability, 70% faster builds")


# ----------------------------------------------------------------------------- JOURNEY
def journey(t):
    W, H, n = 1000, 190, len(JOURNEY)
    step = W / n
    ly = 64
    css = f"""
    .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
    .track{{stroke-dasharray:{W};stroke-dashoffset:{W};animation:draw 2.2s cubic-bezier(.6,0,.2,1) forwards}}
    @keyframes draw{{to{{stroke-dashoffset:0}}}}
    .node{{opacity:0;animation:pop .6s cubic-bezier(.2,1.4,.4,1) forwards}}
    @keyframes pop{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
    .runner{{animation:run 6s cubic-bezier(.5,0,.5,1) 2.2s infinite;opacity:0}}
    @keyframes run{{0%{{transform:translateX(0);opacity:0}}8%{{opacity:1}}85%{{opacity:1}}100%{{transform:translateX({step*(n-1):.0f}px);opacity:0}}}}
    .now{{transform-box:fill-box;transform-origin:center;animation:ping 2s ease-out infinite}}
    @keyframes ping{{from{{transform:scale(1);opacity:.6}}to{{transform:scale(2.6);opacity:0}}}}
    """
    nodes = []
    for i, (year, org, role, what, why) in enumerate(JOURNEY):
        cx = step * i + step / 2
        last = i == n - 1
        col = t["accent"] if last else t["text"]
        ping = f'<circle class="now" cx="{cx:.1f}" cy="{ly}" r="9" fill="{t["accent"]}"/>' if last else ""
        nodes.append(f"""
        <g class="node" style="animation-delay:{0.35 + i * 0.35:.2f}s">
          <text class="mono" x="{cx:.1f}" y="{ly - 26}" font-size="14" text-anchor="middle" fill="{t['muted']}">{year}{' → now' if last else ''}</text>
          {ping}<circle cx="{cx:.1f}" cy="{ly}" r="8" fill="{t['bg']}" stroke="{col}" stroke-width="3"/>
          <text class="sans" x="{cx:.1f}" y="{ly + 42}" font-size="20" font-weight="800" text-anchor="middle" fill="{col}">{escape(org)}</text>
          <text class="sans" x="{cx:.1f}" y="{ly + 66}" font-size="13.5" text-anchor="middle" fill="{t['text']}">{escape(role)}</text>
          <text class="sans" x="{cx:.1f}" y="{ly + 92}" font-size="12.5" text-anchor="middle" fill="{t['muted']}">{escape(what)}</text>
          <text class="sans" x="{cx:.1f}" y="{ly + 111}" font-size="12.5" font-weight="600" text-anchor="middle" fill="{t['accent2']}">{escape(why)}</text>
        </g>""")
    x0, x1 = step / 2, step * (n - 0.5)
    body = f"""
    <line x1="{x0:.1f}" y1="{ly}" x2="{x1:.1f}" y2="{ly}" stroke="{t['line']}" stroke-width="3"/>
    <line class="track" x1="{x0:.1f}" y1="{ly}" x2="{x1:.1f}" y2="{ly}" stroke="{t['accent']}" stroke-width="3" stroke-linecap="round"/>
    {''.join(nodes)}
    <circle class="runner" cx="{x0:.1f}" cy="{ly}" r="4.5" fill="{t['accent2']}"/>
    """
    return svg(W, H, body, css, "Career: BizMotion 2013, IPVision 2014, Aurea 2017, Zalando 2021, Amazon 2022 to now")


# ----------------------------------------------------------------------------- REPO CARDS
def repo_card(t, name, desc, lang, lcolor, stars, forks):
    W, H = 480, 150
    # wrap description to two lines of ~52 chars
    words, lines, cur = desc.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > 54:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    title = name if len(name) <= 30 else name[:28] + "…"
    css = f"""
    .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
    .edge{{stroke-dasharray:180 1100;animation:edge 6s linear infinite}}
    @keyframes edge{{to{{stroke-dashoffset:-1280}}}}
    .star{{transform-box:fill-box;transform-origin:center;animation:tw 3s ease-in-out infinite}}
    @keyframes tw{{0%,70%,100%{{transform:scale(1) rotate(0)}}80%{{transform:scale(1.35) rotate(20deg)}}}}
    """
    star = "M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"
    fork = "M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z"
    repo = "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.25.25 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"
    desc_txt = "".join(f'<text class="sans" x="24" y="{76 + i * 21}" font-size="14" fill="{t["muted"]}">{escape(l)}</text>'
                       for i, l in enumerate(lines[:2]))
    body = f"""
    <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{t['card']}" stroke="{t['line']}"/>
    <rect class="edge" x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="none" stroke="{t['accent']}" stroke-width="2"/>
    <path d="{repo}" transform="translate(24 24)" fill="{t['muted']}"/>
    <text class="sans" x="48" y="37" font-size="17" font-weight="700" fill="{t['cool']}">{escape(title)}</text>
    {desc_txt}
    <circle cx="30" cy="{H - 26}" r="6" fill="{lcolor}"/>
    <text class="sans" x="42" y="{H - 21}" font-size="13" fill="{t['text']}">{lang}</text>
    <g class="star"><path d="{star}" transform="translate(120 {H - 34})" fill="{t['accent2']}"/></g>
    <text class="sans" x="142" y="{H - 21}" font-size="13" font-weight="700" fill="{t['text']}">{stars:,}</text>
    <path d="{fork}" transform="translate(196 {H - 34})" fill="{t['muted']}"/>
    <text class="sans" x="218" y="{H - 21}" font-size="13" fill="{t['text']}">{forks:,}</text>
    """
    return svg(W, H, body, css, f"{name}: {stars} stars, {forks} forks")


# ----------------------------------------------------------------------------- SYSTEM MAP
FUN_FACTS = [
    "has shipped code for VoIP codecs, TV remotes, fashion checkouts and CRMs",
    "phone-to-TV pairing: 80% faster. finding the real remote under the couch: unsolved",
    "favourite build: the one that finishes before the coffee does",
    "bugs in production: 0*   (*that I know of)",
    "learning German: mein Code kompiliert schneller als mein Deutsch",
]


def system_map(t):
    W, H = 1000, 330
    css = f"""
    .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
    .wire{{fill:none;stroke:{t['line']};stroke-width:2}}
    .pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 1.6s ease-out infinite}}
    @keyframes pulse{{from{{transform:scale(1);opacity:.7}}to{{transform:scale(3);opacity:0}}}}
    .hot{{animation:hot 5s linear infinite}}
    @keyframes hot{{0%,70%{{fill:{t['card']}}}76%,88%{{fill:{t['accent']};fill-opacity:.25}}100%{{fill:{t['card']}}}}}
    """
    def chip(x, y, w, h, label, sub=None, color=None, cls=""):
        c = color or t["line"]
        s = f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t["card"]}" stroke="{c}" stroke-width="1.5"/>'
        if sub:
            s += (f'<text class="sans" x="{x + w/2}" y="{y + h/2 - 3}" font-size="15" font-weight="700" text-anchor="middle" fill="{t["text"]}">{escape(label)}</text>'
                  f'<text class="sans" x="{x + w/2}" y="{y + h/2 + 15}" font-size="12" text-anchor="middle" fill="{t["muted"]}">{escape(sub)}</text>')
        else:
            s += f'<text class="sans" x="{x + w/2}" y="{y + h/2 + 5}" font-size="14" font-weight="600" text-anchor="middle" fill="{t["text"]}">{escape(label)}</text>'
        return s

    devices = [("iOS", "Swift · SwiftUI", "#f05138"), ("Android", "Kotlin", "#3ddc84"), ("React Native", "TypeScript · web", "#61dafb")]
    parts, wires, packets = [], [], []
    for i, (name, sub, col) in enumerate(devices):
        y = 58 + i * 62
        parts.append(chip(40, y, 180, 48, name, sub, col))
        d = f"M220 {y + 24} C 300 {y + 24}, 300 140, 380 140"
        wires.append(f'<path class="wire" d="{d}"/>')
        for k, (kp, beg) in enumerate([("0;1", i * 0.5), ("1;0", 1.2 + i * 0.5)]):
            packets.append(f'<circle r="4.5" fill="{col}"><animateMotion dur="2.4s" begin="{beg}s" repeatCount="indefinite" '
                           f'keyPoints="{kp}" keyTimes="0;1" calcMode="linear" path="{d}"/></circle>')
    # BFF
    parts.append(chip(380, 110, 190, 60, "GraphQL BFF", "one API for every app", t["accent2"]))
    d2 = "M570 140 L 690 140"
    wires.append(f'<path class="wire" d="{d2}"/>')
    for beg, kp in [(0, "0;1"), (0.6, "0;1"), (1.2, "1;0"), (1.8, "1;0")]:
        packets.append(f'<circle r="4.5" fill="{t["accent2"]}"><animateMotion dur="1.2s" begin="{beg}s" repeatCount="indefinite" '
                       f'keyPoints="{kp}" keyTimes="0;1" calcMode="linear" path="{d2}"/></circle>')
    # AWS cloud box
    parts.append(f'<rect x="690" y="40" width="270" height="200" rx="16" fill="none" stroke="{t["accent2"]}" stroke-width="1.5" stroke-dasharray="6 6"/>'
                 f'<text class="sans" x="710" y="66" font-size="15" font-weight="800" fill="{t["accent2"]}">AWS</text>'
                 f'<circle cx="842" cy="61" r="5" fill="#3fb950"/><circle class="pulse" cx="842" cy="61" r="5" fill="#3fb950"/>'
                 f'<text class="sans" x="854" y="66" font-size="13" fill="{t["muted"]}">99.99% uptime</text>')
    parts.append(chip(710, 84, 230, 40, "Lambda + Node.js services"))
    parts.append(chip(710, 134, 230, 40, "Data, caching, auth"))
    parts.append(chip(710, 184, 230, 40, "Monitoring & alarms"))
    # system design frame + label
    frame = (f'<rect x="20" y="22" width="{W-40}" height="230" rx="18" fill="none" stroke="{t["line"]}" stroke-dasharray="2 6"/>'
             f'<rect x="40" y="12" width="236" height="22" rx="11" fill="{t["bg"]}"/>'
             f'<text class="mono" x="52" y="28" font-size="13" fill="{t["muted"]}">system design: one map, app to cloud</text>')
    # CI/CD lane
    steps = ["commit", "build", "test", "release", "monitor"]
    lane_y, x0, gap, pw = 288, 230, 150, 110
    lane = [f'<text class="sans" x="40" y="{lane_y + 5}" font-size="14" font-weight="700" fill="{t["text"]}">Infrastructure</text>',
            f'<text class="sans" x="40" y="{lane_y + 23}" font-size="12" fill="{t["muted"]}">CI/CD, builds, releases</text>',
            f'<line x1="{x0}" y1="{lane_y}" x2="{x0 + gap*4 + pw}" y2="{lane_y}" stroke="{t["line"]}" stroke-width="2"/>']
    for i, s_ in enumerate(steps):
        x = x0 + i * gap
        lane.append(f'<rect class="hot" style="animation-delay:{-5 + i*0.9:.1f}s" x="{x}" y="{lane_y - 16}" width="{pw}" height="32" rx="16" fill="{t["card"]}" stroke="{t["line"]}"/>'
                    f'<text class="mono" x="{x + pw/2}" y="{lane_y + 5}" font-size="13" text-anchor="middle" fill="{t["text"]}">{s_}</text>')
    token = (f'<circle r="6" fill="{t["accent"]}"><animate attributeName="cx" values="{x0};{x0 + gap*4 + pw}" dur="5s" repeatCount="indefinite"/>'
             f'<animate attributeName="cy" values="{lane_y - 22};{lane_y - 22}" dur="5s" repeatCount="indefinite"/></circle>')
    body = frame + "".join(wires) + "".join(parts) + "".join(packets) + "".join(lane) + token
    return svg(W, H, body, css, "System map: iOS, Android and React Native apps talk to a GraphQL BFF and AWS services at 99.99% uptime; CI/CD pipeline from commit to monitor")


# ----------------------------------------------------------------------------- BUILD RACE
def build_race(t):
    W, H, cyc = 1000, 200, 12
    bx, bw = 290, 560
    css = f"""
    .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
    .slow{{transform-box:fill-box;transform-origin:left;animation:slow {cyc}s linear infinite}}
    @keyframes slow{{0%{{transform:scaleX(0)}}95%,100%{{transform:scaleX(1)}}}}
    .fast{{transform-box:fill-box;transform-origin:left;animation:fast {cyc}s cubic-bezier(.3,0,.3,1) infinite}}
    @keyframes fast{{0%{{transform:scaleX(0)}}28.5%,100%{{transform:scaleX(1)}}}}
    .w{{opacity:0;animation:w {cyc}s steps(1) infinite}}
    @keyframes w{{0%{{opacity:0}}1%{{opacity:1}}33%,100%{{opacity:0}}}}
    .cup{{opacity:0;animation:cup {cyc}s steps(1) infinite}}
    @keyframes cup{{0%{{opacity:1}}100%{{opacity:0}}}}
    .done{{opacity:0;animation:done {cyc}s infinite}}
    @keyframes done{{0%,28%{{opacity:0;transform:translateY(6px)}}31%,97%{{opacity:1;transform:none}}100%{{opacity:0}}}}
    .steam{{animation:steam 1.6s ease-in-out infinite}}
    @keyframes steam{{0%,100%{{transform:translateY(0);opacity:.3}}50%{{transform:translateY(-3px);opacity:.9}}}}
    """
    def cup(x, y):
        return (f'<g transform="translate({x} {y})"><path d="M0 4 h16 v10 a6 6 0 0 1 -6 6 h-4 a6 6 0 0 1 -6 -6 Z" fill="{t["accent2"]}"/>'
                f'<path d="M16 7 h3 a3 3 0 0 1 0 7 h-3" fill="none" stroke="{t["accent2"]}" stroke-width="2"/>'
                f'<path class="steam" d="M5 0 q2 -3 0 -6 M11 0 q2 -3 0 -6" fill="none" stroke="{t["muted"]}" stroke-width="1.5" stroke-linecap="round"/></g>')
    # coffee cups appear at 1/4, 2/4, 3/4 of the slow build (shown via negative delays)
    cups = ""
    for k in range(3):
        start = (k + 1) * 0.25 * cyc * 0.95
        # visible from 'start' until end of cycle: use a dedicated keyframe per cup
        p = start / cyc * 100
        cups += (f'<style>@keyframes c{k}{{0%,{p - .01:.2f}%{{opacity:0}}{p:.2f}%,97%{{opacity:1}}100%{{opacity:0}}}}</style>'
                 f'<g style="animation:c{k} {cyc}s steps(1) infinite;opacity:0">{cup(bx + bw + 24 + k * 30, 30)}</g>')
    msgs = ["compiling…", "still compiling… coffee #2", "coffee #3. is it Friday yet?"]
    captions = ""
    for k, m in enumerate(msgs):
        a, b = k / 3 * 95, (k + 1) / 3 * 95
        captions += (f'<style>@keyframes m{k}{{0%,{max(a - .01, 0):.2f}%{{opacity:{1 if k == 0 else 0}}}{a:.2f}%,{b - .01:.2f}%{{opacity:1}}{b:.2f}%,100%{{opacity:0}}}}</style>'
                     f'<text class="mono" x="{bx}" y="84" font-size="13" fill="{t["muted"]}" style="animation:m{k} {cyc}s steps(1) infinite;opacity:0">{escape(m)}</text>')
    body = f"""
    <text class="sans" x="30" y="52" font-size="16" font-weight="700" fill="{t['text']}">Before</text>
    <text class="sans" x="30" y="72" font-size="13" fill="{t['muted']}">one big monolith</text>
    <rect x="{bx}" y="38" width="{bw}" height="24" rx="12" fill="{t['card']}" stroke="{t['line']}"/>
    <rect class="slow" x="{bx}" y="38" width="{bw}" height="24" rx="12" fill="{t['muted']}" fill-opacity=".55"/>
    {captions}{cups}
    <text class="sans" x="30" y="142" font-size="16" font-weight="700" fill="{t['text']}">After</text>
    <text class="sans" x="30" y="162" font-size="13" fill="{t['muted']}">modular, cached, parallel</text>
    <rect x="{bx}" y="128" width="{bw}" height="24" rx="12" fill="{t['card']}" stroke="{t['line']}"/>
    <rect class="fast" x="{bx}" y="128" width="{bw * 0.3:.0f}" height="24" rx="12" fill="{t['accent']}"/>
    <g class="done">
      <path d="M{bx + bw*0.3 + 16:.0f} 140 l6 6 l12 -13" fill="none" stroke="#3fb950" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <text class="mono" x="{bx + bw*0.3 + 44:.0f}" y="145" font-size="13" fill="{t['text']}">shipped. went outside.</text>
      <text class="sans" x="{bx + bw + 24}" y="150" font-size="30" font-weight="800" fill="{t['accent']}">-70%</text>
    </g>
    """
    return svg(W, H, body, css, "Build race: the monolith build needs three coffees; the modular build finishes in 30% of the time")


# ----------------------------------------------------------------------------- TERMINAL
def terminal(t):
    W = 1000
    lh, top = 30, 96
    H = top + lh * (len(FUN_FACTS) + 1) + 10
    cmd = "partho --fun-facts"
    cw = 15 * 0.602
    k = len(cmd)
    widths = [round(j * cw, 1) for j in range(k + 1)]
    vals = ";".join(map(str, widths))
    kt = ";".join(str(round(j / k, 4)) for j in range(k + 1))
    css = f"""
    .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
    .ln{{opacity:0;animation:ln .5s ease-out forwards}}
    @keyframes ln{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}
    .blink{{animation:blink 1s steps(1) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    @media (prefers-reduced-motion: reduce){{.ln{{opacity:1!important}}}}
    """
    lines = "".join(
        f'<g class="ln" style="animation-delay:{1.9 + i * 0.75:.2f}s"><text class="mono" x="40" y="{top + (i + 1) * lh}" font-size="15">'
        f'<tspan fill="{t["accent"]}">› </tspan><tspan fill="{t["text"]}">{escape(f)}</tspan></text></g>'
        for i, f in enumerate(FUN_FACTS))
    last_y = top + (len(FUN_FACTS) + 1) * lh + 2
    body = f"""
    <rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{t['card']}" stroke="{t['line']}"/>
    <path d="M.5 40 h{W-1}" stroke="{t['line']}"/>
    <circle cx="26" cy="20" r="6" fill="#ff5f57"/><circle cx="46" cy="20" r="6" fill="#febc2e"/><circle cx="66" cy="20" r="6" fill="#28c840"/>
    <text class="mono" x="{W/2}" y="25" font-size="13" text-anchor="middle" fill="{t['muted']}">~/berlin — zsh</text>
    <defs><clipPath id="cmd"><rect x="{40 + 2 * cw:.1f}" y="60" height="30" width="0">
      <animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="1.4s" begin=".3s" fill="freeze" calcMode="discrete"/></rect></clipPath></defs>
    <text class="mono" x="40" y="{top - 16}" font-size="15"><tspan fill="#3fb950">$ </tspan></text>
    <text class="mono" x="{40 + 2 * cw:.1f}" y="{top - 16}" font-size="15" fill="{t['text']}" clip-path="url(#cmd)">{cmd}</text>
    {lines}
    <g class="ln" style="animation-delay:{1.9 + len(FUN_FACTS) * 0.75:.2f}s"><text class="mono" x="40" y="{last_y}" font-size="15" fill="#3fb950">$ </text>
    <rect class="blink" x="{40 + 2 * cw:.1f}" y="{last_y - 14}" width="9" height="18" fill="{t['accent']}"/></g>
    """
    return svg(W, H, body, css, "partho --fun-facts: " + "; ".join(FUN_FACTS))


# ----------------------------------------------------------------------------- FOOTER
def footer(t):
    W, H = 1000, 120
    css = f"""
    .sans{{font-family:{SANS}}}
    .w{{fill:none;stroke-width:2;animation:sl 8s linear infinite}}
    @keyframes sl{{to{{transform:translateX(-200px)}}}}
    """
    def wave(y, amp, color, op, dur):
        d = f"M0 {y} " + " ".join(f"q 50 {-amp if i % 2 == 0 else amp} 100 0" for i in range(14))
        return f'<path class="w" style="animation-duration:{dur}s" d="{d}" stroke="{color}" opacity="{op}"/>'
    body = f"""
    <defs><linearGradient id="f" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".15" stop-color="#fff"/><stop offset=".85" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
      <mask id="m"><rect width="{W}" height="{H}" fill="url(#f)"/></mask></defs>
    <g mask="url(#m)">{wave(46, 14, t['accent'], .9, 7)}{wave(46, 9, t['accent2'], .6, 11)}{wave(46, 5, t['cool'], .5, 15)}</g>
    <text class="sans" x="{W/2}" y="104" font-size="15" text-anchor="middle" fill="{t['muted']}">
      Thanks for stopping by. If you're building something people open every day, let's talk.</text>
    """
    return svg(W, H, body, css, "Thanks for stopping by")


# ----------------------------------------------------------------------------- MAIN
def main():
    OUT.mkdir(exist_ok=True)
    for mode, t in THEMES.items():
        (OUT / f"hero-{mode}.svg").write_text(hero(t))
        (OUT / f"impact-{mode}.svg").write_text(impact(t))
        (OUT / f"journey-{mode}.svg").write_text(journey(t))
        (OUT / f"footer-{mode}.svg").write_text(footer(t))
        (OUT / f"system-{mode}.svg").write_text(system_map(t))
        (OUT / f"race-{mode}.svg").write_text(build_race(t))
        (OUT / f"terminal-{mode}.svg").write_text(terminal(t))
        for r in REPOS:
            (OUT / f"repo-{r[0]}-{mode}.svg").write_text(repo_card(t, *r))
    print("wrote", len(list(OUT.glob("*.svg"))), "files to", OUT)


if __name__ == "__main__":
    main()
