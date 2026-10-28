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

### [Harry Kane — Goal-Mouth Placement](kane-goal-mouth/) · 28 Oct 2026

![Harry Kane goal-mouth placement](kane-goal-mouth/figures/kane_goal_map.png)

Where Kane's **74 goals** from his 2025/26 campaign actually crossed the line:
a regulation 7.32 × 2.44 m goal frame, a 3 × 6 grid shaded by share of goals
with the percentage and the raw count in each cell, a body-part breakdown
(**50** right foot · **14** headers · **10** left foot) and the penalty /
non-penalty split. Bottom corners dominate — 16.2 % bottom-left, 17.6 %
bottom-right — and the middle of the goal is nearly empty.

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
├── kane-goal-mouth/
│   ├── goals.csv                  # one row per goal (Opta event data)
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
