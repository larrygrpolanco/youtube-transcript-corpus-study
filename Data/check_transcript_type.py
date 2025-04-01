import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

# Function to check transcript availability and type
def check_transcript_details(video_id):
    try:
        # Fetch all available transcripts for the video
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        for transcript in transcript_list:
            if transcript.is_generated:
                return 'Auto-generated'
            else:
                return 'Manually created'
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return 'Not available'

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

        # Check transcript details
        transcript_type = check_transcript_details(video_id)
        report_data.append({
            'Video ID': video_id,
            'Playlist ID': playlist_id,
            'Transcript Type': transcript_type
        })

    # Create a DataFrame for the report and save it to a CSV file
    report_df = pd.DataFrame(report_data)
    report_df.to_csv('transcripts_type_report.csv', index=False)

if __name__ == "__main__":
    main()
