import polars as pl
from polars_cisco_umrella import umbrella_lokup


df = pl.DataFrame(
    {
        "dns": ["github.com", "google.de", "blub.com", "heise.de"],
    }
)

result = df.with_columns(is_in_cisco_umbrella=umbrella_lokup("dns"))
print(result)
