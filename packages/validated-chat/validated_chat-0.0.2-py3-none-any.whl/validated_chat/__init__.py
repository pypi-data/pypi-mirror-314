from typing import List, Type, Optional
from pydantic import BaseModel, ValidationError
from ollama import chat


def get_validated_response(
        messages: List[dict],
        model: str,
        response_model: Type[BaseModel],
        max_attempts: int = 3,
        verbose: bool = False,
        options: Optional[dict] = None
) -> Optional[BaseModel]:
    """
    Attempts to generate and validate a response from the chat model.

    Args:
        messages (List[dict]): The list of message dictionaries to send to the chat model.
        model (str): The name of the chat model to use.
        response_model (Type[BaseModel]): The Pydantic BaseModel class to validate the response.
        max_attempts (int): Maximum number of attempts to get a valid response.
        verbose (bool): If True, prints detailed logs.
        options (Optional[dict]): Optional dictionary of options to pass to the chat
    Returns:
        Optional[BaseModel]: An instance of the response_model if validation is successful, else None.
    """
    for attempt in range(1, max_attempts + 1):
        if verbose:
            print(f"Attempt {attempt} of {max_attempts}...")

        try:
            response = chat(
                messages=messages,
                model=model,
                format=response_model.model_json_schema(),
                options=options
            )

            if verbose:
                print("Received response:", response.message.content)

            validated_response = response_model.model_validate_json(response.message.content)

            if verbose:
                print("Validation successful.")

            return validated_response

        except ValidationError as ve:
            if verbose:
                print(f"Validation failed on attempt {attempt}: {ve}")
        except Exception as e:
            if verbose:
                print(f"An error occurred on attempt {attempt}: {e}")

    if verbose:
        print("All attempts failed to generate a valid response.")

    return None
