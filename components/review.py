import streamlit as st


STATUS_LABELS = {
    "requires_human_review": "Requer revisão",
    "changes_requested": "Alterações solicitadas",
    "approved": "Aprovado",
}


def render_review(
    asset: dict,
    validation_outdated: bool,
) -> dict:

    st.subheader("Human Review")

    current_status = asset[
        "review"
    ].get(
        "status",
        "requires_human_review",
    )

    st.write(
        "**Status atual:** "
        + STATUS_LABELS.get(
            current_status,
            current_status,
        )
    )

    notes = st.text_area(
        "Review notes",
        value=asset[
            "review"
        ].get(
            "notes",
            "",
        ),
        placeholder=(
            "Adicione comentários para "
            "a revisão, se necessário."
        ),
    )

    asset["review"]["notes"] = notes

    if validation_outdated:
        st.warning(
            "O conteúdo foi alterado após "
            "a última validação. Revalide "
            "antes de aprovar."
        )

    left, right = st.columns(2)

    with left:
        request_changes = st.button(
            "Solicitar ajustes",
            use_container_width=True,
        )

    with right:
        approve = st.button(
            "Aprovar asset",
            type="primary",
            disabled=validation_outdated,
            use_container_width=True,
        )

    if request_changes:
        asset["review"][
            "status"
        ] = "changes_requested"

        st.warning(
            "Asset marcado como "
            "'Alterações solicitadas'."
        )

    if approve:
        asset["review"][
            "status"
        ] = "approved"

        st.success(
            "Asset aprovado."
        )

    return asset