# table-generator.py
# coding: utf-8

import sys
import re
import copy

adjtype=re.compile("<Pos>|<Comp>|<Sup>")
gender=re.compile("<Masc>|<Fem>|<Neut>|<NoGend>")
number=re.compile("<Sg>|<Pl>")
case=re.compile("<Nom>|<Gen>|<Dat>|<Akk>")
person=re.compile("<1>|<2>|<3>")
tense=re.compile("<Pres>|<Past>")
form=re.compile("<PPast>|<Inf>|<PPres>")
mood=re.compile("<Ind>|<Konj>|<Imp>")
flexion=re.compile("<St>|<Sw>|<Sw\/Mix>|<St\/Mix>")
brackets=a=re.compile("[\<\>]")

class paradigm:
	def __init__(self,lemma,form,gender,klasse):
		self.lemma=lemma
		self.form=form
		self.gender=gender
		self.klasse=klasse
		self.singular={"Nom":[],"Gen":[],"Dat":[],"Akk":[]}
		self.plural={"Nom":[],"Gen":[],"Dat":[],"Akk":[]}
	def add(self, wordform, case, number):
#		fp.write( "Füge jetzt hinzu:",wordform,case,number
		if number=="Sg":
			try:
				self.singular[case].append(wordform)
			except:
				print "Error with "+case+" "+number	
		if number=="Pl":
			try:
				self.plural[case].append(wordform)
			except:
				print "Error with "+case+" "+number
#		fp.write( "Singular:",self.singular
#		fp.write( "Plural:",self.plural
	def show(self):
		print self.lemma
		print self.klasse
		print self.gender
		print self.form
		print self.plural
		for key in self.singular.keys():
			for item in self.singular[key]:
				print key+":"+item
		for key in self.plural.keys():
			for item in self.plural[key]:
				print key+":"+item
	def getForm(self,number,case):
		try:
			if number=="Sg":
				return self.singular[case]
			else:
				return self.plural[case]
		except:
			return ""

class adjective:
	def __init__(self, lemma):
		self.lemma=lemma
		self.classes=["St","Sw","Mix"]
		self.genders=["Masc","Fem","Neut"]
		self.forms=[]
		self.paradigms={}
		
	def add(self, form, gender, klasse, case, number, wordform):
#		print "number:",number, "klasse:",klasse, "gender:", gender
		genders=[]
		if gender=="NoGend":
			genders=["Masc","Fem","Neut"]
		else: genders=[gender]
		classes=[]
		if klasse=="":
			classes=["St","Sw","Mix"]
		elif klasse=="St/Mix":
			classes=["St","Mix"]
		elif klasse=="Sw/Mix":
			classes=["Sw","Mix"]
		elif klasse=="St":
			classes=["St"]
		else: classes=["Sw"]
		#check, whether form type already included
		if not(form in self.forms):
			self.forms.append(form)
			for gender in self.genders:
				for klasse in self.classes:
					key=form+gender+klasse
#					fp.write( "Erzeuge Paradigma:",key
					foo=paradigm(self.lemma, form, gender, klasse)
					self.paradigms[key]=foo			
		for entry in genders:
			for item in classes:
				key=form+entry+item
#				fp.write( "Key:",key
				try:
					self.paradigms[key].add(wordform,case,number)
				except:
					print "Error with "+form+","+entry+","+item+","+case+","+number
	
	def getParadigm(self, form, gender, klasse):
		key=form+gender+klasse
		return self.paradigms[key]	
	def getClasses(self):
		return self.classes
	def getGenders(self):
		return self.genders			
	def getForms(self):
		return self.forms			

def getFlexion(line):
#	fp.write( "Flexion",line
	try:
		foo=flexion.search(line).group(0)
#		fp.write( foo
		return foo[1:-1]
	except:
		return "unknown"

def getAdjType(line):
	try:
		foo=adjtype.search(line).group(0)
		return foo[1:-1]
	except:
		return "unknown"

def getPerson(line):
	try:
		foo=person.search(line).group(0)
		return foo[1:-1]
	except:
		return "unknown"


def getMood(line):
	try:
		foo=mood.search(line).group(0)
		return foo[1:-1]
	except:
		return "unknown"


def getTense(line):
	try:
		foo=tense.search(line).group(0)
		return foo[1:-1]
	except:
		return "unknown"


def getForm(line):
	try:
		foo=form.search(line).group(0)
		return foo[1:-1]
	except:
		return "unknown"


def getGender(line):
	try:
		foo=gender.search(line).group(0)
		return foo[1:-1]
	except:
		return "unknown"



def isNoun(entry):
	try:
		return entry[0].rfind("<+NN>")
	except:
		return False

def isAdj(entry):
	try:
		return entry[0].rfind("<+ADJ>")
	except:
		return False

def isVerb(entry):
	try:
		return entry[0].rfind("<+V>")
	except:
		return False

def getLemma(line):
	foo=line.find("<")
	if foo>0:
		bar=line[:foo]
		if bar.startswith(">"): return bar[1:].strip()
	return "unknown"

def getCase(line):
	try:
		foo=case.search(line).group(0)
		return foo[1:-1]
	except:
		return "unknown"

def getNumber(line):
	try:
		foo=number.search(line).group(0)
		return foo[1:-1]
	except:
		return "unknown"

def getEnum(list):
	if list==[]: return ""
	returnstring=""
	for elem in list:
		returnstring=returnstring+elem+", "
	return returnstring[:-2]

def getCaseName(case):
	names={"Nom":"Nominativ","Gen":"Genitiv","Dat":"Dativ","Akk":"Akkusativ"}
	return names[case]

def getFormName(case):
	names={"Pos":"Positiv","Comp":"Komparativ","Sup":"Superlativ", "PPres":"Partizip I", "PPast":"Partizip II","ImpSg":"Imperativ Sg.","ImpPl":"Imperativ Pl.","Inf":"Infinitiv"}
	return names[case]

def getGenderName(case):
	names={"Masc":"Maskulinum","Fem":"Femininum","Neut":"Neutrum"}
	return names[case]

def getClassName(case):
	names={"St":"Stark","Sw":"Schwach","Mix":"Gemischt"}
	return names[case]


def print_table_html(table, lemma, gender, fp):
#	fp.write( table, lemma, gender
	fp.write( "<table border='1'>" )
	singular=table["Sg"]
	plural=table["Pl"]
	cases=["Nom","Gen","Dat","Akk"]
	spanne=3
	fp.write( "<table border=\"0\" cellspacing=\""+str(spanne)+"\" cellpadding=\"1\">" )
	fp.write( "<tr>" )
	fp.write( "<td class=\"ParadigmHeaderMain\" colspan=\""+str(spanne)+"\">Nomen:"+lemma+", Genus:"+getGenderName(gender)+"</td>" ) 
	fp.write( "</tr>" )
			
	foo=[]
	fp.write( "<tr>" )
	fp.write( "<td class=\"ParadigmHeaderSubCol2\">Kasus</td>" )
	fp.write( "<td class=\"ParadigmHeaderSubCol2\">Sg</td>" )
	fp.write( "<td class=\"ParadigmHeaderSubCol2\">Pl</td>" )
	fp.write( "</tr>" )
	
	for case in cases:
		case_sg=singular[case]
		case_pl=plural[case]
		if case_sg==[]: case_sg="-"
		if case_pl==[]: case_pl="-"
		fp.write( "<tr><td class=\"ParadigmHeaderSubCol2\">"+case+"</td>" )
		fp.write( "<td class=\"Wortform\">"+getEnum(case_sg)+"</td>" )
		fp.write( "<td class=\"Wortform\">"+getEnum(case_pl)+"</td>" )
		fp.write( "</tr>" )

	fp.write( "</table>" )
	fp.write( "<br>" )
	

def print_verb_persons(table,keys, fp):
	person=["1","2","3"]
	for pers in person:
		fp.write( "<tr>" )
		fp.write( "<td class=\"Wortform\">"+pers+"</td>" )
		for key in keys:
			foo=table[key]
			bar=foo[pers]
			if bar==[]: bar="-"
			fp.write( "<td class=\"Wortform\">"+getEnum(bar)+"</td>" )
		fp.write( "</tr>" )

def print_verbtable_html(table, lemma, fp):
#	fp.write( table
	singular=("PresIndSg","PresKonjSg","PastIndSg","PastKonjSg")
	plural=("PresIndPl","PresKonjPl","PastIndPl","PastKonjPl")
        forms=("Inf","ImpSg","ImpPl","PPres","PPast")
	spanne=5
	fp.write( "<table border=\"0\" cellspacing=\"2\" cellpadding=\"1\">" )
	fp.write( "<tr>" )
	fp.write( "<td class=\"ParadigmHeaderMain\" colspan=\""+str(spanne)+"\">Verb:"+lemma+"</td>" )
	fp.write( "</tr>" )
	fp.write( "<tr>" )
	fp.write( "<td></td>" )
	fp.write( "<td class=\"ParadigmHeaderSubCol2\">Praes.Ind.</td>" )
	fp.write( "<td class=\"ParadigmHeaderSubCol2\">Praes.Konj.</td>" )
	fp.write( "<td class=\"ParadigmHeaderSubCol2\">Praet.Ind.</td>" )
	fp.write( "<td class=\"ParadigmHeaderSubCol2\">Praet.Konj.</td></tr>" )

	print_verb_persons(table,singular, fp)
	print_verb_persons(table,plural, fp)
	
	for form in forms:
		fp.write( "<tr>" )
		fp.write( "<td class=\"ParadigmHeaderSubCol2\" colspan=\""+str(spanne)+"\">"+getFormName(form)+": "+getEnum(table[form])+"</td>" )
		fp.write( "</tr>" )
		
	fp.write( "</table>" )
	fp.write( "<br>" )
	fp.write( "<br>" )




def print_adjtable_html(table, lemma, fp):
	#fp.write( table
	adj=adjective(lemma)
	k1=["Pos","Comp","Sup"]
	k2=["Masc","Fem","Neut","NoGend"]
	k3=["Sg","Pl"]
	k4=["St","Sw","Sw/Mix","St/Mix",""]
	cases=["Nom","Gen","Dat","Akk"]
	keys=[]
	#def add(self, form, gender, klasse, case, number, wordform):

	for form in k1:
		for gender in k2:
			for klasse in k4:
				for number in k3:
					key=form+gender+number+klasse
					foo=table[key]
					for case in cases:
#						fp.write( key, case, foo[case]
						bar=foo[case]
						for item in bar:
							adj.add(form, gender, klasse, case, number, item)
	
	classes=adj.getClasses()
	genders=adj.getGenders()
	forms=adj.getForms()
	for form in forms:
		for gender in genders:
			spanne = len(classes)+1
			fp.write( "<table border=\"0\" cellspacing=\"2\" cellpadding=\"1\">" )
			fp.write( "<tr>" )
			fp.write( "<td class=\"ParadigmHeaderMain\" colspan=\""+str(spanne)+"\">Adjektiv:"+lemma+", Steigerungsstufe:"+getFormName(form)+", Genus:"+getGenderName(gender)+"</td>" )
			fp.write( "</tr>" )
			classcount=len(classes)
			foo=[]
			fp.write( "<tr>" )
			fp.write( "<td class=\"ParadigmHeaderSubCol2\">Kasus</td>" )
			
			for i in range(0,classcount):
				foo.append(adj.getParadigm(form, gender, classes[i]))
				fp.write( "<td class=\"ParadigmHeaderSubCol2\">"+getClassName(classes[i])+"</td>" )
			fp.write( "</tr>" )
			
			for case in cases:
				fp.write( "<tr>" )
				fp.write( "<td class=\"ParadigmHeaderSubCol2\">"+case+". Sg."+"</td>" )
				for i in range(0,classcount):
					fp.write( "<td class=\"Wortform\">"+getEnum(foo[i].getForm("Sg",case))+"</td>" )
				fp.write( "</tr>" )
			
			for case in cases:
				fp.write( "<tr>" )
				fp.write( "<td class=\"ParadigmHeaderSubCol2\">"+case+". Pl."+"</td>" )
				for i in range(0,classcount):
					fp.write( "<td class=\"Wortform\">"+getEnum(foo[i].getForm("Pl",case))+"</td>" )
				fp.write( "</tr>" )
			fp.write( "</table>" )
			fp.write( "<br>" )
			
	
	
	#for form in forms:
	#	fp.write( "<p>"+form+":"+getEnum(table[form])+"</p>"


def print_table_row_noun(lines, fp):
#	fp.write( "fp.write(_table_row_nouns<br>"
	table={"Sg":{"Nom":[],"Gen":[],"Dat":[],"Akk":[]},"Pl":{"Nom":[],"Gen":[],"Dat":[],"Akk":[]}}
	table_changes=False	#have there been any changes to this table data?
	gender=""
	number=""
	case=""
	table_gender=""
	for entry in lines:
#		fp.write( "Entry:"+brackets.sub("#",entry)+"<br>"
		if entry.endswith("-----"):
			continue
		if entry.startswith("> "):
			gender=getGender(entry)
			number=getNumber(entry)
			case=getCase(entry)
			lemma=getLemma(entry)
			continue
		if entry.startswith("no result for"):
			continue
		table_changes=True
		foo=table[number]
		foo[case].append(entry)
		table[number]=foo
		table_gender=gender
	if table_changes:
		print_table_html(table, lemma, table_gender, fp)

def print_table_row_verb(lines, fp):	
	#table={"PresIndSg":{},"PresIndPl":{},"PresKonjSg":{},"PresKonjPl":{},"PretIndSg":{},"PretIndPl":{},"PretKonjSg":{},"PretKonjPl":{},"unknownImpPl":[],"unknownImpSg":[],"PPast":[],"Inf":[]}
	keys=["PresIndSg","PresIndPl","PresKonjSg","PresKonjPl","PastIndSg","PastIndPl","PastKonjSg","PastKonjPl"]
	table={"ImpPl":[],"ImpSg":[],"PPast":[],"Inf":[],"PPres":[]}
	
	for key in keys:
		table[key]={"1":[],"2":[],"3":[]}
		
	persons={"1":[],"2":[],"3":[]}
	table_changes=False	#have there been any changes to this table data?
	tense=""
	form=""
	person=""
	mood=""
	lemma=""
	for entry in lines:
		if entry.endswith("-----"):
			continue
		if entry.startswith("> "):
			tense=getTense(entry)
			form=getForm(entry)
			person=getPerson(entry)
			mood=getMood(entry)
			lemma=getLemma(entry)
			number=getNumber(entry)
			continue
		if entry.startswith("no result for"):
			continue
		
		table_changes=True
		#fp.write( tense,form,person,mood,lemma
		key=tense+mood+number		
		try:
			foo=table[key]
			foo[person].append(entry)
			table[key]=foo
		except:
			key=mood+number
			try: table[key].append(entry)
			except:
				if form!="" and form!="unknown":
					table[form].append(entry)	

	if table_changes:
		print_verbtable_html(table, lemma, fp)

def generateKeys(k1,k2,k3,k4):
	keys=[]
	for e1 in k1:
		for e2 in k2:
			for e3 in k3:
				for e4 in k4:
					keys.append(e1+e2+e3+e4)
	return keys

def print_table_row_adj(lines, fp):	
	#table={"PresIndSg":{},"PresIndPl":{},"PresKonjSg":{},"PresKonjPl":{},"PretIndSg":{},"PretIndPl":{},"PretKonjSg":{},"PretKonjPl":{},"unknownImpPl":[],"unknownImpSg":[],"PPast":[],"Inf":[]}
	keys=generateKeys(["Pos","Comp","Sup"],["Masc","Fem","Neut","NoGend"],["Sg","Pl"],["St","Sw","Sw/Mix","St/Mix",""])
	table={}
	for key in keys:
		table[key]={"Nom":[],"Gen":[],"Dat":[],"Akk":[]}
	table_changes=False	#have there been any changes to this table data?
	case=""
	lemma=""
	number=""
	gender=""
	adjtype=""
	flexion=""
	form=""
	#fp.write( "fp.write(_table_row_adj"
	for entry in lines:
		if entry.startswith("> "):
			case=getCase(entry)
			lemma=getLemma(entry)
			number=getNumber(entry)
			gender=getGender(entry)
			adjtype=getAdjType(entry)
			flexion=getFlexion(entry)
			continue
		if entry.startswith("no result for"):
			continue
		table_changes=True
		#fp.write( tense,form,person,mood,lemma
		key=adjtype+gender+number+flexion
		try:
			#fp.write( "Key:",key, entry
			foo=table[key]
			foo[case].append(entry)
			table[key]=foo
		except:
			key=adjtype+gender+number
			try: 
				
				#fp.write( "2. Key:",key, entry
				foo=table[key]
				#fp.write( "Zuerst stand da:",foo
				foo[case].append(entry)
				table[key]=foo
				#fp.write( "Jetzt steht da:",table[key]
			except:
				if form!="" and form!="unknown":
					table[form].append(entry)	

	if table_changes:
		print_adjtable_html(table, lemma, fp)

def print_entry(entry, fp):
    #fp.write( entry
    #what part of speech is the entry?
    if isNoun(entry)>0: 
        print_table_row_noun(entry, fp)
    elif isVerb(entry)>0: 
        print_table_row_verb(entry, fp)
    elif isAdj(entry)>0:
        #fp.write( "Ist ein Adjektive"
        print_table_row_adj(entry, fp)
    

def process_file(filename, fp2):
	entry=[]
	fp=open(filename,"r")	
	#data=map(str.strip,fp.readlines())
	line=fp.readline().strip()
	while line:
		if line.endswith("-----"):
			print_entry(entry, fp2)
			#fp.write( "<br>"
			entry=[]
			line=fp.readline().strip()
			continue
		entry.append(line)
		line=fp.readline().strip()
	fp.close()



def createCSS(fp):
	fp.write( "<style type=\"text/css\">" )
	fp.write( "body {margin: 1em}" )
	fp.write( "p {}" )
	fp.write( "td    { font-size: 12px; font-family: Verdana, Arial, Helvetica, sans-serif; padding: 2px; border: solid 1px #ccc }" )
	fp.write( "table { border-collapse: collapse; /*vertical-align: top*/ }" )
	fp.write( ".Wortform   { background-color: #f6eeda ;width: 12em;min-width: 12em; }" )
	fp.write( ".BeiText    { text-align: right; width: 12em;min-width: 12em; background-color: #dde5f1 }" )
	fp.write( ".ParadigmHeaderMain      { font-family: Verdana, Arial, Helvetica, sans-serif; font-weight: bold; background-color: #e2e2e2; text-align: center }" )
	fp.write( ".ParadigmHeader      { font-family: Verdana, Arial, Helvetica, sans-serif; font-weight: bold; background-color: #e2e2e2; text-align: center ; overflow: visible}" )
	fp.write( ".ParadigmHeaderSub     { text-align: right; background-color: #e2e2e2 }" )
	fp.write( ".ParadigmHeaderSubCol2      { background-color: #e2e2e2; text-align: left }" )
	fp.write( "span.BeiTextSample { color: #557}" )

	fp.write( "#BetweenGradation { display: block;  margin: 1em  }" )
	fp.write( "#posstrong,#posweak,#posmixed  { display:block;  margin-right:0.0em }" )
	fp.write( "#komstrong,#komweak,#kommixed  { display:block;  margin-right:0.0em }" )
	fp.write( "#supstrong,#supweak,#supmixed  { display:block;  margin-right:0.0em }" )

	fp.write( "#infpres { display: inline;  margin-right:0.5em }" )
	fp.write( "#infzupres { display: inline;  margin-left:0.5em }" )

	fp.write( "#prespart { display: inline;  margin-right:0.5em }" )
	fp.write( "#pastpart { display: inline;    margin-left:0.5em }" )
	fp.write( "</style>\n" )


def getFlextables(filename, fp):
	fp.write( "<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01//EN\" >" )
	fp.write( "<html>" )
	fp.write( "<head>" )
	fp.write( "<meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\">" )
	fp.write( "<title>Flexionstabellen fuer elexiko-Eintraege</title>" )
	createCSS(fp)
	fp.write( "</head>" )
	fp.write( "<body bgcolor=\"#ffffff\">" )
	process_file(filename, fp)
	fp.write( "</body>" )
	fp.write( "</html>" )
	
