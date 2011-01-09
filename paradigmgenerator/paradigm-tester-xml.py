# coding: utf-8
import sys, re, subprocess
from flextables import getFlextables

epsilon=re.compile("0")

def getGenerationStatements(pos, word):
    return_stmts = []
    if pos == "NN":        
        morphsyn_file="generate_nounforms"
    elif pos == "V": 
        morphsyn_file="generate_verbforms"
    else:
        morphsyn_file="generate_adjforms"

    fp=open(morphsyn_file,"r")
    forms=fp.readlines()
    fp.close()

    for tail in forms:
        bar=tail.strip()
        return_stmts.append((word+bar).encode('utf-8'))
    return return_stmts             

# borrowed from Morphisto's align.py
# align upper and lower side representation of string
def align(w1,w2):
    w1_len=len(w1)
    w2_len=len(w2)
    max_len=w1_len
    if w2_len>max_len: max_len=w2_len
    while 1:
        if w1_len==max_len: break
        w1=w1+"0"
        w1_len=w1_len+1
    while 1:
        if w2_len==max_len: break
        w2=w2+"0"
        w2_len=w2_len+1
    result=""
    for i in range(0,max_len):
        if w1[i]==w2[i]: 
            result+=w1[i]
            continue
        if w1[i]!=w2[i]:
            result+=w1[i]+":"+w2[i]
    result=epsilon.sub("<>",result)
    return result


def printUsage():
    print "Usage: ./python paradigm-generator {osx | linux} <your-xml-file> <lemma> {noun|verb|adj}"
    sys.exit(0)



if __name__ == "__main__":
    # temporary file for generation statemnts
    tmp_gen_stmts = "tmp1"
    # temporary file for result of generation process
    tmp_gen_res = "tmp2"
    # temporary automaton for wordform generation
    tmp_auto = "tmp-gen-auto.a"
    if len(sys.argv) not in [5]:
        printUsage()
    platform = sys.argv[1]
    if platform not in ["osx", "linux"]:
        print "Wrong platform!"
        printUsage()
    lexicon_file = sys.argv[2]
    lemma = sys.argv[3].decode('utf-8')
    pos = sys.argv[4]
    if pos not in ["noun","verb","adj"]:
        print "Wrong part of speech specified:"
        printUsage()
    else:
        if pos == "noun": pos = "NN"
        elif pos == "verb" : pos = "V"
        else: pos = "ADJ"

    print "Make sure that you are in a UTF-8 environment!"
    print "You are, if this looks like German letters: äöüß"

    try:
    	cmd = "xsltproc lexicon-transform.xslt "+lexicon_file+" | python align.py >lexicon"
	retcode = subprocess.call(cmd, shell = True)
    except OSError, e:
    	print >> sys.stderr, "Converting XML file to SMOR lexicon failed", e
    	print cmd
    	sys.exit(0)
    	
    print "Successfully created SMOR lexicon file with the following entry"
    print "Starting SFST compiler...."
    retcode = 0
    try:
        cmd = "./"+platform+"/fst-compiler-utf8 -s smor.fst " + tmp_auto
        retcode = subprocess.call(cmd, shell = True)
    except OSError, e:
        print >> sys.stderr, "Compiling lexicon failed", e
        print cmd
        sys.exit(0)
    print lemma
    stmts = getGenerationStatements(pos, lemma)
    # stmts in eine temporaere Datei speichern
    fp = open(tmp_gen_stmts,"w")
    for s in stmts:
        fp.write(s+"\n")
    fp.close()
    try:
        cmd = "./"+platform+"/fst-infl "+tmp_auto+" "+tmp_gen_stmts+" > "+tmp_gen_res
        retcode = subprocess.call(cmd, shell = True)
    except OSError, e:
        print >> sys.stderr, "Compiling lexicon failed", e
        print cmd
        sys.exit(0)
#   getFlexTables darauf laufen lassen...
    flextable_output_file = "flextable-"+lemma+".html"
    fp = open(flextable_output_file,"w")
    getFlextables(tmp_gen_res, fp)
    fp.close()
    print "The inflection paradigm has been successfully created in "+flextable_output_file+" :-)"
    
    
    
