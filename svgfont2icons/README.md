# svgfont2icons Converter #

This converter converts SVG font files to SVG icon images.

## Syntax ##

    $ python svgfont2icons.py <icons.svg> [<icons.glyphs>] [--padding=<padding>]

For example:

    $ python svgfont2icons.py icon-excerpt.svg
    $ python svgfont2icons.py icon-excerpt.svg icon-excerpt.glyphs --padding=200

These commands would create icons directory and populate it with SVG icons from the font file.
If the original Glyphs file is passed to the script as a second parameter,
it will be used to read out the names for each Glyph and use them as the filenames.
If padding is passed, each glyph will be added some padding.

The idea of the script belongs to Thomas Helbig (http://www.dergraph.com / http://www.neuedeutsche.com).

Implemented by Aidas Bendoraitis (aidas@bendoraitis.lt).