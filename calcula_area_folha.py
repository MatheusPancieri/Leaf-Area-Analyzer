# Script para cálculo de área foliar com calibração automática
# Calcula área antes/depois da herbivoria usando barra vermelha de 5cm como referência

import cv2          # Processamento de imagens
import numpy as np   # Arrays e cálculos matemáticos
import matplotlib.pyplot as plt # Visualização
import os           # Sistema de arquivos
import sys          # Controle do programa
import csv          # Relatórios CSV

# Configurações
LARGURA_BARRA_CM = 5.0 # Largura real da barra vermelha (5cm)
FORCAR_LARGURA_PX = 0  # 0 = detecção automática, >0 = valor fixo

def ler_imagens(caminho: str):
    """Carrega imagem e converte BGR->RGB para visualização"""
    img_bgr = cv2.imread(caminho)
    if img_bgr is None:
        raise FileNotFoundError(f"Não encontrei '{caminho}'.")
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return img_bgr, img_rgb

def processar_imagem(caminho: str,
                     largura_barra_cm: float = LARGURA_BARRA_CM,
                     forcar_largura_px: int = FORCAR_LARGURA_PX,
                     mostrar_figuras: bool = True):
    """Processa imagem e calcula área da folha. Retorna (area_px, area_cm2, largura_barra_px)"""
    
    # Carregar imagem e converter para HSV
    img_bgr, img_rgb = ler_imagens(caminho)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Detectar barra vermelha (vermelho está nas duas extremidades do HSV)
    m1 = cv2.inRange(hsv, (0, 80, 60), (10, 255, 255))      # Vermelho claro
    m2 = cv2.inRange(hsv, (170, 80, 60), (179, 255, 255))   # Vermelho escuro
    mask_red = cv2.bitwise_or(m1, m2)

    # Encontrar contornos e medir barra vermelha
    cnts, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if forcar_largura_px > 0:
        # Usar largura forçada
        LARGURA_BARRA_PX = int(forcar_largura_px)
        x = y = 0
        w = LARGURA_BARRA_PX
        h = 0
    else:
        # Detecção automática
        if not cnts:
            raise RuntimeError("Barra vermelha não encontrada. Ajuste foto/iluminação ou defina FORCAR_LARGURA_PX > 0.")
        
        c = max(cnts, key=cv2.contourArea)  # Maior contorno = barra vermelha
        x, y, w, h = cv2.boundingRect(c)
        LARGURA_BARRA_PX = int(w)

    # Visualizar barra detectada
    img_barr = img_rgb.copy()
    if w > 0 and h >= 0:
        cv2.rectangle(img_barr, (x,y), (x+w,y+h), (0, 255, 0), 2)

    if mostrar_figuras:
        plt.figure(figsize=(6,4))
        plt.title(f"Barra vermelha detectada - {os.path.basename(caminho)}")
        plt.imshow(img_barr)
        plt.axis('off')
        plt.show()

    # Calibrar pixels para mm e segmentar folha
    px_por_mm = LARGURA_BARRA_PX / (largura_barra_cm * 10.0)

    # Detectar folha (faixa de verde HSV)
    lower_green = np.array([35, 25, 25], np.uint8)
    upper_green = np.array([85, 255, 255], np.uint8)
    mask_leaf = cv2.inRange(hsv, lower_green, upper_green)

    # Limpeza morfológica da máscara
    k = np.ones((5,5), np.uint8)
    mask_leaf = cv2.morphologyEx(mask_leaf, cv2.MORPH_OPEN, k, iterations=1)   # Remove ruídos
    mask_leaf = cv2.morphologyEx(mask_leaf, cv2.MORPH_CLOSE, k, iterations=1)  # Preenche buracos

    # Calcular área da folha
    area_px = int(np.count_nonzero(mask_leaf))  # Contar pixels brancos
    area_mm2 = area_px /(px_por_mm ** 2)        # Converter para mm²
    area_cm2 = area_mm2 / 100.0                 # Converter para cm²

    # Visualizar folha segmentada
    if mostrar_figuras:
        plt.figure(figsize=(6,4))
        plt.title(f"Folha Segmentada (HSV) - {os.path.basename(caminho)}\nBarra = {LARGURA_BARRA_PX}px ↔ {largura_barra_cm}cm")
        plt.imshow(mask_leaf, cmap='gray')
        plt.axis('off')
        plt.show()

    return area_px, area_cm2, LARGURA_BARRA_PX

def salvar_csv(resultados, caminho_csv="relatorio_area_folha.csv"):
    """Salva resultados em CSV com dados antes/depois e métricas de perda"""
    with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["imagem", "area_px", "area_cm2"])
        w.writerow(["antes.jpg", resultados["antes"][0], f"{resultados['antes'][1]:.6f}"])
        w.writerow(["depois.jpg", resultados["depois"][0], f"{resultados['depois'][1]:.6f}"])
        
        perda_cm2 = max(0.0, resultados["antes"][1] - resultados["depois"][1])
        perda_pct = (perda_cm2 / resultados["antes"][1] * 100.0) if resultados["antes"][1] > 0 else 0.0
        
        w.writerow(["perda_cm2", "", f"{perda_cm2:.6f}"])
        w.writerow(["perda_percentual", "", f"{perda_pct:.3f}"])

    print(f"\nCSV salvo em: {os.path.abspath(caminho_csv)}")

def main():
    """Executa pipeline completo: processa antes/depois, calcula perda e salva CSV"""
    
    caminho_antes = "antes.jpg"
    caminho_depois = "depois.jpg"

    # Validar arquivos
    if not os.path.exists(caminho_antes) or not os.path.exists(caminho_depois):
        print("[ERRO] Coloque 'antes.jpg' e 'depois.jpg' na mesma pasta deste script.", file=sys.stderr)
        sys.exit(1)

    # Processar imagens
    print("Processando ANTES...")
    area_px_a, area_cm2_a, wpx_a = processar_imagem(caminho_antes)

    print("Processando DEPOIS...")
    area_px_d, area_cm2_d, wpx_d = processar_imagem(caminho_depois)

    # Calcular perda
    perda_cm2 = max(0.0, area_cm2_a - area_cm2_d)
    perda_pct = (perda_cm2 / area_cm2_a * 100.0) if area_cm2_a > 0 else 0.0

    # Exibir resultados
    print("\n...::: RESULTADO FINAL :::...")
    print(f"Barra (px) ANTES/DEPOIS: {wpx_a}px / {wpx_d}px  (referência = {LARGURA_BARRA_CM} cm)")
    print(f"Área da folha ANTES : {area_px_a}px² -> {area_cm2_a:.2f} cm²")
    print(f"Área da folha DEPOIS: {area_px_d}px² -> {area_cm2_d:.2f} cm²")
    print(f"Perda por herbivoria : {perda_cm2:.2f} cm² ({perda_pct:.1f}%)")

    # Salvar CSV
    salvar_csv({"antes": (area_px_a, area_cm2_a),
                "depois": (area_px_d, area_cm2_d)})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERRO] {e}", file=sys.stderr)
        sys.exit(1)
