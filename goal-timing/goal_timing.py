# %% [markdown]
# # What Time Are Goals Scored?
#
# One horizontal bar chart per league: goals binned into 15-minute windows,
# with a hatched **1st Half** / **2nd Half** total row after each half, the raw
# count on every bar and its share of all league goals set smaller beside it.
#
# Binning rules: `0–15` opens the first half; anything **over 45 in the first
# half is first-half stoppage** (`45+`); the second half opens at `46–60` (a
# second-half goal clocked at 45 is ranked into that window); anything **over
# 90 in the second half is second-half stoppage** (`90+`).
#
# Clock: WhoScored floors its raw `minute` (a goal at 30:32 is stored as 30),
# so the Top 5 Leagues builder reports the displayed clock — 30:32 becomes 31'
# and stoppage goals become 45+N / 90+N, verified against FotMob on all 1,121
# comparable goals with zero disagreements. Data source: **WhoScored**.
#
# Bars use each league's official brand colour. Data: `goal_times.csv` (one row
# per goal, 2026/27 league matches only). Fonts: DM Sans + Karla in `fonts/`.
# League badges in `logos/`.

# %%
from pathlib import Path
import collections
import csv
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import font_manager as fm

try:
    HERE = Path(__file__).resolve().parent
except NameError:                      # running as a notebook
    HERE = Path.cwd()

DPI = 800                              # repo convention: every figure is 800 dpi
FIG_W, FIG_H = 13.0, 9.0

# --- fonts ship with the repo, so the render is identical anywhere ---------
DISPLAY = fm.FontProperties(fname=HERE / "fonts" / "DMSans-Bold.ttf")
DISPLAY_MED = fm.FontProperties(fname=HERE / "fonts" / "DMSans-Medium.ttf")
BODY = fm.FontProperties(fname=HERE / "fonts" / "Karla-Regular.ttf")
BODY_MED = fm.FontProperties(fname=HERE / "fonts" / "Karla-Medium.ttf")

# --- palette (same canvas as the Kane goal-mouth map) ----------------------
BG = "#F1F0EE"
INK = "#2E2E2E"
INK_SOFT = "#6A6A6A"
SUB = "#4E616C"                        # soc-viz subtitle colour
TOT_FC = "#E6E3DF"                     # hatched half-total bars
# bar colour comes from league_meta.csv -> bar_color (official league brand)

# --- league display strings + counts live in league_meta.csv -------------
LEAGUE_ORDER = ["ENG_1_premier-league", "ESP_1_la-liga", "ITA_1_serie-a",
                "GER_1_bundesliga", "FRA_1_ligue-1"]

FIRST_HALF = ["0-15", "16-30", "31-45", "45+"]
SECOND_HALF = ["46-60", "61-75", "76-90", "90+"]
# the 15-minute windows use an en dash on the figure
PRETTY = {"0-15": "0\u201315", "16-30": "16\u201330", "31-45": "31\u201345",
          "45+": "45+", "46-60": "46\u201360", "61-75": "61\u201375",
          "76-90": "76\u201390", "90+": "90+"}

# %%
def load_goals():
    """goal_times.csv grouped by league folder."""
    with open(HERE / "goal_times.csv", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    by_league = collections.defaultdict(list)
    for r in rows:
        by_league[r["league"]].append(r)
    return by_league


def load_meta():
    """league_meta.csv: display strings, GW span, matches played, goals."""
    with open(HERE / "league_meta.csv", encoding="utf-8") as fh:
        return {r["league"]: r for r in csv.DictReader(fh)}


def half_counts(rows):
    """(ordered rows of the chart, league total)."""
    n = collections.Counter(r["time_bin"] for r in rows)
    fh_total = sum(n[b] for b in FIRST_HALF)
    sh_total = sum(n[b] for b in SECOND_HALF)
    ordered = [(b, n[b], False) for b in FIRST_HALF]
    ordered.append(("1st Half", fh_total, True))
    ordered += [(b, n[b], False) for b in SECOND_HALF]
    ordered.append(("2nd Half", sh_total, True))
    return ordered, len(rows)

# %%
def render(meta, rows, out_png):
    short_name = meta["league_name"]
    accent = meta["bar_color"]                   # official league brand colour
    ordered, total = half_counts(rows)

    gws = sorted({int(r["gw"]) for r in rows})
    gw_span = f"GW {gws[0]}\u2013{gws[-1]}" if len(gws) > 1 else f"GW {gws[0]}"
    matches_played = meta["matches_played"]

    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=BG)

    # ---- header: league badge snug against the left of the title ----------
    logo = mpimg.imread(HERE / "logos" / meta["logo"])
    logo_w = 0.060                                   # fraction of figure width
    logo_h = logo_w * FIG_W / FIG_H                  # keep it square in inches
    logo_y = 0.905 - logo_h / 2                      # centred on the title line
    ax_logo = fig.add_axes([0.06, logo_y, logo_w, logo_h])
    ax_logo.imshow(logo)
    ax_logo.axis("off")

    fig.text(0.06 + logo_w + 0.022, 0.917, "What Time Are Goals Scored?",
             fontproperties=DISPLAY, fontsize=31, color=INK, va="center")
    fig.text(0.06 + logo_w + 0.022, 0.861,
             f"Time when goals are scored in {meta['sub_name']}  |  {gw_span}"
             "  |  Viz by @Oladeeayo",
             fontproperties=BODY, fontsize=15.5, color=SUB, va="center")

    # ---- bars -------------------------------------------------------------
    ax = fig.add_axes([0.185, 0.115, 0.775, 0.66])
    ax.set_facecolor("none")
    n_rows = len(ordered)
    xmax = max(v for _, v, _ in ordered) * 1.30      # room for count + percent

    for y, (label, value, is_total) in enumerate(ordered):
        if is_total:
            ax.barh(y, value, height=0.74, facecolor=TOT_FC, edgecolor=accent,
                    hatch="///", linewidth=1.6, zorder=3)
        else:
            ax.barh(y, value, height=0.66, facecolor=accent, edgecolor="none",
                    zorder=3)

    ax.set_xlim(0, xmax)
    ax.set_ylim(n_rows - 0.5, -0.5)                 # first row on top
    ax.set_xticks([])
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels([PRETTY.get(lbl, lbl.upper()) for lbl, _, _ in ordered])
    for tick, (label, _, is_total) in zip(ax.get_yticklabels(), ordered):
        if is_total:
            tick.set_fontproperties(DISPLAY)
            tick.set_fontsize(13)
            tick.set_color(accent)
        else:
            tick.set_fontproperties(BODY_MED)
            tick.set_fontsize(14.5)
            tick.set_color(INK)
    for side in ax.spines.values():
        side.set_visible(False)

    # ---- labels: count, then the share of all goals set smaller -----------
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    pad = xmax * 0.014                                # gap after the bar
    gap = xmax * 0.010                                # gap between count and %

    for y, (_, value, _) in enumerate(ordered):
        count_txt = ax.text(value + pad, y, str(value), ha="left", va="center",
                            fontproperties=DISPLAY, fontsize=17, color=INK,
                            zorder=4)
        bb = count_txt.get_window_extent(renderer=renderer)
        x_after = inv.transform((bb.x1, bb.y1))[0]
        pct = value / total * 100
        ax.text(x_after + gap, y, f"({pct:.1f}%)", ha="left", va="center",
                fontproperties=BODY, fontsize=13, color=INK_SOFT, zorder=4)

    # ---- credit + data note ------------------------------------------------
    fig.text(0.06, 0.048, "Viz by @Oladeeayo", fontproperties=DISPLAY_MED,
             fontsize=13.5, color=INK, va="center")
    fig.text(0.94, 0.048,
             f"2026/27 season, league matches only  |  {matches_played} matches  "
             f"|  {total} goals  |  Data Source: WhoScored",
             fontproperties=BODY, fontsize=11.5, color=INK_SOFT, va="center",
             ha="right")

    for attempt in range(4):           # retry: the PNG can be locked transiently
        try:                           # by an image viewer on Windows
            fig.savefig(out_png, facecolor=BG, dpi=DPI)
            break
        except OSError:
            if attempt == 3:
                raise
            time.sleep(0.7)
    plt.close(fig)
    return total

# %%
if __name__ == "__main__":
    by_league, meta = load_goals(), load_meta()
    out_dir = HERE / "figures"
    out_dir.mkdir(exist_ok=True)
    for key in LEAGUE_ORDER:
        rows = by_league[key]
        slug = meta[key]["league_name"].lower().replace(" ", "-")
        out = out_dir / f"goal_timing_{slug}.png"
        n = render(meta[key], rows, out)
        print(f"{meta[key]['league_name']:15s} {n:4d} goals -> {out.name}")
