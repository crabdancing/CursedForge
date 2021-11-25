# /usr/bin/env python3
from typing import Optional

from lib.Id2NameDB_CSV import ID2NameDB
from lib.ThirdPartyCurseForgeAPI import ThirdPartyCurseForgeAPI


class Main:
    id2namedb: Optional[ID2NameDB] = None

    def main(self):
        if self.id2namedb is None:
            self.id2namedb = ID2NameDB()

        cf = ThirdPartyCurseForgeAPI()
        print('Getting DL links from IDs...')
        results = open('results-urls.txt', 'w')
        for _id in self.id2namedb.id_iter():
            print(f'Processing ID: {_id}')
            url = cf.get_dl_link(_id)
            if url:
                results.write(url + '\n')


main = Main()
if __name__ == '__main__':
    main.main()
