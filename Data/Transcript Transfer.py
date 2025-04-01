import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import os

# Function to create transcript
def create_transcript(video_id, playlist_id):
    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Create the filename
        filename = f"transcripts/{playlist_id}_{video_id}.txt"

        # Write the transcript to a file
        with open(filename, 'w') as file:
            for line in transcript:
                file.write(f"{line['text']}\n")

        return True
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        print(f"Error for Video ID {video_id}: {e}")
        return False

# Main script
def main():
    # Read the CSV file
    df = pd.read_csv('OCW/Transcript Transfer.csv')

    # Ensure the transcripts directory exists
    if not os.path.exists('transcripts'):
        os.makedirs('transcripts')

    # Prepare a list to store report data
    report_data = []

    # Process each row in the DataFrame
    for _, row in df.iterrows():
        video_id = row['Video ID']
        playlist_id = row['Playlist ID']

        # Create transcript and record its success
        transcript_found = create_transcript(video_id, playlist_id)
        report_data.append({
            'Video ID': video_id,
            'Playlist ID': playlist_id,
            'Transcript Found': 'Yes' if transcript_found else 'No'
        })

    # Create a DataFrame for the report and save it to a CSV file
    report_df = pd.DataFrame(report_data)
    report_df.to_csv('transcripts_report.csv', index=False)

if __name__ == "__main__":
    main()
