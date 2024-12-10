qltool
======

*tool to print some useful stuff with ql700 brother printer*

-   It is in development!
-   It is just a wrapper around the great `ql570.c` of Asbjørn Sloth
    Tønnesen, Marc Juul and Luca Zimmermann

```{=html}
<!-- -->
```
-   Short text
-   Image (dithered)
-   short text+qr code

Example
-------

``` {.python}
qltool Ahoj -c v -q
qltool Ahoj -c p -q
```

Installation
------------

``` {.bash org-language="sh"}
pip3 install qltool
```

Org-mode inventory
------------------

If this function is somewhere in the `.emacs` configfiles ...

It selects two fields fromthe TABLE and puts -q option.

You point to a line of a table and `c-c q` or `c-c w` will view/print
the code for inventory.

  whatever   id            name                        owner   location
  ---------- ------------- --------------------------- ------- ----------
  123        D4-12345678   najaka blbost z inventury   Pepa    Home

and this is run
`./bin_qltool.py "id: D4-12345678; name: najaka blbost z inventury  owner:Pepa " -q`
