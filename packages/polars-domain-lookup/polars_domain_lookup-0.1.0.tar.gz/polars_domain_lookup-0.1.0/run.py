import polars as pl
from polars_domain_lookup import is_common_domain


df = pl.DataFrame(
    {
        "domain": ["github.com", "google.de", "blub.com", "heise.de"],
    }
)

result = df.with_columns(is_common_domain=is_common_domain("domain"))
print(result)
