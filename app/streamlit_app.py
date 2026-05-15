import streamlit as st

from empathy_engine.orchestration.workflow import EmpathyWorkflow
from empathy_engine.storage.interaction_store import InteractionStore

st.set_page_config(
    page_title="Empathy-Interactional-Expertise",
    layout="wide"
)

st.title("Empathy-Interactional-Expertise")
st.subheader("AI-powered communication mediation with local privacy controls")

st.markdown(
    '''
    Describe a communication mismatch. The system will anonymize the text,
    run the multi-agent empathy workflow, and show a possible bridge.
    '''
)

st.info(
    "This tool offers communication support only. It does not provide "
    "clinical, legal, HR, or specialized educational advice."
)

interaction = st.text_area(
    "Interaction to analyze",
    height=200,
    placeholder=(
        "Example: My coworker thought my short message was rude, but I was "
        "trying to be clear because the meeting was running late."
    ),
    help=(
        "Avoid using real personal data during demos. If you include names, "
        "emails, phone numbers, or addresses, the workflow will try to mask them."
    )
)

store_consent = st.checkbox(
    "I consent to local storage of anonymized interactions",
    value=False,
    help="When unchecked, no interaction is written to the local SQLite database."
)

feedback = st.radio(
    "Response feedback",
    ["Useful and safe", "Partially useful", "Not useful"],
    horizontal=True,
    index=None,
    help="Optional feedback is stored only if local storage consent is selected."
)

if st.button("Analyze Interaction", type="primary", use_container_width=True):
    if not interaction.strip():
        st.warning("Please describe an interaction before analyzing.")
    else:
        with st.spinner("Running multi-agent empathy analysis..."):
            workflow = EmpathyWorkflow(use_llm=True)
            result = workflow.run(interaction)

        st.success("Possible empathy bridge identified.")

        if not result["safety"]["safe"]:
            st.warning(result["safety"]["guidance"])

        st.markdown("### Context")
        st.write(
            "The workflow found a possible mismatch in tone expectations and "
            "communication cues."
        )

        st.markdown("### Perspective Translation")
        st.write("For the user:")
        st.write(result["translation"]["translation_for_user"])
        st.write("For the other person:")
        st.write(result["translation"]["translation_for_other_person"])

        st.markdown("### Suggested Bridge")
        st.write(result["response"]["bridge_message"])

        st.markdown("### Learning Insight")
        st.write(result["learning"]["reflection_question"])

        st.markdown("### Privacy")
        if store_consent:
            record_id = InteractionStore().save(
                result["interaction"],
                result,
                feedback
            )
            st.info(f"Anonymized interaction stored locally as record {record_id}.")
        else:
            st.info("No interaction was stored.")
