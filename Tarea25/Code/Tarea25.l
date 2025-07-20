%{
LT, LE, EQ, NE, GT, GE,
IF, THEN, ELSE, ID, NUMBER, RELOP, WHILE
%}

delim   [ \t\n]
ws      {delim}+  /* Whitespace */

letter  [A-Za-z]
digit   [0-9]

id      {letter}({letter}|{digit}|_) 
number  {digit}+(\.{digit}+)?(E[+-]?{digit}+)? 
doubleq \"  /* Double quotes */

%%


ws
if   {return (IF); }

while { return (WHILE); }  
then {return (THEN); }
else {return (ELSE); }
id {yylval = (int) installID(); return (ID); }


doubleq.*doubleq { yylval = (int) installString(); return (STRING); }
number {yylval = (int) installNum(); return (NUMBER); }
"<" {yylval = LT; return (RELOP); }
"<=" {yylval = LE; return (RELOP); }
"==" {yylval = EQ; return (RELOP); }
"!=" {yylval = NE; return (RELOP); }
">" {yylval = GT; return (RELOP); }
">=" {yylval = GE; return (RELOP); }

%%
