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
    print "Usage: ./python paradigm-generator {osx | linux} <upper side> <lower side> <smor-tag> {noun|verb|adj} [-ge]"
    print "Examples for nouns:"
    print "python paradigm-tester.py osx Mutter Mutter NFem_0_\$ noun"
    print "python paradigm-tester.py osx Cello Celli NNeut/Pl noun"
    print "Examples for verbs:"
    print "python paradigm-tester.py osx betrüg betrog VVPastIndStr verb"
    print "    Enter 'betrügen' as form of lemma"
    print "python paradigm-tester.py osx lieb lieb VVReg verb -ge"
    print "    Enter 'lieben' as form of lemma"
    print "python paradigm-tester.py osx kümmer kümmer VVReg-el/er verb -ge"
    print "    Enter 'kümmern' as form of lemma"
    print "Examples for adjectives:"
    print "python paradigm-tester.py osx schön schön Adj+ adj"
    print "python paradigm-tester.py osx schutzlos schutzlos AdjPos adj"
    
    sys.exit(0)

def getLexiconString(upper, lower, smortag, pos, geprefix):
    #<Base_Stems>Aasgeier<NN><base><nativ><NMasc_s_0>
    return_string = "<Base_Stems>"
    return_string += align(upper, lower)
    return_string += "<"+pos+"><base><nativ><"+smortag+">"
    if geprefix:
        return_string = "<ge>" + return_string
    return return_string.encode('utf-8')
    


if __name__ == "__main__":
    # temporary file for generation statemnts
    tmp_gen_stmts = "tmp1"
    # temporary file for result of generation process
    tmp_gen_res = "tmp2"
    # temporary automaton for wordform generation
    tmp_auto = "tmp-gen-auto.a"
    if len(sys.argv) not in [6,7]:
        printUsage()
    platform = sys.argv[1]
    if platform not in ["osx", "linux"]:
        print "Wrong platform!"
        printUsage()
    upperside = sys.argv[2].decode('utf-8')
    lowerside = sys.argv[3].decode('utf-8')
    smortag = sys.argv[4].decode('utf-8')
    pos = sys.argv[5]
    if pos not in ["noun","verb","adj"]:
        print "Wrong part of speech specified:"
        printUsage()
    else:
        if pos == "noun": pos = "NN"
        elif pos == "verb" : pos = "V"
        else: pos = "ADJ"
    ge_prefixed = False
    if len(sys.argv) == 7:
        ge_prefixed = sys.argv[6]
        if ge_prefixed != "-ge":
            print "Expected -ge as parameter"
            printUsage()
        else:
            ge_prefixed = True
    # default case for lemma
    lemma = upperside
    if pos == "V":
        foo = raw_input("Please specify lemma form of verb:")
        lemma = foo.strip().decode('utf-8')

    print "Make sure that you are in a UTF-8 environment!"
    print "You are, if this looks like German letters: äöüß"

    lexiconstring = getLexiconString(upperside, lowerside, smortag, pos, ge_prefixed)

    fp = open("lexicon","w")
    fp.write(lexiconstring + "\n")
    fp.close()
    print "Successfully created SMOR lexicon file with the following entry"
    print lexiconstring
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
    
    
    