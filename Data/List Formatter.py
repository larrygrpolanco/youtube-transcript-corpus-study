def convert_to_python_list(input_text):
    # Splitting the input text into lines
    lines = input_text.strip().split('\n')

    # Stripping extra whitespace and adding quotes
    python_list = [f'{line.strip()}' for line in lines]

    return python_list

# Example usage
input_text = """

"""

result = convert_to_python_list(input_text)
print(result)