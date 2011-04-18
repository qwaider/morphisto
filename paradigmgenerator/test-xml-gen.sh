xsltproc lexicon-transform.xslt $1 | python align.py >lexicon
fst-compiler-utf8 -s smor.fst tmp-gen-auto.a
fst-infl tmp-gen-auto.a < $2
