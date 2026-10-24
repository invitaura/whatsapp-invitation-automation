import pandas as pd
import urllib.parse

df = pd.read_excel("C:\\CloudDevEnv\\AKHM\\2026\\Invitation\\Invitation.xlsx")

df["InviteLink"] = df["Name"].apply(
    lambda x: f"https://mukesh-weds-akhila.netlify.app?guest={urllib.parse.quote(x)}"
)

df.to_excel("guests_with_links.xlsx", index=False)