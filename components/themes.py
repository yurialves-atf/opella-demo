import streamlit as st


ASSET_LABELS = {
    "banner_memed": "Banner Memed",
    "article_pharmacist": "Artigo para farmacêutico",
    "flyer": "Flyer / lâmina",
}


def render_theme_selector(
    analysis: dict,
) -> dict:

    themes = analysis[
        "themes"
    ]

    themes_by_id = {
        theme["id"]: theme
        for theme in themes
    }

    selected_id = (
        st.selectbox(
            "Oportunidade de conteúdo",
            options=list(
                themes_by_id.keys()
            ),
            format_func=lambda theme_id: (
                themes_by_id[
                    theme_id
                ]["title"]
            ),
            label_visibility="collapsed",
        )
    )

    selected_theme = (
        themes_by_id[
            selected_id
        ]
    )


    # ---------------------------------
    # Opportunity card
    # ---------------------------------

    with st.container(
        border=True
    ):

        st.caption(
            "OPORTUNIDADE DE CONTEÚDO"
        )

        st.markdown(
            f"## {selected_theme['title']}"
        )


        # Problem
        st.markdown(
            "#### Problema / contexto"
        )

        st.write(
            selected_theme[
                "problem_context"
            ]
        )


        # Product connection
        st.markdown(
            "#### Como o produto se conecta"
        )

        st.write(
            selected_theme[
                "product_connection"
            ]
        )


        # Rationale
        with st.expander(
            "Por que esta oportunidade "
            "foi sugerida?"
        ):

            st.write(
                selected_theme[
                    "rationale"
                ]
            )


        st.divider()


        # ---------------------------------
        # Indicators
        # ---------------------------------

        col1, col2 = (
            st.columns(2)
        )


        with col1:

            st.metric(
                "Claims de produto",
                selected_theme[
                    "available_product_claims"
                ],
            )


        with col2:

            pages = (
                selected_theme[
                    "relevant_pages"
                ]
            )

            pages_text = (
                ", ".join(
                    str(page)
                    for page in pages
                )
            )

            st.caption(
                "PÁGINAS SUGERIDAS"
            )

            st.write(
                pages_text
            )


        # ---------------------------------
        # Suggested assets
        # ---------------------------------

        suggested_assets = [
            ASSET_LABELS.get(
                asset,
                asset,
            )
            for asset
            in selected_theme[
                "suggested_assets"
            ]
        ]

        st.caption(
            "FORMATOS RECOMENDADOS"
        )

        st.write(
            " · ".join(
                suggested_assets
            )
        )


    return selected_theme