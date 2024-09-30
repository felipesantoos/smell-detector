import os
import unittest
from io import StringIO
import sys
from duplicate_feature_title import extract_features, analyze_features, print_report, find_duplicate_feature_titles

class TestDuplicateFeatureTitles(unittest.TestCase):

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output
        self.test_csv_filename = "test_duplicate_feature_title.csv"

    def tearDown(self):
        sys.stdout = sys.__stdout__
        # Remove the test CSV file if it exists
        if os.path.exists(self.test_csv_filename):
            os.remove(self.test_csv_filename)

    def test_extract_features(self):
        feature_files = [
            "Feature: Example feature 1\n",
            "Feature: Example feature 2\n",
            "Feature: Example feature 3\n"
        ]
        filenames = ["file1.feature", "file2.feature", "file3.feature"]
        expected = [
            ("Feature: Example feature 1", "file1.feature"),
            ("Feature: Example feature 2", "file2.feature"),
            ("Feature: Example feature 3", "file3.feature")
        ]
        self.assertEqual(extract_features(filenames, feature_files), expected)

    def test_analyze_features(self):
        features = [
            ("Feature: Example feature 1", "file1.feature"),
            ("Feature: Example feature 1", "file2.feature"),
            ("Feature: Example feature 2", "file3.feature"),
            ("Feature: Example feature 3", "file4.feature")
        ]
        total_features, total_distinct_features, report_data = analyze_features(features)
        self.assertEqual(total_features, 4)
        self.assertEqual(total_distinct_features, 3)
        self.assertEqual(report_data, [
            ["Feature: Example feature 1", 2, "file1.feature, file2.feature"]
        ])

    def test_print_report(self):
        total_features = 4
        total_distinct_features = 3
        report_data = [
            ["Feature: Example feature 1", 2, "file1.feature, file2.feature"]
        ]
        print_report(total_features, total_distinct_features, report_data, self.test_csv_filename)
        output = self.held_output.getvalue().strip().split('\n')
        self.assertIn("Total number of features across all files: 4", output[0])
        self.assertIn("Total number of distinct features across all files: 3", output[1])
        self.assertIn("Features that appeared more than once:", output[2])
        self.assertIn("+-------+----------------------------+-------+------------------------------+", output[3])
        self.assertIn("| Index |          Feature           | Count |          Filenames           |", output[4])
        self.assertIn("+-------+----------------------------+-------+------------------------------+", output[5])
        self.assertIn("|   1   | Feature: Example feature 1 |   2   | file1.feature, file2.feature |", output[6])
        self.assertIn("+-------+----------------------------+-------+------------------------------+", output[7])

        self.assertTrue(os.path.exists(self.test_csv_filename))
        with open(self.test_csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
            csv_content = csvfile.readlines()
            self.assertEqual(csv_content[0].strip(), "Index,Feature,Count,Filenames")
            self.assertEqual(csv_content[1].strip(), "1,Feature: Example feature 1,2,\"file1.feature, file2.feature\"")

    def test_find_duplicate_feature_titles(self):
        feature_files_example = [
            "Feature: Example feature 1\n",
            "Feature: Example feature 1\n",
            "Feature: Example feature 2\n",
            "Feature: Example feature 1\n"
        ]
        feature_filenames = ["file1.feature", "file2.feature", "file3.feature", "file4.feature"]
        find_duplicate_feature_titles(feature_filenames, feature_files_example)
        output = self.held_output.getvalue().strip()
        self.assertIn("Total number of features across all files: 4", output)
        self.assertIn("Total number of distinct features across all files: 2", output)
        self.assertIn("Features that appeared more than once:", output)        

if __name__ == '__main__':
    unittest.main()
