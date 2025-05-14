# bot_real_etiquetas_streamlit.py
# Versão aprimorada – fluxo completo, histórico de conversa, horário comercial
# Requisitos: streamlit >= 1.25  |  Python ≥ 3.9  (usa zoneinfo)

from datetime import datetime, time
from zoneinfo import ZoneInfo
import pandas as pd
import streamlit as st

# ──────────────────────────────────────────────
# CONFIGURAÇÕES GERAIS
# ──────────────────────────────────────────────
APP_TZ = ZoneInfo("America/Sao_Paulo")
HORA_INICIO = time(9, 0)
HORA_FIM = time(18, 0)
SLA_PADRAO_H = 12
SLA_PRIORITARIO_H = 4

st.set_page_config(page_title="Bot Real Etiquetas", layout="centered")

# ──────────────────────────────────────────────
# FUNÇÕES DE APOIO
# ──────────────────────────────────────────────
def em_horario_comercial() -> bool:
    now = datetime.now(APP_TZ).time()
    return HORA_INICIO <= now <= HORA_FIM

def add_hist(who: str, msg: str) -> None:
    st.session_state.history.append((who, msg))

def go(block: str) -> None:
    st.session_state.block = block

def novo_atendimento() -> None:
    st.session_state.block = "init"
    st.session_state.product = ""
    st.session_state.history = [("bot", SAUDACAO)]
    st.session_state.lead = {}

# ──────────────────────────────────────────────
# MENSAGENS FIXAS
# ──────────────────────────────────────────────
SAUDACAO = (
    "Olá! 👋 Eu sou a *Real*, assistente virtual da Real Etiquetas.\n"
    "Obrigada pelo seu contato!"
)

MSG_HORARIO = (
    "⏰ Nosso horário de atendimento é **Seg–Sex, 09h – 18h (Brasília)**.\n"
    "Pode deixar sua mensagem que responderemos no próximo expediente. 😉"
)

MSG_TRANSBORDO = (
    "⚡️ **Atendimento Humano em Curso!**\n"
    "Um especialista responderá em instantes."
)

MSG_ENCERRAMENTO = (
    "✅ Atendimento concluído. Muito obrigado por falar com a Real Etiquetas! 🙌"
)

# ──────────────────────────────────────────────
# INICIALIZAÇÃO DO ESTADO
# ──────────────────────────────────────────────
if "block" not in st.session_state:
    st.session_state.history = []
    st.session_state.lead_list = []  # armazenamento simples local
    novo_atendimento()

# ──────────────────────────────────────────────
# INTERFACE – HISTÓRICO (simples)
# ──────────────────────────────────────────────
st.title("🤖 Real – Assistente Virtual")
for who, msg in st.session_state.history:
    with st.chat_message("assistant" if who == "bot" else "user"):
        st.markdown(msg)

# ──────────────────────────────────────────────
# BLOCO: FORA DO HORÁRIO
# ──────────────────────────────────────────────
if not em_horario_comercial() and st.session_state.block == "init":
    add_hist("bot", MSG_HORARIO)
    st.chat_message("assistant").markdown(MSG_HORARIO)
    if st.button("📘 Ver Catálogo"):
        add_hist("user", "Ver Catálogo")
        go("catalogo")
    st.stop()

# ──────────────────────────────────────────────
# BLOCO 0 – GATILHO INICIAL
# ──────────────────────────────────────────────
if st.session_state.block == "init":
    add_hist("bot", SAUDACAO)
    st.chat_message("assistant").markdown(SAUDACAO)
    col1, col2, col3 = st.columns(3)
    if col1.button("📘 Ver Catálogo"):
        add_hist("user", "Ver Catálogo")
        go("catalogo")
        st.rerun()
    if col2.button("💰 Solicitar Orçamento"):
        add_hist("user", "Solicitar Orçamento")
        go("produto")
        st.rerun()
    if col3.button("🙋‍♀️ Já sou cliente"):
        add_hist("user", "Cliente existente")
        go("humano_cliente")
        st.rerun()

# ──────────────────────────────────────────────
# BLOCO 1.1 – CATÁLOGO
# ──────────────────────────────────────────────
elif st.session_state.block == "catalogo":
    TXT = (
        "Aqui está nosso catálogo atualizado! 👇\n"
        "📎 [Catálogo](https://realetiquetas.com.br/catalogo)\n"
        "🌐 www.realetiquetas.com.br  |  📸 @real.etiquetas"
    )
    add_hist("bot", TXT)
    st.chat_message("assistant").markdown(TXT)
    col1, col2, col3 = st.columns(3)
    if col1.button("💰 Orçar"):
        add_hist("user", "Ir para orçamento")
        go("produto")
        st.rerun()
    if col2.button("📞 Atendente"):
        add_hist("user", "Atendente")
        go("humano")
        st.rerun()
    if col3.button("❌ Encerrar"):
        add_hist("user", "Encerrar")
        go("fim")
        st.rerun()

# ──────────────────────────────────────────────
# BLOCO 1.2 – SELEÇÃO DE PRODUTO
# ──────────────────────────────────────────────
elif st.session_state.block == "produto":
    TXT = "Vamos montar seu orçamento personalizado! Selecione o tipo de produto:"
    add_hist("bot", TXT)
    st.chat_message("assistant").markdown(TXT)
    prod = st.radio(
        "Tipo de produto",
        [
            "🏷️ Etiquetas Emborrachadas",
            "🧵 Etiquetas de Tecido/Couro",
            "🔖 Tags",
            "🔑 Chaveiros",
            "📦 Outros",
        ],
        key="prod_radio",
    )
    if st.button("Continuar ▶️"):
        add_hist("user", prod)
        st.session_state.product = prod
        if prod.startswith("🏷️"):
            go("emb_qtd")
        elif prod.startswith("🧵"):
            go("tec_menu")
        elif prod.startswith("🔖"):
            go("tags_form")
        elif prod.startswith("🔑"):
            go("chav_menu")
        else:
            go("outros")
        st.rerun()

# ========== BLOCO 1.2.1 – EMBORRACHADAS ==========
elif st.session_state.block == "emb_qtd":
    TXT = "**Etiquetas Emborrachadas** – pedido mínimo 1 000."
    add_hist("bot", TXT)
    st.chat_message("assistant").markdown(TXT)
    qtd = st.radio(
        "Escolha a quantidade",
        ["📦 1 000–3 000", "🚀 +3 000", "🎨 Ver modelos"],
        key="emb_q",
    )
    col_ok, col_bk = st.columns([1, 1])
    if col_ok.button("Prosseguir"):
        add_hist("user", qtd)
        if qtd.startswith("📦"):
            go("emb_form")
        elif qtd.startswith("🚀"):
            go("prioritario")
        else:
            add_hist(
                "bot",
                "📎 [Portfólio Emborrachadas](https://realetiquetas.com.br/emborrachadas)",
            )
        st.rerun()
    if col_bk.button("⬅️ Voltar"):
        go("produto")
        st.rerun()

elif st.session_state.block == "emb_form":
    TXT = "💡 Valor a partir de **R$ 1,00/un** | Frete grátis 🚚"
    add_hist("bot", TXT)
    st.chat_message("assistant").markdown(TXT)
    with st.form("f_emb"):
        tam = st.text_input("Tamanho (AxL)")
        cores = st.selectbox("Cores", ["1", "2", "3"])
        formato = st.selectbox("Formato", ["Quadrada", "Redonda", "Corte Especial"])
        arte = st.file_uploader("Arte (opcional)")
        send = st.form_submit_button("Enviar orçamento")
        if send:
            st.success("✅ Orçamento registrado! SLA 24 h.")
            st.session_state.lead_list.append(
                {"Produto": "Emborrachada", "Qtd": "1‑3k", "Tamanho": tam}
            )
            add_hist("bot", "✅ Orçamento registrado! SLA 24 h.")
            go("fim")
            st.rerun()

# ========== BLOCO 1.2.2 – TECIDO/COURO ==========
elif st.session_state.block == "tec_menu":
    TXT = (
        "**Etiquetas de Tecido/Couro** (mín. 1 000)\n"
        "Escolha visualizar modelos ou prosseguir com quantidade:"
    )
    add_hist("bot", TXT)
    st.chat_message("assistant").markdown(TXT)
    ver = st.checkbox("🎨 Ver modelos (abre link)", key="tec_ver")
    if ver:
        st.markdown("📎 [Portfólio Tecido/Couro](https://realetiquetas.com.br/tecido-e-couro)")
    qtd = st.radio("Quantidade", ["📦 1 000–3 000", "🚀 +3 000"], key="tec_q")
    if st.button("Prosseguir ▶️", key="tec_ok"):
        add_hist("user", f"Tecido: {qtd}")
        if qtd.startswith("📦"):
            go("tec_form")
        else:
            go("prioritario")
        st.rerun()

elif st.session_state.block == "tec_form":
    TXT = "💡 Valor a partir de **R$ 0,80/un** | Frete grátis 🚚"
    add_hist("bot", TXT)
    st.chat_message("assistant").markdown(TXT)
    with st.form("f_tec"):
        tipo = st.text_input("Tipo (Couro sintético, Sarja...)")
        tam = st.text_input("Tamanho (LxA)")
        acabamento = st.text_input("Acabamento")
        cores = st.selectbox("Cores", ["1", "2", "3"])
        arte = st.file_uploader("Arte (opcional)")
        send = st.form_submit_button("Enviar orçamento")
        if send:
            st.success("✅ Orçamento registrado! SLA 12 h.")
            st.session_state.lead_list.append(
                {"Produto": "Tecido/Couro", "Qtd": "1‑3k", "Tipo": tipo}
            )
            add_hist("bot", "✅ Orçamento registrado! SLA 12 h.")
            go("fim")
            st.rerun()

# ========== BLOCO 1.2.3 – TAGS ==========
elif st.session_state.block == "tags_form":
    TXT = "🔖 **Tags** – mín. 5 000 | A partir **R$ 0,20/un** (frete grátis)"
    add_hist("bot", TXT)
    st.chat_message("assistant").markdown(TXT)
    with st.form("f_tag"):
        ref = st.text_input("Modelo / referência")
        qtd = st.number_input("Quantidade", min_value=5000, step=1000, value=5000)
        arte = st.file_uploader("Arte (opcional)")
        send = st.form_submit_button("Enviar orçamento")
        if send:
            st.success("✅ Orçamento registrado! SLA 12 h.")
            st.session_state.lead_list.append(
                {"Produto": "Tags", "Qtd": qtd, "Modelo": ref}
            )
            add_hist("bot", "✅ Orçamento registrado! SLA 12 h.")
            go("fim")
            st.rerun()

# ========== BLOCO 1.2.4 – CHAVEIROS ==========
elif st.session_state.block == "chav_menu":
    TXT = "**Chaveiros** – pedido mínimo 500"
    add_hist("bot", TXT)
    st.chat_message("assistant").markdown(TXT)
    mostrar = st.checkbox("🎨 Ver modelos (abre link)", key="chav_ver")
    if mostrar:
        st.markdown("📎 [Portfólio Chaveiros](https://realetiquetas.com.br/chaveiros)")
    qtd = st.radio("Quantidade", ["500–1 000", "Mais de 1 000"], key="chav_q")
    if st.button("Prosseguir ▶️", key="chav_ok"):
        add_hist("user", f"Chaveiros: {qtd}")
        if qtd == "500–1 000":
            go("chav_form")
        else:
            go("prioritario")
        st.rerun()

elif st.session_state.block == "chav_form":
    TXT = "💡 Valor a partir de **R$ 2,00/un** | Frete grátis 🚚"
    add_hist("bot", TXT)
    st.chat_message("assistant").markdown(TXT)
    with st.form("f_chav"):
        qtd = st.number_input("Quantidade", min_value=500, max_value=1000, value=500)
        tam = st.text_input("Tamanho aproximado")
        formato = st.text_input("Formato / tipo")
        arte = st.file_uploader("Arte (opcional)")
        send = st.form_submit_button("Enviar orçamento")
        if send:
            st.success("✅ Orçamento registrado! SLA 12 h.")
            st.session_state.lead_list.append(
                {"Produto": "Chaveiros", "Qtd": qtd, "Formato": formato}
            )
            add_hist("bot", "✅ Orçamento registrado! SLA 12 h.")
            go("fim")
            st.rerun()

# ========== BLOCO 1.2.5 – OUTROS ==========
elif st.session_state.block == "outros":
    TXT = "📦 Outros Produtos – descreva seu projeto:"
    add_hist("bot", TXT)
    st.chat_message("assistant").markdown(TXT)
    desc = st.text_area("Descrição (tipo, quantidade, arte...)")
    if st.button("Enviar descrição"):
        if desc.strip():
            st.success("✅ Solicitação recebida! Especialista responderá em breve.")
            st.session_state.lead_list.append({"Produto": "Outros", "Desc": desc})
            add_hist("bot", "✅ Solicitação encaminhada ao especialista.")
            go("fim")
            st.rerun()

# ========== BLOCO PRIORITÁRIO ==========
elif st.session_state.block == "prioritario":
    add_hist("bot", MSG_TRANSBORDO)
    st.chat_message("assistant").markdown(MSG_TRANSBORDO)
    detalhe = st.text_area("Envie detalhes adicionais (opcional):")
    if st.button("Encerrar sessão"):
        go("fim")
        st.rerun()

# ========== BLOCO HUMANO ==========
elif st.session_state.block in ["humano", "humano_cliente"]:
    add_hist("bot", MSG_TRANSBORDO)
    st.chat_message("assistant").markdown(MSG_TRANSBORDO)
    if st.button("Encerrar atendimento"):
        go("fim")
        st.rerun()

# ========== BLOCO ENCERRAMENTO ==========
elif st.session_state.block == "fim":
    st.chat_message("assistant").markdown(MSG_ENCERRAMENTO)
    if st.button("🔄 Novo atendimento"):
        novo_atendimento()
        st.rerun()

# ──────────────────────────────────────────────
# RODAPÉ – DOWNLOAD DOS LEADS CAPTURADOS
# ──────────────────────────────────────────────
if st.session_state.lead_list:
    st.markdown("---")
    st.subheader("📑 Leads capturados nesta sessão")
    df = pd.DataFrame(st.session_state.lead_list)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Baixar CSV", csv, "leads_real_etiquetas.csv", "text/csv")
