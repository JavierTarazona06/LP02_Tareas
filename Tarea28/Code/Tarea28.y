%{
#include <stdio.h>
#include <stdlib.h>
void yyerror(const char *s);
%}

%union {
    float fval;
}

%token <fval> NUM
%left '+' '-'
%left '*' '/'
%right NEG 

%%
input: 
     | input line
     ;

line: '\n'
    | expr '\n'  { printf("Resultado: %f\n", $1); }
    ;

expr: NUM            { $$ = $1; }
    | expr '+' expr  { $$ = $1 + $2; }
    | expr '-' expr  { $$ = $1 - $2; }
    | expr '*' expr  { $$ = $1 * $2; }
    | expr '/' expr  { $$ = $1 / $2; }
    | '(' expr ')'   { $$ = $2; }
    | '-' expr %prec NEG { $$ = -$2; }
    ;
%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    printf("Ingrese una expresión matemática:\n");
    yyparse();
    return 0;
}
