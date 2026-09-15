#!/usr/bin/env python3
"""Render the first sheet(s) of an XLSX export as an Excel-looking HTML page (column letters, row numbers,
gridlines, sheet tabs), so the video can show a real export instead of a mock.
Usage: python3 pipeline/render_xlsx.py in.xlsx out.html [max_rows] [max_cols]
"""
import sys, html, datetime
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
src, out = sys.argv[1], sys.argv[2]
max_rows = int(sys.argv[3]) if len(sys.argv) > 3 else 28
max_cols = int(sys.argv[4]) if len(sys.argv) > 4 else 12
wb = load_workbook(src, data_only=True)
ws = wb.worksheets[0]
def fmt(v):
    if v is None: return ""
    if isinstance(v, bool): return "ИСТИНА" if v else "ЛОЖЬ"
    if isinstance(v, int): return f"{v:,}".replace(",", " ")
    if isinstance(v, float):
        return (f"{v:,.1f}" if abs(v - round(v)) > 1e-9 else f"{int(round(v)):,}").replace(",", " ").replace(".", ",")
    if isinstance(v, (datetime.date, datetime.datetime)): return v.strftime("%d.%m.%Y")
    return str(v)
rows = list(ws.iter_rows(min_row=1, max_row=min(ws.max_row, max_rows), max_col=min(ws.max_column, max_cols)))
widths = []
for c in range(1, min(ws.max_column, max_cols) + 1):
    w = ws.column_dimensions[get_column_letter(c)].width or 10
    widths.append(max(56, min(360, int(w * 7.2))))
head_rows = 1
for i, r in enumerate(rows[:6]):
    if any(c.font and c.font.bold for c in r): head_rows = i + 1
cells = []
for ri, r in enumerate(rows):
    tds = []
    for ci, c in enumerate(r):
        v = fmt(c.value); num = isinstance(c.value, (int, float)) and not isinstance(c.value, bool)
        bold = bool(c.font and c.font.bold)
        fill = ""
        if c.fill is not None and c.fill.fgColor is not None and c.fill.fill_type == "solid":
            rgb = c.fill.fgColor.rgb
            if isinstance(rgb, str) and len(rgb) == 8 and rgb != "00000000": fill = f"background:#{rgb[2:]};"
        style = ("text-align:right;" if num else "") + ("font-weight:600;" if bold else "") + fill
        tds.append(f'<td style="{style}" title="{html.escape(v)}">{html.escape(v)}</td>')
    cells.append(f'<tr><th class="rn">{ri+1}</th>{"".join(tds)}</tr>')
colhead = "".join(f'<th style="width:{w}px">{get_column_letter(i+1)}</th>' for i, w in enumerate(widths))
tabs = "".join(f'<span class="tab{" active" if i == 0 else ""}">{html.escape(s.title)}</span>' for i, s in enumerate(wb.worksheets))
page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#fff;font-family:"Segoe UI",Arial,"Liberation Sans",sans-serif;font-size:13px;color:#1f1f1f}}
.ribbon{{height:58px;background:#217346;color:#fff;display:flex;align-items:center;padding:0 18px;font-size:14px;gap:22px}}
.ribbon b{{font-size:15px;font-weight:600}} .ribbon span{{opacity:.9}}
.bar{{height:34px;border-bottom:1px solid #d9d9d9;display:flex;align-items:center;gap:10px;padding:0 10px;color:#444;background:#f3f3f3}}
.bar .nb{{width:80px;height:22px;border:1px solid #c8c8c8;background:#fff;padding:0 6px;line-height:22px}} .bar .fx{{flex:1;height:22px;border:1px solid #c8c8c8;background:#fff;padding:0 6px;line-height:22px}}
table{{border-collapse:collapse;table-layout:fixed}} th,td{{border:1px solid #e1e1e1;padding:3px 6px;height:22px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:13px}}
th{{background:#f0f0f0;color:#444;font-weight:500;text-align:center}} th.rn{{width:38px}} td{{background:#fff}}
tr.h td{{font-weight:600;background:#f7f7f7}} .tabs{{position:fixed;bottom:0;left:0;right:0;height:30px;background:#f3f3f3;border-top:1px solid #d9d9d9;display:flex;align-items:center;gap:0;padding-left:40px}}
.tab{{padding:5px 16px;border-right:1px solid #d9d9d9;color:#444}} .tab.active{{background:#fff;color:#217346;font-weight:600;border-bottom:2px solid #217346}}
</style></head><body>
<div class="ribbon"><b>{html.escape(src.split('/')[-1])}</b><span>Главная</span><span>Вставка</span><span>Формулы</span><span>Данные</span><span>Вид</span></div>
<div class="bar"><div class="nb">A1</div><span>fx</span><div class="fx">{html.escape(fmt(rows[0][0].value) if rows and rows[0] else "")}</div></div>
<table><tr><th class="rn"></th>{colhead}</tr>{"".join(cells)}</table>
<div class="tabs">{tabs}</div></body></html>"""
open(out, "w", encoding="utf-8").write(page)
print("wrote", out, "rows", len(rows), "cols", len(widths), "sheets", [s.title for s in wb.worksheets])
