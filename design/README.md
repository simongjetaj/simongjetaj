# Profile artwork

The offset masthead pairs warm italic emphasis on “starts” and “ends” with three small, unequal strokes of light in the open margin. Whitespace sets the pace between the body and contact footer. Light and dark variants use the same geometry.

The display lettering is outlined Newsreader. The SVGs are self-contained: displaying the profile needs no installed fonts, scripts or external image service. The name and body remain native Markdown text. Email and LinkedIn use separate SVG labels inside ordinary links, with descriptive alt text and native keyboard focus. Their warm palette matches the headline without overriding GitHub styles.

## Regenerate

From the repository root, using Python 3:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r design/requirements.txt
.venv/bin/python design/build_assets.py
```

Edit the text, coordinates or palettes in `build_assets.py`; the script writes six SVGs to `assets/`. Keep the filenames in sync with the picture elements in the main README.

## Typeface

Newsreader, regular and italic, by Production Type. Copyright 2020 The Newsreader Project Authors. The original variable fonts are included in `fonts/` with the SIL Open Font License; their local filenames are simplified. The generator sets weight 400 and optical size 32 for the headline, with optical size 16 for the smaller contact labels.

[Typeface source](https://github.com/productiontype/Newsreader) · [Google Fonts distribution](https://github.com/google/fonts/tree/main/ofl/newsreader)
