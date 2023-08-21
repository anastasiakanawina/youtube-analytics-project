from src.channel import Channel


class Video(Channel):
    """Класс для видео"""

    def __init__(self, video_id) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id
        try:
            self.video_url, self.title, self.view_count, self.like_count = self.get_video_stats()
        except IndexError:
            print('Видео с данным ID не существует')
            self.video_url = None
            self.title = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        """ Метод возвращающий название видео """
        return f'{self.title}'

    def get_video_stats(self):
        """ Здесь происходит получение статистики видео
        """
        youtube = self.get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.__video_id
                                               ).execute()

        video_url = 'https://www.youtube.com/watch?v=' + self.__video_id
        title: str = video_response['items'][0]['snippet']['title']
        view_count: int = video_response['items'][0]['statistics']['viewCount']
        like_count: int = video_response['items'][0]['statistics']['likeCount']

        return video_url, title, view_count, like_count


class PLVideo(Video):
    """Класс для видео из плейлистов"""

    def __init__(self, video_id, playlist_id) -> None:
        """Экземпляр инициализируется по id видео и id плейлиста. """
        super().__init__(video_id)
        self.playlist_id = playlist_id


