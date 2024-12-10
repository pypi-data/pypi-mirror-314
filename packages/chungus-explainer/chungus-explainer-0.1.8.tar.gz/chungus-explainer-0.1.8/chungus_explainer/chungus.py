import numpy as np
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output
import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


def bins(feature_values, num_bins=15):
    """
    Create bins for the given feature values.
    
    Args:
    - feature_values: A pandas Series or numpy array of feature values.
    - num_bins: Number of bins to create (default is 15 for continuous features).
    
    Returns:
    - binned_values: An array of binned values.
    """
    if pd.api.types.is_numeric_dtype(feature_values):
        # Use specified number of bins for continuous values
        binned_values = pd.cut(feature_values, bins=num_bins, labels=False, duplicates="drop")
    else:
        # Use unique categories for discrete values
        binned_values = pd.factorize(feature_values)[0]
    return binned_values


def shap_json_classifier(feature_names, shap_values, feature_values, num_bins=15):
    """
    Generate JSON for classifiers using SHAP values and feature statistics, including ranked feature importance.

    Args:
    - feature_names: List of feature names.
    - shap_values: SHAP values (3D array for classifiers, with shape [n_samples, n_features, n_classes]).
    - feature_values: DataFrame or array of feature values.
    - num_bins: Number of bins for discretizing feature values.

    Returns:
    - shap_json_output: A JSON object containing ranked feature importance and binned SHAP statistics.
    """
    try:
        # Extract SHAP values if they are inside an Explanation object
        shap_values_array = shap_values.values if hasattr(shap_values, 'values') else shap_values

        # Check if SHAP values are for multi-class classification
        num_classes = shap_values_array.shape[2]

        # Compute feature importance (sum of absolute SHAP values for all classes)
        feature_importance = {
            feature_name: np.abs(shap_values_array[:, idx, :]).sum()
            for idx, feature_name in enumerate(feature_names)
        }

        # Rank feature importance in descending order
        ranked_feature_importance = dict(
            sorted(feature_importance.items(), key=lambda item: item[1], reverse=True)
        )

        shap_data = {"Feature Importance": ranked_feature_importance}

        for idx, feature_name in enumerate(feature_names):
            # Create bins for the feature
            binned_features = bins(feature_values.iloc[:, idx], num_bins=num_bins)

            # Collect SHAP data for each class and bin
            feature_shap_data = {}
            for class_idx in range(num_classes):  # Iterate through each class
                class_shap_data = {}
                for bin_idx in np.unique(binned_features):
                    bin_mask = binned_features == bin_idx

                    # Extract SHAP values for the current feature and class
                    bin_shap_values = shap_values_array[bin_mask, idx, class_idx]

                    # Add SHAP statistics to JSON if there are values in the bin
                    if bin_shap_values.size > 0:
                        class_shap_data[f"Bin {bin_idx}"] = {
                            "Median SHAP Value": np.median(bin_shap_values),
                            "Mean Feature Value": feature_values.loc[bin_mask, feature_values.columns[idx]].mean(),
                            "Mean Shap Value": bin_shap_values.mean(),
                            "Number of Samples in Bin": bin_shap_values.size
                        }

                # Add data for the class to the feature data
                feature_shap_data[f"Class {class_idx}"] = class_shap_data

            # Add feature-level statistics
            all_shap_values = shap_values_array[:, idx, :].ravel()
            shap_data[feature_name] = {
                "Feature Median SHAP Value": np.median(all_shap_values),
                "Feature SHAP High": all_shap_values.max(),
                "Feature SHAP Low": all_shap_values.min(),
                "Standard Deviation of SHAP Values": np.std(all_shap_values),
                "Classes": feature_shap_data
            }

        # Convert to JSON
        return json.dumps(shap_data, indent=4)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    
def shap_json_regressor(feature_names, shap_values, feature_values, num_bins=15):
    """
    Generate JSON for regressors using SHAP values and feature statistics, including ranked feature importance.

    Args:
    - feature_names: List of feature names.
    - shap_values: SHAP values (2D array for regressors).
    - feature_values: DataFrame or array of feature values.
    - num_bins: Number of bins for discretizing feature values.

    Returns:
    - shap_json_output: A JSON object containing ranked feature importance and binned SHAP statistics.
    """
    try:
        # Extract SHAP values if they are inside an Explanation object
        shap_values_array = shap_values.values if hasattr(shap_values, 'values') else shap_values

        # Compute feature importance (sum of absolute SHAP values)
        feature_importance = {
            feature_name: np.abs(shap_values_array[:, idx]).sum()
            for idx, feature_name in enumerate(feature_names)
        }

        # Rank feature importance in descending order
        ranked_feature_importance = dict(
            sorted(feature_importance.items(), key=lambda item: item[1], reverse=True)
        )

        shap_data = {"Feature Importance": ranked_feature_importance}

        for idx, feature_name in enumerate(feature_names):
            # Create bins for the feature
            binned_features = bins(feature_values.iloc[:, idx], num_bins=num_bins)

            # Collect SHAP data for each bin
            feature_shap_data = {}
            for bin_idx in np.unique(binned_features):
                bin_mask = binned_features == bin_idx

                # Extract SHAP values for the current bin
                bin_shap_values = shap_values_array[bin_mask, idx]

                # Add SHAP statistics to JSON if there are values in the bin
                if bin_shap_values.size > 0:
                    feature_shap_data[f"Bin {bin_idx}"] = {
                        "Median SHAP Value": np.median(bin_shap_values),
                        "Mean Shap Value": bin_shap_values.mean(),
                        "Mean Feature Value": feature_values.loc[bin_mask, feature_values.columns[idx]].mean(),
                        "Number of Samples in Bin": bin_shap_values.size
                    }

            # Add feature-level statistics
            all_shap_values = shap_values_array[:, idx]
            shap_data[feature_name] = {
                "Feature Median SHAP Value": np.median(all_shap_values),
                "Feature SHAP High": all_shap_values.max(),
                "Feature SHAP Low": all_shap_values.min(),
                "Standard Deviation of SHAP Values": np.std(all_shap_values),
                "Bins": feature_shap_data
            }

        # Convert to JSON
        return json.dumps(shap_data, indent=4)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
       
def chatgpt(shap_json_context, llm, data_dictionary=None):
    """
    Create an interactive chatbox to analyze SHAP values using ChatGPT, with dynamically generated suggested questions.

    Args:
    - shap_json_context: JSON string containing SHAP values and feature statistics.
    - llm: An instance of ChatOpenAI initialized with the desired model and API key.
    - data_dictionary: Optional. A string containing the data dictionary with feature descriptions.

    Returns:
    - None. Displays an interactive chatbox in the notebook.
    """
    import ipywidgets as widgets
    from IPython.display import display, clear_output

    # Initialize output box for chat responses
    output_box = widgets.Output(layout={"border": "1px solid black", "width": "100%"})
    
    # Input box for user questions
    user_input = widgets.Textarea(
        value="",
        placeholder="Type your question here...",
        description="Prompt:",
        layout=widgets.Layout(width="100%", height="100px"),
    )
    
    # Suggestions box
    suggestions_box = widgets.Output(layout={"border": "1px solid gray", "width": "100%", "margin": "10px 0"})
    
    # Submit button for input
    submit_button = widgets.Button(
        description="Send",
        button_style="primary",
        tooltip="Click to send your question to ChatGPT",
    )
    
    # Display user input, suggestions, and output box
    display(user_input, submit_button, suggestions_box, output_box)
    
    # Conversation history with optional data dictionary context
    conversation_history = [
        SystemMessage(
            content="""
            You are a Data Scientist proficient in analyzing SHAP values and numerical datasets. 
            The dataset contains features that influence model predictions, where:

            - **Positive SHAP values**: Indicate an increased likelihood of an outcome.
            - **Negative SHAP values**: Indicate a decreased likelihood of an outcome.

            **Key Metrics:**
            - **Feature Importance**: Ranks features globally based on their contribution to predictions (sum of absolute SHAP values). 
              Features with higher importance have greater influence.
            - **Feature-Level Metrics**: Median, high, and low SHAP values show central tendency and range of feature impact. 
              Standard deviation reflects variability across samples.
            - **Bin-Level Metrics**: Median and mean SHAP values show local contributions within bins. Mean feature value and sample count 
              provide context for bin representativeness.
            """
        ),
        SystemMessage(content=f"Here are the SHAP values and statistics: {shap_json_context}"),
    ]

    if data_dictionary:
        conversation_history.append(
            SystemMessage(
                content=f"The following is the data dictionary of the dataset:\n{data_dictionary}"
            )
        )

    # Function to generate dynamic suggestions
    def generate_dynamic_suggestions():
        # Query GPT to generate suggested questions based on the SHAP JSON and data dictionary
        prompt = """
        You are an assistant helping users analyze SHAP values and their dataset. Based on the SHAP JSON and data dictionary provided, 
        generate five suggested questions that a user might ask to understand the data better or gain insights into the model's predictions.
        """
        conversation = [
            SystemMessage(content=prompt),
            SystemMessage(content=f"SHAP JSON:\n{shap_json_context}"),
        ]
        if data_dictionary:
            conversation.append(SystemMessage(content=f"Data Dictionary:\n{data_dictionary}"))
        
        ai_response = llm.invoke(conversation)
        
        # Display the generated suggestions
        with suggestions_box:
            clear_output(wait=True)
            print("Suggested Questions:")
            print(ai_response.content)
    
    # Generate initial dynamic suggestions
    generate_dynamic_suggestions()

    def send_message_to_chatgpt(user_message):
        """
        Dynamically process the user's input and use GPT's NLP capabilities to determine response strategy.
        """
        # Append the user query to conversation history
        conversation_history.append(HumanMessage(content=user_message))

        # Add a system-level instruction for GPT to evaluate the query
        clarification_instruction = """
            You are a Data Scientist analyzing SHAP values and working with feature-level and bin-level metrics.
    
            Evaluate the user's query and determine:
            - If the question is broad or specific to a feature.
            - If the query lacks sufficient context or needs clarification.

            Respond appropriately:
            - For broad queries: Use global metrics like Feature Importance to provide an overview of the most impactful features.
            - For feature-specific queries: Provide bin-level insights and actionable recommendations, focusing on improving SHAP values. Compare bins and explain how to transition from a bin with a lower SHAP value to one with a higher SHAP value. Use SHAP metrics (e.g., median, mean, variability) to justify recommendations, emphasizing strategies to achieve positive SHAP values and better outcomes.
            - For ambiguous queries: Prioritize seeking clarification. Example: "Could you clarify if you're asking about a specific feature or a general analysis?"

            **Metrics Usage Guidance:**
            - Use **median SHAP value** as the primary metric to represent the central tendency of SHAP values across bins or features, especially when variability (e.g., standard deviation) is high. Median values minimize the influence of extreme SHAP values and provide a robust measure of the typical impact.
            - Use **mean SHAP value** as a supplementary metric to understand overall trends or deviations within a bin or feature, especially when additional context is needed or variability is low.
            - Always refer to the **standard deviation** of SHAP values to identify variability and guide whether to emphasize median or mean in the explanation.

            Leverage the SHAP JSON context and optional data dictionary to tailor your reasoning dynamically to the user's query and dataset.
        """

        # Add clarification instructions to the conversation history
        conversation_history.append(SystemMessage(content=clarification_instruction))

        # Get response from ChatGPT
        ai_response = llm.invoke(conversation_history)

        # Append AI response to conversation history
        conversation_history.append(ai_response)

        # Display user input and GPT's response
        with output_box:
            clear_output(wait=True)
            print(f"User: {user_message}\n")
            print(f"GPT: {ai_response.content}\n")

    def handle_submit(event):
        """
        Triggered when the user clicks the 'Send' button or presses Enter.
        """
        user_message = user_input.value.strip()
        if user_message:
            send_message_to_chatgpt(user_message)
            user_input.value = ""  # Clear the input box after sending
    
    # Bind the submit button click to send the message
    submit_button.on_click(handle_submit)

    
def data_dictionary():
    """
    Capture or upload a data dictionary.

    Returns:
    - data_dict: A string containing the data dictionary.
    """
    text_input = widgets.Textarea(
        value="",
        placeholder="Enter the data dictionary here or upload a text file.",
        description="Data Dictionary:",
        layout=widgets.Layout(width="100%", height="150px"),
    )
    
    file_upload = widgets.FileUpload(
        accept=".txt",  # Only accept text files
        multiple=False,
        description="Upload File"
    )
    
    data_output = widgets.Output()

    def handle_upload(change):
        uploaded_file = list(file_upload.value.values())[0]
        content = uploaded_file['content'].decode("utf-8")
        text_input.value = content
        with data_output:
            clear_output()
            print("Data dictionary loaded from uploaded file.")

    file_upload.observe(handle_upload, names="value")

    display(text_input, file_upload, data_output)

    return text_input
