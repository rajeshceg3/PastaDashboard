# Pasta Paradise

A small Streamlit collection of ten pasta shapes. Browse by family, search names/descriptions, sort the collection, compare common uses in the cards and see representative places on a local map. Each card lists classic dishes for the shape and links one external recipe from a named kitchen.

## Run

Python3.10+ is the executed baseline. From the repository root:

```sh
python -m venv .venv
.venv/bin/pip install -r .cursor/skills/verify-pasta/requirements.txt
.venv/bin/streamlit run pasta_dashboard.py
```

The app reads local JSON, original SVG shape studies and public-domain NaturalEarth geometry. No account, map token or remote photograph is needed for these views. See [asset sources](static/ASSET_SOURCES.md).

## What the collection means

The drawings are schematic shape studies, not photographs. Places and coordinates are inherited catalog associations, not verified birthplaces. Several entries share a representative Rome coordinate and are grouped under one numbered map marker with a name key and table. Culinary traditions can span regions.

Nutrition is general guidance, not dietary advice. Numeric serving claims in the inherited source JSON have not been independently checked and are not shown as measured values. Original data and external photo URLs remain preserved for later review, but remote photos are no longer loaded by the catalog.

## Classic dishes, recipes and content sources

Each card's classic dishes come from the shape's documented culinary tradition; the recipe link on each card opens an external kitchen's recipe (La Cucina Italiana, Great Italian Chefs, Saveur, GialloZafferano, Bologna Welcome, BBC Food, Recipes from Italy, Lidia's Italy, Food Network). Links were opened and title-checked on 2026-11-05. Content sources for shapes, name meanings and places are listed in [asset sources](static/ASSET_SOURCES.md).

## Verification and remaining work

Follow [.cursor/skills/verify-pasta/SKILL.md](.cursor/skills/verify-pasta/SKILL.md) for actual mobile/desktop browser filtering, sorting, search, no-match recovery, nutrition, local-media and numbered-map checks. Inspect pixels after changes.

This is a catalog repair and design foundation, not a finished cooking guide or a claim of full design acceptance. Stronger comparison and geography teaching, sourced nutrition review, full keyboard/screen-reader testing, device testing and hosted acceptance remain unfinished. No accounts/favorites or persistent user storage are provided.
