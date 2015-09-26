(TeX-add-style-hook "rstparser"
 (lambda ()
    (LaTeX-add-bibliographies
     "ref")
    (LaTeX-add-labels
     "fig:tree-example"
     "fig:circled")
    (TeX-add-symbols
     '("codeclass" 1)
     '("codefunc" 1)
     '("codefile" 1))
    (TeX-run-style-hooks
     "bm"
     "multirow"
     "subfigure"
     "amssymb"
     "amsfonts"
     "amsmath"
     "float"
     "epsfig"
     "fancybox"
     "graphicx"
     ""
     "latex2e"
     "art12"
     "article"
     "12pt")))

