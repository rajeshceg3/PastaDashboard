# Catalog, filters and search
## Sub-features
Ten pasta entries, type filtering, ascending/descending sort, case-insensitive name/description search and empty results.
## How to get to it (user POV)
Open dashboard, use sidebar Select Pasta Type and Sort Pasta By. Mobile sidebar overlays content; close it to reach main search field. Enter search and press Enter.
## Driving it with drive.mjs
Drive both390/1365. Long filter must contain Spaghetti/Fettuccine/Bucatini. Assert exact ascending/descending order, Ravioli search match, empty search warning and restoration to10entries.
## Gotchas
Original reusable two-column containers grouped odd/even entries in mobile reading order, so sorted data was visually interleaved. New row-specific columns preserve actual row/mobile order. Harness no longer mistakes column DOM order for sorted data. Original appearance has empty decorative card divs because Streamlit markdown cannot wrap later widgets; no full design acceptance claim.
