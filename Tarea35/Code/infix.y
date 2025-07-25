%{
#include <stdio.h>
#include <stdlib.h>
%}

%token NUMBER

%%
expr    : expr '+' term { printf("+ "); }
        | expr '-' term { printf("- "); }
        | term
        ;
        
term    : term '*' factor { printf("* "); }
        | term '/' factor { printf("/ "); }
        | factor
        ;

factor  : '(' expr ')'  
        | NUMBER { printf("%d ", $1); }
        ;

%%

int main() {
    printf("Ingrese una expresión en notación infija: ");
    yyparse();
    printf("\n");
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}
