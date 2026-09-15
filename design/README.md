# Profile artwork

The unfinished-margin masthead pairs an offset second line with a copper final word crossing an interrupted rule. A smaller broken rule repeats the idea below the body copy. Light and dark variants use the same geometry.

The display lettering is outlined Instrument Serif. The SVGs are self-contained: displaying the profile needs no installed fonts, scripts or external image service. The name and body remain native Markdown text.

## Regenerate

From the repository root, using Python 3:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r design/requirements.txt
.venv/bin/python design/build_assets.py
```

Edit the text, coordinates or palettes in `build_assets.py`; the script writes the four SVGs to `assets/`. Keep the filenames in sync with the picture elements in the main README.

## Typeface

Instrument Serif, regular and italic, by Rodrigo Fuenzalida and Jordan Egstad. Copyright 2022 The Instrument Serif Project Authors. Original font files are included in `fonts/` with the SIL Open Font License.

[Typeface source](https://github.com/Instrument/instrument-serif) · [Google Fonts distribution](https://github.com/google/fonts/tree/main/ofl/instrumentserif)
