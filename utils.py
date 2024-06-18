import re

def get_prompts_gemini(file_path):
    # Define the separator pattern
    # separator_pattern = r'(\r?\n)+[\r\n\s]*'
    separator_pattern = r'(\r?\n){2}[\s]*'

    # Open the file and read its contents
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read()

    # Split the content based on the specified separator pattern
    sections = re.split(separator_pattern, contents.strip())

    # loop through the sections and print them all for debugging
    # for section in sections:
    #     print(sections.index(section), section)

    # Initialize the list with the first section, correctly identifying it as instructions for the oracle
    prompt_parts = [sections[2].strip()]  # Assuming sections[2] contains the instruction.

    # remove the first three secions from sections
    sections = sections[3:]

    # Remove all sections with empty spaces or those with content "Example: "
    sections = [section for section in sections if section.strip() and not section.lower().startswith("examples:")]

    for i, section in enumerate(sections):
        parts = section.split('\n', 1)  # Split the section into two parts by the first newline
        if len(parts) == 2:  # If there are two parts
            prompt_parts.append(f"user: {parts[0].strip()}")  # Prefix the first part with "user: "
            prompt_parts.append(f"oracle: {parts[1].strip()}")  # Prefix the second part with "oracle: "
        else:  # If there's only one part
            prefix = "user: " if i % 2 == 0 else "oracle: "
            prompt_parts.append(f"{prefix}{parts[0].strip()}")

    # Return the prompt_parts list
    return prompt_parts

def get_prompts_openai(file_path):
    # Define the separator pattern
    separator_pattern = r'(\r?\n)+[\r\n\s]*'

    # Open the file and read its contents
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read()

    # Split the content based on the specified separator pattern
    sections = re.split(separator_pattern, contents.strip())

    # Remove all sections with empty spaces
    sections = [section for section in sections if section.strip()]

    # paragraph = "hi."

    # concatenate all the sections back to a long string and appent it to paragraph
    paragraph = "\n".join(sections)

    # for section in sections:
    #     paragraph += "\n" + section

    # Return the prompt_parts list
    return paragraph