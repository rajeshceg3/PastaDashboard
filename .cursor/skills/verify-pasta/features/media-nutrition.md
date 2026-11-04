# Nutrition and external media
## Sub-features
Nutrition expander, distribution chart, remote pasta pictures and origins map.
## How to get to it (user POV)
Open General Nutritional Insights below the map; pictures appear in catalog, chart is in sidebar.
## Driving it with drive.mjs
Drive expands nutrition and asserts visible content; captures pixels. External image loaded-state and map canvas sizes are diagnostic only. Blank map/failed images must stay separate open findings, not passed by canvas existence.
## Gotchas
Current environment all11remote images failed and Mapbox base map did not render, though points/canvases exist. No key creation/provider change is authorized by this skill. Source Mapbox style may need a valid token or reviewed free alternative; source URLs can also be stale. No invented nutritional/source accuracy certification or dietary advice. Chart emits an inherited use_container_width deprecation warning; no chart-design claim.
