#!/usr/bin/env python3
import logging

import get_dl_urls
import get_ids


class Main:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def main(self):
        self.logger.info('Starting full sequence')
        get_ids.main.main()
        get_dl_urls.main.id2namedb = get_ids.main.db
        get_dl_urls.main.main()


main = Main()

if __name__ == '__main__':
    main.main()
