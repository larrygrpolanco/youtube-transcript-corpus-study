
import csv
import os
from youtube_transcript_api import YouTubeTranscriptApi

# Directory where transcripts will be saved
transcript_dir = 'transcripts'

# Create the directory if it doesn't exist
if not os.path.exists(transcript_dir):
    os.makedirs(transcript_dir)

# Create a list to store the video IDs from the CSV file
video_ids = []

# Replace with the actual CSV file containing video IDs
csv_file = 'vlog_rating_videos.csv'

# Open the CSV file and read the video IDs into the list
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        video_id = row['Video ID']
        video_ids.append(video_id)

# Loop through the video IDs and extract transcripts
for video_id in video_ids:
    print(f'Video ID: {video_id}')
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Create a text file for each transcript within the directory with the Video ID as the filename
        transcript_path = os.path.join(transcript_dir, f'{video_id}.txt')
        with open(transcript_path, 'w') as txt_file:
            for x in transcript:
                sentence = x['text']
                txt_file.write(f'{sentence}\n')
        
        print(f'Transcript saved as {transcript_path}')
    except Exception as e:
        print(f'Error: {str(e)}')
