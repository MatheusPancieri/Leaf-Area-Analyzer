Aqui está um **README.md** pronto para acompanhar seu script de cálculo de área foliar:

```markdown
# 📏 Cálculo de Área Foliar com Calibração Automática

Este script em **Python** calcula a área foliar antes e depois da herbivoria utilizando uma **barra vermelha de referência (5 cm)** presente na foto.  
A calibração é feita automaticamente a partir da largura detectada da barra, permitindo converter pixels em unidades reais (cm²).

---

## 🚀 Funcionalidades
- Leitura e conversão de imagens (OpenCV).
- Detecção automática da barra vermelha para calibração de escala.
- Segmentação da folha usando faixa de verde em HSV.
- Cálculo da área em **pixels²** e **cm²**.
- Relatório em **CSV** com:
  - Área antes da herbivoria.
  - Área depois da herbivoria.
  - Perda em cm² e percentual.

---

## 📂 Estrutura esperada
Coloque na mesma pasta:
```

├── script.py                # Este código
├── antes.jpg                # Imagem da folha intacta
├── depois.jpg               # Imagem da folha após herbivoria

````

---

## ⚙️ Dependências
Instale as bibliotecas necessárias com:
```bash
pip install opencv-python numpy matplotlib
````

---

## ▶️ Como usar

Execute o script no terminal:

```bash
python script.py
```

### Saída no console:

* Área da folha antes e depois.
* Perda por herbivoria (cm² e %).
* Largura da barra detectada (em pixels).

### Relatório gerado:

Um arquivo `relatorio_area_folha.csv` será criado contendo:

```
imagem,area_px,area_cm2
antes.jpg,123456,45.678900
depois.jpg,112233,41.234500
perda_cm2,,4.444400
perda_percentual,,9.730
```

---

## ⚠️ Observações

* Se a barra vermelha não for detectada automaticamente (condições de luz/foto ruim), ajuste a variável:

  ```python
  FORCAR_LARGURA_PX = <valor_em_pixels>
  ```
* Para melhor resultado:

  * Use fundo contrastante.
  * Certifique-se de que a barra vermelha esteja visível e não sombreada.
  * Evite reflexos na folha.

---

## 🛠️ Tecnologias

* [OpenCV](https://opencv.org/) → processamento de imagens.
* [NumPy](https://numpy.org/) → cálculos matriciais.
* [Matplotlib](https://matplotlib.org/) → visualização.
* CSV nativo do Python para relatórios.

---

## 📌 Exemplo de execução

```
Processando ANTES...
Processando DEPOIS...

...::: RESULTADO FINAL :::...
Barra (px) ANTES/DEPOIS: 250px / 252px  (referência = 5.0 cm)
Área da folha ANTES : 123456px² -> 45.68 cm²
Área da folha DEPOIS: 112233px² -> 41.23 cm²
Perda por herbivoria : 4.44 cm² (9.7%)

CSV salvo em: /caminho/relatorio_area_folha.csv
```

---

## 📖 Licença

Este projeto é de uso acadêmico/científico.
Fique à vontade para adaptar e melhorar conforme necessário.

```

---

Quer que eu também gere um **fluxograma simples em imagem** (tipo diagrama) mostrando as etapas do processo (input → detecção barra → segmentação → cálculo → CSV)? Isso pode enriquecer bastante seu README.
```
