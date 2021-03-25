# SAT-Solver-Race
Sat solver race amb el joe

### Benchmarks

Hem creat els benchmarks d'aproximadament 90 kbs, amb 300 variables i 300 clausules de 70 variables.

```bash
for i in {1..5}; do ./rnd-cnf-gen.py 300 300 70 > benchmarks/b$i.cnf; done
```

> Per crear testos més facils

```bash
for i in {1..5}; do ./rnd-cnf-gen.py $(($i*2)) $(($i*2)) $(($i*2)) > tests/t$i.cnf; done
```



