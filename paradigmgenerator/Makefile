all: lexicon test.ca

test.ca: tmp-auto.a
	fst-compact $< > $@

tmp-auto.a: smor.fst lexicon phon.fst PRO.fst phon.a map.fst NUM.fst defaults.fst defaults2.fst deko.fst FIX.fst flexion.fst
	fst-compiler-utf8 $< $@

lexicon: mylexicon.xml
	xsltproc lexicon-transform.xslt $< | python align.py > $@

clean:
	rm lexicon test.ca
