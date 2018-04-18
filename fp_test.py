import unittest
from fp import *

class TestMyCode(unittest.TestCase):


    def test_pets_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Breed FROM Pets'
        results = cur.execute(sql)
        result_list = results.fetchall()

        self.assertIn(('American Shorthair',), result_list)
        self.assertIn(('Hound',), result_list)
        self.assertIn(('Mixed Breed',), result_list)
        self.assertEqual(type(result_list[0]), tuple)
        self.assertEqual(type(result_list), list)
        self.assertEqual(len(result_list), 100)

        conn.close()

    def test_shelters_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT shelterName FROM Shelters'
        results = cur.execute(sql)
        result_list = results.fetchall()

        self.assertIn(('Huron Humane Society',), result_list)
        self.assertIn(('Paws Patrol',), result_list)
        self.assertEqual(type(result_list[0]), tuple)
        self.assertEqual(type(result_list), list)
        self.assertEqual(len(result_list), 29)

        conn.close()

    def test_make_bar_graph_data(self):

    	results = make_bar_graph_data()

    	self.assertIn(("Baby"), bar_graph_x_values)
    	self.assertIn(("Adult"), bar_graph_x_values)
    	self.assertIn(("Senior"), bar_graph_x_values)
    	self.assertEqual(len(bar_graph_y_values), 8)
    	self.assertEqual(len(bar_graph_x_values), 8)

    def test_get_list_of_shelters_for_google_api(self):

    	results = get_list_of_shelters_for_google_api()

    	self.assertIn('Huron Humane Society', shelterstr)
    	self.assertEqual(len(shelterstr), 29)



unittest.main()
