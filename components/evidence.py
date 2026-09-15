import streamlit as st


def render_evidence(asset: dict) -> None:
    st.subheader("Medical Evidence")

    grounding = asset["grounding"]
    claims = grounding.get("claims", [])
    warnings = grounding.get("warnings", [])

    if not claims:
        st.info("Nenhuma evidência disponível.")
        return

    for index, claim in enumerate(claims, start=1):
        with st.expander(
            f"Claim {index} — página {claim['source_page']}",
            expanded=True,
        ):
            st.markdown("**Claim**")
            st.write(claim["claim"])

            st.markdown("**Evidência**")
            st.write(claim["source_evidence"])

    st.markdown("### Validação")

    st.success(
        f"{len(claims)} claim(s) possuem evidência associada."
    )

    if warnings:
        for warning in warnings:
            st.warning(warning)
    else:
        st.success("Nenhum warning identificado no mock.")