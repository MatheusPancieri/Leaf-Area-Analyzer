````markdown
# 🌿 Leaf Area Measurement with Automatic Calibration

Script em **Python** para calcular a área de folhas antes e depois da herbivoria.  
Ele usa uma **barra vermelha de 5 cm** na foto como referência para converter pixels em cm².

---

##  O que faz
- Detecta automaticamente a barra vermelha (ou define manualmente).
- Segmenta a folha (verde em HSV).
- Calcula a área em **pixels²** e **cm²**.
- Gera relatório em **CSV** com perda de área e percentual.

---

## ⚙ Instalação
Instale as dependências:
```bash
pip install opencv-python numpy matplotlib
````

---

##  Como usar

Coloque na pasta:

```
antes.jpg   # folha intacta
depois.jpg  # folha após herbivoria
```

Rode:

```bash
python script.py
```

---

## Saída

* Mostra área antes/depois no terminal.
* Cria o arquivo `relatorio_area_folha.csv` com os resultados.

Exemplo:

```
Área ANTES : 45.68 cm²
Área DEPOIS: 41.23 cm²
Perda      : 4.44 cm² (9.7%)
```

---

## Observações

* Se a barra não for detectada, ajuste `FORCAR_LARGURA_PX`.
* Fotos claras e sem reflexo dão melhor resultado.

```
