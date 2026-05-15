import streamlit as st
from pydantic import ValidationError

from empathy_engine.errors import EmpathyEngineError
from empathy_engine.config import load_settings
from empathy_engine.i18n.language import (
    LANGUAGE_LABELS,
    SUPPORTED_UI_LANGUAGES,
    get_default_ui_language,
    translate,
)
from empathy_engine.operations import get_local_runtime_status
from empathy_engine.safety.logging import configure_safe_logging
from empathy_engine.storage.interaction_store import InteractionStore
from empathy_engine.use_cases.analyze_interaction import (
    AnalyzeInteractionCommand,
    AnalyzeInteractionUseCase,
)

st.set_page_config(
    page_title="Empathy-Interactional-Expertise",
    layout="wide"
)

st.title("Empathy-Interactional-Expertise")
configure_safe_logging()

try:
    settings = load_settings()
    default_language = get_default_ui_language()
except (ValueError, ValidationError) as error:
    st.error(f"Invalid application configuration: {error}")
    st.stop()

selected_language = st.sidebar.selectbox(
    translate(default_language, "ui_language"),
    SUPPORTED_UI_LANGUAGES,
    index=SUPPORTED_UI_LANGUAGES.index(default_language),
    format_func=lambda language: LANGUAGE_LABELS[language],
)

t = lambda key: translate(selected_language, key)
store = InteractionStore()

with st.sidebar.expander("Local status", expanded=False):
    status = get_local_runtime_status(settings)
    st.text(f"Model: {status.model}")
    st.text(f"Ollama: {'available' if status.ollama_available else 'unavailable'}")
    st.text(f"Processing language: {status.processing_language}")
    st.text(f"Database: {status.database_path}")

with st.sidebar.expander("Local data", expanded=False):
    records = store.list(limit=5)
    st.caption(f"Stored records: {len(records)} shown")

    if records:
        for record in records:
            st.text(f"#{record.id} - {record.created_at}")
            st.caption(record.feedback or "no feedback")

        delete_id = st.number_input(
            "Delete record id",
            min_value=1,
            step=1,
            value=records[0].id,
        )
        if st.button("Delete selected local record"):
            deleted = store.delete(int(delete_id))
            st.info(f"Deleted records: {deleted}")

        if st.button("Delete all local records"):
            deleted = store.delete_all()
            st.info(f"Deleted records: {deleted}")
    else:
        st.caption("No local records.")

st.subheader(t("subtitle"))

st.markdown(t("intro"))

st.info(t("notice"))

interaction = st.text_area(
    t("interaction_label"),
    height=200,
    placeholder=t("interaction_placeholder"),
    help=t("interaction_help")
)

store_consent = st.checkbox(
    t("consent"),
    value=False,
    help=t("consent_help")
)

feedback = st.radio(
    t("feedback"),
    t("feedback_options"),
    horizontal=True,
    index=None,
    help=t("feedback_help")
)

if st.button(t("analyze"), type="primary", use_container_width=True):
    if not interaction.strip():
        st.warning(t("missing_interaction"))
    else:
        with st.spinner(t("spinner")):
            try:
                use_case = AnalyzeInteractionUseCase()
                analysis = use_case.execute(
                    AnalyzeInteractionCommand(
                        interaction=interaction,
                        output_language=selected_language,
                        store_consent=store_consent,
                        feedback=feedback,
                    )
                )
            except EmpathyEngineError as error:
                st.error(str(error))
                st.stop()
            result = analysis.workflow_result
            display_result = analysis.display_result

        st.success(t("success"))

        if not display_result["safety"]["safe"]:
            st.warning(display_result["safety"]["guidance"])

        st.markdown(t("context_heading"))
        st.write(t("context_text"))
        st.caption(
            t("language_note").format(
                user_language=LANGUAGE_LABELS[result["language"]["user_language"]]
            )
        )

        st.markdown(t("translation_heading"))
        st.write(t("for_user"))
        st.write(display_result["translation"]["translation_for_user"])
        st.write(t("for_other"))
        st.write(display_result["translation"]["translation_for_other_person"])

        st.markdown(t("bridge_heading"))
        st.write(display_result["response"]["bridge_message"])

        st.markdown(t("learning_heading"))
        st.write(display_result["learning"]["reflection_question"])

        st.markdown(t("privacy_heading"))
        if store_consent:
            st.info(t("stored").format(record_id=analysis.stored_record_id))
        else:
            st.info(t("not_stored"))
