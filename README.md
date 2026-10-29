# Soc Viz

Football visualisations made with **matplotlib** in Python, by
[**@oladeeayo**](https://github.com/oladeeayo).

Every folder here is self-contained: the data it uses, the fonts it renders
with, the finished figure, and the notebook that produces it. Run the notebook,
get the image.

## Usage

```
pip install -r requirements.txt
jupyter notebook kane-goal-mouth/kane_goal_map.ipynb
```

Figures render at **800 dpi** into each folder's `figures/`. The fonts
(DM Sans and Karla, both SIL Open Font License) ship inside each folder, so
the output is identical on any machine.

## Visuals

### [What Time Are Goals Scored?](goal-timing/) · 29 Oct 2026

![Goal timing by league](goal-timing/figures/goal_timing_premier-league.png)

One image per league — Premier League, La Liga, Serie A, Bundesliga and
Ligue 1 — binning every 2026/27 league goal into **0–15 · 16–30 · 31–45 ·
45+** for the first half and **46–60 · 61–75 · 76–90 · 90+** for the second,
with a hatched **1st Half** / **2nd Half** total row closing each block. Every
bar carries the raw count and its share of all league goals, the percentage
set four points smaller than the number.

The binning rules are explicit: anything **over 45 in the first half is
first-half stoppage** (`45+`), anything **over 90 in the second half is
second-half stoppage** (`90+`), and a second-half goal clocked at 45 is ranked
into `46-60`. Bars are painted in each league's official brand colour, the
league badge sits beside the title, and the subtitle carries the GW span that
the data actually covers (GW 1–7 to 1–10 depending on the league).

**Clock correction.** Opta's raw `minute` is *whole elapsed minutes* — a
floor — so a goal at 30:32 was stored as 30 even though WhoScored and FotMob
both show **31'**. The Top 5 Leagues builder now reports the displayed clock
(`+1` once a second has ticked over, stoppage capped to `45+N` / `90+N`),
which was checked against FotMob's shotmap on **all 1,121 comparable goals
with zero disagreements**. Every figure and `goal_times.csv` were rebuilt
from the corrected data, so stoppage goals now read `90+1`, `90+6`, `90+9`.

[Run the notebook](goal-timing/goal_timing.ipynb) ·
Data source: **WhoScored** — 1,232 goals from 402 league matches

### [Harry Kane — Goal-Mouth Placement](kane-goal-mouth/) · 28 Oct 2026

![Harry Kane goal-mouth placement](kane-goal-mouth/figures/kane_goal_map.png)

Where Kane's **73 goals** from his 2025/26 campaign actually crossed the line:
a regulation 7.32 × 2.44 m goal frame, a 3 × 6 grid shaded by share of goals
with the percentage and the raw count in each cell, a body-part breakdown
(**49** right foot · **14** headers · **10** left foot) and the penalty /
non-penalty split. Bottom corners dominate — 16.4 % bottom-left, 17.8 %
bottom-right — and the middle of the goal is nearly empty.

**Why 73 and not 74.** The notebook used to plot every row that happened to
carry goal-mouth coordinates, with no season filter, and `goals.csv` tags one
row wrongly: the World Cup qualifier against Andorra (2025-06-07) sat in
`2025/26` even though it was played in June 2025, alongside the Senegal
friendly that was correctly tagged `2024/25`. Season tags follow an
August-start season, so that row now reads 2024/25, and the notebook filters
explicitly on `season == "2025/26"` rather than on who has coordinates. The
2026 World Cup, played June–July 2026 straight after the season ended, stays
inside 2025/26.

The interesting work is in the calibration: Opta's goal-mouth coordinates are
not in metres, so the frame is anchored with the community conversion
(posts at GoalMouthY 45.2 / 54.8, crossbar at GoalMouthZ = 38) and checked
against Opta's own `Low*` / `High*` qualifiers in the data.

[Run the notebook](kane-goal-mouth/kane_goal_map.ipynb) ·
data: WhoScored & Sofascore (Opta) event data

### [Ballon d'Or 2025/26 — Goal Contributions by Opponent Ranking](ballon-dor-contributions/) · 27 Oct 2026

![Goals contribution by opponents ranking](ballon-dor-contributions/figures/contribution_histograms.png)

Every goal and assist by the six Ballon d'Or candidates — Kane, Mbappé,
Yamal, Dembélé, Haaland, Olise — binned by how strong the opponent was: club
opponents by their global **Club Elo** rank position, countries by the current
**FIFA world ranking**. Headshot and name at the left of each row, counts on
the bars, no panel boxes and no gridlines.

![Contribution histograms split by club and country](ballon-dor-contributions/figures/contribution_histograms_by_type.png)

A stacked variant separates club (hatched) from country contributions.

[Run the notebook](ballon-dor-contributions/ballon_dor_contributions.ipynb) ·
data: Sofascore incidents, Club Elo, FIFA ranking (July 2026)

## Repo layout

```
soc-viz/
├── goal-timing/
│   ├── goal_times.csv          # one row per goal (1,232, displayed clock, +added_minute)
│   ├── league_meta.csv         # GW span, matches, goals, badge, brand colour
│   ├── fonts/                  # DM Sans + Karla (SIL OFL)
│   ├── logos/                  # the five league badges (FotMob)
│   ├── figures/                # one goal-timing chart per league
│   ├── goal_timing.ipynb
│   └── goal_timing.py          # same code, runnable as a script
├── kane-goal-mouth/
│   ├── goals.csv                  # 75 rows: 73 in 2025/26 + 2 June-2025 internationals
│   ├── fonts/                     # DM Sans + Karla (SIL OFL)
│   ├── figures/                   # kane_goal_map.png and .pdf
│   └── kane_goal_map.ipynb
└── ballon-dor-contributions/
    ├── goals_assists.csv          # every goal & assist, Aug 2025 – Jul 2026
    ├── club_ranks.csv             # Club Elo rank position per club opponent
    ├── players/                   # FotMob headshots
    ├── ballon_icon.png
    ├── fonts/
    ├── figures/                   # three contribution histograms
    └── ballon_dor_contributions.ipynb
```

## Credit

Viz by **[@oladeeayo](https://github.com/oladeeayo)**.
Fonts: [DM Sans](https://fonts.google.com/specimen/DM+Sans) and
[Karla](https://fonts.google.com/specimen/Karla), SIL Open Font License.
Player images: FotMob. Data: WhoScored, Sofascore, Club Elo and FIFA rankings.
League badges: FotMob; league brand colours follow each league's own identity.
