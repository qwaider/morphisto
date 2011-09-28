%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  File:         defaults2.fst
%  Author:       Kay-Michael Würzner; Universitaet Potsdam
%  Adapted from: defaults.fst
%  Date:         September 2011
%  Content:      generation of default base, derivation and composition stems
%                from suffix-conversions
%  Coding:	 utf-8
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


$TMPL$ = ($BaseStems$ | $TMP$) || $KOMPOSFILTER$


$ANY$ = [\!-\~¡-ÿ <FB><SS><n><~n><e><d><Ge-Nom><UL> <NoHy><NoDef><ge><no-ge><CB>\
	<Base_Stems><Deriv_Stems><Kompos_Stems><Pref_Stems><Suff_Stems>]*

$TMPL$ = $TMPL$ $FLEXION$ 
$TMPL$ = $TMPL$ || $ANY$ $FLEXFILTER$
$TMPL$ = $TMPL$ || $INFIXFILTER$
$TMPL$ = $TMPL$ || $UPLOW$


$TMPL$ = <>:<WB> $TMPL$ <>:<WB> || $PHON$

% default noun derivation stems

$DefDerivNN2$ = (\
([\!-\~¡-ÿ<PREF>]* \
 ([<V>]<SUFF>)? \
 <>:<+NN> <>:[<Masc><Fem><Neut><NoGend>] <>:<Nom> <>:<Sg> || $TMPL$) \
<NN>) || $Del-e$ || $Uml$

% default adjective base stems

$DefBaseADJ2$ = \
  (([\!-\~¡-ÿ<PREF><ge>]* [<NN><ADJ>]<SUFF> en <V>:<+V><zu>?<PPast> ||\
   $TMPL$ || $NoDef2NULL$ t) <>:<ADJ><SUFF>:<><>:<base><>:<nativ><>:<Adj+e>) |\
  (([\!-\~¡-ÿ<PREF>]* [<NN><ADJ>]<SUFF> en <V>:<+V><zu>?[<PPres><PPast>] ||\
   $TMPL$ || $NoDef2NULL$ (en|nd)) <>:<ADJ><SUFF>:<><>:<base><>:<nativ><>:<Adj+>)

% default adjective composition and derivation stems

$DefKomposADJ2$ = (\
  ([\!-\~¡-ÿ]* <OTHER>al<SUFF> <>:<+ADJ> <>:[<Pos><Comp><Sup>] <>:<Pred> |\
   [\!-\~¡-ÿ<PREF>]* <NN><SUFF> en <V>:<+V><zu>?[<PPres><PPast>]) ||\
  $TMPL$ || $NoDef2NULL$) <ADJ>

$DefDerivADJ2$ = $DefKomposADJ2$

% default verb composition stems

$DefKomposV2$ = ([\!-\~¡-ÿ<PREF><ge>]* [<NN><ADJ>]<SUFF> en {<>}:{<+V><Inf>} || $TMP$) <V> ||\
	[\!-\~¡-ÿ]* ({en}:{<>} | e[rlg]n:<>) <V>

% default verb derivation stems

$DefDerivV2$ = ([\!-\~¡-ÿ<PREF><ge>]* [<NN><ADJ>]<SUFF> en {<>}:{<+V><Inf>} || $TMPL$) <V> ||\
	<NoDef>:<>? [\!-\~¡-ÿ]* ({en}:{<>} | e:<e> [rl] n:<>) <V> || $Uml$

$BDKStems2$ = <>:<Base_Stems> $DefBaseADJ2$ |\
(<>:<Deriv_Stems> ($DefDerivV2$ | $DefDerivADJ2$ | $DefDerivNN2$)\
 <>:<deriv> |\
 <>:<Kompos_Stems> ($DefKomposADJ2$ |$DefKomposV2$) <>:<kompos>)\
<>:<nativ>
