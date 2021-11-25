import sys
from pathlib import Path
from urllib import request


class GrabThing:
    dl_url: str
    dl_path: Path

    @staticmethod
    def _report_hook(blocks_so_far, block_size, total_size):
        if blocks_so_far % 5 != 0:
            # if we're not on a 5th block
            return
        sys.stdout.write('\r')
        sys.stdout.flush()
        if total_size == -1:
            sys.stdout.write('Downloading (size not specified by server)...')
            return

        total_size_so_far = blocks_so_far * block_size
        total_kb = total_size / 1024
        fraction_of_total = total_size_so_far / total_size
        num_kb_so_far = fraction_of_total * total_kb
        percent = fraction_of_total * 100
        sys.stdout.write(f'Downloaded {num_kb_so_far:.0f} of {total_kb:.0f} KiB\t{percent:.2f}%')

        if blocks_so_far >= total_size:
            sys.stdout.write('\n')

    def dl(self):
        response = request.urlretrieve(self.dl_url, str(self.dl_path), reporthook=self._report_hook)
        sys.stdout.write('\n')
