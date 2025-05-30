import os
import time
import tempfile
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="OCR Benchmark Dashboard",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Sidebar – parâmetros
st.sidebar.header("Configuração")

INPUT_SIZES = [(320, 320), (640, 640), (960, 960), (1280, 1280)]
input_size = st.sidebar.selectbox("Input Size (px)", INPUT_SIZES,
                                  format_func=lambda s: f"{s[0]}×{s[1]}")

iterations = st.sidebar.number_input("Iterações por modelo",
                                     min_value=1, max_value=50,
                                     value=10, step=1)

st.sidebar.subheader("Upload dos modelos (opcional)")
east_up = st.sidebar.file_uploader("EAST (.pb)", type=["pb"])
db18_up = st.sidebar.file_uploader("DB-ResNet18 (.onnx)", type=["onnx"])
db50_up = st.sidebar.file_uploader("DB-ResNet50 (.onnx)", type=["onnx"])

st.sidebar.subheader("Imagem de teste")
uploaded_img = st.sidebar.file_uploader("Enviar imagem", type=["jpg", "jpeg", "png"])
visuals_path = Path("./visuals")
example_files = [f.name for f in visuals_path.glob("*") if f.suffix.lower() in {".jpg", ".jpeg", ".png"}]
example_img = st.sidebar.selectbox("Exemplo local", example_files) if example_files else None

run_btn = st.sidebar.button("Executar")

# Funções utilitárias
def temp_save(file_obj, suffix):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(file_obj.read())
    tmp.flush()
    return tmp.name

def detect_and_time(detector, img):
    start = time.perf_counter()
    boxes, _ = detector.detect(img)
    return boxes, time.perf_counter() - start

def draw_polys(img, boxes, color):
    cv2.polylines(img, boxes, True, color, 4)
    return img

# Execução principal
if run_btn:
    # Carregamento da imagem
    if uploaded_img:
        img_pil = Image.open(uploaded_img).convert("RGB")
        img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    elif example_img:
        img = cv2.imread(str(visuals_path / example_img))
    else:
        st.error("Nenhuma imagem fornecida.")
        st.stop()

    if img is None:
        st.error("Falha ao carregar imagem.")
        st.stop()

    modelos_presentes = all([east_up, db18_up, db50_up])

    if not modelos_presentes:
        st.info("Modelos não enviados. Exibindo somente a imagem.")
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), use_column_width=True)
        st.stop()

    # Persistência temporária dos modelos
    east_path = temp_save(east_up, ".pb")
    db18_path = temp_save(db18_up, ".onnx")
    db50_path = temp_save(db50_up, ".onnx")

    # Carregamento dos modelos
    try:
        east  = cv2.dnn_TextDetectionModel_EAST(east_path)
        db18  = cv2.dnn_TextDetectionModel_DB(db18_path)
        db50  = cv2.dnn_TextDetectionModel_DB(db50_path)
    except cv2.error as e:
        st.error(f"Falha ao carregar modelos: {e}")
        st.stop()

    # Parâmetros
    east.setConfidenceThreshold(0.8).setNMSThreshold(0.4)
    db18.setBinaryThreshold(0.3).setPolygonThreshold(0.5)
    db50.setBinaryThreshold(0.3).setPolygonThreshold(0.5)
    MEAN_DB = (122.67891434, 116.66876762, 104.00698793)
    east.setInputParams(1.0, input_size, (123.68, 116.78, 103.94), True)
    db18.setInputParams(1.0/255, input_size, MEAN_DB, True)
    db50.setInputParams(1.0/255, input_size, MEAN_DB, True)

    detectors = {"EAST": east, "DB18": db18, "DB50": db50}

    # Benchmark
    timings = {"Modelo": [], "Iteração": [], "Tempo (s)": []}
    progress = st.progress(0, text="Benchmarking…")

    for i in range(iterations):
        for name, det in detectors.items():
            _, t = detect_and_time(det, img)
            timings["Modelo"].append(name)
            timings["Iteração"].append(i+1)
            timings["Tempo (s)"].append(t)
        progress.progress((i+1)/iterations)

    df = pd.DataFrame(timings)
    summary = df.groupby("Modelo")["Tempo (s)"].agg(["mean", "std"]).reset_index()

    col1, col2 = st.columns([1,2], gap="large")
    with col1:
        st.subheader("Tempo médio ± σ (s)")
        st.dataframe(summary.style.format({"mean":"{:.4f}","std":"{:.4f}"}))
    with col2:
        fig, ax = plt.subplots()
        ax.bar(summary["Modelo"], summary["mean"], yerr=summary["std"], capsize=4)
        ax.set_ylabel("Tempo (s)")
        ax.set_title(f"Input {input_size[0]}×{input_size[1]} – {iterations} it.")
        st.pyplot(fig)

    # Detecção e visualização
    boxes_east,_ = east.detect(img)
    boxes_db18,_ = db18.detect(img)
    boxes_db50,_ = db50.detect(img)

    vis = cv2.hconcat([
        img,
        draw_polys(img.copy(),boxes_east,(255,0,255)),
        draw_polys(img.copy(),boxes_db18,(0,255,0)),
        draw_polys(img.copy(),boxes_db50,(0,255,255))
    ])
    st.subheader("Original | EAST | DB18 | DB50")
    st.image(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB), use_column_width=True)

    # Download
    out_path = Path(tempfile.gettempdir()) / "resultado_benchmark.jpg"
    cv2.imwrite(str(out_path), vis)
    with open(out_path, "rb") as f:
        st.download_button("Download resultado", data=f,
                           file_name="resultado_benchmark.jpg",
                           mime="image/jpeg")

    # Limpeza
    for p in (east_path, db18_path, db50_path):
        try: os.remove(p)
        except OSError: pass
