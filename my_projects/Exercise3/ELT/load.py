import time, requests
import pandas as pd
from setup import paths_directory

class Load:
    def __init__(self, data_warehouse_path) -> None:
        self.avatar_path = data_warehouse_path / "avatars"
        self.data_warehouse_path = data_warehouse_path

    def load_avatars(self, urls, ids):
        
        for avatar_url, id in zip(urls, ids):
            response = requests.get(avatar_url)

            with open(self.avatar_path / f"{id}.png" , "wb") as file:
                file.write(response.content)

            time.sleep(2)
    
    def load_csv_dashboard(self, df):
        out_path = self.data_warehouse_path / "users.csv"
        # Idempotent merge + dedup
        if out_path.exists():
            old = pd.read_csv(out_path)
            combined = pd.concat([old, df], ignore_index=True)
            combined = combined.drop_duplicates(subset=["id"]).sort_values("id")
        else:
            combined = df.sort_values("id")
        combined.to_csv(out_path, index=False)  # <-- viktiga biten: index=False