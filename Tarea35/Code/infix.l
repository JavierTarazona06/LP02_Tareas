%{
#include "y.tab.h"
%}

%%
[0-9]+      { yylval = atoi(yytext); return NUMBER; }
[\+\-\*/]   { return yytext[0]; }
"("         { return '('; }
")"         { return ')'; }
[ \t\n]     { /* ignorar espacios en blanco */ }
.           { printf("Carácter no válido: %s\n", yytext); }
%%

int yywrap() { return 1; }
