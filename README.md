# 📘 Reconhecimento de Sinais em Libras com IA (Python + OpenCV + MediaPipe)

Projeto **simples e de baixo custo** para **capturar (treinar)** e **reconhecer (detectar)** sinais em **Libras** usando apenas **webcam + IA** (OpenCV + MediaPipe).  
> **Destaque:** Este projeto recebeu **destaque no Samsung Innovation Campus (Programação Python e Introdução à IA)** e foi **avaliado por professores da USP**.

## 💡 Problema que resolvemos
Como tornar **acessível** o reconhecimento de sinais de Libras **sem luvas especiais ou sensores caros**?  
Aqui, você **coleta seus próprios exemplos** (CSV com landmarks das mãos) e o sistema **reconhece em tempo real** comparando o que a câmera vê com o que já foi gravado.

---

## 🚀 Funcionalidades
- **Treinamento (`treino.py`)**: captura landmarks (21 pontos por mão) via webcam e **salva em CSV** por **sinal** e **etapa**.
- **Detecção (`deteccao.py`)**: lê os CSVs, **compara** com a pose atual e **exibe o rótulo** do sinal mais provável.
- **Visualização**: desenha e numera os landmarks (OpenCV + MediaPipe) para orientar o posicionamento da mão.

---
## 🧠 Como funciona (resumo)

1. **MediaPipe Hands** retorna **21 landmarks** por mão (coordenadas normalizadas X/Y/Z).
2. **Treino (`coletagem.py`)**: você grava **várias amostras** por **sinal**.  
   - Para **sinais simples** (gesto estático) → basta **1 etapa**.  
   - Para **sinais que exigem mais de um movimento** (ex.: gestos compostos em Libras) → use **múltiplas etapas**, registrando cada parte do gesto.
   - Todos os dados são salvos em **CSV**.
3. **Detecção em tempo real (`main.py`)**: a cada frame da webcam, o sistema extrai os mesmos pontos e **compara** com as amostras salvas  
   (ex.: **distância euclidiana**, **DTW** ou **k-NN simples**).
4. O **rótulo** com **menor distância média** (ou melhor score) é exibido na tela.

---

### ▶️ Execução (bem simples)

1) Abra o terminal na pasta do projeto.  

2) Para **treinar/coletar** os sinais:
```bash
run python file coletagem.py

Para **detectar em tempo real**:
```bash
run python file coletagem.py

---

## 🛠️ Tecnologias
- **Python 3.10+**
- **OpenCV** (`opencv-python`)
- **MediaPipe** (`mediapipe`)
- **NumPy** e **Pandas**
- **CSV** (armazenamento leve e portátil, não sendo necessário a configuração de um banco de dados)

---

## 📦 Instalação

### 0) Clonar o projeto
```bash
git clone https://github.com/seu-usuario/libras-mediapipe-opencv.git
pip install opencv-python mediapipe numpy pandas
run python file