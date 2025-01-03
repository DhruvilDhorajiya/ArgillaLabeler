import streamlit as st

def display_question_page():

    # Initialize session state variables
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "selected_question_type" not in st.session_state:
        st.session_state.selected_question_type = "Label"  # Default to Label

    st.markdown("### Add Questions and Related Information")

    # Dropdown for selecting question type (outside the form)
    st.markdown("**Select question type:**")
    selected_question_type = st.selectbox(
        "Choose the type of question",
        ["Label", "Multi-label", "Rating"],
        index=["Label", "Multi-label", "Rating"].index(st.session_state.selected_question_type)
    )

    # Update session state when the user changes the question type
    st.session_state.selected_question_type = selected_question_type

    # Input fields for adding a question within a form
    with st.form(key="add_question_form", clear_on_submit=True):
        question_title = st.text_input("Describe Question Title (e.g., overall Quality):", key="question_title")

        # Label description input
        label_description = st.text_input("Describe Question information (e.g., overall Quality of LLM Response):", key="label_description")

        # Conditionally show labels input based on question type
        labels = []
        if st.session_state.selected_question_type in ["Label", "Multi-label"]:
            st.markdown(f"**Define possible {st.session_state.selected_question_type.lower()} options (comma-separated):**")
            labels_input = st.text_input("Example: Good, Average, Bad", key="labels_input")
            labels = [label.strip() for label in labels_input.split(",") if label.strip()]

        # Form submission button
        submit_button = st.form_submit_button("Add Question")

    # Handle form submission
    if submit_button:
        if not label_description.strip():
            st.warning("Please provide a question description.")
        elif not question_title.strip():
             st.warning("Please provide a question title.")
        elif st.session_state.selected_question_type in ["Label", "Multi-label"] and not labels:
            st.warning("Please define at least one label.")
        else:
            # Add question details to session state
            question_data = {
                'question_title': question_title,
                "label_description": label_description,
                "question_type": st.session_state.selected_question_type,
                "labels": labels if st.session_state.selected_question_type in ["Label", "Multi-label"] else None,
            }
            st.session_state.questions.append(question_data)
            st.success("Question added successfully!")

    # Display the list of added questions
    if st.session_state.questions:
        st.markdown("### Added Questions")
        for idx, question in enumerate(st.session_state.questions, start=1):
            st.markdown(f"**{idx}. Question title:** {question['question_title']}")
            st.markdown(f"**Question Description:** {question['label_description']}")
            st.markdown(f"**Question Type:** {question['question_type']}")
            if question['question_type'] in ["Label", "Multi-label"]:
                st.markdown(f"**Labels:** {', '.join(question['labels'])}")
            st.markdown("---")

    # Go back button
    if st.button("Go Back"):
        st.session_state.page = 1
    
    # Next button to navigate to the labeling page (third page)
    if st.button("Next"):
        # You can optionally add any validation to ensure questions are added before proceeding.
        if st.session_state.questions:
            st.session_state.page = 3  # Move to the labeling page
        else:
            st.warning("Please add at least one question before proceeding.")
