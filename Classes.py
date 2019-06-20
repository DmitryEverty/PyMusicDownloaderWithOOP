import requests
import re
import bs4
import tkinter as tk
from tkinter import filedialog


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
    lastTrack = ''

    def __init__(self, lastTrack):
        self.source = 'Frk'
        self.lastTrack = lastTrack

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
            classTags = postlink.attrs['class']
            if 'tag-upcoming' in classTags:
                break
            link = postlink.find('a').get('href')
            if link == self.lastTrack:
                self.isRelevant = False
                break
            else:
                self.postLinks.append(link)
        if self.isRelevant:
            self.nextPage()

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
            print(artists + ' - ' + trackName)

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
        print('Reached the last track ' +
              'At a Page Number ' + str(self.pageNumber))
        # return(self.postLinks)

    def exportDownloadLinks(self,):
        self.gatherPostLinks()
        print('\n' + 'Collecting Tracks...')
        self.getNewReleases()
        print('\n' + 'Mr Propper at Work...')
        self.mrPropper()
        print('\n' + 'Wait a bit more...')
        mp3files = self.linkConverter()
        self.saveFile(mp3files)

    def linkConverter(self,):
        extracted = []
        n = 1
        for trackLibraryItem in self.trackLibrary:
            print('Element ' + str(n), end='\r')
            s = requests.session()
            s.headers.update(
                {'referer': self.trackLibrary[trackLibraryItem]['parrentLink']})
            r = s.get(self.trackLibrary[trackLibraryItem]
                      ['actualLink'], stream=True)
            extracted.append(r.url)
            n += 1
        return(extracted)

    def saveFile(self, mp3s):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askdirectory()
        with open(file_path + '/Links.txt', 'w') as file:
            for mp3 in mp3s:
                file.write(mp3 + '\n')
        pass

    def nextPage(self,):
        self.pageNumber += 1
        pass

    def mrPropper(self,):
        badLabels = ['MMXVAC',
                     'NCS',
                     'Global Records',
                     'Circus Records',
                     'Future Bass Records',
                     'Thrive Music',
                     'Enhanced Music',
                     'Break It Down',
                     'Magic Records'
                     'Sirup Music',
                     'Clout.NU',
                     'Elysian Records',
                     'Vibes Records',
                     'BrednButter',
                     'UXN Recording',
                     ]
        # badGenres = []
        kicked = []
        for badLabel in badLabels:
            for trackId in self.trackLibrary:
                if badLabel in self.trackLibrary[trackId]['label']:
                    kicked.append(trackId)
                    print('Someone was kicked...')
        for victim in kicked:
            self.trackLibrary.pop(victim)
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
