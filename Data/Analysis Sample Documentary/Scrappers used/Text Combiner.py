import os

# Function to combine all txt files in a specified directory
def combine_txt_files(folder_path, output_file_name):
    """
    Combines all .txt files in the given folder into a single file.
    
    Parameters:
    folder_path (str): The path to the folder containing .txt files.
    output_file_name (str): The name of the output file.
    """
    # Initialize an empty string to store the combined content
    combined_content = ""

    # Loop through each file in the directory
    for filename in os.listdir(folder_path):
        # Check if the file is a .txt file
        if filename.endswith('.txt'):
            # Open the file and read its contents
            with open(os.path.join(folder_path, filename), 'r') as file:
                content = file.read()
                combined_content += content + "\n" # Add content to combined_content

    # Write the combined content to the output file
    with open(output_file_name, 'w') as output_file:
        output_file.write(combined_content)

# Editable section for the user to specify the folder path and output file name
folder_path = 'Transcripts' # Replace with your folder path
output_file_name = 'combined_output.txt' # Replace with your desired output file name

# Call the function to combine files
combine_txt_files(folder_path, output_file_name)