%{
#include <stdio.h>
#include <stdlib.h>
#include "y.tab.h"
%}

%%
[0-9]+(\.[0-9]+)?    { yylval.fval = atof(yytext); return NUM; }
[\+\-\*/\(\)]       { return yytext[0]; }
[ \t\n]+             { /* Ignorar espacios y saltos de línea */ }
.                    { printf("Carácter no reconocido: %s\n", yytext); }
%%

int yywrap() { return 1; }