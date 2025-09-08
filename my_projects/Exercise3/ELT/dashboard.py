# ELT/dashboard.py
import base64
from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import dcc, Dash, Output, Input
from dash.html import H1, H2, H3, P
from dash_bootstrap_components import Row, Col, Card, CardImg, Container, themes

from setup import paths_directory

# --- Ladda data robust ---
csv_path = paths_directory["data_warehouse"] / "users.csv"
avatars_dir = paths_directory["avatars"]

# Läs CSV (eller skapa tom df första gången)
if csv_path.exists():
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=["id", "name", "date_of_birth", "city", "latitude", "longitude"])

# Sätt id som index om kolumnen finns
if "id" in df.columns:
    df = df.set_index("id")

# Skapa image-kolumn per rad, kopplat till id
def id_to_avatar_path(uid: int):
    p = avatars_dir / f"{uid}.png"
    return p.as_posix() if p.exists() else None

if not df.empty:
    df["image"] = [id_to_avatar_path(i) for i in df.index]
else:
    df["image"] = []  # tom lista om ingen data än

# --- Kartkomponent ---
def user_map():
    if df.empty:
        fig = px.scatter_mapbox(lat=[], lon=[], hover_name=[], zoom=2)
        fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    # reset_index så att id finns som kolumn för hover om du vill använda den
    fig = px.scatter_mapbox(
        data_frame=df.reset_index(),
        lat="latitude",
        lon="longitude",
        hover_name="name",
        zoom=2,
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox=dict(center=dict(lat=40.7749, lon=-96.4194)),
    )
    return fig

# --- Bild → base64 (för att kunna bädda in lokalt) ---
def image_to_base64(image_path: str | None):
    if not image_path or not Path(image_path).exists():
        return None
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Dropdown-data
if df.empty:
    user_options = []
    id_list = []
    placeholder_text = "No users yet"
else:
    name_list = df["name"].fillna("").astype(str).tolist()
    id_list = df.index.tolist()
    user_options = [{"label": name, "value": _id} for name, _id in zip(name_list, id_list)]
    placeholder_text = name_list[0] if name_list else "Select user"

app = Dash(__name__, external_stylesheets=[themes.FLATLY])

app.layout = Container(
    [
        Row(H1("Tracking users", className="text-primary text-center p-3")),
        Row(
            [
                Col([H2("Map"), dcc.Graph(id="user-map", figure=user_map())], width=8),
                Col(
                    [
                        H2("User data", id="card-header"),
                        Card(id="user-card"),
                        dcc.Dropdown(
                            id="users-dropdown",
                            options=user_options,
                            value=(id_list[0] if id_list else None),
                            className="mt-4",
                            placeholder=placeholder_text,
                        ),
                    ],
                    className="mx-5",
                ),
            ]
        ),
    ],
    fluid=False,
)

@app.callback(Output("user-card", "children"), Input("users-dropdown", "value"))
def user_card(user_id):
    if user_id is None or df.empty or user_id not in df.index:
        return Row([Col(P("No user selected yet."))])

    img_path = id_to_avatar_path(user_id)
    img64 = image_to_base64(img_path)

    user = df.loc[user_id]
    return Row(
        [
            Col(CardImg(src=(f"data:image/png;base64,{img64}" if img64 else None)), className="col-md-4"),
            Col(
                [
                    H3(f"{user.get('name','')}", className="mt-2"),
                    P(f"{user.get('date_of_birth','')}", className="card-info"),
                    P(f"{user.get('city','')}", className="card-info"),
                ]
            ),
        ]
    )

if __name__ == "__main__":
    # Viktigt i container: exponera på alla interfaces
    app.run_server(host="0.0.0.0", debug=True, port=8050)