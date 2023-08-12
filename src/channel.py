import os
from googleapiclient.discovery import build
from pprint import pprint
import json


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title, self.description, self.url, self.subscribers, self.video_count, self.views = self.get_channel_stats()


    @classmethod
    def get_service(cls):
        """ Класс-метод, возвращающий объект для работы с YouTube API
        """
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


    def get_channel_stats(self):
        """ Здесь происходит получение статистики канала
        """
        youtube = self.get_service()
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        title = channel['items'][0]['snippet']['title']
        description = channel['items'][0]['snippet']['description']
        url = 'https://www.youtube.com/channel/' + self.__channel_id
        subscribers = channel['items'][0]['statistics']['subscriberCount']
        video_count = channel['items'][0]['statistics']['videoCount']
        views = channel['items'][0]['statistics']['viewCount']
        return title, description, url, subscribers, video_count, views

    @property
    def channel_id(self):
        """Возвращает полное имя сотрудника. К атрибуту можно обращаться без ().
        """
        return self.__channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале.
        """
        youtube = self.get_service()
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        pprint(channel)


    def to_json(self, filename):
        """ Метод, сохраняющий в файл значения атрибутов экземпляра Channel
        """
        data = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscribers': self.subscribers,
            'video_count': self.video_count,
            'views': self.views
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
