from langchain.schema import HumanMessage, SystemMessage
import ipywidgets as widgets
from IPython.display import display, clear_output
import json
import shap
import pandas as pd

def generate_prompt(shap_json_context, intent, feature_of_interest=None, custom_prompt=None, enable_engineering=True, llm=None):
    """
    Generate or enhance a prompt for interacting with SHAP JSON data based on user input and intent.

    Args:
    - shap_json_context: JSON string containing SHAP values and feature statistics.
    - intent: Selected intent for the prompt (e.g., "general_insights", "business_insights").
    - feature_of_interest: (Optional) Specific feature to focus on in the analysis.
    - custom_prompt: (Optional) A user-provided custom prompt to be enhanced.
    - enable_engineering: (bool) If False, returns the custom prompt without modification.
    - llm: (Optional) Instance of the GPT model to refine the custom prompt.

    Returns:
    - prompt: A dynamically generated or enhanced prompt string.
    """
    if not enable_engineering:
        # Return the user's custom prompt as is if engineering is disabled
        return custom_prompt or "Please provide a custom prompt."

    # Add intent-specific descriptions
    intent_descriptions = {
        "general_insights": (
            "Analyze the SHAP values to summarize key insights. "
            "Highlight the most influential features and explain their impact on model predictions. "
            "Ensure the explanation is clear for a non-technical audience."
        ),
        "business_insights": (
            "Provide actionable business insights based on the SHAP values. "
            "Explain how features contribute to outcomes and recommend strategies or actions that can be derived from the data."
        ),
        "focus_on_feature": (
            f"Focus your analysis on the feature '{feature_of_interest}'. "
            "Explain its role in influencing predictions, describe trends across bins, and highlight its SHAP value ranges (25th to 75th percentiles)."
        ),
        "compare_features": (
            "Compare the contributions of different features and identify the most impactful ones. "
            "Provide a clear ranking of feature importance and justify the rankings using SHAP statistics."
        ),
    }

    # Get the task description based on the intent
    task_description = intent_descriptions.get(intent, "Provide detailed insights based on the SHAP values for the dataset.")

    # If a custom prompt is provided, refine it using GPT
    if custom_prompt and llm:
        # Create a GPT-friendly prompt for refinement
        refinement_context = (
            f"Task: {task_description}\n\n"
            f"User's Custom Prompt:\n{custom_prompt}\n\n"
            "Refine the user's custom prompt to better align with this task and intent."
        )
        # Use GPT to refine the prompt
        response = llm.invoke([HumanMessage(content=refinement_context)])
        refined_prompt = response.content.strip()
    else:
        # Combine task description with SHAP definitions if no custom prompt is provided
        refined_prompt = task_description

    # Return the refined prompt without the context
    return refined_prompt


def prompt_generator(shap_json_context, llm):
    """
    Interactive tool for generating or enhancing prompts based on user-selected intent and custom input.

    Args:
    - shap_json_context: JSON string containing SHAP values and feature statistics.
    - llm: An instance of the GPT model for prompt refinement.

    Returns:
    - None. Displays an interactive widget in the notebook.
    """
    # Dropdown for intent selection
    intent_dropdown = widgets.Dropdown(
        options=["general_insights", "business_insights", "focus_on_feature", "compare_features"],
        value="general_insights",
        description="Intent:"
    )

    # Text input for custom prompt
    custom_prompt_box = widgets.Textarea(
        value="",
        placeholder="Type your custom prompt here...",
        description="Prompt:",
        layout=widgets.Layout(width="100%", height="100px")
    )

    # Toggle for enabling or disabling prompt engineering
    engineering_toggle = widgets.Checkbox(
        value=True,
        description="Enable Prompt Engineering"
    )

    # Text input for specific feature (optional)
    feature_input = widgets.Text(
        value="",
        placeholder="Enter a feature name (optional)...",
        description="Feature:"
    )

    # Output box for displaying the generated prompt
    output_box = widgets.Output(layout={"border": "1px solid black", "width": "100%"})

    # Button to generate the prompt
    generate_button = widgets.Button(description="Generate Prompt")

    # Function to generate and display the prompt
    def generate_prompt_action(_):
        intent = intent_dropdown.value
        custom_prompt = custom_prompt_box.value.strip()
        feature_of_interest = feature_input.value.strip() or None
        enable_engineering = engineering_toggle.value

        # Generate the prompt using the updated function
        prompt = generate_prompt(
            shap_json_context=shap_json_context,
            intent=intent,
            feature_of_interest=feature_of_interest,
            custom_prompt=custom_prompt,
            enable_engineering=enable_engineering,
            llm=llm
        )

        # Display the generated prompt
        with output_box:
            clear_output(wait=True)
            print(prompt)

    # Bind the button click to the action
    generate_button.on_click(generate_prompt_action)

    # Display all widgets
    display(intent_dropdown, custom_prompt_box, feature_input, engineering_toggle, generate_button, output_box)