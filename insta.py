import os
import time
import requests

# Instagram API details
ACCESS_TOKEN = 'access token here'
USER_ID = '17841464589615650'  # Replace with your Instagram user ID
GRAPH_API_URL = 'https://graph.facebook.com/v15.0'

# Folder containing reels
REELS_FOLDER = 'C:\\Users\\hp\\Desktop\\accec\\vid'

def get_reels_from_folder(folder_path):
    """
    Get the list of video files in the specified folder.
    """
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.mp4', '.mov'))]

def upload_reel(video_path):
    """
    Uploads a reel to Instagram using the Graph API.
    """
    try:
        # Step 1: Upload video to Instagram (requires a video container ID)
        with open(video_path, 'rb') as video_file:
            print(f"Uploading video: {video_path}")
            files = {
                'file': video_file
            }
            params = {
                'access_token': ACCESS_TOKEN,
            }
            response = requests.post(f'{GRAPH_API_URL}/{USER_ID}/media', params=params, files=files)
            response_data = response.json()

            if 'id' not in response_data:
                print(f"Error during upload: {response_data}")
                return None
            
            media_id = response_data['id']
            print(f"Media ID: {media_id}")

        # Step 2: Publish the uploaded video as a reel
        publish_response = requests.post(
            f'{GRAPH_API_URL}/{USER_ID}/media_publish',
            params={
                'creation_id': media_id,
                'access_token': ACCESS_TOKEN,
            }
        )
        publish_data = publish_response.json()

        if 'id' in publish_data:
            print(f"Reel published successfully: {publish_data['id']}")
        else:
            print(f"Error publishing reel: {publish_data}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    Main function to post reels every 46 minutes.
    """
    videos = get_reels_from_folder(REELS_FOLDER)
    if not videos:
        print("No reels found in the folder.")
        return

    while videos:
        video = videos.pop(0)  # Get the first video in the list
        upload_reel(video)
        print("Waiting for 46 minutes before posting the next reel...")
        time.sleep(46 * 60)  # Wait for 46 minutes (2760 seconds)

if __name__ == '__main__':
    main()
