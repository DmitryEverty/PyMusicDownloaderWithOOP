import requests
import re
import bs4


class MusicSite:

    def __init__(self):  # Frk or EdmFull
        self.source = 'To Be Set'
        pass


class FrkMusic(MusicSite):

    # Attributes
    domen = 'https://www.frkmusic.cc/'
    query = 'genre/english/page/'
    pageUrl = ''
    trackLinks = []

    def __init__(self):
        self.source = 'Frk'

    def page(self, pageNumber):
        if isinstance(pageNumber, int):
            self.pageUrl = self.domen + self.query + str(pageNumber)
            return(self.pageUrl)
        else:
            raise TypeError('Only Numbers Are Allowed')
        return()

    def getLinks(self):
        # Extracting links for each post
        res = requests.get(self.page(1))
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        posts = soup.findAll('article')
        for postlink in posts:
            link = postlink.find('a').get('href')
            self.trackLinks.append(link)
        pass


class Track:

    # Attributes
    artists = ''
    trackName = ''
    link = ''
    pass
