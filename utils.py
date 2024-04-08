import re

def get_prompts_gemini(file_path):
    # Define the separator pattern
    separator_pattern = r'(\r?\n)+[\r\n\s]*'

    # Open the file and read its contents
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read()

    # Split the content based on the specified separator pattern
    sections = re.split(separator_pattern, contents.strip())

    # Initialize the list with the first section, correctly identifying it as instructions for the oracle
    prompt_parts = [sections[2].strip()]  # Assuming the first section after split contains the instruction.

    # Remove all sections with empty spaces or those with content "Example: "
    sections = [section for section in sections if section.strip() and not section.lower().startswith("examples:")]

    # Iterate over the remaining sections, adding "user: " before the odd-indexed ones and "oracle: " before the even-indexed ones
    for i, section in enumerate(sections):
        prefix = "user: " if i % 2 == 0 else "oracle: "
        prompt_parts.append(f"{prefix}{section.strip()}")

    # Return the prompt_parts list
    return prompt_parts