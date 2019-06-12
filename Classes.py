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
    pageNumber = 1  # Will be changing dynamicaly
    postLinks = []  # Links for every post
    trackLibrary = {}
    isRelevant = True  # Will be used for While loop
    lastTrack = 'https://www.frkmusic.cc/breathe-nytrix-awakend-mp3-320kbps-download-free/'

    def __init__(self):
        self.source = 'Frk'

    def makePageUrl(self,):
        if isinstance(self.pageNumber, int):
            self.pageUrl = self.domen + self.query + str(self.pageNumber)
            return(self.pageUrl)
        else:
            raise TypeError('Only Numbers Are Allowed')
        return()

    def getLinks(self):
        # Extracting links for each post
        res = requests.get(self.makePageUrl())
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        posts = soup.findAll('article')
        for postlink in posts:
            link = postlink.find('a').get('href')
            if link == self.lastTrack:
                self.isRelevant = False
                break
            else:
                self.postLinks.append(link)
        if self.isRelevant:
            self.pageNumber += 1

        pass

    def getNewReleases(self,):

        for post in self.postLinks:
            parrentLink = post
            res = requests.get(post)
            soup = bs4.BeautifulSoup(res.text, 'lxml')

        # Getting Track info
            label = soup.find_all('h2')[3].findAll(
                'span')[1].findAll('span')[1].text
            genre = soup.find_all('h2')[2].findAll(
                'span')[1].findAll('span')[1].text

            listGroup = soup.findAll('div', {'class': 'list-group'})
            try:
                listGroupParagraph = listGroup[1].findAll('p')
            except:
                listGroupParagraph = listGroup[0].findAll('p')
            trackContainer = listGroupParagraph[0].findAll(
                'a', {'class': 'list-group-item'})

            for trackInfo in trackContainer:
                # Getting a Single Track's Parrent Link
                actualLink = trackInfo.get('href')  # Actual link
                trackId = actualLink.split('/', 3)[-1].replace('/', '-')  # Id
                info = trackInfo.text.split('\n')[0].split(' – ')
                if len(info) == 3:
                    artists = info[2]
                    trackName = info[1]
                else:
                    artists = info[1]
                    trackName = info[0]
                self.createTrack(trackId, artists, trackName,
                                 parrentLink, actualLink, label, genre)

    def createTrack(self, trackId, artists, trackName, parrentLink, actualLink, label, genre):
        self.trackLibrary[trackId] = {
            'artists': artists,
            'trackName': trackName,
            'parrentLink': parrentLink,
            'actualLink': actualLink,
            'label': label,
            'genre': genre}

        return()

    def gatherPostLinks(self,):
        while self.isRelevant:
            print('Working On a Page Number ' + str(self.pageNumber), end='\r')
            self.getLinks()
        print('Reached the last track' + (' ' * 8))
        return(self.postLinks)

    def nextPage(self,):
        self.pageNumber += 1
        pass

    def trackInfoCheck(self, property):
        properties = ['trackId', 'artists', 'trackName',
                      'parrentLink', 'actualLink', 'label', 'genre']
        extractedData = []
        if property in properties:
            for entry in self.trackLibrary:
                data = self.trackLibrary[entry][property]
                extractedData.append(data)
            return(extractedData)
        else:
            pass
