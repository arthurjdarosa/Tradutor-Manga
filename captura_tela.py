import ctypes
import os
import re
import threading
import time
import tkinter as tk
import cv2
import mss
import numpy as np
from PIL import Image
import pytesseract
import argostranslate.translate

# Força resolução real no Windows para a janela não encolher
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# Caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Coordenadas calibradas do quadro de captura
LARGURA = 900
ALTURA = 860
POS_X = 50
POS_Y = 180

bbox_captura = {
    "top": POS_Y,
    "left": POS_X,
    "width": LARGURA,
    "height": ALTURA
}

def processar_recorte(frame_bgra):
    gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

    # 1. Upscale para melhorar nitidez das fontes
    ampliado = cv2.resize(gray, (0, 0), fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    # 2. Respiro branco nas bordas
    padded = cv2.copyMakeBorder(ampliado, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    # 3. Binarização Otsu para contraste do texto
    _, binarizada = cv2.threshold(padded, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img_pil = Image.fromarray(binarizada)

    # PSM 3: analisa o quadro todo como uma página (ideal para livros, artigos e mangás)
    config_tesseract = r'--oem 3 --psm 3'
    texto_bruto = pytesseract.image_to_string(img_pil, lang="eng", config=config_tesseract)

    # Limpeza de ruídos e quebras de linha artificiais
    linhas = [re.sub(r'[\\|/_~]+', ' ', linha).strip() for linha in texto_bruto.split('\n')]
    paragrafos = [l for l in linhas if len(l) > 2 and any(c.isalpha() for c in l)]

    if not paragrafos:
        return

    texto_completo = " ".join(paragrafos)

    os.system('cls' if os.name == 'nt' else 'clear')
    print("📖 Texto detectado no quadro:\n" + "="*50)
    print(f"EN: {texto_completo}\n")

    try:
        texto_pt = argostranslate.translate.translate(texto_completo, "en", "pt")
        print(f"PT: {texto_pt}")
    except Exception:
        pass
    print("="*50)

def loop_monitoramento():
    print("Monitorando a área vermelha automaticamente ao rolar...")
    with mss.mss() as sct:
        ultimo_frame_gray = None

        while True:
            screenshot = sct.grab(bbox_captura)
            frame = np.array(screenshot)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

            if ultimo_frame_gray is not None:
                diff = cv2.absdiff(frame_gray, ultimo_frame_gray)
                mudanca = np.mean(diff)

                # Dispara leitura após parar de rolar
                if mudanca > 4.0:
                    time.sleep(0.35)
                    frame_estavel = np.array(sct.grab(bbox_captura))
                    processar_recorte(frame_estavel)
                    ultimo_frame_gray = cv2.cvtColor(frame_estavel, cv2.COLOR_BGRA2GRAY)
            else:
                processar_recorte(frame)
                ultimo_frame_gray = frame_gray

            time.sleep(0.2)

# Interface visual da moldura vermelha
root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "black")
root.geometry(f"{LARGURA}x{ALTURA}+{POS_X}+{POS_Y}")

canvas = tk.Canvas(root, width=LARGURA, height=ALTURA, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

canvas.create_rectangle(
    2, 2, LARGURA - 2, ALTURA - 2,
    outline="red",
    width=3
)

# Fecha a aplicação clicando com o botão direito na linha vermelha
canvas.bind("<Button-3>", lambda e: os._exit(0))

# Thread paralela para OCR sem travar o Tkinter
thread = threading.Thread(target=loop_monitoramento, daemon=True)
thread.start()

root.mainloop()