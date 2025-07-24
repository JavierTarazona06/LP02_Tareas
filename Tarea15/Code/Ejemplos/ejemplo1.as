ICARGA 4, 0    ; sum = 0
ICARGA 5, 1    ; i = 1
ICARGA 6, 6    ; n = 6

LOOP:
SUMA 4, 5      ; sum += i
INCRE 5        ; i++
COMP 5, 6      ; i ? n
SIMENOR LOOP   ; si i <= n vuelve
GUARD 4, 131072 ; guarda suma
PARA