# Two Phase Simplex
Implementação básica do Simplex de duas fases para programações do tipo Ax ≤ b e x ≥ 0

### Entrada
n m  
c<sub>1</sub> ... c<sub>m</sub>  
a<sub>11</sub> ... a<sub>1m</sub>   b<sub>1</sub>  
               .  
               .  
               .  
a<sub>n1</sub> ... a<sub>nm</sub>   b<sub>n</sub>

### Saída
3 saídas possíveis:
1) "Otima" + valor ótimo + solução + certificado de otimalidade
2) "Inviavel" + certificado de inviabilidade 
3) "Ilimitada" + solução viável + certificado de ilimitada
