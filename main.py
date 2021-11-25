#!/usr/bin/env python3

# Copyleft (C) Alexandria Pettit 2021, GNU GPLv3

# TODO: replace f-string formatting with logging-based so that string ops don't execute when logs aren't being produced
# TODO: add click-powered console UI? Need to dust off my old skills with that library.

# TODO: add actual downloading functionality (With progress bar!?)

# TODO: add ability to generate curseforge-formatted manifest.json modpack file
# TODO: See: https://github.com/PistolRcks/curseforge-mass-downloader/wiki/Structuring-manifest.json
# TODO: add thing to make sure we're getting 'text only version' to prevent parsing errors
# TODO: detect consistent Google 404 page (e.g., broken link)
# TODO: detect when Google tries to fake us out with a fake 404 page (wait a bit, then reload)
# TODO: abstract out ADT for 'parser that reads project ID number', implement in dedicated class

import logging

import get_dl_urls
import get_ids
from lib import SimpleLogger


class Main:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def main(self):
        """ Runs through full sequence, first pulling IDs from website & local db,
        then getting using those to extract download URLs from third-party API """
        print('Starting full sequence...')
        get_ids.main.main()
        # Rather than have it load from the ID file at next stage,
        # we can instead transfer list directly
        get_dl_urls.main.ids = get_ids.main.ids
        get_dl_urls.main.main()
        print('Sequence complete.')


main = Main()

if __name__ == '__main__':
    main.main()
