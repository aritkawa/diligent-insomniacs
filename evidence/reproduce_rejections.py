# -*- coding: utf-8 -*-
"""
VizCon 2026 "The World's Most Diligent Insomniacs"
GenAI Usage Document evidence: reproduces the theme-validation scatterplots (rejected / adopted).

The original validation was done in dialogue sessions with Aki (the AI) on 2026-07-08..09 and 07-12.
This script reproduces the same conclusions from the same raw data (under C:/Viz).
Run: python reproduce_rejections.py (using the python in streamlit_app/.venv)
Output: 4 evidence/fig_*.png files + the correlation values printed to the console.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["figure.dpi"] = 150

BASE = "C:/Viz"
OUT = os.path.dirname(os.path.abspath(__file__))  # write figures next to this script

INK = "#1b2440"; AMBER = "#c8922a"; RED = "#c0392b"; GREY = "#8a90a2"

def style(ax, title, sub):
    ax.set_title(title, fontsize=12, fontweight="bold", color=INK, loc="left", pad=42)
    ax.text(0, 1.025, sub, transform=ax.transAxes, fontsize=8.5, color=GREY, va="bottom")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.grid(alpha=0.25, linewidth=0.5)

def corr(a, b):
    m = a.notna() & b.notna()
    return float(np.corrcoef(a[m], b[m])[0, 1]), int(m.sum())

# ---------------------------------------------------------------
# Figure 1 [REJECTED] Income x Happiness -- correlation too strong, no Discovery
# ---------------------------------------------------------------
gdp = pd.read_csv(f"{BASE}/02_money_happiness/gdp_per_capita_worldbank.csv")
hap = pd.read_csv(f"{BASE}/02_money_happiness/happiness_cantril_ladder.csv")
gdp.columns = ["Entity", "Code", "Year", "gdp", "region"]
hap.columns = ["Entity", "Code", "Year", "life_sat"]
yr = int(min(gdp.Year.max(), hap.Year.max()))
m1 = pd.merge(gdp[gdp.Year == yr], hap[hap.Year == yr], on=["Entity", "Code"])
m1 = m1[m1.Code.notna() & (m1.Code != "OWID_WRL")]
m1["log_gdp"] = np.log10(m1.gdp)
r1, n1 = corr(m1.log_gdp, m1.life_sat)

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(m1.gdp, m1.life_sat, s=18, color=INK, alpha=0.55)
jp = m1[m1.Code == "JPN"]
if len(jp):
    ax.scatter(jp.gdp, jp.life_sat, s=60, color=RED, zorder=5)
    ax.annotate("Japan", (jp.gdp.iloc[0], jp.life_sat.iloc[0]),
                xytext=(8, -16), textcoords="offset points", color=RED, fontsize=9)
ax.set_xscale("log")
ax.set_xlabel("GDP per capita (log, int-$)", fontsize=9)
ax.set_ylabel("Life satisfaction (Cantril ladder)", fontsize=9)
style(ax, f"[REJECTED] Income x Happiness   r = {r1:.3f} (log income, N={n1}, yr {yr})",
      "Correlation too strong = no one is surprised. No ceiling (saturation) shows either;\nno Discovery, so the theme was rejected (2026-07-08)")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_rejected_01_money_happiness.png"); plt.close(fig)
print(f"[1] income x happiness: r={r1:.3f} N={n1} ({yr})")

# ---------------------------------------------------------------
# Figure 2 [REJECTED] Marriage x Fertility -- ~zero correlation worldwide, holds only conditionally
# ---------------------------------------------------------------
bom = pd.read_csv(f"{BASE}/03_marriage_fertility/births_outside_marriage.csv")
tfr = pd.read_csv(f"{BASE}/03_marriage_fertility/total_fertility_rate.csv")
bom.columns = ["Entity", "Code", "Year", "bom"]
tfr.columns = ["Entity", "Code", "Year", "tfr"]
# join each country's latest-year births-outside-marriage with the same-year TFR
bom_latest = bom.sort_values("Year").groupby("Code", as_index=False).last()
m2 = pd.merge(bom_latest, tfr, on=["Code", "Year"], suffixes=("", "_t"))
m2 = m2[m2.Code.str.len() == 3]
r2_all, n2_all = corr(m2.bom, m2.tfr)
# Europe + East Asia subset (same intent as the original validation: exclude regions with
# different birth-registration cultures).
# Note: the details of the country list and year-matching differ from the original spike
#   values (worldwide 0.029 / subset 0.574, 41/32 countries), so the numbers don't match
#   exactly -- but the rejection rationale ("it vanishes worldwide and only a moderate
#   correlation surfaces on a subset = it holds only conditionally") has the same structure.
EU_EA = {"AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU",
         "GRC", "HUN", "ISL", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "NOR",
         "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE", "CHE", "GBR", "TUR",
         "JPN", "KOR"}
m2e = m2[m2.Code.isin(EU_EA)]
r2_sub, n2_sub = corr(m2e.bom, m2e.tfr)

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(m2.bom, m2.tfr, s=18, color=GREY, alpha=0.5, label=f"Worldwide r={r2_all:.3f} (N={n2_all})")
ax.scatter(m2e.bom, m2e.tfr, s=22, color=INK, alpha=0.75, label=f"Europe + East Asia r={r2_sub:.3f} (N={n2_sub})")
for code, name in [("JPN", "Japan"), ("KOR", "South Korea"), ("FRA", "France")]:
    row = m2[m2.Code == code]
    if len(row):
        ax.scatter(row.bom, row.tfr, s=60, color=RED, zorder=5)
        ax.annotate(name, (row.bom.iloc[0], row.tfr.iloc[0]),
                    xytext=(6, 6), textcoords="offset points", color=RED, fontsize=9)
ax.set_xlabel("Births outside marriage (%)", fontsize=9)
ax.set_ylabel("Total fertility rate (TFR)", fontsize=9)
ax.legend(fontsize=8, frameon=False)
style(ax, "[REJECTED] Marriage x Fertility -- the correlation vanishes worldwide",
      "A conditional correlation that can be told only on a subset\n+ three minefields (COVID-year exaggeration / birth-registration culture / over-familiarity) -> rejected (2026-07-09)")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_rejected_02_marriage_fertility.png"); plt.close(fig)
print(f"[2] marriage x fertility: worldwide r={r2_all:.3f} N={n2_all} / subset r={r2_sub:.3f} N={n2_sub}")

# ---------------------------------------------------------------
# Figure 3 [REJECTED] Happiness x unpaid-work gender gap -- an expansion that decayed on re-spike
# ---------------------------------------------------------------
summ = pd.read_csv(f"{BASE}/01_sleep_work/QS_ready/qs_country_summary.csv", encoding="utf-8-sig")
summ["yr"] = summ["survey_year"].astype(str).str.extract(r"(\d{4})").astype(float)
def match_hap(country, yr_):
    sub = hap[hap.Entity == country]
    if sub.empty:
        sub = hap[hap.Entity == {"Korea": "South Korea"}.get(country, "")]
    if sub.empty or pd.isna(yr_):
        return np.nan
    return sub.loc[(sub.Year - yr_).abs().idxmin(), "life_sat"]
summ["life_sat"] = [match_hap(c, y) for c, y in zip(summ.country, summ.yr)]
r3, n3 = corr(summ.life_sat, summ.unpaid_gap_women_minus_men)

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(summ.unpaid_gap_women_minus_men, summ.life_sat, s=26, color=INK, alpha=0.7)
jp = summ[summ.is_japan == 1]
ax.scatter(jp.unpaid_gap_women_minus_men, jp.life_sat, s=70, color=RED, zorder=5)
ax.annotate("Japan", (jp.unpaid_gap_women_minus_men.iloc[0], jp.life_sat.iloc[0]),
            xytext=(8, -4), textcoords="offset points", color=RED, fontsize=9)
ax.set_xlabel("Unpaid-work gap (women - men, min/day)", fontsize=9)
ax.set_ylabel("Life satisfaction (Cantril ladder)", fontsize=9)
style(ax, f"[REJECTED] Happiness x unpaid-work gap   r = {r3:.3f} (N={n3})",
      "Initial spike r=-0.74 -> decayed on a re-spike with strict survey-year matching\n-> too weak as an act, not adopted (2026-07-16)")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_rejected_03_happiness_unpaidgap.png"); plt.close(fig)
print(f"[3] happiness x unpaid gap: r={r3:.3f} N={n3}")

# ---------------------------------------------------------------
# Figure 4 [ADOPTED] the "twist" of work rank x sleep rank -- the pillar of the piece
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(summ.pure_work_min, summ.sleep_min, s=26, color=INK, alpha=0.7)
r4, n4 = corr(summ.pure_work_min, summ.sleep_min)
jp = summ[summ.is_japan == 1]
ax.scatter(jp.pure_work_min, jp.sleep_min, s=90, color=RED, zorder=5)
ax.annotate("Japan\nwork #1, sleep #33", (jp.pure_work_min.iloc[0], jp.sleep_min.iloc[0]),
            xytext=(-150, 6), textcoords="offset points", color=RED, fontsize=9, fontweight="bold")
ax.set_xlabel("Pure work time (min/day)", fontsize=9)
ax.set_ylabel("Sleep time (min/day)", fontsize=9)
style(ax, f"[ADOPTED] Work x Sleep   r = {r4:.3f} (OECD TUS, 33 countries)",
      "Japan as the outlier = 'works the most, sleeps the least in the world'.\nUnlike the 2 rejected themes, a single anomaly becomes a story -> adopted (2026-07-09)")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_adopted_04_work_sleep.png"); plt.close(fig)
print(f"[4] work x sleep (adopted): r={r4:.3f} N={n4} / Japan work={jp.pure_work_min.iloc[0]} sleep={jp.sleep_min.iloc[0]}")
print("done ->", OUT)
