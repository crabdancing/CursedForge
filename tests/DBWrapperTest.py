import unittest
from DBWrapperADT_GarbageCSVTables import DBWrapper


class DBWrapperADTTest(unittest.TestCase):
    db = DBWrapper()

    def test_retrieve_from_db(self):
        # I don't know why the internet keeps making this dumb joke, but I'll do my part I guess
        # NOTE: this one is not added to DB -- the idea is to test whether it's detected.
        self.assertEqual(69, self.db.query_project_id('funny-sex-number'))

    def test_set_query(self):
        # ha ha funny internet number go brrr
        self.db.set_project_id(420, 'blaze-it')
        self.assertEqual(420, self.db.query_project_id('blaze-it'))


if __name__ == '__main__':
    unittest.main()
