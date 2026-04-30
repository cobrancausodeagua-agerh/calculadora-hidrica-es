import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora de Recursos Hídricos ES", layout="centered")

st.title("💧 Simulador de Cobrança - Decreto 6.184-R/2025")
st.markdown("Esta ferramenta simula os valores de cobrança pelo uso da água no Espírito Santo.")

# --- BARRA LATERAL (PARÂMETROS GERAIS) ---
st.sidebar.header("Configurações Gerais")
vrte_valor = st.sidebar.number_input("Valor da VRTE (R$)", value=4.50, step=0.01)
k_gestao = st.sidebar.slider("Kgestão (Eficiência)", 0.0, 1.0, 1.0)
k_crise = st.sidebar.slider("Kcrise (Escassez)", 1.0, 1.5, 1.0)

# --- SEÇÃO 1: CAPTAÇÃO ---
st.header("1. Captação de Água")
col1, col2 = st.columns(2)

with col1:
    vol_cap = st.number_input("Volume Anual Captado (m³)", min_value=0.0, value=10000.0)
    tipo_agua = st.selectbox("Tipo de Água", ["Superficial", "Subterrânea"])

with col2:
    classe = st.selectbox("Classe de Enquadramento", ["Classe Especial", "Classe 1", "Classe 2", "Classe 3", "Classe 4"], index=2)

# Lógica de coeficientes (Anexos I e II)
ppu_cap = 0.013 if tipo_agua == "Superficial" else 0.015
k_classe_map = {"Classe Especial": 2.0, "Classe 1": 1.5, "Classe 2": 1.0, "Classe 3": 0.7, "Classe 4": 0.5}
k_classe = k_classe_map[classe]

vr_cap = vol_cap * ppu_cap * k_classe

# --- SEÇÃO 2: LANÇAMENTO ---
st.header("2. Lançamento de Efluentes")
col3, col4, col5 = st.columns(3)

with col3:
    vol_lan = st.number_input("Volume de Lançamento (m³)", min_value=0.0, value=5000.0)
with col4:
    conc_dbo = st.number_input("DBO (mg/L)", min_value=0.0, value=300.0)
with col5:
    conc_p = st.number_input("Fósforo Total (mg/L)", min_value=0.0, value=10.0)

# Cálculo da Carga (Art. 5º)
carga_dbo = (vol_lan * conc_dbo) / 1000  # converte para kg
carga_p = (vol_lan * conc_p) / 1000      # converte para kg
ppu_lan = 0.06

vr_lan = (carga_dbo * ppu_lan + carga_p * ppu_lan) * k_classe

# --- RESULTADO FINAL ---
st.divider()
valor_total_vrte = (vr_cap + vr_lan) * k_gestao * k_crise
valor_total_reais = valor_total_vrte * vrte_valor

st.subheader("Resumo da Simulação")
res1, res2 = st.columns(2)
res1.metric("Total em VRTE", f"{valor_total_vrte:,.2f}")
res2.metric("Total Estimado (R$)", f"R$ {valor_total_reais:,.2f}")

with st.expander("Ver detalhes dos cálculos"):
    st.write(f"**Parcela de Captação:** {vr_cap:,.2f} VRTE")
    st.write(f"**Parcela de Lançamento:** {vr_lan:,.2f} VRTE")
    st.write(f"**Carga de DBO:** {carga_dbo:,.2f} kg/ano")
    st.write(f"**Carga de Fósforo:** {carga_p:,.2f} kg/ano")
    st.caption("Baseado nos Anexos I, II e V do Decreto 6.184-R.")
