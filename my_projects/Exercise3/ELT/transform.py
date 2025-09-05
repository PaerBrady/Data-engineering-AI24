# transform.py
# %%
import json
import pandas as pd


class _DatalakeProvider:
    """Provides raw data in an easy interface"""
    def __init__(self, users_directory) -> None:
        self.all_users = []
        # läs endast .json-filer och ignorera annat
        for filepath in users_directory.glob("*.json"):
            with open(filepath, 'r') as file:
                user_data = json.load(file)
            self.all_users.append(user_data)

    @property
    def raw_df(self):
        # Om tom datalake, returnera tom DF med förväntade nycklar (så resten inte krashar)
        if not self.all_users:
            return pd.DataFrame([])
        return pd.DataFrame(self.all_users)


#%%
class Transforms:
    """Different transforms for different downstream use cases"""
    def __init__(self, users_directory):
        raw_df = _DatalakeProvider(users_directory).raw_df

        if raw_df.empty:
            # tomt → tom bas-DF med rätt kolumnuppsättning
            self.base_df = pd.DataFrame(
                columns=["id", "first_name", "last_name", "email",
                         "phone_number", "date_of_birth", "avatar", "address"]
            )
        else:
            required_min = {"id", "first_name", "last_name", "email",
                            "date_of_birth", "avatar", "address"}
            missing = required_min - set(raw_df.columns)
            if missing:
                raise ValueError(f"Saknade nycklar i rådata: {sorted(missing)}")

            # Behåll bara kolumner som finns (username är frivillig)
            preferred_order = ["id", "first_name", "last_name", "username", "email",
                               "phone_number", "date_of_birth", "avatar", "address"]
            columns_keep = [c for c in preferred_order if c in raw_df.columns]
            df = raw_df[columns_keep].copy()

            # Om username saknas: härled från email (delen före @)
            if "username" not in df.columns and "email" in df.columns:
                df["username"] = df["email"].str.split("@").str[0]

            self.base_df = df

    @property
    def map_dashboard_df(self):
        # Bygg dashboard-tabell: id, name, date_of_birth, city, lat, lng
        df = self.base_df[["id", "first_name", "last_name", "date_of_birth"]].copy()

        # address är ett nästat fält → plocka city och coordinates
        cities = self.base_df["address"].apply(lambda row: row.get("city") if isinstance(row, dict) else None)
        coordinates = self.base_df["address"].apply(lambda row: row.get("coordinates") if isinstance(row, dict) else None)

        longitudes = coordinates.apply(lambda row: row.get("lng") if isinstance(row, dict) else None)
        latitudes  = coordinates.apply(lambda row: row.get("lat") if isinstance(row, dict) else None)

        df.insert(loc=df.shape[1], column="city", value=cities)
        df.insert(loc=df.shape[1], column="latitude", value=latitudes)
        df.insert(loc=df.shape[1], column="longitude", value=longitudes)

        full_name = df["first_name"] + " " + df["last_name"]
        df.insert(2, "name", full_name)
        df = df.drop(columns=["first_name", "last_name"])

        return df

    def avatar_df(self):
        return self.base_df[["id", "avatar"]]