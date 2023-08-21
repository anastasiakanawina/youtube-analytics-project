from src.channel import Channel
import isodate
import datetime


class PlayList(Channel):
    """Класс для плейлистов"""

    def __init__(self, playlist_id) -> None:
        """Экземпляр инициализируется по id плейлиста. """
        self.playlist_id = playlist_id
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id
        self.title = f'{self.get_playlist_stats()[1]}'

    def get_playlist_stats(self):
        """ Здесь происходит получение статистики плейлиста
        """
        youtube = self.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()

        playlists = youtube.playlists().list(id=self.playlist_id,
                                             part='contentDetails,snippet',
                                             ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        playlist_title = playlists['items'][0]['snippet']['title']
        return video_ids, playlist_title

    @property
    def total_duration(self):
        """ Возвращает общую длительность плейлиста в формате datetime.timedelta """
        youtube = self.get_service()
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.get_playlist_stats()[0])
                                               ).execute()
        total_seconds = 0
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration_video = isodate.parse_duration(iso_8601_duration)
            total_seconds += duration_video.total_seconds()

        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        """ Возвращает смое популярное виидео """
        youtube = self.get_service()
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.get_playlist_stats()[0])
                                               ).execute()
        dict_videos = {}
        for video in video_response['items']:
            cnt_likes = video['statistics']['likeCount']
            video_url = 'https://youtu.be/' + video['id']
            dict_videos[video_url] = int(cnt_likes)

        list_dict = list(dict_videos.items())
        list_dict.sort(key=lambda i: i[1])
        list_dict.reverse()

        return list_dict[0][0]

