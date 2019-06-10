class MusicSite:

    def __init__(self):  # Frk or EdmFull
        self.source = 'To Be Set'
        pass


class FrkMusic(MusicSite):

    # Attributes
    domen = 'https://www.frkmusic.cc/'
    query = 'genre/english/page/'
    pageUrl = ''

    def __init__(self):
        self.source = 'Frk'

    def page(self, pageNumber):
        if isinstance(pageNumber, int):
            self.pageUrl = self.domen + self.query + str(pageNumber)
            return(self.pageUrl)
        else:
            raise TypeError('Only Numbers Are Allowed')


class Track:

    # Attributes
    artists = ''
    trackName = ''
    link = ''
    pass
