import csv
from youtube_transcript_api import YouTubeTranscriptApi

# It seems that "rating" produces the least amount of errors

csv_file = 'vlog_viewCount_videos.csv'
output_file = 'check_transcripts.csv'

with open(csv_file, 'r') as file, open(output_file, 'w', newline='') as csvfile:
    reader = csv.DictReader(file)
    writer = csv.writer(csvfile)
    writer.writerow(['Video Title', 'Video ID', 'Transcript Found'])

    for row in reader:
        video_title = row['Video Title']
        video_id = row['Video ID']

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            writer.writerow([video_title, video_id, 'Yes'])
        except Exception as e:
            print(f"Error for video {video_id}: {type(e).__name__}")
            writer.writerow([video_title, video_id, 'No'])

print(f'Transcript check results saved in {output_file}')
