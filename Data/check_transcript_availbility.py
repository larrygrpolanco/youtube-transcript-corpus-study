import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

# Function to check transcript availability
def check_transcript_availability(video_id):
    try:
        # Attempt to fetch the transcript to check availability
        YouTubeTranscriptApi.get_transcript(video_id)
        return True
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return False

# Main script
def main():
    # Read the CSV file
    df = pd.read_csv('OCW/Transcript Transfer.csv')

    # Prepare a list to store report data
    report_data = []

    # Process each row in the DataFrame
    for _, row in df.iterrows():
        video_id = row['Video ID']
        playlist_id = row['Playlist ID']

        # Check transcript availability
        transcript_available = check_transcript_availability(video_id)
        report_data.append({
            'Video ID': video_id,
            'Playlist ID': playlist_id,
            'Transcript Available': 'Yes' if transcript_available else 'No'
        })

    # Create a DataFrame for the report and save it to a CSV file
    report_df = pd.DataFrame(report_data)
    report_df.to_csv('transcripts_availability_report.csv', index=False)

if __name__ == "__main__":
    main()
