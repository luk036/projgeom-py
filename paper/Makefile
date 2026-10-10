# Build projgeom.pdf from projgeom.md. Run from paper/.
#
# Flag rationale (md-to-latex skill), so the knowledge is not tribal:
#  - Title/author/abstract live in the .md YAML front matter, so the body
#    headings start at `##`; `--shift-heading-level-by=-1` maps them to
#    \section (otherwise pandoc emits no \section and numbering degrades to
#    0.1, 0.2).
#  - `-F pandoc-crossref` resolves the {#sec:..}/{#eq:..}/{#fig:..} labels.
#  - `--citeproc` builds the reference list from projgeom.bib using the vendored,
#    self-contained ieee.csl (no independent-parent link): offline and
#    reproducible. Prove it with HTTP(S)_PROXY=http://127.0.0.1:9.
#  - Build options live in paper/latex.yaml (IEEEtran journal class, amsmath,
#    booktabs) and paper/crossref.yaml (reference prefixes); they are loaded with
#    --metadata-file because pandoc 3.11 does not read a positional *.yaml as
#    metadata.
#  - Two-column IEEEtran: pandoc emits `longtable` for every pipe table, which is
#    illegal in two-column mode, so tables are authored as raw LaTeX `table*`
#    floats; their `\label`s are plain LaTeX labels referenced with
#    `Table~\ref{...}`.
#  - pdflatex cannot embed SVG; the *.svg sources live upstream and their *.pdf
#    twins are committed under figures/, so a normal build never needs a
#    converter. Do not use ImageMagick (it rasterizes); cairosvg keeps the
#    figure vector.
#
# Requires: pandoc, pandoc-crossref, a LaTeX engine with pdflatex.

PANDOC := pandoc
FLAGS  := -F pandoc-crossref --citeproc -s -t latex -N --reference-links \
          --shift-heading-level-by=-1 --pdf-engine=pdflatex \
          --metadata-file=latex.yaml --metadata-file=crossref.yaml

# --- Beamer talk -----------------------------------------------------------
# The deck needs LuaLaTeX (emoji font fallback) and two passes (outline and
# section navigation), so emit projgeom-talk.tex with pandoc, then run lualatex
# twice. The preamble is a CLI flag: pandoc mangles raw LaTeX in YAML
# header-includes (md-to-beamer rule 3/4).
SLIDE_FLAGS := -F pandoc-crossref --citeproc -t beamer --slide-level=2 \
               --metadata-file=beamer.yaml

FIG_PDF := $(wildcard figures/*.pdf)

.PHONY: paper talk clean

paper: projgeom.pdf

projgeom.pdf: projgeom.md projgeom.bib ieee.csl latex.yaml crossref.yaml $(FIG_PDF)
	$(PANDOC) $(FLAGS) projgeom.md -o $@

talk: projgeom-talk.pdf

projgeom-talk.tex: projgeom-talk.md beamer.yaml preamble.tex projgeom.bib ieee.csl $(FIG_PDF)
	$(PANDOC) $(SLIDE_FLAGS) --include-in-header=preamble.tex projgeom-talk.md -o $@

projgeom-talk.pdf: projgeom-talk.tex
	lualatex -interaction=nonstopmode -halt-on-error projgeom-talk.tex
	lualatex -interaction=nonstopmode -halt-on-error projgeom-talk.tex

clean:
	-@rm -f projgeom.tex projgeom.aux projgeom.log projgeom.out projgeom.toc \
	       projgeom-talk.tex projgeom-talk.aux projgeom.log projgeom.out \
	       projgeom-talk.toc projgeom-talk.nav projgeom-talk.snm \
	       projgeom-talk.vrb ; true
