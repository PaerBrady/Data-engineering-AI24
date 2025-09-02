#!/usr/bin/env python3
from pathlib import Path
import os, glob
from datetime import datetime

import pandas as pd
import streamlit as st

# ---- Paths ----
ROOT = Path(__file__).resolve().parent.parent  # .../Exercise2
OBS_DIR = ROOT / "pokedata" / "observations"

# ---- Page config ----
st.set_page_config(page_title="Pokémon Happiness Dashboard", layout="centered")
st.title("🧪 Pokémon Happiness Dashboard")
st.caption("Välj observation och jämför Pokémon efter 'happiness'.")

# ---- Auto-refresh (kompatibel) ----
# Använd st.autorefresh om den finns; annars visa en Refresh-knapp.
has_autorefresh = hasattr(st, "autorefresh")
rerun_fn = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)

if has_autorefresh:
    # Uppdatera var 5:e minut (300 000 ms)
    st.autorefresh(interval=5 * 60 * 1000, key="auto-refresh-5min")
else:
    with st.sidebar:
        st.info("Automatisk uppdatering saknas i din Streamlit-version.")
        if st.button("Refresh now"):
            if rerun_fn:
                rerun_fn()

# ---- Hitta observationsfiler ----
files = sorted(glob.glob(str(OBS_DIR / "observation_*.csv")))
if not files:
    st.error(f"Hittade inga observationsfiler i `{OBS_DIR}`.\n\nKör `scripts/transform_load.py` först.")
    st.stop()

def nice_label(p: str) -> str:
    name = os.path.basename(p).replace("observation_", "").replace(".csv", "")
    try:
        dt = datetime.strptime(name, "%y-%m-%d_%H_%M")
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return name

labels = [nice_label(p) for p in files]
options = ["Latest (auto)"] + labels
choice = st.sidebar.selectbox("Välj observation:", options, index=0)

if choice == "Latest (auto)":
    chosen_path = files[-1]
else:
    chosen_path = files[labels.index(choice)]

@st.cache_data(ttl=60)
def load_observation(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()
    df["pokemon"] = df["pokemon"].astype(str).str.strip()
    df["happiness"] = pd.to_numeric(df["happiness"], errors="coerce").fillna(0).astype(int)
    return df

df = load_observation(chosen_path)

# ---- Kontroller ----
with st.sidebar:
    st.markdown("### Visningsalternativ")
    sort_choice = st.selectbox("Sortera efter:", ["happiness (desc)", "happiness (asc)", "pokemon (A→Ö)"])
    top_n = st.slider("Visa topp N (0 = alla)", min_value=0, max_value=len(df), value=min(len(df), 10), step=1)

# Sortera
if sort_choice == "happiness (desc)":
    df_view = df.sort_values("happiness", ascending=False)
elif sort_choice == "happiness (asc)":
    df_view = df.sort_values("happiness", ascending=True)
else:
    df_view = df.sort_values("pokemon", ascending=True)

# Topp N
if top_n > 0:
    df_view = df_view.head(top_n)

# ---- Tabell + Diagram ----
st.subheader("Data")
st.dataframe(df_view, hide_index=True, width="stretch")  # ersätter use_container_width

st.subheader("Happiness per Pokémon")
st.bar_chart(df_view.set_index("pokemon")["happiness"])

st.caption(
    f"Vald fil: `{os.path.basename(chosen_path)}` • "
    f"Rader: {len(df_view)} • "
    f"Min: {int(df_view['happiness'].min())} • "
    f"Medel: {round(float(df_view['happiness'].mean()), 1)} • "
    f"Max: {int(df_view['happiness'].max())}"
)