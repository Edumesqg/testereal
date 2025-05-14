import streamlit as st

st.set_page_config(page_title="Bot Real Etiquetas", layout="centered")

st.title("🤖 Real – Assistente Virtual da Real Etiquetas")
st.markdown("Olá! 👋 Eu sou a *Real*, assistente virtual da Real Etiquetas.\n"
            "Obrigada pelo seu contato! Para agilizar seu atendimento, escolha uma das opções abaixo:")

# Menu inicial
opcao = st.selectbox("Selecione uma opção:", [
    "📘 Ver Catálogo",
    "💰 Solicitar Orçamento",
    "🙋‍♀️ Já sou cliente – Falar com um atendente"
])

# 1.1 Ver Catálogo
if opcao == "📘 Ver Catálogo":
    st.markdown("### 📘 Catálogo")
    st.markdown("📎 [Catálogo Atualizado](https://realetiquetas.com.br/catalogo)")
    st.markdown("🌐 Site: [www.realetiquetas.com.br](https://realetiquetas.com.br)")
    st.markdown("📸 Instagram: [@real.etiquetas](https://instagram.com/real.etiquetas)")

    next_opt = st.radio("Deseja seguir com:", [
        "💰 Solicitar Orçamento",
        "📞 Falar com um atendente",
        "❌ Encerrar atendimento"
    ])

    if next_opt == "💰 Solicitar Orçamento":
        opcao = "💰 Solicitar Orçamento"
    elif next_opt == "📞 Falar com um atendente":
        st.markdown("🔁 Direcionando para um atendente humano.")
    elif next_opt == "❌ Encerrar atendimento":
        st.markdown("✅ Atendimento encerrado. Obrigado pelo contato!")

# 1.2 Solicitar Orçamento
if opcao == "💰 Solicitar Orçamento":
    st.markdown("### 💰 Solicitar Orçamento")
    st.info("Vamos montar seu orçamento personalizado! Nossa equipe retornará em até **12 horas úteis**.")
    produto = st.radio("Qual tipo de produto você deseja?", [
        "🏷️ Etiquetas Emborrachadas",
        "🧵 Etiquetas de Tecido/Couro",
        "🔖 Tags",
        "🔑 Chaveiros",
        "📦 Outros"
    ])

    # Emborrachadas
    if produto == "🏷️ Etiquetas Emborrachadas":
        qtd = st.radio("Quantas unidades você deseja?", [
            "📦 1.000 a 3.000 unidades",
            "🚀 Mais de 3.000 unidades",
            "🎨 Ver modelos de etiquetas"
        ])

        if qtd == "🎨 Ver modelos de etiquetas":
            st.markdown("📎 [Modelos de Etiquetas Emborrachadas](https://realetiquetas.com.br/emborrachadas)")
            st.success("Deseja seguir com o orçamento acima de 1.000 unidades?")

        elif qtd == "📦 1.000 a 3.000 unidades":
            st.markdown("💡 A partir de **R$1,00/unidade** | Frete grátis para todo o Brasil")
            with st.form("form_emborrachada"):
                tam = st.text_input("Tamanho (altura x largura)")
                cores = st.radio("Número de cores:", ["1", "2", "3"])
                formato = st.selectbox("Formato:", ["Quadrada", "Redonda", "Corte especial"])
                arte = st.file_uploader("Anexe sua arte ou referência")
                enviar = st.form_submit_button("Enviar orçamento")
                if enviar:
                    st.success("✅ Orçamento solicitado com sucesso! Responderemos em até 24h úteis.")

        elif qtd == "🚀 Mais de 3.000 unidades":
            st.markdown("🚀 Atendimento Prioritário em andamento!")
            st.text_area("Descreva seu pedido (tamanho, arte, modelo etc.)")

    # Tecido ou Couro
    elif produto == "🧵 Etiquetas de Tecido/Couro":
        st.markdown("**Pedido mínimo: 1.000 unidades**")
        tecido_opt = st.radio("Deseja:", [
            "🎨 Ver modelos de tecido/couro",
            "💰 Solicitar orçamento direto",
            "❌ Encerrar atendimento"
        ])

        if tecido_opt == "🎨 Ver modelos de tecido/couro":
            st.markdown("📎 [Modelos de Tecido/Couro](https://realetiquetas.com.br/tecido-e-couro)")

        qtd = st.radio("Quantas unidades deseja?", [
            "📦 1.000 a 3.000 unidades",
            "🚀 Mais de 3.000 unidades"
        ])

        if qtd == "📦 1.000 a 3.000 unidades":
            st.markdown("💡 A partir de **R$0,80/unidade** | Frete grátis")
            with st.form("form_tecido"):
                tipo = st.text_input("Tipo de etiqueta (couro sintético, sarja etc.)")
                tam = st.text_input("Tamanho (largura x altura)")
                acabamento = st.text_input("Acabamento (costura, termocolante etc.)")
                cores = st.selectbox("Número de cores:", ["1", "2", "3"])
                arte = st.file_uploader("Anexe sua arte ou referência")
                enviar = st.form_submit_button("Enviar orçamento")
                if enviar:
                    st.success("✅ Orçamento recebido! Retornaremos em até 12h úteis.")

        elif qtd == "🚀 Mais de 3.000 unidades":
            st.markdown("🚀 Atendimento Prioritário ativado!")
            st.text_area("Descreva seu pedido (tipo, tamanho, aplicação, arte etc.)")

    # Tags
    elif produto == "🔖 Tags":
        st.markdown("Pedido mínimo: **5.000 unidades** | A partir de **R$0,20/un** | Frete grátis")
        if st.button("Solicitar orçamento"):
            st.text_area("Descreva seu pedido (modelo, quantidade, arte...)")
            st.success("✅ Encaminhando sua solicitação para o especialista.")

    # Chaveiros
    elif produto == "🔑 Chaveiros":
        st.markdown("Pedido mínimo: **500 unidades**")
        chaveiro_opt = st.radio("Deseja:", [
            "🎨 Ver modelos de chaveiros",
            "💰 Solicitar orçamento"
        ])

        if chaveiro_opt == "🎨 Ver modelos de chaveiros":
            st.markdown("📎 [Modelos de Chaveiros](https://realetiquetas.com.br/chaveiros)")

        qtd = st.radio("Quantas unidades deseja?", ["500 a 1.000", "Mais de 1.000"])
        if qtd == "500 a 1.000":
            st.markdown("💡 A partir de **R$2,00/unidade** | Frete grátis")
            with st.form("form_chaveiro"):
                qtd_input = st.text_input("Quantidade exata")
                tam = st.text_input("Tamanho aproximado")
                formato = st.text_input("Formato ou tipo")
                arte = st.file_uploader("Anexe arte ou referência")
                enviar = st.form_submit_button("Enviar orçamento")
                if enviar:
                    st.success("✅ Orçamento solicitado com sucesso! Em breve retornaremos.")

        elif qtd == "Mais de 1.000":
            st.markdown("🚀 Atendimento Prioritário ativado!")
            st.text_area("Descreva seu pedido (quantidade, tamanho, formato, arte etc.)")

    # Outros
    elif produto == "📦 Outros":
        st.text_area("Conte para nós o que você precisa:")
        st.success("Recebido! Estamos direcionando ao especialista.")
        
# 1.3 Já sou cliente
elif opcao == "🙋‍♀️ Já sou cliente – Falar com um atendente":
    st.markdown("### 🙋‍♀️ Atendimento para Clientes")
    with st.form("form_cliente"):
        nome = st.text_input("Seu nome completo:")
        tel = st.text_input("Telefone cadastrado:")
        enviado = st.form_submit_button("Enviar para atendimento")
        if enviado:
            st.success("🔁 Encaminhado com sucesso! Nossa equipe falará com você em instantes.")
