#!/usr/bin/env python3
"""Generate the Higgsedit edit script (build/edit.jsx) and the sandbox fetch list (build/fetch.sh).

Inputs: pipeline/timing.json (scene timeline), pipeline/map/kz_oblasts.json (map paths),
pipeline/asset_sizes.json (pixel sizes of the captured screenshots), pipeline/assets.json (name -> https URL).

Usage: python3 pipeline/build_edit.py --mode frames|draft|final
  frames : write one PNG per scene (storyboard pass)
  draft  : render a low-quality preview
  final  : render the 1080p master
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mode = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "frames"
font_mode = sys.argv[sys.argv.index("--fonts") + 1] if "--fonts" in sys.argv else "shaped"
word_motion = "--no-word-motion" not in sys.argv
sans_family = sys.argv[sys.argv.index("--sans") + 1] if "--sans" in sys.argv else "Manrope"
serif_family = sys.argv[sys.argv.index("--serif") + 1] if "--serif" in sys.argv else "Spectral"

timing = json.load(open(os.path.join(ROOT, "pipeline", "timing.json")))
T = {s["n"]: s for s in timing["scenes"]}
MAP = json.load(open(os.path.join(ROOT, "pipeline", "map", "kz_oblasts.json")))
SIZES = json.load(open(os.path.join(ROOT, "pipeline", "asset_sizes.json")))
ASSETS = json.load(open(os.path.join(ROOT, "pipeline", "assets.json")))  # name -> url

# extra known sizes (generated assets / videos)
SIZES.update({"mark3d.png": [2688, 1520], "cubes.png": [2688, 1520], "devices.png": [2688, 1520],
              "mark3d.mp4": [1920, 1080], "cubes.mp4": [1920, 1080], "admin-tour.mp4": [1600, 1000], "staff-tour.mp4": [1600, 1000]})
media_names = [n for n in ASSETS if n.split(".")[-1] in ("png", "mp4")]
asset_keys = {n: n.rsplit(".", 1)[0].replace("-", "_") for n in media_names}

JSX = r'''
export default async ({ project, icon }) => {
  const C = { paper: '#f6f4ef', paper2: '#efebe2', paper3: '#e8e3d8', sheet: '#ffffff', line: '#e6e1d6', line2: '#d6cfc0',
    ink: '#17150f', ink2: '#57534a', ink3: '#8a8478', clay: '#d9613f', clayInk: '#a8401f', claySoft: '#f7e4db', clayBorder: '#ecc6b6',
    ops: '#14120d', opsSurface: '#262218', opsLine: '#45402f', opsInk: '#ede9df', ops2: '#9b9484', glow: '#e8835a',
    ok: '#2f7d5b', okSoft: '#e2efe7', okStrong: '#1c4d38', warnSoft: '#f6ecd6', warnBorder: '#e3cd9c', warnInk: '#8a5b0e',
    brick: '#bf4034', brickSoft: '#f8e3e0', brickBorder: '#ecbfb9', mapBase: '#d9d3c4', mapInk: '#2b2822' };
  const T = __TIMING__;
  const TOTAL = __TOTAL__;
  const MAP = __MAP__;
  const SIZES = __SIZES__;
  const FONT_MODE = '__FONT_MODE__';
  const WORD_MOTION = __WORD_MOTION__;
  const RENDER_MODE = '__RENDER_MODE__';

  const p = await project({ dir: '.', size: '1920x1080', fps: 30, background: C.paper });
  const FONTS = {};
  if (FONT_MODE === 'shaped') {
    FONTS.serif = await p.add('fonts-src/Spectral-Regular.ttf');
    FONTS.serifM = await p.add('fonts-src/Spectral-Medium.ttf');
    const m = await p.add('fonts-src/Manrope[wght].ttf');
    FONTS.sans = m; FONTS.sans500 = m; FONTS.sans600 = m;
  }
  const A = {};
__ASSET_ADDS__
  const mix = await p.add('media/mix.mp3');
  p.cut(mix, { from: 0, dur: TOTAL, at: 0 });

  // ---------- helpers ----------
  const isCyr = (s) => /[Ѐ-ӿ]/.test(s);
  const WGHT = { sans: 400, sans500: 500, sans600: 600 };
  function fontProps(kind, s) {
    if (FONT_MODE === 'shaped') {
      const o = { fontAssetId: FONTS[kind].id, script: isCyr(s) ? 'Cyrl' : 'Latn', language: isCyr(s) ? 'ru' : 'en' };
      if (kind in WGHT) o.axes = { wght: WGHT[kind] };
      return { typography: o };
    }
    return kind in WGHT ? { fontFamily: '__SANS__', fontWeight: WGHT[kind] } : { fontFamily: '__SERIF__', fontWeight: kind === 'serifM' ? 500 : 400 };
  }
  const tx = (s, o) => {
    const props = { x: o.x, y: o.y, width: o.w, height: o.h, fontSize: o.size, color: o.color || C.ink, ...fontProps(o.font || 'sans', s) };
    if (o.align) props.align = o.align;
    if (o.lh) props.lineHeight = o.lh;
    if (o.at != null) props.at = o.at;
    if (o.duration != null) props.duration = o.duration;
    if (o.reveal != null) {
      if (WORD_MOTION && o.words) props.motion = { by: 'word', from: { opacity: 0, y: 10 }, at: o.reveal, duration: 0.35, overlap: 0.5 };
      else props.animate = [{ property: 'opacity', from: 0, to: 1, at: o.reveal, duration: 0.45, easing: 'ease-out' }];
    } else if (o.animate) props.animate = o.animate;
    return <text {...props}>{s}</text>;
  };
  const mh = (k, w) => Math.round(w * SIZES[k][1] / SIZES[k][0]);
  const enter = (extra) => ({ motion: { enter: { from: { opacity: 0, ...(extra || {}) }, duration: 0.45 } } });
  const ico = (name, o) => (
    <frame x={o.x} y={o.y} width={o.size} height={o.size} layout="column" align="center" justify="center">
      {icon(name, { size: o.size, color: o.color || C.ink, strokeWidth: o.sw || 1.5 })}
    </frame>);
  function win(k, o) {
    const w = o.w, h = o.h, mw = o.mw || w, mhh = o.mh || mh(k, mw);
    const anim = [];
    const zd = o.zdur || o.dur;
    if (o.zoom) anim.push({ property: 'scale', from: 1, to: o.zoom, at: o.delay || 0, duration: zd, easing: 'smooth' });
    if (o.dx) anim.push({ property: 'offsetX', from: 0, to: o.dx, at: o.delay || 0, duration: zd, easing: 'smooth' });
    if (o.dy) anim.push({ property: 'offsetY', from: 0, to: o.dy, at: o.delay || 0, duration: zd, easing: 'smooth' });
    const manim = [];
    if (o.pan) manim.push({ property: 'offsetY', from: 0, to: -o.pan, at: o.pdelay || 0, duration: o.pdur || o.dur, easing: 'smooth' });
    const wrap = { x: o.x, y: o.y, width: w, height: h, layout: 'none', origin: 'center' };
    if (anim.length) wrap.animate = anim;
    if (o.at != null) wrap.at = o.at;
    if (o.duration != null) wrap.duration = o.duration;
    if (o.fade) wrap.motion = { enter: { from: { opacity: 0 }, duration: 0.35 } };
    const media = { file: A[k], x: o.mx || 0, y: o.my || 0, width: mw, height: mhh };
    if (o.trim != null) media.trimStart = o.trim;
    if (manim.length) media.animate = manim;
    const r = o.r == null ? 14 : o.r;
    return (
      <frame {...wrap}>
        <rect x={0} y={0} width={w} height={h} radius={r} fill={C.sheet} strokeColor={o.stroke || C.line2} strokeWidth={2} />
        <frame x={1} y={1} width={w - 2} height={h - 2} layout="none" clip radius={r - 1} background={C.sheet}>
          <media {...media} />
        </frame>
        {o.children || null}
      </frame>);
  }
  const card = (o) => {
    const props = { x: o.x, y: o.y, width: o.w, height: o.h, layout: 'none', origin: 'center', motion: { enter: { from: { y: 18, opacity: 0, scale: 0.97 }, duration: 0.45 } } };
    if (o.at != null) props.at = o.at;
    if (o.duration != null) props.duration = o.duration;
    return (
      <frame {...props}>
        <rect x={0} y={0} width={o.w} height={o.h} radius={o.r == null ? 16 : o.r} fill={o.fill || C.sheet} strokeColor={o.stroke || C.line} strokeWidth={1.5} />
        {o.children}
      </frame>);
  };
  const pill = (label, iconName, o) => (
    <frame x={o.x} y={o.y} width={o.w} height={o.h} layout="none" origin="center" motion={{ enter: { from: { scale: 0.9, opacity: 0 }, duration: 0.5 } }}>
      <rect x={0} y={0} width={o.w} height={o.h} radius={o.h / 2} fill={o.fill || C.sheet} strokeColor={o.stroke || C.line2} strokeWidth={1.5} />
      {ico(iconName, { x: 44, y: (o.h - 48) / 2, size: 48, color: o.color || C.ink })}
      {tx(label, { x: 116, y: (o.h - 54) / 2, w: o.w - 130, h: 60, size: 44, font: 'sans600', color: o.color || C.ink })}
    </frame>);
  const mark = (size, x, y, o = {}) => {
    const props = { x, y, width: size, height: size, layout: 'none', origin: 'center' };
    if (o.animate) props.animate = o.animate;
    return (
      <frame {...props}>
        <rect x={0} y={0} width={size} height={size} radius={size * 0.25} fill={C.clay} />
        <rect x={size * 0.23} y={size * 0.30} width={size * 0.045} height={size * 0.40} radius={size * 0.02} fill="#ffffff" />
        {tx('О', { x: size * 0.33, y: size * 0.10, w: size * 0.6, h: size * 0.85, size: size * 0.6, font: 'serifM', color: '#ffffff', align: 'center' })}
      </frame>);
  };
  const wordmark = (size, x, y, o = {}) => (
    <frame x={x} y={y} width={size * 5} height={size} layout="none">
      {mark(size, 0, 0, o)}
      {tx('ИС ОТО', { x: size * 1.22, y: size * 0.02, w: size * 3.8, h: size, size: size * 0.86, font: 'sans600', reveal: o.reveal })}
    </frame>);
  const grid = () => [
    ...Array.from({ length: 16 }, (_, i) => <rect x={60 + i * 120} y={0} width={1} height={1080} fill="#ece8df" />),
    ...Array.from({ length: 9 }, (_, i) => <rect x={0} y={60 + i * 120} width={1920} height={1} fill="#ece8df" />)];
  function scene(n, bg, children, opt = {}) {
    const t = T[n]; const off = opt.off || 0; const at = t.at + off; const dur = opt.dur || (t.dur - off);
    const props = { width: 1920, height: 1080, layout: 'none', background: bg };
    if (opt.fade !== 0) props.motion = { enter: { from: { opacity: 0 }, duration: opt.fade || 0.3 } };
    p.compose(<frame {...props}>{children}</frame>, { at, dur, name: 's' + n + (opt.tag || '') });
  }
  const D = (n) => T[n].dur;

  // ---------- Act A ----------
  scene(1, C.paper, [
    wordmark(120, 700, 470, { animate: [{ property: 'scale', from: 0.7, to: 1, duration: 0.55, easing: 'house' }], reveal: 0.2 }),
    tx('организация труда осуждённых', { x: 460, y: 620, w: 1000, h: 50, size: 28, color: C.ink2, align: 'center', reveal: 0.6 }),
  ], { fade: 0 });

  scene(2, C.paper, [
    ...grid(),
    <frame x={60} y={150} width={MAP.w} height={MAP.h} layout="none" origin="center" animate={[{ property: 'scale', from: 1.05, to: 1, duration: D(2), easing: 'smooth' }]}>
      {MAP.oblasts.map((s) => <path d={s.d} width={MAP.w} height={MAP.h} fill={C.mapBase} stroke={{ color: C.paper, width: 1.5 }} />)}
      {MAP.oblasts.map((s, i) => <path d={s.d} width={MAP.w} height={MAP.h} fill={C.mapInk} stroke={{ color: C.paper, width: 1.5 }} animate={[{ property: 'opacity', from: 0, to: 1, at: 0.7 + i * 0.12, duration: 0.5, easing: 'ease-out' }]} />)}
      {MAP.lakes.map((s) => <path d={s.d} width={MAP.w} height={MAP.h} fill={C.paper} />)}
      {MAP.cities.map((s) => <path d={s.d} width={MAP.w} height={MAP.h} fill={C.clay} />)}
    </frame>,
    ...[['20', 'регионов', 0.9], ['18', 'департаментов', 2.4], ['78', 'учреждений', 3.9]].map(([num, cap, at], i) => (
      <frame x={1540} y={150 + i * 250} width={360} height={230} layout="none" at={at} motion={{ enter: { from: { opacity: 0, y: 16 }, duration: 0.5 } }}>
        {tx(num, { x: 0, y: 0, w: 360, h: 170, size: 150, font: 'serif' })}
        {tx(cap, { x: 6, y: 172, w: 340, h: 40, size: 26, color: C.ink2 })}
      </frame>)),
  ]);

  const MODULES = [['users', 'Осуждённые'], ['file-signature', 'Договоры'], ['user-search', 'Подбор персонала'], ['calendar-days', 'Табель'],
    ['banknote', 'Заработная плата'], ['chart-bar', 'Отчётность'], ['hard-hat', 'Охрана труда'], ['graduation-cap', 'Обучение'],
    ['factory', 'Площадки'], ['tablet', 'Кабинет осуждённого'], ['scan-face', 'Face ID'], ['shopping-cart', 'Магазин']];
  scene(3, C.paper3, MODULES.map(([ic, label], i) => card({ x: 324 + (i % 4) * 324, y: 291 + Math.floor(i / 4) * 174, w: 300, h: 150, at: 0.15 + i * 0.07, children: [
    ico(ic, { x: 24, y: 24, size: 44 }),
    tx(label, { x: 24, y: 94, w: 260, h: 40, size: 22, font: 'sans600' }),
  ] })));

  scene(4, C.paper, [
    <frame x={300} y={370} width={820} height={300} layout="none"
      motion={{ timeline: { duration: 1.4, easing: 'ease-out', targets: [{ target: 'Kpi', counter: { from: 41, to: 70, decimals: 0, suffix: ' %' } }] } }}>
      <frame name="Kpi" x={0} y={0} width={820} height={300} layout="none">
        {tx('41 %', { x: 0, y: 0, w: 820, h: 300, size: 240, font: 'serif' })}
      </frame>
    </frame>,
    tx('трудозанятость\nпо системе', { x: 1160, y: 420, w: 700, h: 130, size: 40, color: C.ink2, lh: 1.25, reveal: 1.3, words: true }),
    <rect x={1160} y={580} width={160} height={3} fill={C.clay} animate={[{ property: 'scaleX', from: 0, to: 1, at: 1.9, duration: 0.5, easing: 'house' }]} />,
    tx('целевой показатель — 70 %', { x: 1160, y: 600, w: 700, h: 40, size: 24, color: C.ink3, reveal: 2.1 }),
  ]);

  const frag = (x, y, w, h, fromX, at, children) => (
    <frame x={x} y={y} width={w} height={h} layout="none" at={at} motion={{ enter: { from: { x: fromX, opacity: 0 }, duration: 0.55 } }}>
      <rect x={0} y={0} width={w} height={h} radius={16} fill={C.sheet} strokeColor={C.line} strokeWidth={1.5} />
      {children}
    </frame>);
  scene(5, C.paper, [
    mark(170, 875, 455, { animate: [{ property: 'scale', from: 0.8, to: 1, duration: 0.5, easing: 'house' }] }),
    frag(260, 260, 440, 190, -260, 0.1, [
      tx('Трудозанятость', { x: 28, y: 22, w: 380, h: 30, size: 20, color: C.ink3 }),
      tx('70,0 %', { x: 28, y: 56, w: 380, h: 90, size: 72, font: 'serif' }),
      tx('цель 70 % · +1,2 п.п. к прошлому месяцу', { x: 28, y: 146, w: 400, h: 30, size: 19, color: C.ok }),
    ]),
    frag(1230, 300, 400, 90, 260, 0.25, [
      <rect x={24} y={22} width={200} height={46} radius={23} fill={C.okSoft} strokeColor="#bfd9cb" strokeWidth={1} />,
      <rect x={44} y={39} width={12} height={12} radius={6} fill={C.ok} />,
      tx('Действует', { x: 66, y: 32, w: 150, h: 30, size: 21, font: 'sans500', color: C.okStrong }),
    ]),
    frag(1200, 610, 440, 170, 260, 0.4, [
      <rect x={16} y={18} width={408} height={44} radius={8} fill={C.claySoft} />,
      <rect x={16} y={18} width={4} height={44} radius={2} fill={C.clay} />,
      tx('Панель управления', { x: 40, y: 27, w: 360, h: 30, size: 20, font: 'sans500', color: C.clayInk }),
      tx('Осуждённые', { x: 40, y: 76, w: 360, h: 30, size: 20, color: C.ink2 }),
      tx('Договоры', { x: 40, y: 120, w: 360, h: 30, size: 20, color: C.ink2 }),
    ]),
    frag(300, 640, 520, 120, -260, 0.55, [
      tx('УК-161/10', { x: 28, y: 22, w: 200, h: 30, size: 20, font: 'sans600' }),
      tx('Учреждение УК-161/10 · Актобе', { x: 28, y: 54, w: 380, h: 30, size: 18, color: C.ink3 }),
      tx('43,1 %', { x: 380, y: 28, w: 120, h: 50, size: 36, font: 'serif', color: C.brick }),
    ]),
  ]);

  scene(6, C.paper, [
    <frame x={0} y={0} width={1920} height={1080} layout="none" origin="center" animate={[{ property: 'scale', from: 1.04, to: 1, duration: D(6), easing: 'smooth' }]}>
      <media file={A.devices} x={0} y={-3} width={1920} height={1086} />
      <frame x={323} y={269} width={863} height={547} layout="none" clip animate={[{ property: 'opacity', from: 0, to: 1, at: 0.35, duration: 0.5 }]}>
        <media file={A.dashboard} x={0} y={0} width={863} height={539} />
      </frame>
      <frame x={1351} y={284} width={256} height={551} layout="none" clip animate={[{ property: 'opacity', from: 0, to: 1, at: 0.55, duration: 0.5 }]}>
        <media file={A.kiosk_checkpoint_phone} x={0} y={0} width={256} height={554} />
      </frame>
    </frame>,
    tx('Планшет сотрудника', { x: 380, y: 880, w: 760, h: 40, size: 26, color: C.ink2, align: 'center', reveal: 0.9 }),
    tx('Киоск Face ID · Android', { x: 1240, y: 880, w: 480, h: 40, size: 26, color: C.ink2, align: 'center', reveal: 1.1 }),
  ]);

  const BADGES = [['shield-check', 'Суверенный контур'], ['lock', 'Права на уровне запроса'], ['scroll-text', 'Журнал аудита'], ['languages', 'RU / KK']];
  scene(7, C.paper, BADGES.map(([ic, label], i) => (
    <frame x={330 + i * 360} y={380} width={300} height={320} layout="none" at={0.1 + i * 0.14} motion={{ enter: { from: { opacity: 0, y: 14 }, duration: 0.45 } }}>
      <rect x={80} y={0} width={140} height={140} radius={70} fill={C.sheet} strokeColor={C.line2} strokeWidth={1.5} />
      {ico(ic, { x: 118, y: 38, size: 64 })}
      {tx(label, { x: 0, y: 176, w: 300, h: 70, size: 24, font: 'sans500', color: C.ink2, align: 'center', lh: 1.25 })}
    </frame>)));

  {
    const d = D(8); const cut = Math.max(2.5, d - 4.9);
    scene(8, C.paper, [
      <media file={A.cubes} x={0} y={-3} width={1920} height={1086} />,
      <frame x={0} y={0} width={1920} height={1080} layout="none" duration={Math.min(cut, 5)}><media file={A.cubes_mp4} x={0} y={0} width={1920} height={1080} /></frame>,
      <frame x={0} y={0} width={1920} height={1080} layout="none" at={cut} motion={{ enter: { from: { opacity: 0 }, duration: 0.45 } }}>
        <media file={A.mark3d} x={0} y={-3} width={1920} height={1086} />
        <frame x={0} y={0} width={1920} height={1080} layout="none" duration={Math.min(d - cut, 5)}><media file={A.mark3d_mp4} x={0} y={0} width={1920} height={1080} /></frame>
      </frame>,
    ], { fade: 0.4 });
  }

  // ---------- Act B ----------
  scene(9, C.paper3, [pill('Панель руководителя', 'layout-dashboard', { x: 520, y: 470, w: 880, h: 140 })]);

  {
    const d = D(10); const still = Math.min(5.5, d);
    scene(10, C.paper3, [
      win('dashboard', { x: 100, y: 56, w: 1720, h: 968, zoom: 1.18, dur: still, duration: still }),
      ...(d > still ? [win('admin_tour', { x: 100, y: 56, w: 1720, h: 968, mh: 1075, trim: 9.5, at: still, fade: true, dur: d - still })] : []),
    ]);
  }
  {
    const d = D(11); const vid = Math.min(6.0, d);
    scene(11, C.paper3, [
      win('facilities_catalog', { x: 100, y: 56, w: 1720, h: 968, zoom: 1.12, dur: d }),
      win('admin_tour', { x: 100, y: 56, w: 1720, h: 968, mh: 1075, trim: 22.0, duration: vid, dur: vid }),
    ]);
  }
  scene(12, C.paper3, [
    win('recruitment_new', { x: 100, y: 56, w: 1100, h: 968, pan: 420, pdelay: 0.8, pdur: D(12) - 1 }),
    card({ x: 1260, y: 300, w: 560, h: 440, at: 0.5, children: [
      tx('Запрос на подбор', { x: 32, y: 28, w: 500, h: 40, size: 28, font: 'sans600' }),
      ...[['Профессия', 'Швея', 1.2], ['Количество', '25 человек', 2.0], ['Разряд', 'не ниже 3', 2.8]].map(([k, v, at], i) => (
        <frame x={32} y={96 + i * 106} width={496} height={96} layout="none" at={at} motion={{ enter: { from: { opacity: 0, x: -16 }, duration: 0.4 } }}>
          {tx(k, { x: 0, y: 0, w: 480, h: 30, size: 20, color: C.ink3 })}
          {tx(v, { x: 0, y: 30, w: 480, h: 60, size: 44, font: 'serif' })}
          <rect x={0} y={94} width={496} height={1} fill={C.line} />
        </frame>)),
    ] }),
  ]);
  {
    const navBlock = (k, x, label, at) => (
      <frame x={x} y={120} width={640} height={880} layout="none" at={at} motion={{ enter: { from: { opacity: 0, y: 14 }, duration: 0.45 } }}>
        {tx(label, { x: 0, y: 0, w: 640, h: 40, size: 26, font: 'sans600' })}
        <rect x={0} y={56} width={640} height={824} radius={14} fill={C.sheet} strokeColor={C.line2} strokeWidth={2} />
        <frame x={1} y={57} width={638} height={822} layout="none" clip radius={13} background={C.sheet}>
          <media file={A[k]} x={0} y={0} width={SIZES[k + '.png'][0]} height={SIZES[k + '.png'][1]} />
        </frame>
        <rect x={0} y={56} width={5} height={824} radius={2} fill={C.clay} />
      </frame>);
    scene(13, C.paper3, [
      navBlock('dashboard_employer', 260, 'Представитель работодателя — 4 раздела', 0.1),
      navBlock('dashboard', 1020, 'Администратор КУИС — 20 модулей', 0.5),
    ]);
  }
  const CRITERIA = [['Профессия совпадает', 40], ['Разряд не ниже требуемого', 20], ['Нет медицинских ограничений', 15], ['Действующий инструктаж по ОТ', 10], ['Нет дисциплинарных ограничений', 8], ['Остаток срока не менее 6 месяцев', 7]];
  scene(14, C.paper3, [
    win('recruitment_staff', { x: 80, y: 208, w: 1060, h: 662, zoom: 1.15, dur: D(14) }),
    card({ x: 1200, y: 208, w: 640, h: 662, at: 0.4, children: [
      tx('Почему этот кандидат', { x: 32, y: 28, w: 560, h: 40, size: 28, font: 'sans600' }),
      tx('шесть критериев · 100 баллов', { x: 32, y: 66, w: 560, h: 30, size: 20, color: C.ink3 }),
      ...CRITERIA.map(([label, pts], i) => (
        <frame x={32} y={118 + i * 88} width={576} height={80} layout="none" at={0.9 + i * 0.32} motion={{ enter: { from: { opacity: 0 }, duration: 0.35 } }}>
          {tx(label, { x: 0, y: 0, w: 460, h: 30, size: 20, color: C.ink2 })}
          {tx(String(pts), { x: 480, y: -8, w: 96, h: 52, size: 40, font: 'serif', align: 'right' })}
          <rect x={0} y={44} width={440} height={10} radius={5} fill={C.paper3} />
          <rect x={0} y={44} width={440 * pts / 40} height={10} radius={5} fill={C.clay} animate={[{ property: 'scaleX', from: 0, to: 1, at: 0.05, duration: 0.7, easing: 'house' }]} />
        </frame>)),
    ] }),
  ]);
  const EXCL = [['Без действующего инструктажа по ТБ', 'исключены'], ['Медицинские ограничения по виду работ', 'исключены'], ['Действующие дисциплинарные ограничения', 'исключены']];
  scene(15, C.paper3, [
    win('convicts_readiness', { x: 80, y: 208, w: 1060, h: 662, zoom: 1.1, dur: D(15) }),
    card({ x: 1200, y: 208, w: 640, h: 662, at: 0.3, children: [
      tx('Сводка исключённых', { x: 32, y: 28, w: 560, h: 40, size: 28, font: 'sans600' }),
      ...EXCL.map(([label, chip], i) => (
        <frame x={32} y={100 + i * 120} width={576} height={104} layout="none" at={0.8 + i * 0.5} motion={{ enter: { from: { opacity: 0, x: -12 }, duration: 0.4 } }}>
          <rect x={0} y={0} width={576} height={104} radius={12} fill={C.brickSoft} strokeColor={C.brickBorder} strokeWidth={1} animate={[{ property: 'scaleX', from: 0, to: 1, duration: 0.5, easing: 'house' }]} />
          {tx(label, { x: 20, y: 18, w: 420, h: 60, size: 20, color: C.ink, lh: 1.3 })}
          <rect x={446} y={34} width={112} height={36} radius={18} fill={C.brick} />
          {tx(chip, { x: 446, y: 40, w: 112, h: 30, size: 18, font: 'sans600', color: '#ffffff', align: 'center' })}
        </frame>)),
      <rect x={32} y={470} width={576} height={150} radius={12} fill={C.warnSoft} strokeColor={C.warnBorder} strokeWidth={1} animate={[{ property: 'opacity', from: 0, to: 1, at: 2.6, duration: 0.5 }]} />,
      tx('Проверка встроена в операцию,\nа не в предупреждение, которое можно закрыть.', { x: 56, y: 496, w: 530, h: 110, size: 22, color: C.warnInk, lh: 1.35, reveal: 2.7 }),
    ] }),
  ]);
  const STEPS = ['проект', 'согласование', 'согласован', 'подписан', 'действует'];
  scene(16, C.paper3, [
    win('contracts', { x: 100, y: 40, w: 1720, h: 740, zoom: 1.06, dur: D(16) }),
    <frame x={0} y={830} width={1920} height={200} layout="none">
      <rect x={300} y={40} width={1320} height={4} radius={2} fill={C.line2} />
      <rect x={300} y={40} width={1320} height={4} radius={2} fill={C.clay} animate={[{ property: 'scaleX', from: 0, to: 1, at: 0.8, duration: 3.6, easing: 'linear' }]} />
      {STEPS.map((s, i) => (
        <frame x={300 + i * 330 - 22} y={20} width={44} height={120} layout="none">
          <rect x={0} y={0} width={44} height={44} radius={22} fill={C.sheet} strokeColor={C.line2} strokeWidth={2} />
          <rect x={0} y={0} width={44} height={44} radius={22} fill={C.clay} animate={[{ property: 'opacity', from: 0, to: 1, at: 0.8 + i * 0.85, duration: 0.3 }]} />
          {tx(s, { x: -120, y: 62, w: 284, h: 36, size: 24, font: 'sans500', color: C.ink2, align: 'center' })}
        </frame>))}
    </frame>,
  ]);
  scene(17, C.paper3, [
    win('signing', { x: 100, y: 56, w: 1080, h: 675, zoom: 1.08, dur: D(17) }),
    win('production_print', { x: 1240, y: 56, w: 580, h: 968, pan: 500, pdelay: 1.2, pdur: D(17) - 1.4, fade: true, at: 0.6 }),
    card({ x: 100, y: 780, w: 1080, h: 244, at: 1.4, children: [
      tx('Печатные формы', { x: 32, y: 28, w: 900, h: 40, size: 28, font: 'sans600' }),
      tx('А4 · реквизиты и подписи · метка времени каждой версии', { x: 32, y: 78, w: 1000, h: 40, size: 22, color: C.ink2 }),
      tx('Типовой трудовой договор — казахская и русская колонки', { x: 32, y: 126, w: 1000, h: 40, size: 22, color: C.ink2 }),
      tx('Подпись ЭЦП на стенде — имитация (плашка сохраняется в кадре)', { x: 32, y: 174, w: 1000, h: 40, size: 20, color: C.warnInk }),
    ] }),
  ]);

  // ---------- Act C ----------
  const INTEG = [['database', 'ЦАБД УИС', 'единый реестр осуждённых'], ['scan-face', 'СКУД и Face ID', 'события проходов через КПП'], ['file-signature', 'ЭЦП НУЦ РК', 'электронная подпись документов']];
  scene(18, C.paper, [
    wordmark(96, 560, 250, { reveal: 0.1 }),
    tx('+', { x: 1080, y: 236, w: 100, h: 110, size: 90, font: 'serif', color: C.ink3, reveal: 0.6 }),
    tx('модуль расширения', { x: 1180, y: 262, w: 500, h: 80, size: 44, font: 'serif', reveal: 0.8 }),
    ...INTEG.map(([ic, name, sub], i) => (
      <frame x={560} y={440 + i * 150} width={1000} height={120} layout="none" at={1.6 + i * 0.6} motion={{ enter: { from: { opacity: 0, y: 14 }, duration: 0.45 } }}>
        <rect x={0} y={0} width={1000} height={120} radius={16} fill={C.sheet} strokeColor={C.line} strokeWidth={1.5} />
        {ico(ic, { x: 32, y: 34, size: 52 })}
        {tx(name, { x: 116, y: 24, w: 840, h: 40, size: 30, font: 'sans600' })}
        {tx(sub, { x: 116, y: 66, w: 840, h: 36, size: 22, color: C.ink2 })}
      </frame>)),
  ]);
  scene(19, C.paper3, [
    win('timesheets_full', { x: 100, y: 56, w: 1720, h: 968, pan: 900, pdelay: 0.6, pdur: D(19) - 0.8, zoom: 1.06, dur: D(19) }),
  ]);
  scene(20, C.paper3, [
    win('timesheets', { x: 100, y: 56, w: 1720, h: 968, zoom: 1.28, dur: D(20), children: [
      <rect x={40} y={520} width={1640} height={46} radius={6} fill={C.brickSoft} strokeColor={C.brick} strokeWidth={2} animate={[{ property: 'opacity', from: 0, to: 0.95, at: 1.2, duration: 0.5 }]} />,
    ] }),
    card({ x: 1120, y: 720, w: 700, h: 200, at: 2.2, fill: C.sheet, stroke: C.brickBorder, children: [
      <rect x={0} y={0} width={6} height={200} radius={3} fill={C.brick} />,
      tx('Расхождение со СКУД', { x: 36, y: 28, w: 640, h: 40, size: 28, font: 'sans600', color: C.brick }),
      tx('Корректировка не сохраняется без обоснования', { x: 36, y: 76, w: 640, h: 40, size: 22, color: C.ink2 }),
      <rect x={36} y={126} width={628} height={46} radius={8} fill={C.paper} strokeColor={C.brick} strokeWidth={2} />,
      tx('Обоснование — обязательное поле', { x: 52, y: 136, w: 600, h: 30, size: 20, color: C.ink3 }),
    ] }),
  ]);
  {
    const d = D(21); const h1 = Math.min(4.2, d);
    scene(21, C.paper3, [
      win('payroll', { x: 100, y: 56, w: 1720, h: 968, zoom: 1.1, dur: h1, duration: h1 }),
      win('transfers', { x: 100, y: 56, w: 1720, h: 968, zoom: 1.1, dur: d - h1, at: h1, fade: true }),
    ]);
  }

  // ---------- Act D ----------
  scene(22, C.ops, [pill('Отчётность', 'chart-bar', { x: 610, y: 470, w: 700, h: 140, fill: C.opsSurface, stroke: C.opsLine, color: C.opsInk })], { fade: 0 });
  {
    const d = D(23); const a = Math.min(3.2, d / 3); const b = Math.min(6.8, 2 * d / 3);
    scene(23, C.paper3, [
      win('reports', { x: 100, y: 56, w: 1720, h: 968, zoom: 1.08, dur: a, duration: a }),
      win('report_6', { x: 100, y: 56, w: 1720, h: 968, zoom: 1.1, dur: b - a, at: a, duration: b - a, fade: true }),
      win('report_9', { x: 100, y: 56, w: 1720, h: 968, zoom: 1.1, dur: d - b, at: b, fade: true }),
    ]);
  }
  {
    const d = D(24); const a = Math.min(3.4, d / 2);
    scene(24, C.paper3, [
      win('report_6', { x: 100, y: 56, w: 1720, h: 968, zoom: 1.35, dx: -420, dy: 300, dur: a, duration: a }),
      win('report_6_print', { x: 460, y: 40, w: 1000, h: 1000, pan: 420, pdur: d - a - 0.4, at: a, fade: true, dur: d - a }),
    ]);
  }

  // ---------- Act E ----------
  const tablet = (k, o) => (
    <frame x={o.x} y={o.y} width={1200} height={860} layout="none" origin="center" {...(o.at != null ? { at: o.at } : {})} {...(o.duration != null ? { duration: o.duration } : {})}
      motion={{ enter: { from: { opacity: 0, y: 24 }, duration: 0.5 } }} animate={[{ property: 'scale', from: 1, to: o.zoom || 1.04, duration: o.dur, easing: 'smooth' }]}>
      <rect x={0} y={0} width={1200} height={860} radius={40} fill="#26231d" />
      <rect x={20} y={20} width={1160} height={820} radius={24} fill="#0f0e0c" />
      <frame x={32} y={32} width={1136} height={796} layout="none" clip radius={14} background={C.sheet}>
        <media file={A[k]} x={0} y={0} width={1136} height={mh(k + '.png', 1136)} />
      </frame>
    </frame>);
  scene(25, C.paper3, [
    pill('Кабинет осуждённого', 'tablet', { x: 520, y: 50, w: 880, h: 120 }),
    tablet('cabinet', { x: 360, y: 200, dur: D(25) }),
  ]);
  {
    const d = D(26); const a = d / 3;
    scene(26, C.paper3, [
      tablet('cabinet_finance', { x: 360, y: 110, dur: a, duration: a }),
      tablet('cabinet_documents', { x: 360, y: 110, dur: a, at: a, duration: a }),
      tablet('cabinet_vacancies', { x: 360, y: 110, dur: d - 2 * a, at: 2 * a }),
    ]);
  }
  {
    const d = D(27); const a = d / 2;
    scene(27, C.paper3, [
      <frame x={300} y={100} width={420} height={880} layout="none" motion={{ enter: { from: { opacity: 0, y: 24 }, duration: 0.5 } }}>
        <rect x={0} y={0} width={420} height={880} radius={52} fill="#26231d" />
        <frame x={18} y={18} width={384} height={844} layout="none" clip radius={38} background="#0f0e0c">
          <media file={A.kiosk_checkpoint_phone} x={0} y={0} width={384} height={831} />
        </frame>
      </frame>,
      win('face_id', { x: 800, y: 215, w: 1040, h: 650, zoom: 1.1, dur: a, duration: a, fade: true }),
      win('shop', { x: 800, y: 215, w: 1040, h: 650, zoom: 1.1, dur: d - a, at: a, fade: true }),
    ]);
  }
  scene(28, C.paper3, [
    win('shop', { x: 100, y: 56, w: 1720, h: 968, dur: D(28) }),
    <rect x={0} y={0} width={1920} height={1080} fill={C.paper} animate={[{ property: 'opacity', from: 0, to: 0.72, at: 0.3, duration: 0.5 }]} />,
    <frame x={410} y={270} width={1100} height={540} layout="none" origin="center" at={0.5} motion={{ enter: { from: { opacity: 0, scale: 0.94 }, duration: 0.5 } }}>
      <rect x={0} y={0} width={1100} height={540} radius={24} fill={C.sheet} strokeColor={C.line2} strokeWidth={2} />
      <frame x={60} y={70} width={460} height={260} layout="none"
        motion={{ timeline: { duration: 1.2, easing: 'ease-out', at: 0.3, targets: [{ target: 'Cnt', counter: { from: 0, to: 107, decimals: 0 } }] } }}>
        <frame name="Cnt" x={0} y={0} width={460} height={260} layout="none">
          {tx('0', { x: 0, y: 0, w: 460, h: 260, size: 200, font: 'serif' })}
        </frame>
      </frame>
      {tx('сквозных сценариев\nпроверяют изоляцию данных\nпри каждой сборке', { x: 60, y: 340, w: 460, h: 150, size: 24, color: C.ink2, lh: 1.3, reveal: 1.4 })}
      <rect x={550} y={70} width={1} height={420} fill={C.line} />
      {tx('0', { x: 600, y: 0, w: 460, h: 260, size: 200, font: 'serif', reveal: 0.9 })}
      {tx('внешних обращений\nв рантайме: шрифты, иконки\nи графики — локальные', { x: 600, y: 340, w: 460, h: 150, size: 24, color: C.ink2, lh: 1.3, reveal: 1.6 })}
    </frame>,
  ]);

  // ---------- Act F ----------
  scene(29, C.paper3, [
    pill('Витрина мощностей', 'factory', { x: 520, y: 50, w: 880, h: 120 }),
    win('public_catalog', { x: 100, y: 200, w: 1720, h: 840, zoom: 1.1, dy: -110, delay: 0.6, dur: D(29) - 0.6 }),
  ]);
  {
    const d = D(30); const a = Math.min(4.8, d / 2.4);
    const ROUTE = ['Инспектор заполняет список', 'Работодатель подписывает', 'Пять виз должностных лиц', 'Начальник утверждает'];
    scene(30, C.paper3, [
      win('public_catalog', { x: 100, y: 56, w: 1720, h: 968, zoom: 1.3, dy: 260, dur: a, duration: a }),
      win('workforce', { x: 80, y: 208, w: 1060, h: 662, zoom: 1.08, at: a, fade: true, dur: d - a }),
      card({ x: 1200, y: 208, w: 640, h: 662, at: a + 0.3, children: [
        tx('Вывод на работу', { x: 32, y: 28, w: 560, h: 40, size: 28, font: 'sans600' }),
        tx('маршрут — как на бумаге', { x: 32, y: 66, w: 560, h: 30, size: 20, color: C.ink3 }),
        ...ROUTE.map((label, i) => (
          <frame x={32} y={120 + i * 130} width={576} height={110} layout="none" at={0.6 + i * 0.55} motion={{ enter: { from: { opacity: 0, y: 10 }, duration: 0.4 } }}>
            <rect x={0} y={0} width={576} height={84} radius={12} fill={i === 3 ? C.claySoft : C.paper} strokeColor={i === 3 ? C.clayBorder : C.line2} strokeWidth={1.5} />
            <rect x={24} y={26} width={32} height={32} radius={16} fill={C.clay} />
            {tx(String(i + 1), { x: 24, y: 29, w: 32, h: 30, size: 20, font: 'sans600', color: '#ffffff', align: 'center' })}
            {tx(label, { x: 76, y: 26, w: 480, h: 36, size: 22, font: 'sans500' })}
            {i < 3 ? <rect x={286} y={84} width={4} height={46} fill={C.line2} animate={[{ property: 'scaleY', from: 0, to: 1, at: 0.3, duration: 0.3 }]} /> : null}
          </frame>)),
      ] }),
    ]);
  }

  // ---------- Act G ----------
  {
    const d = D(31); const a = Math.min(3.6, d / 3);
    const FACTS = [['7', 'ролей и область видимости\nна уровне запроса к базе'], ['2', 'языка интерфейса —\nрусский и казахский, парно'], ['0', 'внешних обращений\nв рантайме'], ['№ 735', 'приказ МВД РК от 30.09.2025 —\nПравила организации труда осуждённых']];
    scene(31, C.ops, [
      tx('20', { x: 560, y: 300, w: 500, h: 340, size: 300, font: 'serif', color: C.opsInk, animate: [{ property: 'opacity', from: 0, to: 1, duration: 0.5 }] }),
      tx('модулей', { x: 1080, y: 470, w: 500, h: 80, size: 54, color: C.ops2, reveal: 0.5 }),
      tx('от реестра осуждённых до витрины площадей', { x: 1080, y: 540, w: 700, h: 40, size: 24, color: C.ops2, reveal: 0.9 }),
    ], { dur: a, fade: 0 });
    scene(31, C.paper3, FACTS.map(([num, cap], i) => card({ x: 240 + (i % 2) * 740, y: 220 + Math.floor(i / 2) * 340, w: 700, h: 300, at: 0.2 + i * 0.22, children: [
      tx(num, { x: 40, y: 40, w: 620, h: 160, size: 130, font: 'serif' }),
      tx(cap, { x: 40, y: 200, w: 620, h: 90, size: 24, color: C.ink2, lh: 1.3 }),
    ] })), { off: a, tag: 'b' });
  }
  scene(32, C.paper, [
    tx('Труд осуждённых — в цифровом контуре.', { x: 160, y: 340, w: 1600, h: 110, size: 76, font: 'serif', align: 'center', reveal: 0.2, words: true }),
    wordmark(72, 800, 560, { reveal: 0.9 }),
    tx('ТОО «AltaiLabs» · КУИС МВД Республики Казахстан · 2026', { x: 260, y: 700, w: 1400, h: 40, size: 24, color: C.ink3, align: 'center', reveal: 1.4 }),
    <rect x={0} y={0} width={1920} height={1080} fill="#000000" animate={[{ property: 'opacity', from: 0, to: 1, at: D(32) - 1.6, duration: 1.3, easing: 'ease-in' }]} />,
  ], { fade: 0.6 });

  // ---------- output ----------
  if (RENDER_MODE === 'frames') {
    for (const n of Object.keys(T)) {
      const t = T[n];
      await p.frame(t.at + Math.min(t.dur * 0.6, t.dur - 0.2), `renders/sb${String(n).padStart(2, '0')}.png`);
    }
  } else if (RENDER_MODE === 'draft') {
    await p.render('renders/draft.mp4', { draft: true });
  } else {
    await p.render('renders/is-oto-overview.mp4', { bitrate: 12000000, concurrency: 8 });
  }
};
'''

asset_adds = "\n".join(f"  A['{asset_keys[n]}'] = await p.add('media/{n}');" for n in media_names)
out = (JSX.replace("__TIMING__", json.dumps({n: {"at": s["at"], "dur": s["dur"]} for n, s in T.items()}))
          .replace("__TOTAL__", str(timing["total"]))
          .replace("__MAP__", json.dumps({k: MAP[k] for k in ("w", "h", "oblasts", "cities", "lakes")}, ensure_ascii=False))
          .replace("__SIZES__", json.dumps({k: v for k, v in SIZES.items()}))
          .replace("__FONT_MODE__", font_mode)
          .replace("__WORD_MOTION__", "true" if word_motion else "false")
          .replace("__RENDER_MODE__", mode)
          .replace("__SANS__", sans_family).replace("__SERIF__", serif_family)
          .replace("__ASSET_ADDS__", asset_adds))
os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
open(os.path.join(ROOT, "build", "edit.jsx"), "w", encoding="utf-8").write(out)

fetch = ["#!/bin/bash", "set -e", "mkdir -p media fonts-src"]
for n, url in ASSETS.items():
    fetch.append(f"curl -sS -f -m 240 -o 'media/{n}' '{url}'")
fetch += [
    "curl -sS -f -L -m 120 -o fonts-src/Spectral-Regular.ttf https://raw.githubusercontent.com/google/fonts/main/ofl/spectral/Spectral-Regular.ttf",
    "curl -sS -f -L -m 120 -o fonts-src/Spectral-Medium.ttf https://raw.githubusercontent.com/google/fonts/main/ofl/spectral/Spectral-Medium.ttf",
    "curl -sS -f -L -m 120 -o 'fonts-src/Manrope[wght].ttf' 'https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/Manrope%5Bwght%5D.ttf'",
    "ls -la media fonts-src | head -80",
]
open(os.path.join(ROOT, "build", "fetch.sh"), "w").write("\n".join(fetch) + "\n")
print("wrote build/edit.jsx", len(out), "bytes; assets", len(ASSETS), "; mode", mode, "; fonts", font_mode)
