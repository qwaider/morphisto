# Introduction #

_morphisto_ is an open-source lexicon for the morphological analysis of German. It is designed to be used with SMOR, an open-source implementation of the German morphology rules. This page is supposed to discuss questions and problems of both morphisto and SMOR which are not obvious bugs or simple feature requests.

# Open questions #

  * Relation between Base- and KomposStem
> > Despite of defining a KomposStem for a base entry, it is still possible to infer compounds from that base.
```
    Alter<NN>:<>W:weisheit<+NN>:<><Fem>:<><Nom>:<><Sg>:<>
```
> > Should we define a special origin class for words which have a KomposStem and should not be used in compounds?
```
    <BaseStem><Lemma>Alter</Lemma><Stem>Alter</Stem><Pos>NN</Pos><Origin>special</Origin><InfClass>NNeut_s_0</InfClass> <Frequency>10</Frequency> </BaseStem>
    <KomposStem><Upper>Alter</Upper><Lower>Alters</Lower><Pos>NN</Pos><Origin>nativ</Origin><Frequency>0</Frequency</KomposStem>
```
> > Is there an equivalent type of entry for derivations (e.g. DerivStem)?


> Comments by **CWRSimon**:
> Yes, there is the _DerivStem_ class, but honestly, I have never understood how to use it properly:
```
<Deriv_Stems>Pantomime:<><NN><deriv><fremd>
<Deriv_Stems>Seku:?nde:<><NN><deriv><frei>
<Deriv_Stems>Standard<NN><deriv><frei>
<Deriv_Stems>Thema<>:t<NN><deriv><frei>
<Deriv_Stems>divis<V><deriv><lang>
<Deriv_Stems>erkunde:<>n:<><V><deriv><nativ>
<Deriv_Stems>ertra:?g<V><deriv><nativ>
```
> This would be a top-priority thing to ask Helmut Schmid...
> Regarding the first question:
The idea to exclude base stems for which a compound stem has been defined appeals to me. However, would it still be possible to analyze _Zeitalter_ or _Zeitalterbestimmung_ then?

  * Derivation of complex verbs in different forms
> > Comparing the analyses of "ernstmachen" und "ernstgemacht" shows that morphisto/SFST lacks ways to construct infinitives for (NN|ADJ)V constructions. The analysis with "ernst" as prefix seems to serve as a fallback but is (at least in my opinion and the one expressed in Fleischer/Barz) not correct. Two steps are two be taken:
    1. Find out of the construction of complex verbs from a free morphem and a base verb form is (still) a constructive one.
    1. If this is the case, add a rule similar to the past participle for infinitives. If not, add an entry for "ernstmachen" and similar forms to the lexicon and remove the means for constructing "ernst-ADJ-gemacht-V" from deko.fst.

# Resolved questions #

**Prefix + Noun

> (Arbitrary)Combinations of prefix + noun are not possible in SMOR:
```
    Absicht<+NN>:<><Fem>:<><Nom>:<><Sg>:<>
    Aufsicht<+NN>:<><Fem>:<><Nom>:<><Sg>:<>
    Hinsicht<+NN>:<><Fem>:<><Nom>:<><Sg>:<>
```
> But:
```
    Durch<OTHER>:<>S:sicht<+NN>:<><Fem>:<><Nom>:<><Sg>:<>
    Durch<OTHER>:<>D:durch<OTHER>:<>S:sicht<+NN>:<><Fem>:<><Nom>:<><Sg>:<>
```**

> Solution a: Add productive noun prefixation in SMOR (deko.fst).

> Solution b: Add 'ab', 'auf' etc. as 'OTHER' to morphisto.

> Comments by **CWRSimon**:
> I do like the ideas, but I am wondering, whether prefixation is     productive enough for German nouns in general: E.g., Morphisto already  analyzes "Durchhund" and "Durchstuhl". Of course, one could argue that  only nouns with a certain semantic feature can be prefixed with a prefix  that embodies the same feature (e.g. Durch[+direction] and  Gang[+direction] can form Durchgang). But then again, is prefixation  really a process that applies to German nouns? I don't know what the  literature says, but I would imagine the following: Prefixation is  process that typically applies to verbs: durchgehen, durchsehen,  hingehen, absehen, etc. And Durchgang, Aufsicht, Hinsicht, etc. are just the nominalizations of theses verbs. I do concede that I don't know, how to tell an FST-based morphology about German etymological wordformation processes....

> Comments by **wuerzner**:
> You are absolutely right: According to Fleischer/Barz, prefixation of nouns is a rare phenomenon. Nouns as 'Durchgang' should then be analysed as deverbal:
```
    <CAP>durch<PREF>gehen<V><SUFF><+NN><Masc><Nom><Sg>
```
> Are we able to implement that with SFST?

> Comments by **CWRSimon**:
> With FST-based technologies possibly, but not necessarily in the framework of Morphisto. What we need is a means of defining conversion rules from one POS class to another.

> Closing Remark by **wuerzner**:
> We can use 

&lt;DerivStem&gt;

 to implement this conversion. Have a look at the entry "fahren" in derivates.xml: The trick is to add the inflection class as origin and voilà "Ausfahrt" can be traced to "fahren"! It also works with compositions like "Freifahrt".

**Verb participle to adjective conversion
> The following example shows that an adjective reading is only available for base verbs not for complex ones.
```
    ver<PREF>suchen<+V><1><Sg><Past><Konj>
    ver<PREF>suchen<+V><1><Sg><Past><Ind>
    ver<PREF>suchen<+V><3><Sg><Past><Konj>
    ver<PREF>suchen<+V><3><Sg><Past><Ind>
    versuchen<+V><1><Sg><Past><Konj>
    versuchen<+V><1><Sg><Past><Ind>
    versuchen<+V><3><Sg><Past><Konj>
    versuchen<+V><3><Sg><Past><Ind>
    versuchen<V><PPast><SUFF><+ADJ><Pos><Masc><Nom><Sg><Sw>
    versuchen<V><PPast><SUFF><+ADJ><Pos><Fem><Nom><Sg>
    versuchen<V><PPast><SUFF><+ADJ><Pos><Fem><Akk><Sg>
    versuchen<V><PPast><SUFF><+ADJ><Pos><Neut><Nom><Sg><Sw>
    versuchen<V><PPast><SUFF><+ADJ><Pos><Neut><Akk><Sg><Sw>
    versuchen<V><PPast><SUFF><+ADJ><Pos><NoGend><Nom><Pl><St>
    versuchen<V><PPast><SUFF><+ADJ><Pos><NoGend><Akk><Pl><St>
```
> For the (in principle superflous) full form entry of 'versuchen' but not for the derived form 'ver + suchen', adjective readings are generated. Assumedly, this is also a problem in 'deko.fst'.**

> Comments by **CWRSimon**:
> What exact wordform have you analyzed? _versuchen_ is not exactly a hypothetic attributive adjective form, only maybe a predicative one ("Dieses Angebot ist versuchen."). If one makes Morphisto analyze _versuchendes_, one will receive the analysis for an attributive adjective:
```
versuchen<V><PPres><SUFF><+ADJ><Pos><Neut><Akk><Sg><St/Mix>
versuchen<V><PPres><SUFF><+ADJ><Pos><Neut><Nom><Sg><St/Mix>
ver<PREF>suchen<V><PPres><SUFF><+ADJ><Pos><Neut><Akk><Sg><St/Mix>
ver<PREF>suchen<V><PPres><SUFF><+ADJ><Pos><Neut><Nom><Sg><St/Mix>
```
> But I agree that the internal workings of deko.fst are not very transparent and need to be examined in detail!

> Comments by **wuerzner**:
> The concrete form was 'versuchte' ('Der zunächst versuchte Weg erwies sich als falsch.'). I confirm that everything is fine for 'versuchendes'. Do we have a bug here?

> Comments by **CWRSimon**:
> Possibly. Do you know the general rule for creating attribute adjectives from verbs? SMOR/Morphisto seems to use the Partizip-II form, because _vergesuchte_ works. Compare with _abgrasen_: It is possible to use _abgegraste_ as an adjective (_das abgegraste Feld_), but you cannote say _das abgraste Feld_ which is analogous to _versuchte_. That brings me to another complicated matter. Morphisto analyzes _abgraste_ as an inflected verb form of 'abgrasen' (_Ich abgraste das Feld_). That is BS, because it should actually be (_Ich graste das Feld ab_). But that matter gets us closer to parsing than mere morphological analysis...

> Closing Remark by **wuerzner**:
> It is possible to make use of the MorphMarker 'no-ge' to allow for the analysis of derived verb forms as past participle. Conversion to ADJ works if such an analysis is available.