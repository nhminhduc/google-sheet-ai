import os
import streamlit as st
import streamlit_analytics

from core.GoogleSheetPublic import fetch_data
from core.OpenAI import llm_run


def apply_custom_css():
    """
    Applies custom CSS for styling the app.
    """
    custom_css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Open+Sans&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');
            
            body {
                font-family: 'Open Sans', sans-serif;
            }
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Poppins', sans-serif;
            }
            footer {
                visibility: hidden !important;
            }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def apply_analytics():
    """
    Applies analytics to the app.
    """
    ga_code = """
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-EZ0GF3XPK5"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-EZ0GF3XPK5');
    </script>
    """
    st.markdown(ga_code, unsafe_allow_html=True)


def create_save_to_clipboard(button_key, state_key):
    """
    Generates 'Save to Clipboard' functionality.
    """
    left_column, right_column = st.columns([5, 1])
    with left_column:
        st.write(
            "Ensure you've saved all necessary information. Press the button to copy the above refined output fields to the clipboard."
        )
    with right_column:
        st.components.v1.html(
            f"""
            <textarea id='{button_key}' readonly style='height:0;overflow:hidden;visibility:hidden;'>{st.session_state[state_key]}</textarea>
            <button onclick='copyToClipboard()' class='streamlit-button'>OneShot Copy to Clipboard</button>
            <script>
                function copyToClipboard() {{
                    navigator.clipboard.writeText(document.getElementById('{button_key}').value);
                }}
            </script>
            <style>
                .streamlit-button {{
                    background-color: rgb(42, 56, 152);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 0.5rem;
                    padding: .5rem;
                    font-size: 1rem;
                    cursor: pointer;
                }}
                .streamlit-button:hover {{
                    border-color: rgb(61, 73, 160);
                    color: rgb(61, 73, 160);

                }}
                .streamlit-button:active {{
                    border-color: rgb(61, 73, 160);
                    background-color: rgb(61, 73, 160);
                    color: white;
                }}
            </style>
            """,
            width=114,
            height=100,
        )


def create_text_area_and_clipboard(data_item, height=100):
    """
    Creates a text area and clipboard functionality based on data_item.
    """
    if data_item["name"] not in st.session_state:
        st.session_state[data_item["name"]] = ""

    st.session_state[data_item["name"]] = st.text_area(
        data_item["name"],
        label_visibility="collapsed",
        key=f"text_area_{data_item['name']}",
        value=st.session_state.get(data_item["name"], ""),
        height=height,
    )

    create_save_to_clipboard(f"copy_btn_{data_item['name']}", data_item["name"])


def handle_button_and_llm_run(data_item, position="left"):
    if position == "left":
        left_column, right_column = st.columns([5, 1])
        with left_column:
            st.write(data_item["button_label"])
        with right_column:
            if st.button(
                "Generate",
                key=f"btn_generate_{data_item['name']}",
                use_container_width=True,
            ):
                st.session_state[data_item["name"]] = llm_run(
                    model=data_item["model"],
                    temperature=data_item["temperature"],
                    template=data_item["prompt"],
                    **{
                        param.strip(): st.session_state.get(param.strip(), "")
                        for param in data_item["input_params"].split(",")
                    },
                )
    if position == "middle":
        left_column, middle_column, right_column = st.columns([1, 4, 1])
        with middle_column:
            if st.button(
                data_item["button_label"],
                key=f"btn_generate_{data_item['name']}",
                use_container_width=True,
            ):
                st.session_state[data_item["name"]] = llm_run(
                    model=data_item["model"],
                    temperature=data_item["temperature"],
                    template=data_item["prompt"],
                    **{
                        param.strip(): st.session_state.get(param.strip(), "")
                        for param in data_item["input_params"].split(",")
                    },
                )
    if position == "right":
        st.write(data_item["button_label"])
        left_column, right_column = st.columns([5, 1])
        with right_column:
            if st.button(
                "Generate",
                key=f"btn_generate_{data_item['name']}",
                use_container_width=True,
            ):
                st.session_state[data_item["name"]] = llm_run(
                    model=data_item["model"],
                    temperature=data_item["temperature"],
                    template=data_item["prompt"],
                    **{
                        param.strip(): st.session_state.get(param.strip(), "")
                        for param in data_item["input_params"].split(",")
                    },
                )


def main():
    apply_analytics()
    apply_custom_css()
    st.title("Grants OneShot")

    data = fetch_data()

    st.write(
        """Navigating the complexities of grant applications requires a robust and informed knowledge base about the company in question. This dedicated platform empowers consultants to craft a nuanced, detailed, and tailored profile of the company, laying the foundation for effectively answering every grant-related query. From understanding the company's core product or service to articulating its mission and vision, this tool harnesses advanced AI capabilities to streamline and enhance the content creation process.\n\nYour confidentiality is paramount. Please be assured that the integrity and privacy of your information are upheld to the highest standard. This session operates in a secure environment where no external entity, be it our team at GrowthGarner or the AI providers, has access to the data you input. However, do bear in mind that upon closing this session, unsaved data will be irretrievably lost. We urge you to diligently save and backup your progress.\n\nPlease Note: This session is private and secure. No third party, including our team at GrowthGarner and the AI providers, can access the information you input here.\n\nEnsure you save your progress regularly. Once this session is closed, any unsaved information will be lost permanently.\n\nEmbark on this collaborative journey between human expertise and AI efficiency to craft compelling narratives that resonate with grant evaluators."""
    )

    # Text Input Area
    st.session_state["input_string"] = st.text_area(
        "Initial Text or Notes",
        key="text_area_0",
        placeholder="Enter any available text about the company...",
    )

    # Iterate through each item in data, creating UI and functionality for each.
    for index, data_item in enumerate(data):
        # Use handle_right_button_and_llm_run for data items at index 4 and 5,
        # otherwise use handle_button_and_llm_run
        if index in [4, 5]:
            handle_button_and_llm_run(data_item, position="right")
        elif index == 2:
            handle_button_and_llm_run(data_item, position="middle")
        else:
            handle_button_and_llm_run(data_item, position="left")

        # Create a text area and 'Save to Clipboard' functionality
        if index == 5:
            create_text_area_and_clipboard(data_item, height=400)
        else:
            create_text_area_and_clipboard(data_item)


if __name__ == "__main__":
    st.set_page_config("Grants OneShot")
    with streamlit_analytics.track(
        unsafe_password=os.environ.get("ANALYTICS_PASSWORD")
    ):
        main()
