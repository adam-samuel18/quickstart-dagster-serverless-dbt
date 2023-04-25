import duckdb


class DuckDBLoadAuth:

    def establish_connection(self):
        conn = duckdb.connect
        return conn

class DuckDBExport:

    def view_df_into_ddb(self, df):
        """
        Copies data into DuckDB table while not overwriting old data
        """
        #self.conn = DuckDBLoadAuth.establish_connection(self)
        print(duckdb.query("SELECT * FROM df").to_df())
        #self.conn.close