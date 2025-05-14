import streamlit as st
# bot_real_etiquetas_streamlit.py
# Bot de atendimento – Real Etiquetas (protótipo Web)

import streamlit as st

# ---------------------------
# Configuração da página
# ---------------------------
st.set_page_config(page_title="Bot Real Etiquetas", layout="centered")

# ---------------------------
# Funções utilitárias
# ---------------------------
def reset_state() -> None:
    """Limpa variáveis de sessão."""
    for k in ["block", "product"]:
        st.session_state.pop(k, None)

def go(to_block: str) -> None:
    """Navega para outro bloco."""
    st.session_state["block"] = to_block

# ---------------------------
# Inicialização do estado
# ---------------------------
if "block" not in st.session_state:
    st.session_state["block"] = "init"

st.title("🤖 Real – Assistente Virtual da Real Etiquetas")

# ---------------------------
# Fluxo de atendimento
# ---------------------------

# 0. Gatilho Inicial
if st.session_state["block"] == "init":
    st.info(
        "Olá! 👋 Eu sou a *Real*, assistente virtual da Real Etiquetas.\n"
        "Obrigada pelo seu contato! Para agilizar seu atendimento, escolha uma das opções abaixo:"
    )
    col1, col2, col3 = st.columns(3)
    if col1.button("📘 Ver Catálogo"):
        go("catalogo")
    if col2.button("💰 Solicitar Orçamento"):
        go("produto")
    if col3.button("🙋‍♀️ Já sou cliente – Falar com atendente"):
        go("humano_cliente")

# 1.1 Ver Catálogo
elif st.session_state["block"] == "catalogo":
    st.subheader("📘 Catálogo")
    st.markdown("📎 [Catálogo Atualizado](https://realetiquetas.com.br/catalogo)")
    st.markdown("🌐 www.realetiquetas.com.br")
    st.markdown("📸 Instagram: @real.etiquetas")
    st.write("---")
    col1, col2, col3 = st.columns(3)
    if col1.button("💰 Solicitar Orçamento"):
        go("produto")
    if col2.button("📞 Falar com atendente"):
        go("humano")
    if col3.button("❌ Encerrar"):
        go("fim")

# 1.2 Seleção do Produto
elif st.session_state["block"] == "produto":
    st.subheader("💰 Solicitar Orçamento")
    st.info("Selecione o tipo de produto que deseja orçar:")
    prod = st.radio(
        "Produto",
        [
            "🏷️ Etiquetas Emborrachadas",
            "🧵 Etiquetas de Tecido/Couro",
            "🔖 Tags",
            "🔑 Chaveiros",
            "📦 Outros",
        ],
    )
    st.session_state["product"] = prod
    col_ok, col_back = st.columns([1, 1])
    if col_ok.button("Continuar ▶️"):
        if prod.startswith("🏷️"):
            go("emborrachada_qtd")
        elif prod.startswith("🧵"):
            go("tecido_menu")
        elif prod.startswith("🔖"):
            go("tags_form")
        elif prod.startswith("🔑"):
            go("chaveiro_menu")
        else:
            go("outros_form")
    if col_back.button("⬅️ Voltar"):
        go("init")

# ----- Etiquetas Emborrachadas -----
elif st.session_state["block"] == "emborrachada_qtd":
    st.subheader("🏷️ Etiquetas Emborrachadas")
    qtd = st.radio(
        "Quantidade",
        [
            "📦 1 000 – 3 000 unidades",
            "🚀 Mais de 3 000 unidades",
            "🎨 Ver modelos",
        ],
    )
    if qtd == "🎨 Ver modelos":
        st.markdown(
            "📎 [Modelos de Etiquetas Emborrachadas](https://realetiquetas.com.br/emborrachadas)"
        )
    col_ok, col_back = st.columns([1, 1])
    if col_ok.button("Prosseguir ▶️"):
        if qtd.startswith("📦"):
            go("emborrachada_form")
        elif qtd.startswith("🚀"):
            go("prioritario")
    if col_back.button("⬅️ Voltar"):
        go("produto")

elif st.session_state["block"] == "emborrachada_form":
    st.subheader("Formulário – Emborrachadas (1k–3k)")
    with st.form("form_emb"):
        tam = st.text_input("Tamanho (Altura x Largura)")
        cores = st.selectbox("Número de cores", ["1", "2", "3"])
        formato = st.selectbox("Formato", ["Quadrada", "Redonda", "Corte Especial"])
        arte = st.file_uploader("Arte / referência (opcional)")
        sub = st.form_submit_button("Enviar orçamento")
        if sub:
            st.success(
                "✅ Orçamento solicitado com sucesso!\nResponderemos em até **24 h úteis**."
            )
            go("fim")

# ----- Etiquetas de Tecido / Couro -----
elif st.session_state["block"] == "tecido_menu":
    st.subheader("🧵 Etiquetas de Tecido / Couro")
    st.markdown("**Pedido mínimo:** 1 000 unidades")
    menu = st.radio("Opções", ["🎨 Ver modelos", "💰 Orçar agora"])
    if menu == "🎨 Ver modelos":
        st.markdown(
            "📎 [Modelos Tecido/Couro](https://realetiquetas.com.br/tecido-e-couro)"
        )
    qtd = st.radio("Quantidade", ["📦 1 000–3 000", "🚀 +3 000"])
    col_ok, col_back = st.columns([1, 1])
    if col_ok.button("Prosseguir ▶️"):
        if qtd.startswith("📦"):
            go("tecido_form")
        else:
            go("prioritario")
    if col_back.button("⬅️ Voltar"):
        go("produto")

elif st.session_state["block"] == "tecido_form":
    st.subheader("Formulário – Tecido/Couro (1k–3k)")
    with st.form("form_tecido"):
        tipo = st.text_input("Tipo de material (Couro sintético, Sarja...)")
        tam = st.text_input("Tamanho (Largura x Altura)")
        acabamento = st.text_input("Acabamento (costura, termocolante...)")
        cores = st.selectbox("Número de cores", ["1", "2", "3"])
        arte = st.file_uploader("Arte / referência (opcional)")
        sub = st.form_submit_button("Enviar orçamento")
        if sub:
            st.success(
                "✅ Orçamento recebido!\nNosso time retornará em até **12 h úteis**."
            )
            go("fim")

# ----- Tags -----
elif st.session_state["block"] == "tags_form":
    st.subheader("🔖 Tags – Pedido mínimo 5 000")
    st.markdown("Valor a partir de **R$ 0,20/unidade** | Frete grátis 🚚")
    with st.form("form_tags"):
        ref = st.text_input("Referência / modelo")
        qtd = st.number_input("Quantidade", min_value=5_000, step=1_000, value=5_000)
        arte = st.file_uploader("Arte (opcional)")
        sub = st.form_submit_button("Enviar orçamento")
        if sub:
            st.success(
                "✅ Tags solicitadas! Nosso especialista responderá em até **12 h úteis**."
            )
            go("fim")

# ----- Chaveiros -----
elif st.session_state["block"] == "chaveiro_menu":
    st.subheader("🔑 Chaveiros")
    st.markdown("**Pedido mínimo:** 500 unidades")
    menu = st.radio("Deseja:", ["🎨 Ver modelos", "💰 Orçar"])
    if menu == "🎨 Ver modelos":
        st.markdown(
            "📎 [Modelos de Chaveiros](https://realetiquetas.com.br/chaveiros)"
        )
    qtd = st.radio("Quantidade", ["500–1 000", "Mais de 1 000"])
    col_ok, col_back = st.columns([1, 1])
    if col_ok.button("Prosseguir ▶️"):
        if qtd == "500–1 000":
            go("chaveiro_form")
        else:
            go("prioritario")
    if col_back.button("⬅️ Voltar"):
        go("produto")

elif st.session_state["block"] == "chaveiro_form":
    st.subheader("Formulário – Chaveiros (500–1 000)")
    with st.form("form_chav"):
        qtd = st.number_input(
            "Quantidade", min_value=500, max_value=1_000, step=50, value=500
        )
        tam = st.text_input("Tamanho aproximado")
        formato = st.text_input("Formato / tipo")
        arte = st.file_uploader("Arte / referência (opcional)")
        sub = st.form_submit_button("Enviar orçamento")
        if sub:
            st.success(
                "✅ Orçamento solicitado! Em breve entraremos em contato (SLA 12 h)."
            )
            go("fim")

# ----- Outros Produtos -----
elif st.session_state["block"] == "outros_form":
    st.subheader("📦 Outros Produtos")
    desc = st.text_area(
        "Descreva seu projeto (tipo de produto, quantidade, referências, arte...)"
    )
    if st.button("Enviar"):
        if desc.strip():
            st.success(
                "✅ Solicitação recebida!\nEncaminharemos para o especialista responsável."
            )
            go("fim")

# ----- Atendimento Prioritário (volumes grandes) -----
elif st.session_state["block"] == "prioritario":
    st.warning(
        "🚀 **Atendimento Prioritário em andamento!**\n"
        "Um especialista humano está sendo acionado para atender seu pedido.\n"
        "Envie abaixo qualquer detalhe adicional (tamanho, aplicação, arte...) enquanto isso."
    )
    st.text_area("Detalhes adicionais (opcional):")
    if st.button("Continuar para humano"):
        go("humano")

# ----- Atendimento Humano (genérico) -----
elif st.session_state["block"] in ["humano", "humano_cliente"]:
    st.success(
        "⚡️ **Atendimento Humano em Curso!**\n"
        "Um especialista responderá em instantes."
    )
    if st.button("Encerrar atendimento"):
        go("fim")

# ----- Encerramento -----
elif st.session_state["block"] == "fim":
    st.balloons()
    st.success("✅ Atendimento concluído.\nMuito obrigado por falar com a Real Etiquetas! 🙌")
    if st.button("🔄 Novo atendimento"):
        reset_state()

