# Profile artwork

The offset masthead pairs warm italic emphasis on “starts” and “ends” with three small, unequal strokes of light in the open margin. Whitespace separates the current-role note from the body. Light and dark variants use the same geometry.

The display lettering is outlined Instrument Serif. The SVGs are self-contained: displaying the profile needs no installed fonts, scripts or external image service. The name and body remain native Markdown text. The contact footer uses separate SVG labels inside ordinary links, with descriptive alt text and native keyboard focus. Email, LinkedIn and Piece use the same warm palette as the headline without overriding GitHub styles.

## Regenerate

From the repository root, using Python 3:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r design/requirements.txt
.venv/bin/python design/build_assets.py
```

Edit the text, coordinates or palettes in `build_assets.py`; the script writes the eight SVGs to `assets/`. Keep the filenames in sync with the picture elements in the main README.

## Typeface

Instrument Serif, regular and italic, by Rodrigo Fuenzalida and Jordan Egstad. Copyright 2022 The Instrument Serif Project Authors. Original font files are included in `fonts/` with the SIL Open Font License.

[Typeface source](https://github.com/Instrument/instrument-serif) · [Google Fonts distribution](https://github.com/google/fonts/tree/main/ofl/instrumentserif)
