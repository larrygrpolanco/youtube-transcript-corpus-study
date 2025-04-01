import pandas as pd
import requests
import time

# Read the CSV file
df = pd.read_csv('input.csv')

# Function to check if the video is a YouTube short
def is_short(video_id):
    try:
        # Constructing the URL for the YouTube short
        url = f"https://www.youtube.com/shorts/{video_id}"

        # Sending a HEAD request to the URL
        response = requests.head(url, allow_redirects=False)

        # Returning 'Yes' if status code is 200, otherwise 'No'
        return 'Yes' if response.status_code == 200 else 'No'
    except requests.RequestException as e:
        # Handling any request errors (network issues, etc.)
        print(f"An error occurred: {e}")
        return 'Error'

# Apply the function to each row in the DataFrame
for index, row in df.iterrows():
    df.at[index, 'Short'] = is_short(row['Video ID'])
    
    # Optional: Add a delay between requests to avoid rate limiting
    # time.sleep(1)

# Save the updated DataFrame to a new CSV file
df.to_csv('output.csv', index=False)

# Print completion message
print("The script has finished executing and the output has been saved to 'output.csv'.")
