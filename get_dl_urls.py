# /usr/bin/env python3
import logging
from typing import Optional, List

from lib import SimpleLogger
from lib.Id2NameDB_CSV import ID2NameDB
from lib.ThirdPartyCurseForgeAPI import ThirdPartyCurseForgeAPI


class MainGetDlURLs:
    ids: List[str] = []

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def main(self):
        print('Getting download URLs...')
        if self.ids is []:
            # will automatically load from file
            for line in open('results-ids.txt').readlines():
                _id = line.strip()
                self.ids.append(_id)

        cf = ThirdPartyCurseForgeAPI()
        self.logger.info('Getting DL links from IDs...')
        results = open('results-urls.txt', 'w')
        for _id in self.ids:
            _id = _id.strip()
            self.logger.info(f'Processing ID: {_id}')
            url = cf.get_dl_link(_id)
            if url:
                results.write(url + '\n')
        print('Done.')


main = MainGetDlURLs()
if __name__ == '__main__':
    main.main()
