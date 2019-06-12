import Classes

musicSource = Classes.FrkMusic()

# links = musicSource.gatherPostLinks()
musicSource.exportDownloadLinks()
musicSource.getNewReleases()  # It should return the all new tracks
print('word')
