%{
#define LT 300
#define LE 301
#define EQ 302  
#define NE 303
#define GT 304
#define GE 305
#define IF 306
#define THEN 307
#define ELSE 308
#define ID 309
#define NUMBER 310
#define RELOP 311
#define KW 312  /* New category for keywords */
%}

delim   [ \t\n]+
ws      {delim}
letter  [A-Za-z]
digit   [0-9]
id      {letter}({letter}|{digit})*
number  {digit}+(\.{digit}+)?(E[+-]?{digit}+)?

%%
ws          { /* no action and no return */ }

"if"        { yylval = IF; return(KW); }
"then"      { yylval = THEN; return(KW); }
"else"      { yylval = ELSE; return(KW); }

{id}        { yylval = (int) installID(); return(ID); }

{number}    { yylval = (int) installNum(); return(NUMBER); }

"<"         { yylval = LT; return(RELOP); }
"<="        { yylval = LE; return(RELOP); }
"="         { yylval = EQ; return(RELOP); } 
"<>"        { yylval = NE; return(RELOP); }
">"         { yylval = GT; return(RELOP); }
">="        { yylval = GE; return(RELOP); }
%%
