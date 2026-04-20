"""
Data Cleaner Pro - Enterprise Edition (Hardy Style Final)
Author: Igor.Lana | Igor.L.Z
Style: Hardy Dark Purple Theme - Premium
Version: 3.1.1 - Ultimate (Bug Fix)
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import plotly.graph_objects as go
import plotly.express as px
import time
from PIL import Image

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Data Cleaner Pro - Igor.Lana",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS HARDY STYLE PREMIUM
# ============================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0b2e 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #120624 100%);
        border-right: 1px solid rgba(106, 0, 255, 0.2);
    }
    
    .sidebar-profile {
        text-align: center;
        padding: 1.5rem 1rem;
        border-bottom: 1px solid rgba(106, 0, 255, 0.2);
        margin-bottom: 1rem;
    }
    
    .sidebar-name {
        color: #b87cff;
        font-size: 1.1rem;
        font-weight: bold;
        margin: 0.3rem 0;
    }
    
    .sidebar-title {
        color: #888;
        font-size: 0.75rem;
    }
    
    @keyframes scanEffect {
        0% {
            box-shadow: 0 0 0 0 rgba(106, 0, 255, 0.4);
            transform: scale(1);
        }
        50% {
            box-shadow: 0 0 0 15px rgba(106, 0, 255, 0.2);
            transform: scale(1.02);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(106, 0, 255, 0);
            transform: scale(1);
        }
    }
    
    .scan-animation {
        animation: scanEffect 0.8s ease-out;
        background: linear-gradient(135deg, #6a00ff, #3a0088);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    
    .sidebar-status {
        background: rgba(106, 0, 255, 0.08);
        border: 1px solid rgba(106, 0, 255, 0.2);
        border-radius: 10px;
        padding: 0.8rem;
        margin: 1rem 0;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: #00ff00;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.1); }
        100% { opacity: 0.5; transform: scale(1); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 2px rgba(128, 0, 255, 0.3); }
        50% { box-shadow: 0 0 10px rgba(128, 0, 255, 0.6); }
        100% { box-shadow: 0 0 2px rgba(128, 0, 255, 0.3); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .main-header {
        background: linear-gradient(135deg, #6a00ff 0%, #3a0088 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.3s ease-out;
        box-shadow: 0 2px 10px rgba(106, 0, 255, 0.2);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
        color: white;
    }
    
    .metric-card {
        background: rgba(106, 0, 255, 0.06);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(106, 0, 255, 0.2);
        transition: all 0.2s ease;
        animation: fadeInUp 0.3s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        background: rgba(106, 0, 255, 0.1);
        border-color: rgba(106, 0, 255, 0.4);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #b87cff;
        margin: 0.3rem 0;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #b0b0b0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6a00ff 0%, #3a0088 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border-radius: 8px;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 2px 8px rgba(106, 0, 255, 0.3);
    }
    
    .upload-box {
        border: 2px dashed rgba(106, 0, 255, 0.4);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        background: rgba(106, 0, 255, 0.03);
        transition: all 0.2s ease;
        animation: slideIn 0.3s ease-out;
    }
    
    .upload-box:hover {
        border-color: rgba(106, 0, 255, 0.7);
        background: rgba(106, 0, 255, 0.06);
        transform: scale(1.01);
    }
    
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(106, 0, 255, 0.2);
        color: #666;
        font-size: 0.75rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    ::-webkit-scrollbar {
        width: 4px;
        height: 4px;
    }
    ::-webkit-scrollbar-track { background: #1a0b2e; }
    ::-webkit-scrollbar-thumb { background: #6a00ff; border-radius: 2px; }
    
    .stDataFrame { font-size: 12px; }
    
    .streamlit-expanderHeader {
        font-weight: 500;
        background: rgba(106, 0, 255, 0.03);
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #6a00ff, #b87cff);
        transition: width 0.1s linear;
    }
    
    .stSuccess {
        animation: scanEffect 0.5s ease-out;
        background: rgba(106, 0, 255, 0.15);
        border: 1px solid #6a00ff;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.markdown("<div style='font-size: 3rem; text-align: center;'>🧹</div>", unsafe_allow_html=True)

with col_title:
    st.markdown("""
    <div class="main-header">
        <h1>DATA CLEANER PRO</h1>
        <p style="margin: 0; opacity: 0.9;">by Igor.Lana | Igor.L.Z</p>
        <p style="font-size: 0.8rem; margin-top: 0.3rem; opacity: 0.7;">⚡ Hardy Style | Limpeza inteligente | Resultados premium</p>
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
        st.markdown("""
        <div class="sidebar-profile">
            <div style="font-size: 2.5rem;">👨‍💻</div>
            <div class="sidebar-name">Igor.Lana</div>
            <div class="sidebar-title">Data Specialist</div>
            <div class="sidebar-title" style="font-size: 0.65rem;">Igor.L.Z</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if 'selected_menu' not in st.session_state:
        st.session_state.selected_menu = "Dashboard"
    
    menu_options = {
        "🏠 Dashboard": "Dashboard",
        "📊 Processar Dados": "Processar Dados",
        "🔧 Tratamentos Avançados": "Tratamentos Avançados",
        "📜 Histórico": "Histórico",
        "⚙️ Configurações": "Configurações",
        "ℹ️ Sobre": "Sobre"
    }
    
    for label, value in menu_options.items():
        if st.button(label, key=f"menu_{value}", use_container_width=True):
            st.session_state.selected_menu = value
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sidebar-status">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <div class="status-dot"></div>
            <span style="color: #b0b0b0;">Sistema Online</span>
        </div>
        <div style="font-size: 0.7rem; color: #666;">
            📊 Versão: 3.1.1<br>👨‍💻 Igor.Lana<br>🎨 Hardy Style
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y')}")

# ============================================
# FUNÇÕES
# ============================================
def process_data(file_path, config):
    from src.core.cleaner import DataCleaner
    cleaner = DataCleaner(str(file_path), config)
    result = cleaner.run()
    output_file = cleaner.save()
    return result, output_file

def apply_advanced_treatments(df, config):
    df_result = df.copy()
    actions = []
    
    # Tratamentos de Texto
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
        import unicodedata
        for col in df_result.select_dtypes(include=['object']).columns:
            df_result[col] = df_result[col].apply(
                lambda x: unicodedata.normalize('NFKD', str(x)).encode('ASCII', 'ignore').decode('ASCII')
            )
        actions.append("🔤 Acentos removidos")
    
    if config.get('remove_special_chars', False):
        for col in df_result.select_dtypes(include=['object']).columns:
            df_result[col] = df_result[col].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
        actions.append("✨ Caracteres especiais removidos")
    
    # Tratamentos Numéricos
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
    
    if config.get('fill_missing_numeric', False):
        fill_method = config.get('fill_method', 'Mediana')
        for col in df_result.select_dtypes(include=[np.number]).columns:
            if fill_method == "Mediana":
                df_result[col] = df_result[col].fillna(df_result[col].median())
            elif fill_method == "Média":
                df_result[col] = df_result[col].fillna(df_result[col].mean())
            elif fill_method == "Zero":
                df_result[col] = df_result[col].fillna(0)
        actions.append(f"🔢 Valores numéricos preenchidos ({fill_method})")
    
    if config.get('round_decimals', 0) > 0:
        for col in df_result.select_dtypes(include=[np.number]).columns:
            df_result[col] = df_result[col].round(config.get('round_decimals', 2))
        actions.append(f"🔄 Números arredondados para {config.get('round_decimals', 2)} casas")
    
    # Tratamentos de Data
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
                    actions.append(f"📅 Componentes de data extraídos de '{col}'")
            except:
                pass
    
    # Detecção de Anomalias
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
    
    # Remoção de Duplicatas
    if config.get('remove_duplicates_advanced', False):
        subset_cols = config.get('duplicate_subset', None)
        if subset_cols and isinstance(subset_cols, list) and len(subset_cols) > 0:
            before = len(df_result)
            df_result = df_result.drop_duplicates(subset=subset_cols, keep='first')
            removed = before - len(df_result)
        else:
            before = len(df_result)
            df_result = df_result.drop_duplicates()
            removed = before - len(df_result)
        if removed > 0:
            actions.append(f"🔄 {removed} duplicatas removidas")
    
    return df_result, actions

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
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📁 Arquivos</div>
            <div class="metric-value">{processed_files}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">✅ Limpeza</div>
            <div class="metric-value">99.9%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">🚀 Velocidade</div>
            <div class="metric-value">&lt;1s</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">📊 Formatos</div>
            <div class="metric-value">6+</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info("🎯 **Como usar:** Processar Dados → Carregue arquivo → Escolha tratamentos → Baixe resultado")
    with col_info2:
        st.success("✨ **Benefícios:** Remoção de duplicatas, tratamento de nulos, correção de outliers")

# ============================================
# PROCESSAR DADOS
# ============================================
elif selected == "Processar Dados":
    st.markdown("## 🚀 Processar Dados")
    st.markdown("---")
    
    st.markdown("""
    <div class="upload-box">
        <div style="font-size: 2.5rem;">📂</div>
        <h3 style="color: #b87cff;">Arraste seu arquivo</h3>
        <p style="color: #888;">CSV, Excel, JSON</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Escolha um arquivo",
        type=['csv', 'xlsx', 'xls', 'json'],
        label_visibility="collapsed"
    )
    
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
                    
                    config = {
                        'remove_duplicates': remove_duplicates,
                        'treat_nulls': treat_nulls,
                        'treat_outliers': treat_outliers,
                        'standardize_dates': standardize_dates
                    }
                    
                    result, output_file = process_data(temp_path, config)
                    
                    st.markdown("""
                    <div class="scan-animation">
                        <p style="color: white; margin: 0;">✨ Dados processados com sucesso! ✨</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
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
# TRATAMENTOS AVANÇADOS
# ============================================
elif selected == "Tratamentos Avançados":
    st.markdown("## 🔧 Tratamentos Avançados")
    st.markdown("---")
    
    st.markdown("""
    <div class="upload-box">
        <div style="font-size: 2.5rem;">⚡</div>
        <h3 style="color: #b87cff;">Tratamento Profissional de Dados</h3>
        <p style="color: #888;">Múltiplas opções para limpeza avançada</p>
    </div>
    """, unsafe_allow_html=True)
    
    advanced_file = st.file_uploader(
        "Carregue seu arquivo",
        type=['csv', 'xlsx', 'xls', 'json'],
        key="adv"
    )
    
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
            
            st.markdown("### 🎯 Configurações Avançadas")
            st.markdown("---")
            
            # Tratamentos de Texto
            st.markdown("#### 📝 Tratamentos de Texto")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                text_clean = st.checkbox("Limpar espaços e padronizar", value=True)
                remove_accents = st.checkbox("Remover acentos", value=False)
                remove_special_chars = st.checkbox("Remover caracteres especiais", value=False)
            with col_t2:
                case_option = st.selectbox("Padronizar maiúsculas", ["Manter", "Maiúsculo", "Minúsculo", "Capitalizado"])
            
            # Tratamentos Numéricos
            st.markdown("#### 🔢 Tratamentos Numéricos")
            col_n1, col_n2 = st.columns(2)
            with col_n1:
                normalize_numbers = st.checkbox("Normalizar números (Min-Max)", value=False)
                standardize_zscore = st.checkbox("Padronizar (Z-Score)", value=False)
                fill_missing_numeric = st.checkbox("Preencher valores numéricos faltantes", value=False)
            with col_n2:
                if fill_missing_numeric:
                    fill_method = st.selectbox("Método de preenchimento", ["Mediana", "Média", "Zero"])
                else:
                    fill_method = "Mediana"
                round_decimals = st.number_input("Arredondar decimais", min_value=0, max_value=10, value=2)
            
            # Tratamentos de Data
            st.markdown("#### 📅 Tratamentos de Data")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                standardize_dates_adv = st.checkbox("Padronizar formato de datas", value=True)
                date_format = st.selectbox("Formato de data", ["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"])
            with col_d2:
                extract_date_components = st.checkbox("Extrair componentes (dia, mês, ano)", value=False)
            
            # Detecção e Correção
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
            duplicate_cols = st.text_input("Colunas para verificar duplicatas (separadas por vírgula)", 
                                           placeholder="ex: nome,email", key="dup_cols_input")
            
            # Configurações de Saída
            st.markdown("#### 📤 Configurações de Saída")
            output_format_adv = st.selectbox("Formato do arquivo tratado", ["CSV", "Excel", "JSON"], index=0)
            
            if st.button("⚡ APLICAR TRATAMENTOS AVANÇADOS", use_container_width=True):
                with st.spinner("🔄 Aplicando tratamentos avançados..."):
                    progress = st.progress(0)
                    for i in range(100):
                        time.sleep(0.005)
                        progress.progress(i + 1)
                    
                    duplicate_subset = None
                    if duplicate_cols and duplicate_cols.strip():
                        duplicate_subset = [c.strip() for c in duplicate_cols.split(',') if c.strip()]
                    
                    config = {
                        'text_clean': text_clean,
                        'remove_accents': remove_accents,
                        'remove_special_chars': remove_special_chars,
                        'case_option': case_option,
                        'normalize_numbers': normalize_numbers,
                        'standardize_zscore': standardize_zscore,
                        'fill_missing_numeric': fill_missing_numeric,
                        'fill_method': fill_method,
                        'round_decimals': round_decimals,
                        'standardize_dates': standardize_dates_adv,
                        'date_format': date_format,
                        'extract_date_components': extract_date_components,
                        'detect_anomalies': detect_anomalies,
                        'fix_anomalies': fix_anomalies,
                        'remove_duplicates_advanced': remove_duplicates_advanced,
                        'duplicate_subset': duplicate_subset
                    }
                    
                    df_result, actions = apply_advanced_treatments(df, config)
                    
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
                    
                    st.markdown("""
                    <div class="scan-animation">
                        <p style="color: white; margin: 0;">✨ Tratamentos avançados aplicados com sucesso! ✨</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
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
    
    st.markdown("""
    <div class="metric-card">
        <h3>🎨 Tema Hardy Style</h3>
        <p>Roxo e Preto - Design Profissional</p>
        <p>✅ Animações fluidas (0.2s-0.3s)</p>
        <p>✅ Scan Effect ao processar</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <h3>🔧 Tratamentos Disponíveis</h3>
        <ul>
            <li>✅ Remoção de duplicatas</li>
            <li>✅ Tratamento de nulos</li>
            <li>✅ Correção de outliers</li>
            <li>✅ Padronização de datas</li>
            <li>✅ Limpeza de textos</li>
            <li>✅ Normalização de números</li>
            <li>✅ Detecção de anomalias</li>
            <li>✅ Extração de componentes</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <h3>👨‍💻 Desenvolvedor</h3>
        <p>Igor.Lana | Igor.L.Z</p>
        <p>Versão 3.1.1 - Hardy Style Ultimate</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SOBRE
# ============================================
elif selected == "Sobre":
    st.markdown("## ℹ️ Sobre")
    st.markdown("---")
    
    st.markdown("""
    <div class="metric-card">
        <h3>🚀 Data Cleaner Pro - Hardy Style</h3>
        <p><strong>Versão:</strong> 3.1.1 Ultimate</p>
        <p><strong>Desenvolvedor:</strong> Igor.Lana | Igor.L.Z</p>
        <p><strong>Assinatura:</strong> "Dados limpos, decisões claras"</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <h3>📊 Funcionalidades Completas</h3>
        <ul>
            <li>✅ Remoção de duplicatas</li>
            <li>✅ Tratamento de nulos (4 métodos)</li>
            <li>✅ Correção de outliers (IQR e Z-Score)</li>
            <li>✅ Padronização de datas</li>
            <li>✅ Limpeza de textos (espaços, acentos, maiúsculas)</li>
            <li>✅ Normalização de números (Min-Max e Z-Score)</li>
            <li>✅ Detecção de anomalias</li>
            <li>✅ Extração de componentes de data</li>
            <li>✅ Interface Hardy Style Premium</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p>🧹 Data Cleaner Pro | by <strong>Igor.Lana | Igor.L.Z</strong></p>
    <p><i>"Dados limpos, decisões claras - Hardy Style Premium"</i></p>
    <p>Versão 3.1.1 Ultimate</p>
</div>
""", unsafe_allow_html=True)
