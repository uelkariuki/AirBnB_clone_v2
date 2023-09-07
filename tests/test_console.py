#!/usr/bin/python3
""" Testing the console"""
from console import HBNBCommand
from  unittest.mock import patch
from io import StringIO
import unittest
import datetime
from uuid import UUID
import json
import os


class test_console(unittest.TestCase):
    """ class test_console"""
    def setUp(self):
        """ initial setup process"""
        self.console = HBNBCommand()

    def tearDown(self):
        """ method to clean up any resources set up"""
        pass

    @patch('sys.stdout', new_callable=StringIO)

    def test_quit(self, mock_stdout):
        """ Tests if the console exits correctly when user enters quit command"""
        with patch('builtins.input', side_effect=["quit"]):
            with self.assertRaises(SystemExit):
                self.console.cmdloop()
            self.assertEqual(mock_stdout.getvalue().strip(), "")
