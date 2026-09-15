from copy import deepcopy
from pathlib import Path

import streamlit as st

from models.asset import MedicalAsset

from components.editor import render_editor
from components.evidence import render_evidence
from components.preview import render_preview
from components.review import render_review
from components.themes import render_theme_selector
from components.section import render_section_header
from components.stepper import (
    init_stepper,
    render_stepper,
    render_navigation,
)

from services.provider_factory import (
    get_medical_ai_service,
)


BASE_DIR = Path(__file__).parent

ASSETS_DIR = (
    BASE_DIR
    / "assets"
).resolve()


INITIAL_FLYER_PATH = (
    ASSETS_DIR
    / "flyer_dipirona_flash.jpg"
).resolve()


EDITED_FLYER_PATH = (
    ASSETS_DIR
    / "flyer_dipirona_flash_alterado_1.jpg"
).resolve()

# ==================================================
# CONFIGURAÇÕES
# ==================================================

MOCK_FILES = {
    "Banner Memed": "banner.json",
    "Artigo para farmacêutico": "article.json",
    "Flyer / lâmina": "flyer.json",
}


ASSET_DESCRIPTIONS = {
    "Banner Memed": (
        "Mensagem curta, direta e de alto impacto."
    ),
    "Artigo para farmacêutico": (
        "Conteúdo técnico com maior profundidade."
    ),
    "Flyer / lâmina": (
        "Resumo visual e educacional."
    ),
}


# ==================================================
# HELPERS
# ==================================================


def validate_mock_image(
    image_path: Path,
    image_name: str,
) -> bool:

    if not image_path.is_file():

        st.error(
            f"Imagem mock não encontrada: "
            f"{image_name}"
        )

        st.code(
            str(image_path)
        )

        return False

    return True

def load_css():
    css_path = (
        BASE_DIR
        / "styles"
        / "opella.css"
    )

    css = css_path.read_text(
        encoding="utf-8"
    )

    st.html(
        f"<style>{css}</style>"
    )


@st.cache_data
def load_mock_asset(
    case_name: str,
) -> dict:

    file_name = MOCK_FILES[
        case_name
    ]

    file_path = (
        BASE_DIR
        / "mocks"
        / file_name
    )

    json_content = (
        file_path.read_text(
            encoding="utf-8"
        )
    )

    asset = (
        MedicalAsset
        .model_validate_json(
            json_content
        )
    )

    return asset.model_dump()


@st.cache_resource
def get_ai_service():
    return get_medical_ai_service()


def clear_generated_content():

    keys_to_clear = [
        "selected_theme",
        "asset",
        "generated_for",
        "validated_content_snapshot",
        "validation_outdated",
        "visual_direction",

        # Asset generation
        "asset_version",
        "current_asset_image",

        # Refinement
        "refinement_prompt",
        "refinement_notes",
        "refinement_applied",
        "refinement_reference_names",
    ]

    for key in keys_to_clear:
        st.session_state.pop(
            key,
            None,
        )


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Medical Content Studio",
    page_icon="🧬",
    layout="wide",
)

load_css()


# ==================================================
# HERO
# ==================================================

hero_html = """
<section class="opella-hero">

    <div class="opella-eyebrow">
        OPELLA · MEDICAL CONTENT STUDIO
    </div>

    <div class="opella-hero-title">
        From monograph<br>
        to meaningful content.
    </div>

    <div class="opella-hero-subtitle">
        Transforme evidências médicas em oportunidades
        de comunicação, conteúdo e assets — mantendo
        rastreabilidade até a fonte.
    </div>

    <div class="opella-challenger-badge">
        AI-assisted
    </div>

</section>
"""

st.html(hero_html)


# ==================================================
# WORKFLOW
# ==================================================

init_stepper()

render_stepper()

st.divider()


current_step = (
    st.session_state.current_step
)


# ==================================================
# STEP 01
# SOURCE & OPPORTUNITIES
# ==================================================

if current_step == 1:

    render_section_header(
        1,
        "Source & Opportunities",
        (
            "Faça upload da monografia, processe o documento "
            "e escolha uma oportunidade de comunicação."
        ),
    )


    # ----------------------------------------------
    # SOURCE
    # ----------------------------------------------

    st.markdown(
        "### Fonte médica"
    )

    uploaded_file = st.file_uploader(
        "Monografia",
        type=["pdf"],
        key="monograph_uploader",
    )


    if uploaded_file is None:

        st.info(
            "Faça upload de uma monografia para iniciar."
        )

    else:

        st.success(
            f"Arquivo carregado: {uploaded_file.name}"
        )


    analyze_clicked = st.button(
        "Analisar monografia",
        type="primary",
        disabled=(
            uploaded_file is None
        ),
    )


    # ----------------------------------------------
    # ANALYSIS
    # ----------------------------------------------

    if analyze_clicked:

        try:

            service = (
                get_ai_service()
            )

            pdf_bytes = (
                uploaded_file.getvalue()
            )

            with st.status(
                "Analisando monografia...",
                expanded=True,
            ) as status:

                st.write(
                    "Carregando análise da monografia..."
                )

                analysis_model = (
                    service.analyze_monograph(
                        pdf_bytes=pdf_bytes,
                        filename=uploaded_file.name,
                    )
                )

                analysis = (
                    analysis_model.model_dump()
                )

                analysis[
                    "document_name"
                ] = uploaded_file.name

                status.update(
                    label="Análise concluída",
                    state="complete",
                )


            clear_generated_content()


            st.session_state[
                "monograph_analysis"
            ] = analysis


            st.success(
                "Monografia analisada com sucesso."
            )


        except Exception as exc:

            st.error(
                "Não foi possível carregar "
                "a análise da monografia."
            )

            st.exception(exc)


    # ----------------------------------------------
    # CONTENT OPPORTUNITIES
    # ----------------------------------------------

    analysis = st.session_state.get(
        "monograph_analysis"
    )


    if analysis:

        st.divider()

        st.markdown(
            "### Content Opportunities"
        )

        st.caption(
            "Oportunidades de comunicação "
            "identificadas a partir da monografia."
        )


        # Product card

        with st.container(
            border=True
        ):

            st.caption(
                "PRODUTO IDENTIFICADO"
            )

            st.markdown(
                f"## {analysis['product_name']}"
            )

            st.write(
                analysis[
                    "document_summary"
                ]
            )


        st.markdown(
            "### Escolha uma oportunidade"
        )


        selected_theme = (
            render_theme_selector(
                analysis
            )
        )


        st.session_state[
            "selected_theme"
        ] = selected_theme


    # ----------------------------------------------
    # NAVIGATION
    # ----------------------------------------------

    can_advance = (
        st.session_state.get(
            "monograph_analysis"
        )
        is not None
        and
        st.session_state.get(
            "selected_theme"
        )
        is not None
    )


    st.divider()

    render_navigation(
        can_advance=can_advance
    )


# ==================================================
# STEP 02
# AI DRAFT & CLAIMS
# ==================================================

elif current_step == 2:

    render_section_header(
        2,
        "AI Draft & Claims",
        (
            "Escolha o formato, gere o draft e revise "
            "o conteúdo junto às evidências."
        ),
    )


    selected_theme = (
        st.session_state.get(
            "selected_theme"
        )
    )


    if selected_theme is None:

        st.warning(
            "Nenhuma oportunidade de conteúdo "
            "foi selecionada."
        )

        render_navigation(
            can_advance=False
        )

        st.stop()


    # ----------------------------------------------
    # SELECTED THEME
    # ----------------------------------------------

    st.caption(
        "OPORTUNIDADE SELECIONADA"
    )

    st.markdown(
        f"## {selected_theme['title']}"
    )


    # ----------------------------------------------
    # ASSET TYPE
    # ----------------------------------------------

    st.markdown(
        "### Formato do asset"
    )


    case_name = st.radio(
        "Escolha o asset",
        list(
            MOCK_FILES.keys()
        ),
        horizontal=True,
        label_visibility="collapsed",
        key="asset_type_choice",
    )


    st.caption(
        ASSET_DESCRIPTIONS[
            case_name
        ]
    )


    # Recommended format

    asset_ids = {
        "Banner Memed":
            "banner_memed",

        "Artigo para farmacêutico":
            "article_pharmacist",

        "Flyer / lâmina":
            "flyer",
    }


    selected_asset_id = (
        asset_ids[
            case_name
        ]
    )


    if (
        selected_asset_id
        in selected_theme[
            "suggested_assets"
        ]
    ):

        st.caption(
            "✓ Formato recomendado "
            "para esta oportunidade"
        )


    generate_clicked = (
        st.button(
            "Gerar conteúdo",
            type="primary",
        )
    )


    # ----------------------------------------------
    # GENERATE MOCK CONTENT
    # ----------------------------------------------

    if generate_clicked:

        asset = (
            load_mock_asset(
                case_name
            )
        )


        st.session_state[
            "asset"
        ] = asset


        st.session_state[
            "generated_for"
        ] = {
            "theme_id":
                selected_theme[
                    "id"
                ],

            "case_name":
                case_name,
        }


        st.session_state[
            "validated_content_snapshot"
        ] = deepcopy(
            asset[
                "content"
            ]
        )


        st.session_state[
            "validation_outdated"
        ] = False


        # --------------------------
        # MOCK VISUAL GENERATION
        # --------------------------

        st.session_state[
            "asset_version"
        ] = "initial"

        st.session_state[
            "current_asset_image"
        ] = str(
            INITIAL_FLYER_PATH
        )

        st.session_state[
            "refinement_applied"
        ] = False

        st.session_state[
            "refinement_skipped"
        ] = False

        st.success(
            "Conteúdo gerado."
        )


    # ----------------------------------------------
    # VERIFY SELECTION
    # ----------------------------------------------

    generated_for = (
        st.session_state.get(
            "generated_for"
        )
    )


    asset = (
        st.session_state.get(
            "asset"
        )
    )


    selection_matches = False


    if (
        generated_for
        and asset
    ):

        selection_matches = (
            generated_for[
                "theme_id"
            ]
            ==
            selected_theme[
                "id"
            ]
            and
            generated_for[
                "case_name"
            ]
            ==
            case_name
        )


    if (
        asset
        and not selection_matches
    ):

        st.info(
            "Você alterou o tipo de asset. "
            "Clique em 'Gerar conteúdo' "
            "para criar um novo draft."
        )


    # ----------------------------------------------
    # AI DRAFT
    # ----------------------------------------------

    if (
        asset
        and selection_matches
    ):

        st.divider()

        st.markdown(
            "### Content Draft"
        )


        left, right = (
            st.columns(
                [1.35, 1],
                gap="large",
            )
        )


        # CONTENT EDITOR

        with left:

            edited_asset = (
                render_editor(
                    asset
                )
            )


        # VALIDATION STATE

        validated_snapshot = (
            st.session_state.get(
                "validated_content_snapshot"
            )
        )


        validation_outdated = (
            edited_asset[
                "content"
            ]
            !=
            validated_snapshot
        )


        st.session_state[
            "validation_outdated"
        ] = validation_outdated


        # EVIDENCE PANEL

        with right:

            if validation_outdated:

                st.warning(
                    "O conteúdo foi editado "
                    "após a última validação."
                )


                revalidate = (
                    st.button(
                        "Revalidar conteúdo"
                    )
                )


                if revalidate:

                    # MOCK:
                    # futuramente será
                    # validação por modelo.

                    st.session_state[
                        "validated_content_snapshot"
                    ] = deepcopy(
                        edited_asset[
                            "content"
                        ]
                    )


                    st.session_state[
                        "validation_outdated"
                    ] = False


                    st.success(
                        "Conteúdo revalidado."
                    )


                    st.rerun()


            else:

                st.success(
                    "Conteúdo validado."
                )


            render_evidence(
                edited_asset
            )


        st.session_state[
            "asset"
        ] = edited_asset


    # ----------------------------------------------
    # NAVIGATION
    # ----------------------------------------------

    asset = (
        st.session_state.get(
            "asset"
        )
    )


    validation_outdated = (
        st.session_state.get(
            "validation_outdated",
            False,
        )
    )


    can_advance = (
        asset is not None
        and selection_matches
        and not validation_outdated
    )


    st.divider()

    render_navigation(
        can_advance=can_advance
    )


# ==================================================
# STEP 03
# INITIAL ASSET
# ==================================================

elif current_step == 3:

    render_section_header(
        3,
        "Initial Asset",
        (
            "Confira a primeira versão visual "
            "gerada a partir do conteúdo aprovado."
        ),
    )


    asset = (
        st.session_state.get(
            "asset"
        )
    )


    selected_theme = (
        st.session_state.get(
            "selected_theme"
        )
    )


    if asset is None:

        st.warning(
            "Nenhum conteúdo foi gerado."
        )

        render_navigation(
            can_advance=False
        )

        st.stop()


    # ----------------------------------------------
    # CONTEXT
    # ----------------------------------------------

    with st.container(
        border=True
    ):

        st.caption(
            "ASSET GERADO"
        )

        if selected_theme:

            st.markdown(
                f"### {selected_theme['title']}"
            )

        st.write(
            "Primeira versão visual criada "
            "a partir do conteúdo e das "
            "evidências selecionadas."
        )


    # ----------------------------------------------
    # INITIAL ASSET
    # ----------------------------------------------

    st.markdown(
        "### Versão inicial"
    )


    # Para o mock atual, o flyer visual é
    # a fonte oficial da etapa 3.

    current_image = (
        st.session_state.get(
            "current_asset_image"
        )
    )


    # Caso o estado ainda não tenha sido
    # inicializado, usamos o flyer mock.

    if not current_image:

        current_image = str(
            INITIAL_FLYER_PATH
        )

        st.session_state[
            "current_asset_image"
        ] = current_image

        st.session_state[
            "asset_version"
        ] = "initial"


    current_image_path = Path(
        current_image
    )


    image_ok = validate_mock_image(
        current_image_path,
        "Flyer Novalgina Flash — versão inicial",
    )


    if not image_ok:

        render_navigation(
            can_advance=False
        )

        st.stop()


    # ----------------------------------------------
    # DISPLAY
    # ----------------------------------------------

    preview_col, info_col = st.columns(
        [0.8, 1.2],
        gap="large",
    )


    with preview_col:

        st.image(
        str(
            current_image_path
        ),
        caption="Flyer gerado — versão 1",
        use_container_width=True,
    )


    with info_col:

        st.caption(
            "VERSÃO ATUAL"
        )

        st.markdown(
            "### Asset inicial"
        )

        st.write(
            "Esta é a primeira versão "
            "gerada antes de qualquer "
            "refinamento visual."
        )

        st.markdown(
            "**Próximo passo**"
        )

        st.write(
            "Na etapa seguinte você poderá "
            "pedir alterações pontuais usando "
            "um prompt e imagens de referência."
        )


    st.divider()


    render_navigation(
        can_advance=True
    )


# ==================================================
# STEP 04
# REFINE WITH PROMPT
# ==================================================

elif current_step == 4:

    render_section_header(
        4,
        "Refine with Prompt",
        (
            "Peça alterações pontuais no asset usando "
            "instruções textuais e referências visuais."
        ),
    )


    asset = st.session_state.get(
        "asset"
    )


    if asset is None:

        st.warning(
            "Nenhum asset disponível "
            "para refinamento."
        )

        render_navigation(
            can_advance=False
        )

        st.stop()


    # ==================================================
    # CURRENT VERSION
    # ==================================================

    st.markdown(
        "### Asset atual"
    )


    current_image = (
        st.session_state.get(
            "current_asset_image"
        )
    )


    # Caso o estado não exista por algum motivo,
    # voltamos explicitamente para o flyer inicial.

    if not current_image:

        current_image = str(
            INITIAL_FLYER_PATH
        )

        st.session_state[
            "current_asset_image"
        ] = current_image

        st.session_state[
            "asset_version"
        ] = "initial"


    current_image_path = Path(
        current_image
    )


    # Validação antes de chamar st.image()

    image_ok = validate_mock_image(
        current_image_path,
        "Asset atual",
    )


    if not image_ok:

        render_navigation(
            can_advance=False
        )

        st.stop()


    # ----------------------------------------------
    # DISPLAY CURRENT ASSET
    # ----------------------------------------------

    asset_col, info_col = st.columns(
        [1.05, 0.95],
        gap="large",
    )


    with asset_col:

        st.image(
            str(
                current_image_path
            ),
            caption="Versão atual",
            width=520,
        )


    with info_col:

        asset_version = (
            st.session_state.get(
                "asset_version",
                "initial",
            )
        )

        st.caption(
            "VERSÃO DO ASSET"
        )


        if asset_version == "edited":

            st.markdown(
                "### Versão refinada"
            )

            st.write(
                "Esta versão já contém "
                "alterações solicitadas "
                "anteriormente."
            )

        else:

            st.markdown(
                "### Versão inicial"
            )

            st.write(
                "Esta é a primeira versão "
                "gerada. Você pode solicitar "
                "alterações abaixo."
            )


    st.divider()


    # ==================================================
    # EDIT REQUEST
    # ==================================================

    st.markdown(
        "### Solicite uma alteração"
    )

    st.write(
        "Descreva o que deseja modificar. "
        "Você também pode anexar imagens "
        "para orientar a alteração visual."
    )


    # ----------------------------------------------
    # PROMPT
    # ----------------------------------------------

    refinement_prompt = st.text_area(
        "Prompt de edição",
        value=st.session_state.get(
            "refinement_prompt",
            "",
        ),
        placeholder=(
            "Ex.: Troque os elementos visuais dos "
            "relógios por barras de carregamento. "
            "Utilize a referência anexada para o "
            "estilo das barras, mantendo o restante "
            "da composição e identidade visual."
        ),
        height=150,
        key="refinement_prompt_input",
    )


    st.session_state[
        "refinement_prompt"
    ] = refinement_prompt


    # ----------------------------------------------
    # REFERENCE IMAGES
    # ----------------------------------------------

    reference_images = st.file_uploader(
        "Imagens de referência",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp",
        ],
        accept_multiple_files=True,
        key="refinement_reference_images",
    )


    if reference_images:

        st.caption(
            "REFERÊNCIAS ANEXADAS"
        )


        reference_names = [
            file.name
            for file in reference_images
        ]


        st.session_state[
            "refinement_reference_names"
        ] = reference_names


        number_of_columns = min(
            len(reference_images),
            3,
        )


        columns = st.columns(
            number_of_columns
        )


        for index, image in enumerate(
            reference_images
        ):

            with columns[
                index
                % number_of_columns
            ]:

                st.image(
                    image,
                    caption=image.name,
                    use_container_width=True,
                )


    else:

        # Evita manter nomes de arquivos
        # removidos pelo usuário.

        st.session_state[
            "refinement_reference_names"
        ] = []


    # ----------------------------------------------
    # ADDITIONAL TEXT / NOTES
    # ----------------------------------------------

    refinement_notes = st.text_area(
        "Texto ou observações adicionais",
        value=st.session_state.get(
            "refinement_notes",
            "",
        ),
        placeholder=(
            "Opcional: inclua textos que devem "
            "ser adicionados, removidos ou preservados."
        ),
        height=100,
        key="refinement_notes_input",
    )


    st.session_state[
        "refinement_notes"
    ] = refinement_notes


    # ==================================================
    # ACTIONS
    # ==================================================

    st.markdown(
        "#### O que deseja fazer?"
    )


    skip_col, apply_col = st.columns(
        [1, 1],
        gap="medium",
    )


    with skip_col:

        skip_refinement = st.button(
            "Pular refinamento",
            use_container_width=True,
        )


    with apply_col:

        apply_change = st.button(
            "Aplicar alteração",
            type="primary",
            disabled=(
                not refinement_prompt.strip()
            ),
            use_container_width=True,
        )


    # ==================================================
    # SKIP REFINEMENT
    # ==================================================

    if skip_refinement:

        initial_image_ok = (
            validate_mock_image(
                INITIAL_FLYER_PATH,
                (
                    "Flyer Novalgina Flash "
                    "— versão inicial"
                ),
            )
        )


        if not initial_image_ok:

            st.stop()


        # Volta explicitamente para a
        # versão inicial.

        st.session_state[
            "current_asset_image"
        ] = str(
            INITIAL_FLYER_PATH
        )

        st.session_state[
            "asset_version"
        ] = "initial"

        st.session_state[
            "refinement_applied"
        ] = False

        st.session_state[
            "refinement_skipped"
        ] = True


        # Vai diretamente para Review & Approval

        st.session_state[
            "current_step"
        ] = 5


        st.rerun()


    # ==================================================
    # APPLY MOCK EDIT
    # ==================================================

    if apply_change:

        # Antes de simular a IA,
        # verificamos se o resultado mock existe.

        edited_image_ok = (
            validate_mock_image(
                EDITED_FLYER_PATH,
                (
                    "Flyer Novalgina Flash "
                    "— versão refinada"
                ),
            )
        )


        if not edited_image_ok:

            st.stop()


        with st.status(
            "Aplicando alterações...",
            expanded=True,
        ) as status:

            st.write(
                "Interpretando instruções..."
            )

            st.write(
                "Analisando referências visuais..."
            )

            st.write(
                "Preservando conteúdo médico "
                "e identidade do produto..."
            )


            # --------------------------------------
            # MOCK
            #
            # Futuramente:
            #
            # updated_image =
            # image_ai_service.refine_asset(
            #     current_asset=current_image,
            #     prompt=refinement_prompt,
            #     references=reference_images,
            #     notes=refinement_notes,
            # )
            #
            # --------------------------------------

            st.session_state[
                "current_asset_image"
            ] = str(
                EDITED_FLYER_PATH
            )

            st.session_state[
                "asset_version"
            ] = "edited"

            st.session_state[
                "refinement_applied"
            ] = True

            st.session_state[
                "refinement_skipped"
            ] = False


            status.update(
                label="Nova versão gerada",
                state="complete",
            )


        st.rerun()


    # ==================================================
    # RESULT
    # ==================================================

    if st.session_state.get(
        "refinement_applied",
        False,
    ):

        st.divider()

        st.markdown(
            "### Resultado da alteração"
        )


        initial_ok = validate_mock_image(
            INITIAL_FLYER_PATH,
            "Versão inicial",
        )

        edited_ok = validate_mock_image(
            EDITED_FLYER_PATH,
            "Versão refinada",
        )


        if initial_ok and edited_ok:

            before, after = st.columns(
                2,
                gap="large",
            )


            with before:

                st.caption(
                    "ANTES"
                )

                st.image(
                    str(
                        INITIAL_FLYER_PATH
                    ),
                    caption="Versão inicial",
                    use_container_width=True,
                )


            with after:

                st.caption(
                    "VERSÃO ATUALIZADA"
                )

                st.image(
                    str(
                        EDITED_FLYER_PATH
                    ),
                    caption="Versão refinada",
                    use_container_width=True,
                )


            st.success(
                "Alteração aplicada. "
                "A versão atualizada será "
                "enviada para revisão."
            )


    # ==================================================
    # NAVIGATION
    # ==================================================

    st.divider()


    render_navigation(
        can_advance=(
            st.session_state.get(
                "refinement_applied",
                False,
            )
        )
    )

# ==================================================
# STEP 05
# REVIEW & APPROVAL
# ==================================================

elif current_step == 5:

    render_section_header(
        5,
        "Revisão & Aprovação",
        (
            "Revise a versão final do asset, "
            "confira as evidências e finalize "
            "a aprovação."
        ),
    )


    asset = (
        st.session_state.get(
            "asset"
        )
    )


    if asset is None:

        st.warning(
            "Nenhum asset disponível "
            "para revisão."
        )

        render_navigation()

        st.stop()


    # ----------------------------------------------
    # FINAL ASSET
    # ----------------------------------------------

    st.markdown(
        "### Versão para aprovação"
    )


    final_image = (
        st.session_state.get(
            "current_asset_image"
        )
    )


    refinement_applied = (
        st.session_state.get(
            "refinement_applied",
            False,
        )
    )

    refinement_skipped = (
        st.session_state.get(
            "refinement_skipped",
            False,
        )
    )


    if final_image:

        left, right = st.columns(
            [1.15, 1],
            gap="large",
        )


        with left:

            st.image(
                final_image,
                caption=(
                    "Asset final proposto"
                ),
                use_container_width=True,
            )


        with right:

            st.caption(
                "VERSÃO"
            )

            if refinement_applied:

                st.markdown(
                    "### Versão refinada"
                )

                st.write(
                    "Este asset contém as alterações "
                    "solicitadas na etapa anterior."
                )


                prompt = (
                    st.session_state.get(
                        "refinement_prompt",
                        ""
                    )
                )


                if prompt:

                    st.markdown(
                        "#### Alteração solicitada"
                    )

                    st.write(
                        prompt
                    )


                reference_names = (
                    st.session_state.get(
                        "refinement_reference_names",
                        [],
                    )
                )


                if reference_names:

                    st.markdown(
                        "#### Referências utilizadas"
                    )

                    for name in reference_names:

                        st.write(
                            f"• {name}"
                        )


                notes = (
                    st.session_state.get(
                        "refinement_notes",
                        ""
                    )
                )


                if notes:

                    st.markdown(
                        "#### Observações adicionais"
                    )

                    st.write(
                        notes
                    )

            else:

                st.markdown(
                    "### Versão inicial"
                )

                if refinement_skipped:

                    st.write(
                        "O refinamento foi pulado. "
                        "A versão original gerada será "
                        "utilizada para aprovação."
                    )

                else:

                    st.write(
                        "Nenhum refinamento visual "
                        "foi aplicado."
                    )


    st.divider()


    # ----------------------------------------------
    # MEDICAL EVIDENCE
    # ----------------------------------------------

    st.markdown(
        "### Evidence & Validation"
    )


    validation_outdated = (
        st.session_state.get(
            "validation_outdated",
            False,
        )
    )


    if validation_outdated:

        st.warning(
            "O conteúdo foi alterado após "
            "a última validação."
        )

    else:

        st.success(
            "O conteúdo está validado."
        )


    render_evidence(
        asset
    )


    st.divider()


    # ----------------------------------------------
    # HUMAN REVIEW
    # ----------------------------------------------

    reviewed_asset = (
        render_review(
            asset,
            validation_outdated,
        )
    )


    st.session_state[
        "asset"
    ] = reviewed_asset


    st.divider()


    # ----------------------------------------------
    # NAVIGATION
    # ----------------------------------------------

    render_navigation()