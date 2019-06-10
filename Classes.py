class MusicSite:

    def __init__(self):  # Frk or EdmFull
        self.source = 'To Be Set'
        pass


class FrkMusic(MusicSite):

    # Attributes
    domen = 'https://www.frkmusic.cc/'
    query = 'genre/english/page/'
    firstPage = 1
    pageUrl = ''

    def __init__(self):
        self.source = 'Frk'

    def page(self, pageNumber):
        if isinstance(pageNumber, int):
            self.pageUrl = self.domen + self.query + str(pageNumber)
        else:
            raise TypeError('Only Numbers Are Allowed')

    def pageCounter(self,):
        i = 1
        while i <= 6:
            self.page(i)
            print(self.pageUrl)
            i += 1


class Track:

    # Attributes
    artists = ''
    trackName = ''
    pass
