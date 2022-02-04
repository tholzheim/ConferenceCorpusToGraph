from os.path import expanduser

from corpus.datasources.download import Download


class RawDataSources:
    """
    Manages the download of raw datasources that are needed to init the ConferenceCorpus
    """

    @classmethod
    def downloadDblp(cls, onlySample:bool=True, forceUpdate:bool=False):
        """
        download the dblp xml dump
        Args:
             onlySample(bool): If False the complete xml dump is downloaded (~4GB). Otherwise only a sample is downloaded.
             forceUpdate(bool): If True the file will be downloaded even if already existent
        """
        sampleUrl = "https://github.com/WolfgangFahl/ConferenceCorpus/wiki/data/dblpsample.xml.gz"
        dumpUrl = "https://dblp.uni-trier.de/xml/dblp.xml.gz"
        if onlySample:
            url=sampleUrl
        else:
            url = dumpUrl
        home = expanduser("~")
        Download.downloadBackupFile(url=url,
                                    fileName="dblp.xml",
                                    targetDirectory=f"{home}/.dblp",
                                    force=forceUpdate,
                                    profile=True)

if __name__ == '__main__':
    RawDataSources.downloadDblp(onlySample=True, forceUpdate=False)