# Bicliotecas

imports ctypes: Módulo nativo do python usado para conversar direto com a API do Windows. Ele ajusta a resolução para evitar que a caixa vermelha encolha em telas com escala e zoom ativado

import os: Interagir com o sistema operacional

import re: Módulo de expressão reguladores (RegEX), usado para fazer a limpeza de ruídos e caracteres estranhos do texto extraído

import threading: Permite criar uma thread paralela no processador para rodar o OCR no fundo sem travar a interface do Tkinter

import time: Módulo nativo para controlar o tempo (usando nas pausas para esperar a tela parar de se mexer)

import tkinter as tk: Biblioteca nativa do Python para criar a interface grafica (a janela com a borda vermelha)

import cv2: Biblioteca do OpenCV usada para manipular e tratar as imagens (converter para cinza, dar zoom, binarizar e comparar telas)

import mss: Biblioteca de alta velocidade focada em tirar capturas de tela super rapidas

import numpy as np: Biblioteca de computação numerica. O OpenCV e o MSS usam o NumPu para processar as imagens como matrizes de dados

from PIL import Imagem: Biblioteca Pillow usada para converter as matrizes do OpenCV no formato de imagem aceito pelo Tesseract

import pytesseract: Biblioteca que faz a ponte entre o Python e o motor do Tesseract OCR para ler o texto das imagens

import argostranslate.translate: Biblioteca de tradução offline que traduz do ingles para um portugues de portugal ou cortez direto no computador sem precisar de internet ou API que essa é a proposta para ler um manga de boa.

# Configurações Iniciais e Calibração

ctypes.windll...: Ajuste de DPI do Windows força o sistema a usar os pixels reais da tela para que a caixa vermelha não fique minuscula em monitores com zoom 

pytesseract...tesseract_cmd: Aposta o caminho exato no Windows aonde o executavel do Tesseract OCR esta instalado

LARGURA, ALTURA, POS_X, POS_Y: Posição e tamanho da área da tela que vai ser usada

bbox_captura: Dicionario que guarda as coordenadas da área da tela no formato exato que a biblioteca mss exige para tirar a foto

# Função de processamento (processar_recorte)

cv2.cvtColor(...,cv2.COLOR_BGRA2GRAY): Transforma a imagem colorida em escala de cinza para facilitar a leitura do OCR

1.Upscale(cv2.resize): Aumenta a imagem de 1.5(fx=1.5, fy=1.5) para dar mais nitidez e detalhe as letras

2.Borda(cv2.copyMakeBorder): Adiciona uma margem de 20 pixels brancos ao redor da imagem para garantir que o Tesseract não corte textos colados no canto

3.Binarização Otsu(cv2.threshold): Transforma a imagem em preto e branco puro. O texto vira preto e o fundo vira branco, gerando contraste maximo

config_tesseract(--oem 3 --psm 3): Configuração do Tesseract (PSM 3 analisa o quadro como uma pagina completa, otimo para ler mangas)

Limpeza com RegEx(re.sub):Remove caracteres inuteis (como barras e acentos soltos) e ignora linhas que não contêm palavras reais

os.system('cls'): Limpa o terminal antes de exibir a nova leitura 

argostranslate...translate: Pega o texto limpo em ingles e traduz direto para o portugues exibindo tudo no terminal

# Loop de monitoramento Automatico (loop_monitoramento)


