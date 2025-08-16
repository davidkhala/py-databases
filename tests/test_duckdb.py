import unittest
import duckdb
import seaborn
import matplotlib.pyplot as plt
class AirlineTestCase(unittest.TestCase):

    db = duckdb.connect()
    airport_csv= "fixtures/airports.csv"
    @classmethod
    def tearDownClass(cls):
        cls.db.close()
    def test_file_direct(self):

        df_airports = self.db.execute(
            f'''
            SELECT *
            FROM read_csv_auto('{self.airport_csv}')
            '''
        ).df()
        self.db.register("airports", df_airports)
        print()
        print(self.db.execute('SHOW TABLES').df())


    def test_plot(self):
        df_airports = self.db.execute(
            f'''
            SELECT *
            FROM read_csv_auto('{self.airport_csv}')
            '''
        ).df()
        self.db.register("airports", df_airports)
        df_canvas = self.db.execute('''
                           SELECT count(*) as Count,STATE
                           FROM airports
                           GROUP BY STATE
                           ORDER BY Count DESC
                           ''').df()
        palette_color = seaborn.color_palette('pastel')
        plt.figure(figsize=(7, 7))

        plt.pie(df_canvas['Count'],
                labels=df_canvas['STATE'],
                colors=palette_color,
                autopct='%.0f%%', )

        plt.legend(df_canvas['STATE'], loc="best")


if __name__ == '__main__':
    unittest.main()
