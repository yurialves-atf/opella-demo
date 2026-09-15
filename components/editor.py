from copy import deepcopy

import streamlit as st


def render_editor(asset: dict) -> dict:
    data = deepcopy(asset)

    content = data["content"]
    asset_type = data["asset_type"]

    st.subheader("Conteúdo gerado")
    st.caption("Nesta etapa os valores vêm de um mock.")

    content["headline"] = st.text_input(
        "Headline",
        value=content.get("headline", ""),
        key=f"{asset_type}_headline",
    )

    content["subheadline"] = st.text_area(
        "Subheadline",
        value=content.get("subheadline", ""),
        key=f"{asset_type}_subheadline",
        height=80,
    )

    if content.get("sections"):
        st.markdown("#### Seções")

        for i, section in enumerate(content["sections"]):
            section["title"] = st.text_input(
                f"Título da seção {i + 1}",
                value=section["title"],
                key=f"{asset_type}_section_title_{i}",
            )

            section["text"] = st.text_area(
                f"Texto da seção {i + 1}",
                value=section["text"],
                key=f"{asset_type}_section_text_{i}",
                height=110,
            )

    if content.get("key_points"):
        st.markdown("#### Key points")

        key_points_text = "\n".join(content["key_points"])

        edited_points = st.text_area(
            "Um item por linha",
            value=key_points_text,
            key=f"{asset_type}_key_points",
            height=130,
        )

        content["key_points"] = [
            item.strip()
            for item in edited_points.splitlines()
            if item.strip()
        ]

    if content.get("evidence_blocks"):
        st.markdown("#### Blocos de destaque")

        for i, block in enumerate(content["evidence_blocks"]):
            block["metric"] = st.text_input(
                f"Métrica {i + 1}",
                value=block.get("metric") or "",
                key=f"{asset_type}_metric_{i}",
            )

            block["message"] = st.text_area(
                f"Mensagem {i + 1}",
                value=block["message"],
                key=f"{asset_type}_metric_message_{i}",
                height=80,
            )

    content["product_message"] = st.text_area(
        "Mensagem do produto",
        value=content.get("product_message", ""),
        key=f"{asset_type}_product",
        height=80,
    )

    content["cta"] = st.text_input(
        "CTA",
        value=content.get("cta", ""),
        key=f"{asset_type}_cta",
    )

    content["disclaimer"] = st.text_area(
        "Disclaimer",
        value=content.get("disclaimer", ""),
        key=f"{asset_type}_disclaimer",
        height=80,
    )

    data["content"] = content

    return data