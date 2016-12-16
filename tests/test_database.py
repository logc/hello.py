import datetime
import random
import unittest

import MySQLdb
import MySQLdb.cursors
from nose.plugins.attrib import attr
from nose.tools import assert_equals, assert_less

import hello.main


@attr('integration')
class DatabaseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls, connect=MySQLdb.connect):
        """
        Sets up the database connection only once per instance of DatabaseTests
        """
        config = hello.main.parse_config('hello.cfg')
        credentials = hello.main.get_database_credentials(config)
        if not credentials:
            cls.fail("No database credentials for DatabaseTests")
        host, name, user, password = credentials
        cls.conn = connect(host=host, db=name, user=user,
                           passwd=password,
                           cursorclass=MySQLdb.cursors.DictCursor)
        cls.create_cursor = cls.conn.cursor()
        create_stmt = (
            "CREATE TABLE greeted_test ("
            "  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
            "  name VARCHAR(100), "
            "  counter INT NOT NULL DEFAULT 1, "
            "  INDEX(name(10))"
            ");")
        cls.create_cursor.execute(create_stmt)

    def setUp(self):
        """
        Sets up a database cursor for each test method
        """
        self.db = DatabaseTests.conn.cursor()
        self.select_stmt = (
            "SELECT counter FROM greeted_test WHERE name = %(name)s;")
        self.insert_statement = (
            "INSERT INTO greeted_test(name) VALUES (%(name)s)")

    def tearDown(self):
        """
        Cleans up the database table after each test method
        """
        self.db.execute("TRUNCATE TABLE greeted_test;")
        self.db.close()

    @classmethod
    def tearDownClass(cls):
        cls.create_cursor.execute("DROP TABLE IF EXISTS greeted_test")
        cls.create_cursor.close()
        cls.conn.close()

    def test_production_table_exists(self):
        """
        Check that relevant tables exist in db
        """
        self.db.execute("""
            SELECT * FROM information_schema.tables
            WHERE table_name = 'greeted';
        """)
        result = self.db.fetchall()
        assert_equals(len(result), 1)
        row = result[0]
        expected_name = 'hellodb'
        actual_name = row['TABLE_SCHEMA']
        assert_equals(actual_name, expected_name)
        actual_created_time = row['CREATE_TIME']
        assert_less(actual_created_time, datetime.datetime.now())

    def test_production_and_test_tables_are_equal(self):
        """
        Check that fields in production and test tables are equal
        """
        self.db.execute("DESC greeted")
        production_desc = self.db.fetchall()
        self.db.execute("DESC greeted_test")
        test_desc = self.db.fetchall()
        assert_equals(production_desc, test_desc)

    def test_select(self):
        """
        Check that selecting data from db works
        """
        non_existing_name = 'does_not_exist'
        self.db.execute(self.select_stmt, {'name': non_existing_name})
        result = self.db.fetchall()
        assert_equals(len(result), 0)

    def test_insert(self):
        """
        Check that inserting a new row into db works
        """
        name = "some_name"
        self.db.execute(self.insert_statement, {'name': name})
        DatabaseTests.conn.commit()
        self.db.execute(self.select_stmt, {'name': name})
        result = self.db.fetchall()
        assert_equals(len(result), 1)

    def test_update(self):
        """
        Check that updating an existing row in the db table works
        """
        name = "another_name"
        self.db.execute(self.insert_statement, {'name': name})
        update_stmt = (
            "UPDATE greeted_test SET counter=%(counter)s WHERE name=%(name)s")
        counter = random.randint(0, 100)
        self.db.execute(update_stmt, {'name': name, 'counter': counter + 1})
        DatabaseTests.conn.commit()
        self.db.execute(self.select_stmt, {'name': name})
        result = self.db.fetchall()
        new_counter = result[0]['counter']
        assert_equals(new_counter, counter + 1)
