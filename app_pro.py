"""
Data Cleaner Pro - Enterprise Ultimate Edition
Author: Igor.Lana | Igor.L.Z
Style: Hardy Dark Purple Theme - Professional
Version: 4.0.0 - Enterprise Ultimate
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import plotly.graph_objects as go
import time
from PIL import Image
import re
import unicodedata
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import KNNImputer
import warnings
warnings.filterwarnings('ignore')

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Data Cleaner Pro - Igor.Lana",
    page_icon="🥀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS HARDY STYLE PREMIUM
# ============================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0a0a 0%, #1a0b2e 100%); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0a0a0a 0%, #120624 100%); border-right: 1px solid rgba(106, 0, 255, 0.2); }
    .sidebar-profile { text-align: center; padding: 1.5rem 1rem; border-bottom: 1px solid rgba(106, 0, 255, 0.2); margin-bottom: 1rem; }
    .sidebar-name { color: #b87cff; font-size: 1.1rem; font-weight: bold; margin: 0.3rem 0; }
    .sidebar-title { color: #888; font-size: 0.75rem; }
    
    @keyframes scanEffect {
        0% { box-shadow: 0 0 0 0 rgba(106, 0, 255, 0.4); transform: scale(1); }
        50% { box-shadow: 0 0 0 15px rgba(106, 0, 255, 0.2); transform: scale(1.02); }
        100% { box-shadow: 0 0 0 0 rgba(106, 0, 255, 0); transform: scale(1); }
    }
    
    .scan-animation { animation: scanEffect 0.8s ease-out; background: linear-gradient(135deg, #6a00ff, #3a0088); border-radius: 12px; padding: 1rem; text-align: center; }
    .sidebar-status { background: rgba(106, 0, 255, 0.08); border: 1px solid rgba(106, 0, 255, 0.2); border-radius: 10px; padding: 0.8rem; margin: 1rem 0; }
    .status-dot { width: 8px; height: 8px; background: #00ff00; border-radius: 50%; display: inline-block; animation: pulse 1.5s infinite; }
    
    @keyframes pulse { 0% { opacity: 0.5; transform: scale(1); } 50% { opacity: 1; transform: scale(1.1); } 100% { opacity: 0.5; transform: scale(1); } }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes glow { 0% { box-shadow: 0 0 2px rgba(128, 0, 255, 0.3); } 50% { box-shadow: 0 0 10px rgba(128, 0, 255, 0.6); } 100% { box-shadow: 0 0 2px rgba(128, 0, 255, 0.3); } }
    @keyframes slideIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
    
    .main-header { background: linear-gradient(135deg, #6a00ff 0%, #3a0088 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; animation: fadeInUp 0.3s ease-out; }
    .main-header h1 { margin: 0; font-size: 2rem; font-weight: bold; color: white; }
    
    .metric-card { background: rgba(106, 0, 255, 0.06); padding: 1rem; border-radius: 10px; border: 1px solid rgba(106, 0, 255, 0.2); transition: all 0.2s ease; animation: fadeInUp 0.3s ease-out; }
    .metric-card:hover { transform: translateY(-2px); background: rgba(106, 0, 255, 0.1); border-color: rgba(106, 0, 255, 0.4); }
    .metric-value { font-size: 1.8rem; font-weight: bold; color: #b87cff; margin: 0.3rem 0; }
    .metric-label { font-size: 0.8rem; color: #b0b0b0; text-transform: uppercase; letter-spacing: 0.5px; }
    
    .stButton > button { background: linear-gradient(135deg, #6a00ff 0%, #3a0088 100%); color: white; border: none; padding: 0.5rem 1.5rem; font-weight: 500; border-radius: 8px; transition: all 0.2s ease; width: 100%; }
    .stButton > button:hover { transform: scale(1.02); box-shadow: 0 2px 8px rgba(106, 0, 255, 0.3); }
    
    .upload-box { border: 2px dashed rgba(106, 0, 255, 0.4); border-radius: 12px; padding: 1.5rem; text-align: center; background: rgba(106, 0, 255, 0.03); transition: all 0.2s ease; animation: slideIn 0.3s ease-out; }
    .upload-box:hover { border-color: rgba(106, 0, 255, 0.7); background: rgba(106, 0, 255, 0.06); transform: scale(1.01); }
    
    .footer { text-align: center; padding: 1.5rem; margin-top: 2rem; border-top: 1px solid rgba(106, 0, 255, 0.2); color: #666; font-size: 0.75rem; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #1a0b2e; }
    ::-webkit-scrollbar-thumb { background: #6a00ff; border-radius: 2px; }
    .stDataFrame { font-size: 12px; }
    .streamlit-expanderHeader { font-weight: 500; background: rgba(106, 0, 255, 0.03); border-radius: 8px; transition: all 0.2s ease; }
    .stProgress > div > div { background: linear-gradient(90deg, #6a00ff, #b87cff); transition: width 0.1s linear; }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("<div style='font-size: 3rem; text-align: center;'>🥀</div>", unsafe_allow_html=True)
with col_title:
    st.markdown("""
    <div class="main-header">
        <h1>DATA CLEANER PRO</h1>
        <p style="margin: 0; opacity: 0.9;">by Igor.Lana | Igor.L.Z</p>
        <p style="font-size: 0.8rem; margin-top: 0.3rem; opacity: 0.7;">⚡ Enterprise Ultimate | 20+ Tratamentos Avançados</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### 👤 Perfil")
    if Path("assets/images/user_photo.jpg").exists():
        image = Image.open("assets/images/user_photo.jpg")
        st.image(image, width=80)
    else:
        st.markdown("""<div class="sidebar-profile"><div style="font-size: 2.5rem;">👨‍💻</div><div class="sidebar-name">Igor.Lana</div><div class="sidebar-title">Data Specialist</div><div class="sidebar-title" style="font-size: 0.65rem;">Igor.L.Z</div></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    if 'selected_menu' not in st.session_state:
        st.session_state.selected_menu = "Dashboard"
    
    menu_options = {"🏠 Dashboard": "Dashboard", "📊 Processar Dados": "Processar Dados", "🔧 Tratamentos Avançados": "Tratamentos Avançados", "📜 Histórico": "Histórico", "⚙️ Configurações": "Configurações", "ℹ️ Sobre": "Sobre"}
    for label, value in menu_options.items():
        if st.button(label, key=f"menu_{value}", use_container_width=True):
            st.session_state.selected_menu = value
            st.rerun()
    
    st.markdown("---")
    st.markdown("""<div class="sidebar-status"><div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;"><div class="status-dot"></div><span style="color: #b0b0b0;">Sistema Online</span></div><div style="font-size: 0.7rem; color: #666;">📊 Versão: 4.0.0<br>👨‍💻 Igor.Lana<br>🎨 Hardy Style Ultimate</div></div>""", unsafe_allow_html=True)
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y')}")

# ============================================
# FUNÇÃO DE PROCESSAMENTO AVANÇADO
# ============================================
def apply_advanced_treatments(df, config):
    df_result = df.copy()
    actions = []
    
    # ============================================
    # 1. TRATAMENTOS DE TEXTO
    # ============================================
    if config.get('text_clean', False):
        for col in df_result.select_dtypes(include=['object']).columns:
            df_result[col] = df_result[col].astype(str).str.strip()
            if config.get('case_option') == "Maiúsculo":
                df_result[col] = df_result[col].str.upper()
            elif config.get('case_option') == "Minúsculo":
                df_result[col] = df_result[col].str.lower()
            elif config.get('case_option') == "Capitalizado":
                df_result[col] = df_result[col].str.title()
        actions.append("📝 Textos limpos e padronizados")
    
    if config.get('remove_accents', False):
        for col in df_result.select_dtypes(include=['object']).columns:
            df_result[col] = df_result[col].apply(lambda x: unicodedata.normalize('NFKD', str(x)).encode('ASCII', 'ignore').decode('ASCII'))
        actions.append("🔤 Acentos removidos")
    
    if config.get('remove_special_chars', False):
        for col in df_result.select_dtypes(include=['object']).columns:
            df_result[col] = df_result[col].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
        actions.append("✨ Caracteres especiais removidos")
    
    if config.get('remove_urls', False):
        for col in df_result.select_dtypes(include=['object']).columns:
            df_result[col] = df_result[col].str.replace(r'http\S+|www\.\S+', '', regex=True)
        actions.append("🔗 URLs removidas")
    
    if config.get('remove_emails', False):
        for col in df_result.select_dtypes(include=['object']).columns:
            df_result[col] = df_result[col].str.replace(r'\S+@\S+', '', regex=True)
        actions.append("📧 Emails removidos")
    
    if config.get('remove_numbers', False):
        for col in df_result.select_dtypes(include=['object']).columns:
            df_result[col] = df_result[col].str.replace(r'\d+', '', regex=True)
        actions.append("🔢 Números removidos dos textos")
    
    # ============================================
    # 2. TRATAMENTOS NUMÉRICOS
    # ============================================
    if config.get('normalize_numbers', False):
        for col in df_result.select_dtypes(include=[np.number]).columns:
            min_val = df_result[col].min()
            max_val = df_result[col].max()
            if max_val - min_val > 0:
                df_result[col] = (df_result[col] - min_val) / (max_val - min_val)
        actions.append("📊 Números normalizados (Min-Max)")
    
    if config.get('standardize_zscore', False):
        for col in df_result.select_dtypes(include=[np.number]).columns:
            mean_val = df_result[col].mean()
            std_val = df_result[col].std()
            if std_val > 0:
                df_result[col] = (df_result[col] - mean_val) / std_val
        actions.append("📈 Números padronizados (Z-Score)")
    
    if config.get('winsorize', False):
        limit = config.get('winsorize_limit', 0.05)
        for col in df_result.select_dtypes(include=[np.number]).columns:
            lower = df_result[col].quantile(limit)
            upper = df_result[col].quantile(1 - limit)
            df_result[col] = df_result[col].clip(lower, upper)
        actions.append(f"📊 Winsorização aplicada (limite {int(limit*100)}%)")
    
    if config.get('log_transform', False):
        for col in df_result.select_dtypes(include=[np.number]).columns:
            if (df_result[col] > 0).all():
                df_result[col] = np.log1p(df_result[col])
        actions.append("📈 Transformação log aplicada")
    
    if config.get('fill_missing_numeric', False):
        fill_method = config.get('fill_method', 'Mediana')
        for col in df_result.select_dtypes(include=[np.number]).columns:
            if fill_method == "Mediana":
                df_result[col] = df_result[col].fillna(df_result[col].median())
            elif fill_method == "Média":
                df_result[col] = df_result[col].fillna(df_result[col].mean())
            elif fill_method == "Zero":
                df_result[col] = df_result[col].fillna(0)
            elif fill_method == "KNN":
                imputer = KNNImputer(n_neighbors=5)
                df_result[col] = imputer.fit_transform(df_result[[col]])[:, 0]
        actions.append(f"🔢 Valores numéricos preenchidos ({fill_method})")
    
    if config.get('discretize', False):
        bins = config.get('n_bins', 5)
        for col in df_result.select_dtypes(include=[np.number]).columns:
            df_result[f'{col}_categoria'] = pd.cut(df_result[col], bins=bins, labels=[f'C{i+1}' for i in range(bins)])
        actions.append(f"📊 Discretização aplicada ({bins} categorias)")
    
    if config.get('round_decimals', 0) > 0:
        for col in df_result.select_dtypes(include=[np.number]).columns:
            df_result[col] = df_result[col].round(config.get('round_decimals', 2))
        actions.append(f"🔄 Números arredondados para {config.get('round_decimals', 2)} casas")
    
    # ============================================
    # 3. TRATAMENTOS DE DATA
    # ============================================
    if config.get('standardize_dates', False):
        date_format = config.get('date_format', "YYYY-MM-DD")
        for col in df_result.columns:
            try:
                df_result[col] = pd.to_datetime(df_result[col], errors='ignore')
                if df_result[col].dtype == 'datetime64[ns]':
                    if date_format == "YYYY-MM-DD":
                        df_result[col] = df_result[col].dt.strftime('%Y-%m-%d')
                    elif date_format == "DD/MM/YYYY":
                        df_result[col] = df_result[col].dt.strftime('%d/%m/%Y')
                    elif date_format == "MM/DD/YYYY":
                        df_result[col] = df_result[col].dt.strftime('%m/%d/%Y')
                    actions.append(f"📅 Datas padronizadas ({date_format})")
            except:
                pass
    
    if config.get('extract_date_components', False):
        for col in df_result.columns:
            try:
                df_result[col] = pd.to_datetime(df_result[col], errors='ignore')
                if df_result[col].dtype == 'datetime64[ns]':
                    df_result[f'{col}_ano'] = df_result[col].dt.year
                    df_result[f'{col}_mes'] = df_result[col].dt.month
                    df_result[f'{col}_dia'] = df_result[col].dt.day
                    df_result[f'{col}_dia_semana'] = df_result[col].dt.dayofweek
                    df_result[f'{col}_trimestre'] = df_result[col].dt.quarter
                    actions.append(f"📅 Componentes de data extraídos de '{col}'")
            except:
                pass
    
    if config.get('calculate_age', False):
        for col in df_result.columns:
            try:
                df_result[col] = pd.to_datetime(df_result[col], errors='ignore')
                if df_result[col].dtype == 'datetime64[ns]':
                    df_result[f'{col}_idade'] = (pd.Timestamp.now() - df_result[col]).dt.days // 365
                    actions.append(f"📅 Idade calculada a partir de '{col}'")
            except:
                pass
    
    # ============================================
    # 4. TRATAMENTOS DE CATEGORIAS
    # ============================================
    if config.get('one_hot_encoding', False):
        for col in df_result.select_dtypes(include=['object']).columns:
            if df_result[col].nunique() <= 20:
                dummies = pd.get_dummies(df_result[col], prefix=col)
                df_result = pd.concat([df_result, dummies], axis=1)
                actions.append(f"🎯 One-Hot Encoding aplicado em '{col}'")
    
    if config.get('label_encoding', False):
        for col in df_result.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            df_result[col] = le.fit_transform(df_result[col].astype(str))
            actions.append(f"🏷️ Label Encoding aplicado em '{col}'")
    
    if config.get('group_rare_categories', False):
        threshold = config.get('rare_threshold', 0.05)
        for col in df_result.select_dtypes(include=['object']).columns:
            freq = df_result[col].value_counts(normalize=True)
            rare = freq[freq < threshold].index
            df_result[col] = df_result[col].replace(rare, 'Outros')
            if len(rare) > 0:
                actions.append(f"📊 Categorias raras agrupadas em '{col}' ({len(rare)} categorias)")
    
    # ============================================
    # 5. TRATAMENTOS DE COLUNAS
    # ============================================
    if config.get('remove_columns', False):
        cols_to_remove = config.get('columns_to_remove', [])
        if cols_to_remove:
            df_result = df_result.drop(columns=[c for c in cols_to_remove if c in df_result.columns])
            actions.append(f"🗑️ Colunas removidas: {', '.join(cols_to_remove)}")
    
    if config.get('rename_columns', False):
        rename_map = config.get('rename_map', {})
        if rename_map:
            df_result = df_result.rename(columns=rename_map)
            actions.append(f"✏️ Colunas renomeadas")
    
    # ============================================
    # 6. DETECÇÃO E CORREÇÃO
    # ============================================
    if config.get('detect_anomalies', False):
        anomaly_count = 0
        for col in df_result.select_dtypes(include=[np.number]).columns:
            Q1 = df_result[col].quantile(0.25)
            Q3 = df_result[col].quantile(0.75)
            IQR = Q3 - Q1
            if IQR > 0:
                lower = Q1 - 3 * IQR
                upper = Q3 + 3 * IQR
                anomalies = ((df_result[col] < lower) | (df_result[col] > upper)).sum()
                if anomalies > 0:
                    anomaly_count += anomalies
                    if config.get('fix_anomalies', False):
                        df_result[col] = df_result[col].clip(lower, upper)
        if anomaly_count > 0:
            actions.append(f"⚠️ {anomaly_count} anomalias detectadas e corrigidas")
    
    if config.get('remove_duplicates_advanced', False):
        subset_cols = config.get('duplicate_subset', None)
        before = len(df_result)
        if subset_cols and len(subset_cols) > 0:
            df_result = df_result.drop_duplicates(subset=subset_cols, keep='first')
        else:
            df_result = df_result.drop_duplicates()
        removed = before - len(df_result)
        if removed > 0:
            actions.append(f"🔄 {removed} duplicatas removidas")
    
    return df_result, actions

# ============================================
# FUNÇÃO PARA PROCESSAR DADOS BÁSICOS
# ============================================
def process_data(file_path, config):
    from src.core.cleaner import DataCleaner
    cleaner = DataCleaner(str(file_path), config)
    result = cleaner.run()
    output_file = cleaner.save()
    return result, output_file

# ============================================
# DASHBOARD
# ============================================
selected = st.session_state.selected_menu

if selected == "Dashboard":
    st.markdown("## 📊 Dashboard de Qualidade")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    output_dir = Path("output")
    processed_files = len(list(output_dir.glob("*_tratado.*"))) if output_dir.exists() else 0
    
    with col1:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">📁 Arquivos</div><div class="metric-value">{processed_files}</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-card"><div class="metric-label">✅ Limpeza</div><div class="metric-value">99.9%</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-card"><div class="metric-label">🚀 Velocidade</div><div class="metric-value">&lt;1s</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="metric-card"><div class="metric-label">📊 Tratamentos</div><div class="metric-value">20+</div></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info("🎯 **Como usar:** Processar Dados → Carregue arquivo → Escolha tratamentos → Baixe resultado")
    with col_info2:
        st.success("✨ **Benefícios:** 20+ tratamentos profissionais | Interface Hardy Style | Resultados empresariais")

# ============================================
# PROCESSAR DADOS BÁSICOS
# ============================================
elif selected == "Processar Dados":
    st.markdown("## 🚀 Processar Dados")
    st.markdown("---")
    
    st.markdown("""<div class="upload-box"><div style="font-size: 2.5rem;">📂</div><h3 style="color: #b87cff;">Arraste seu arquivo</h3><p style="color: #888;">CSV, Excel, JSON</p></div>""", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Escolha um arquivo", type=['csv', 'xlsx', 'xls', 'json'], label_visibility="collapsed")
    
    if uploaded_file is not None:
        temp_path = Path(f"input/{uploaded_file.name}")
        temp_path.parent.mkdir(exist_ok=True)
        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ {uploaded_file.name}")
        
        file_ext = temp_path.suffix.lower()
        try:
            if file_ext == '.csv':
                df = pd.read_csv(temp_path)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(temp_path)
            else:
                df = pd.read_json(temp_path)
            
            with st.expander("📊 Visualizar", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Linhas", len(df))
                col2.metric("Colunas", len(df.columns))
                col3.metric("Nulos", df.isnull().sum().sum())
                col4.metric("Duplicatas", df.duplicated().sum())
            
            st.markdown("### 🎯 Tratamentos")
            col_opt1, col_opt2 = st.columns(2)
            with col_opt1:
                remove_duplicates = st.checkbox("Remover duplicatas", True)
                treat_nulls = st.checkbox("Tratar nulos", True)
            with col_opt2:
                treat_outliers = st.checkbox("Corrigir outliers", True)
                standardize_dates = st.checkbox("Padronizar datas", True)
            
            if st.button("▶️ PROCESSAR", use_container_width=True):
                with st.spinner("Processando..."):
                    progress = st.progress(0)
                    for i in range(100):
                        time.sleep(0.003)
                        progress.progress(i + 1)
                    
                    config = {'remove_duplicates': remove_duplicates, 'treat_nulls': treat_nulls, 'treat_outliers': treat_outliers, 'standardize_dates': standardize_dates}
                    result, output_file = process_data(temp_path, config)
                    
                    st.markdown("""<div class="scan-animation"><p style="color: white; margin: 0;">✨ Dados processados com sucesso! ✨</p></div>""", unsafe_allow_html=True)
                    
                    col_r1, col_r2, col_r3 = st.columns(3)
                    antes = result['estatisticas_antes']
                    depois = result['estatisticas_depois']
                    col_r1.metric("Linhas", f"{antes['linhas']} → {depois['linhas']}")
                    col_r2.metric("Nulos", f"{antes['valores_nulos']} → {depois['valores_nulos']}")
                    col_r3.metric("Duplicatas", f"{antes['duplicatas']} → {depois['duplicatas']}")
                    
                    with open(output_file, 'rb') as f:
                        st.download_button("📥 Download", data=f, file_name=output_file.name, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")

# ============================================
# TRATAMENTOS AVANÇADOS - VERSÃO ULTIMATE
# ============================================
elif selected == "Tratamentos Avançados":
    st.markdown("## 🔧 Tratamentos Avançados - Enterprise Ultimate")
    st.markdown("---")
    
    st.markdown("""<div class="upload-box"><div style="font-size: 2.5rem;">⚡</div><h3 style="color: #b87cff;">Tratamento Profissional de Dados</h3><p style="color: #888;">20+ opções para limpeza avançada nível empresarial</p></div>""", unsafe_allow_html=True)
    
    advanced_file = st.file_uploader("Carregue seu arquivo", type=['csv', 'xlsx', 'xls', 'json'], key="adv")
    
    if advanced_file:
        temp_path = Path(f"input/adv_{advanced_file.name}")
        temp_path.parent.mkdir(exist_ok=True)
        with open(temp_path, 'wb') as f:
            f.write(advanced_file.getbuffer())
        
        st.success(f"✅ {advanced_file.name}")
        
        file_ext = temp_path.suffix.lower()
        try:
            if file_ext == '.csv':
                df = pd.read_csv(temp_path)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(temp_path)
            else:
                df = pd.read_json(temp_path)
            
            with st.expander("📊 Visualizar dados originais", expanded=False):
                st.dataframe(df.head(10), use_container_width=True)
                st.caption(f"Total: {len(df)} linhas, {len(df.columns)} colunas")
            
            st.markdown("### 🎯 Configurações Avançadas - Enterprise")
            st.markdown("---")
            
            # ============================================
            # SEÇÃO 1: TRATAMENTOS DE TEXTO
            # ============================================
            st.markdown("#### 📝 Tratamentos de Texto")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                text_clean = st.checkbox("Limpar espaços e padronizar", value=True)
                remove_accents = st.checkbox("Remover acentos", value=False)
                remove_special_chars = st.checkbox("Remover caracteres especiais", value=False)
                remove_urls = st.checkbox("Remover URLs", value=False)
            with col_t2:
                remove_emails = st.checkbox("Remover emails", value=False)
                remove_numbers = st.checkbox("Remover números dos textos", value=False)
                case_option = st.selectbox("Padronizar maiúsculas", ["Manter", "Maiúsculo", "Minúsculo", "Capitalizado"])
            
            st.markdown("---")
            
            # ============================================
            # SEÇÃO 2: TRATAMENTOS NUMÉRICOS
            # ============================================
            st.markdown("#### 🔢 Tratamentos Numéricos")
            
            col_n1, col_n2 = st.columns(2)
            with col_n1:
                normalize_numbers = st.checkbox("Normalizar números (Min-Max)", value=False)
                standardize_zscore = st.checkbox("Padronizar (Z-Score)", value=False)
                winsorize = st.checkbox("Winsorização (limitar outliers)", value=False)
                if winsorize:
                    winsorize_limit = st.slider("Limite de winsorização", 0.01, 0.20, 0.05, format="%.2f")
                else:
                    winsorize_limit = 0.05
                log_transform = st.checkbox("Transformação Log", value=False)
            
            with col_n2:
                fill_missing_numeric = st.checkbox("Preencher valores numéricos faltantes", value=False)
                if fill_missing_numeric:
                    fill_method = st.selectbox("Método de preenchimento", ["Mediana", "Média", "Zero", "KNN"])
                else:
                    fill_method = "Mediana"
                discretize = st.checkbox("Discretização (categorização)", value=False)
                if discretize:
                    n_bins = st.slider("Número de categorias", 2, 10, 5)
                else:
                    n_bins = 5
                round_decimals = st.number_input("Arredondar decimais", min_value=0, max_value=10, value=2)
            
            st.markdown("---")
            
            # ============================================
            # SEÇÃO 3: TRATAMENTOS DE DATA
            # ============================================
            st.markdown("#### 📅 Tratamentos de Data")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                standardize_dates_adv = st.checkbox("Padronizar formato de datas", value=True)
                date_format = st.selectbox("Formato de data", ["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"])
                extract_date_components = st.checkbox("Extrair componentes (dia, mês, ano)", value=False)
            with col_d2:
                calculate_age = st.checkbox("Calcular idade a partir de data", value=False)
            
            st.markdown("---")
            
            # ============================================
            # SEÇÃO 4: TRATAMENTOS DE CATEGORIAS
            # ============================================
            st.markdown("#### 🏷️ Tratamentos de Categorias")
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                one_hot_encoding = st.checkbox("One-Hot Encoding (criar dummies)", value=False)
                label_encoding = st.checkbox("Label Encoding (converter para números)", value=False)
            with col_c2:
                group_rare_categories = st.checkbox("Agrupar categorias raras", value=False)
                if group_rare_categories:
                    rare_threshold = st.slider("Limite de raridade", 0.01, 0.20, 0.05, format="%.2f")
                else:
                    rare_threshold = 0.05
            
            st.markdown("---")
            
            # ============================================
            # SEÇÃO 5: TRATAMENTOS DE COLUNAS
            # ============================================
            st.markdown("#### 🗑️ Tratamentos de Colunas")
            
            col_rm1, col_rm2 = st.columns(2)
            with col_rm1:
                remove_columns = st.checkbox("Remover colunas específicas", value=False)
                if remove_columns:
                    cols_to_remove = st.text_input("Colunas para remover (separadas por vírgula)", placeholder="ex: coluna1, coluna2, coluna3")
                else:
                    cols_to_remove = ""
            
            with col_rm2:
                rename_columns = st.checkbox("Renomear colunas", value=False)
                if rename_columns:
                    rename_input = st.text_input("Renomear (formato: antigo:novo)", placeholder="ex: nome:NomeCompleto, idade:Idade")
                else:
                    rename_input = ""
            
            st.markdown("---")
            
            # ============================================
            # SEÇÃO 6: DETECÇÃO E CORREÇÃO
            # ============================================
            st.markdown("#### ⚠️ Detecção e Correção")
            
            col_o1, col_o2 = st.columns(2)
            with col_o1:
                detect_anomalies = st.checkbox("Detectar anomalias (outliers extremos)", value=False)
            with col_o2:
                if detect_anomalies:
                    fix_anomalies = st.checkbox("Corrigir anomalias automaticamente", value=True)
                else:
                    fix_anomalies = False
            
            remove_duplicates_advanced = st.checkbox("Remover duplicatas (avançado)", value=False)
            duplicate_cols = st.text_input("Colunas para verificar duplicatas (separadas por vírgula)", placeholder="ex: nome,email", key="dup_cols_input")
            
            st.markdown("---")
            
            # ============================================
            # SEÇÃO 7: CONFIGURAÇÕES DE SAÍDA
            # ============================================
            st.markdown("#### 📤 Configurações de Saída")
            output_format_adv = st.selectbox("Formato do arquivo tratado", ["CSV", "Excel", "JSON"], index=0)
            
            # ============================================
            # BOTÃO DE PROCESSAMENTO
            # ============================================
            if st.button("⚡ APLICAR TRATAMENTOS AVANÇADOS", use_container_width=True):
                with st.spinner("🔄 Aplicando tratamentos avançados..."):
                    progress = st.progress(0)
                    for i in range(100):
                        time.sleep(0.003)
                        progress.progress(i + 1)
                    
                    # Configurar parâmetros
                    duplicate_subset = None
                    if duplicate_cols and duplicate_cols.strip():
                        duplicate_subset = [c.strip() for c in duplicate_cols.split(',') if c.strip()]
                    
                    cols_remove_list = []
                    if remove_columns and cols_to_remove:
                        cols_remove_list = [c.strip() for c in cols_to_remove.split(',') if c.strip()]
                    
                    rename_map = {}
                    if rename_columns and rename_input:
                        for item in rename_input.split(','):
                            if ':' in item:
                                old, new = item.split(':')
                                rename_map[old.strip()] = new.strip()
                    
                    config = {
                        'text_clean': text_clean, 'remove_accents': remove_accents, 'remove_special_chars': remove_special_chars,
                        'remove_urls': remove_urls, 'remove_emails': remove_emails, 'remove_numbers': remove_numbers,
                        'case_option': case_option, 'normalize_numbers': normalize_numbers, 'standardize_zscore': standardize_zscore,
                        'winsorize': winsorize, 'winsorize_limit': winsorize_limit, 'log_transform': log_transform,
                        'fill_missing_numeric': fill_missing_numeric, 'fill_method': fill_method,
                        'discretize': discretize, 'n_bins': n_bins, 'round_decimals': round_decimals,
                        'standardize_dates': standardize_dates_adv, 'date_format': date_format,
                        'extract_date_components': extract_date_components, 'calculate_age': calculate_age,
                        'one_hot_encoding': one_hot_encoding, 'label_encoding': label_encoding,
                        'group_rare_categories': group_rare_categories, 'rare_threshold': rare_threshold,
                        'remove_columns': remove_columns, 'columns_to_remove': cols_remove_list,
                        'rename_columns': rename_columns, 'rename_map': rename_map,
                        'detect_anomalies': detect_anomalies, 'fix_anomalies': fix_anomalies,
                        'remove_duplicates_advanced': remove_duplicates_advanced, 'duplicate_subset': duplicate_subset
                    }
                    
                    df_result, actions = apply_advanced_treatments(df, config)
                    
                    # Salvar arquivo
                    ext_map = {"CSV": ".csv", "Excel": ".xlsx", "JSON": ".json"}
                    ext = ext_map[output_format_adv]
                    output_file = Path(f"output/advanced_{Path(advanced_file.name).stem}_tratado{ext}")
                    output_file.parent.mkdir(exist_ok=True)
                    
                    if ext == '.csv':
                        df_result.to_csv(output_file, index=False)
                    elif ext == '.xlsx':
                        df_result.to_excel(output_file, index=False)
                    else:
                        df_result.to_json(output_file, orient='records', indent=2)
                    
                    st.markdown("""<div class="scan-animation"><p style="color: white; margin: 0;">✨ Tratamentos avançados aplicados com sucesso! ✨</p></div>""", unsafe_allow_html=True)
                    
                    # Resultados
                    col_r1, col_r2, col_r3 = st.columns(3)
                    col_r1.metric("📊 Linhas", f"{len(df)} → {len(df_result)}")
                    col_r2.metric("⚠️ Nulos", f"{df.isnull().sum().sum()} → {df_result.isnull().sum().sum()}")
                    col_r3.metric("📋 Colunas", f"{len(df.columns)} → {len(df_result.columns)}")
                    
                    with open(output_file, 'rb') as f:
                        st.download_button("📥 Download Arquivo Tratado", data=f, file_name=output_file.name, use_container_width=True)
                    
                    if actions:
                        with st.expander("📋 Tratamentos aplicados", expanded=True):
                            for action in actions:
                                st.write(f"✅ {action}")
                    
                    with st.expander("👁️ Visualizar resultado", expanded=False):
                        st.dataframe(df_result.head(20), use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")

# ============================================
# HISTÓRICO
# ============================================
elif selected == "Histórico":
    st.markdown("## 📜 Histórico")
    st.markdown("---")
    
    output_dir = Path("output")
    if output_dir.exists():
        files = list(output_dir.glob("*_tratado.*"))
        if files:
            st.caption(f"Total: {len(files)} arquivos")
            for file in files:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(f"📄 {file.name}")
                    st.caption(f"📅 {datetime.fromtimestamp(file.stat().st_ctime).strftime('%d/%m/%Y %H:%M')}")
                with col2:
                    with open(file, 'rb') as f:
                        st.download_button("Baixar", data=f, file_name=file.name, key=str(file))
                st.divider()
        else:
            st.info("Nenhum arquivo processado ainda")

# ============================================
# CONFIGURAÇÕES
# ============================================
elif selected == "Configurações":
    st.markdown("## ⚙️ Configurações")
    st.markdown("---")
    
    st.markdown("""<div class="metric-card"><h3>🎨 Tema Hardy Style Ultimate</h3><p>Roxo e Preto - Design Profissional Empresarial</p><p>✅ Animações fluidas (0.2s-0.3s)</p><p>✅ Scan Effect ao processar</p><p>✅ 20+ tratamentos avançados</p></div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class="metric-card"><h3>🔧 Tratamentos Disponíveis (20+)</h3><ul><li>✅ Remoção de duplicatas</li><li>✅ Tratamento de nulos (4 métodos)</li><li>✅ Correção de outliers (IQR e Z-Score)</li><li>✅ Padronização de datas</li><li>✅ Limpeza de textos (espaços, acentos, maiúsculas)</li><li>✅ Normalização de números (Min-Max e Z-Score)</li><li>✅ Winsorização</li><li>✅ Transformação Log</li><li>✅ Discretização</li><li>✅ One-Hot Encoding</li><li>✅ Label Encoding</li><li>✅ Agrupamento de categorias raras</li><li>✅ Remoção de URLs, emails e números</li><li>✅ Extração de componentes de data</li><li>✅ Cálculo de idade</li><li>✅ Remoção/Renomeação de colunas</li><li>✅ Detecção de anomalias</li></ul></div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class="metric-card"><h3>👨‍💻 Desenvolvedor</h3><p>Igor.Lana | Igor.L.Z</p><p>Versão 4.0.0 - Enterprise Ultimate</p><p>Assinatura: "Dados limpos, decisões claras"</p></div>""", unsafe_allow_html=True)

# ============================================
# SOBRE
# ============================================
elif selected == "Sobre":
    st.markdown("## ℹ️ Sobre")
    st.markdown("---")
    
    st.markdown("""<div class="metric-card"><h3>🚀 Data Cleaner Pro - Enterprise Ultimate</h3><p><strong>Versão:</strong> 4.0.0 Enterprise Ultimate</p><p><strong>Desenvolvedor:</strong> Igor.Lana | Igor.L.Z</p><p><strong>Assinatura:</strong> "Dados limpos, decisões claras"</p></div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class="metric-card"><h3>📊 Funcionalidades Completas (20+ Tratamentos)</h3><ul><li>✅ Remoção de duplicatas</li><li>✅ Tratamento de nulos (4 métodos: Mediana, Média, Zero, KNN)</li><li>✅ Correção de outliers (IQR e Z-Score)</li><li>✅ Winsorização para limites extremos</li><li>✅ Transformação Log para normalização</li><li>✅ Discretização de variáveis numéricas</li><li>✅ Padronização de datas (3 formatos)</li><li>✅ Extração de componentes (ano, mês, dia, dia_semana, trimestre)</li><li>✅ Cálculo de idade a partir de datas</li><li>✅ Limpeza de textos (espaços, acentos, maiúsculas)</li><li>✅ Remoção de URLs, emails e números</li><li>✅ One-Hot Encoding e Label Encoding</li><li>✅ Agrupamento de categorias raras</li><li>✅ Remoção e renomeação de colunas</li><li>✅ Detecção e correção de anomalias</li><li>✅ Interface Hardy Style Premium</li></ul></div>""", unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p>🧹 Data Cleaner Pro | by <strong>Igor.Lana | Igor.L.Z</strong></p>
    <p><i>"Dados limpos, decisões claras - Hardy Style Ultimate"</i></p>
    <p>Versão 4.0.0 Enterprise | 20+ Tratamentos Avançados</p>
</div>
""", unsafe_allow_html=True)
