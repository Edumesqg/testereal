# bot_real_etiquetas_streamlit.py
# Bot de atendimento Real Etiquetas – versão estável com histórico,
# horário comercial, transbordo humano e exportação de leads.

from datetime import datetime, time
from zoneinfo import ZoneInfo
import pandas as pd
import streamlit as st

# ──────────────────────────────────
# CONFIGURAÇÕES GERAIS
# ──────────────────────────────────
APP_TZ       = ZoneInfo("America/Sao_Paulo")
H_START      = time(9, 0)
H_END        = time(18, 0)

st.set_page_config(page_title="Bot Real Etiquetas", layout="centered")

# ──────────────────────────────────
# TEXTOS FIXOS
# ──────────────────────────────────
SAUDACAO   = "Olá! 👋 Eu sou a *Real*, assistente virtual da Real Etiquetas."
MSG_HORARIO= "⏰ Atendemos **Seg–Sex, 09h‑18h (Brasília)**. " \
             "Deixe sua mensagem e responderemos no próximo expediente."
MSG_HUMANO = "⚡️ **Atendimento Humano em Curso!** Um especialista responderá em instantes."
MSG_FIM    = "✅ Atendimento concluído. Muito obrigado por falar com a Real Etiquetas! 🙌"

# ──────────────────────────────────
# HELPERS
# ──────────────────────────────────
def worktime() -> bool:
    now = datetime.now(APP_TZ).time()
    return H_START <= now <= H_END

def add(sender: str, text: str):
    """Adiciona ao histórico apenas se diferente da última linha."""
    if not st.session_state.history or st.session_state.history[-1] != (sender, text):
        st.session_state.history.append((sender, text))

def go(block: str):
    st.session_state.block = block

def reset():
    st.session_state.update(
        block="init",
        product="",
        history=[("bot", SAUDACAO)],
        entered_blocks={},
        lead_list=[]
    )

def block_once(name: str, text: str):
    """Mostra mensagem‑bot só na 1ª entrada do bloco."""
    if not st.session_state.entered_blocks.get(name):
        add("bot", text)
        with st.chat_message("assistant"):
            st.markdown(text)
        st.session_state.entered_blocks[name] = True

# ──────────────────────────────────
# ESTADO INICIAL
# ──────────────────────────────────
if "block" not in st.session_state:
    reset()

# ──────────────────────────────────
# RENDER HISTÓRICO
# ──────────────────────────────────
for who, msg in st.session_state.history:
    with st.chat_message("assistant" if who == "bot" else "user"):
        st.markdown(msg)

# ╭──────────────── BLOCO INICIAL ─────────────────╮
if st.session_state.block == "init":
    block_once("init", SAUDACAO)

    # Fora de horário
    if not worktime():
        block_once("horario", MSG_HORARIO)

    col1, col2, col3 = st.columns(3)
    if col1.button("📘 Ver Catálogo"):
        add("user", "Ver Catálogo")
        go("catalogo"); st.rerun()
    if col2.button("💰 Solicitar Orçamento"):
        add("user", "Solicitar Orçamento")
        go("produto");  st.rerun()
    if col3.button("🙋‍♀️ Já sou cliente"):
        add("user", "Cliente existente")
        go("humano");   st.rerun()

# ╭──────────────── BLOCO 1.1 – CATÁLOGO ─────────────────╮
elif st.session_state.block == "catalogo":
    block_once("catalogo",
        "Aqui está nosso catálogo! 📎 [Catálogo](https://realetiquetas.com.br/catalogo)\n"
        "🌐 www.realetiquetas.com.br | 📸 @real.etiquetas"
    )
    col1, col2, col3 = st.columns(3)
    if col1.button("💰 Orçar"):
        add("user", "Ir para orçamento"); go("produto"); st.rerun()
    if col2.button("📞 Atendente"):
        add("user", "Falar com atendente"); go("humano"); st.rerun()
    if col3.button("❌ Encerrar"):
        add("user", "Encerrar"); go("fim"); st.rerun()

# ╭──────────────── BLOCO 1.2 – SELEÇÃO PRODUTO ─────────────────╮
elif st.session_state.block == "produto":
    block_once("produto", "Vamos montar seu orçamento! Escolha o produto:")
    prod = st.radio(
        "Produto",
        ["🏷️ Etiquetas Emborrachadas", "🧵 Etiquetas de Tecido/Couro",
         "🔖 Tags", "🔑 Chaveiros", "📦 Outros"],
        key="prod"
    )
    if st.button("Continuar ▶️"):
        add("user", prod)
        st.session_state.product = prod
        go({"🏷️": "emb_qtd", "🧵": "tec_menu",
            "🔖": "tag_form", "🔑": "chav_menu"}.get(prod[:2], "outros"))
        st.rerun()

# ╭──────────────── EMBORRACHADAS ─────────────────╮
elif st.session_state.block == "emb_qtd":
    block_once("emb_qtd", "**Etiquetas Emborrachadas** – mín. 1 000 un.")
    qtd = st.radio("Quantidade",
                   ["📦 1 000–3 000", "🚀 +3 000", "🎨 Ver modelos"], key="emb_q")
    if st.button("Prosseguir ▶️"):
        add("user", qtd)
        go("emb_form" if qtd.startswith("📦")
           else "prioritario" if qtd.startswith("🚀")
           else "emb_models")
        st.rerun()

elif st.session_state.block == "emb_models":
    block_once("emb_models",
        "📎 [Portfólio Emborrachadas](https://realetiquetas.com.br/emborrachadas)")
    if st.button("⏪ Voltar"): go("emb_qtd"); st.rerun()

elif st.session_state.block == "emb_form":
    block_once("emb_form",
        "💡 De **R$ 1,00/un** | Frete grátis 🚚 (1 000–3 000 un)")
    with st.form("f_emb"):
        tam  = st.text_input("Tamanho (AxL)")
        cor  = st.selectbox("Cores", ["1", "2", "3"])
        fmt  = st.selectbox("Formato", ["Quadrada", "Redonda", "Corte especial"])
        art  = st.file_uploader("Arte (opcional)")
        if st.form_submit_button("Enviar orçamento"):
            add("bot", "✅ Orçamento registrado! SLA 24 h.")
            st.session_state.lead_list.append(
                {"Produto":"Emb", "Qtd":"1‑3k", "Tam":tam, "Cores":cor})
            go("fim"); st.rerun()

# ╭──────────────── TECIDO / COURO ─────────────────╮
elif st.session_state.block == "tec_menu":
    block_once("tec_menu",
        "**Etiquetas de Tecido/Couro** (mín. 1 000)")
    ver = st.checkbox("🎨 Ver modelos", key="tec_ver")
    if ver:
        st.markdown("📎 [Portfólio Tecido/Couro](https://realetiquetas.com.br/tecido-e-couro)")
    qtd = st.radio("Quantidade", ["📦 1 000–3 000", "🚀 +3 000"], key="tec_q")
    if st.button("Prosseguir ▶️"):
        add("user", f"Tecido {qtd}")
        go("tec_form" if qtd.startswith("📦") else "prioritario"); st.rerun()

elif st.session_state.block == "tec_form":
    block_once("tec_form", "💡 De **R$ 0,80/un** | Frete grátis 🚚")
    with st.form("f_tec"):
        tipo = st.text_input("Tipo de material")
        tam  = st.text_input("Tamanho (LxA)")
        acb  = st.text_input("Acabamento")
        cor  = st.selectbox("Cores", ["1", "2", "3"])
        art  = st.file_uploader("Arte (opcional)")
        if st.form_submit_button("Enviar orçamento"):
            add("bot", "✅ Orçamento registrado! SLA 12 h.")
            st.session_state.lead_list.append(
                {"Produto":"Tecido", "Tipo":tipo, "Qtd":"1‑3k"})
            go("fim"); st.rerun()

# ╭──────────────── TAGS ─────────────────╮
elif st.session_state.block == "tag_form":
    block_once("tag_form", "🔖 **Tags** – mín. 5 000 | de **R$ 0,20/un** + frete 🚚")
    with st.form("f_tags"):
        ref = st.text_input("Modelo / referência")
        qtd = st.number_input("Quantidade", min_value=5000, step=1000, value=5000)
        art = st.file_uploader("Arte (opcional)")
        if st.form_submit_button("Enviar orçamento"):
            add("bot", "✅ Orçamento registrado! SLA 12 h.")
            st.session_state.lead_list.append({"Produto":"Tags", "Qtd":qtd})
            go("fim"); st.rerun()

# ╭──────────────── CHAVEIROS ─────────────────╮
elif st.session_state.block == "chav_menu":
    block_once("chav_menu", "**Chaveiros** – mín. 500 un.")
    ver = st.checkbox("🎨 Ver modelos", key="chv_ver")
    if ver:
        st.markdown("📎 [Portfólio Chaveiros](https://realetiquetas.com.br/chaveiros)")
    qtd = st.radio("Quantidade", ["500–1 000", "Mais de 1 000"], key="chv_q")
    if st.button("Prosseguir ▶️"):
        add("user", f"Chaveiro {qtd}")
        go("chav_form" if qtd == "500–1 000" else "prioritario"); st.rerun()

elif st.session_state.block == "chav_form":
    block_once("chav_form", "💡 De **R$ 2,00/un** | Frete grátis 🚚 (500–1 000 un)")
    with st.form("f_chav"):
        q   = st.number_input("Quantidade", min_value=500, max=1000, step=50, value=500)
        tam = st.text_input("Tamanho")
        fmt = st.text_input("Formato / tipo")
        art = st.file_uploader("Arte (opcional)")
        if st.form_submit_button("Enviar orçamento"):
            add("bot", "✅ Orçamento registrado! SLA 12 h.")
            st.session_state.lead_list.append({"Produto":"Chaveiro", "Qtd":q})
            go("fim"); st.rerun()

# ╭──────────────── OUTROS ─────────────────╮
elif st.session_state.block == "outros":
    block_once("outros", "📦 Outros produtos – descreva seu projeto:")
    desc = st.text_area("Descrição (tipo, quantidade, arte...)")
    if st.button("Enviar descrição") and desc.strip():
        add("user", desc)
        add("bot", "✅ Solicitação enviada ao especialista.")
        st.session_state.lead_list.append({"Produto":"Outros", "Desc":desc})
        go("fim"); st.rerun()

# ╭──────────────── HUMANO / PRIORITÁRIO ─────────────────╮
elif st.session_state.block in ["prioritario", "humano"]:
    block_once(st.session_state.block, MSG_HUMANO)
    st.text_area("Envie detalhes adicionais (opcional):")
    if st.button("Encerrar sessão"):
        go("fim"); st.rerun()

# ╭──────────────── FIM ─────────────────╮
elif st.session_state.block == "fim":
    block_once("fim", MSG_FIM)
    if st.button("🔄 Novo atendimento"):
        reset(); st.rerun()

# ──────────────────────────────────
# TABELA + DOWNLOAD DE LEADS
# ──────────────────────────────────
if st.session_state.lead_list:
    st.markdown("---")
    df = pd.DataFrame(st.session_state.lead_list)
    st.dataframe(df, use_container_width=True)
    st.download_button("⬇️ Baixar leads (CSV)",
                       df.to_csv(index=False).encode("utf-8"),
                       file_name="leads_real_etiquetas.csv",
                       mime="text/csv")
