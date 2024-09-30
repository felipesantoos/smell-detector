import unittest
from io import StringIO
import sys
import os
from untitled_feature import find_untitled_features

class TestFindUntitledFeatures(unittest.TestCase):

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output
        self.test_csv_filename = "test_untitled_feature.csv"

    def tearDown(self):
        sys.stdout = sys.__stdout__
        # Remove the test CSV file if it exists
        if os.path.exists(self.test_csv_filename):
            os.remove(self.test_csv_filename)

    def test_untitled_feature_found(self):
        feature_file_names = [
            "file1.feature",
            "file2.feature",
            "file3.feature",
            "file4.feature"
        ]
        feature_file_contents = [
            "Feature:\nScenario: Valid scenario",
            "Feature: \n",
            "Feature:     \n",
            "Feature: Some title\nScenario: Another valid scenario"
        ]
        find_untitled_features(feature_file_names, feature_file_contents, self.test_csv_filename)
        output = self.held_output.getvalue().strip().split('\n')
        self.assertIn("+---------------+---------------+----------------+", output[0])
        self.assertIn("| Filename      |   Line Number | Matched Line   |", output[1])
        self.assertIn("+===============+===============+================+", output[2])
        self.assertIn("| file1.feature |             1 | Feature:       |", output[3])
        self.assertIn("+---------------+---------------+----------------+", output[4])
        self.assertIn("| file2.feature |             1 | Feature:       |", output[5])
        self.assertIn("+---------------+---------------+----------------+", output[6])
        self.assertIn("| file3.feature |             1 | Feature:       |", output[7])
        self.assertIn("+---------------+---------------+----------------+", output[8])
        self.assertIn("Results saved to test_untitled_feature.csv.", output[9])

    def test_no_files(self):
        find_untitled_features([], [], self.test_csv_filename)
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, "No untitled features found.")

    def test_mixed_features(self):
        feature_file_names = [
            "file1.feature",
            "file2.feature",
            "file3.feature",
            "file4.feature"
        ]
        feature_file_contents = [
            "Feature:\nScenario: A scenario",
            "Feature: This is titled\n",
            "Feature:    \n",
            "Feature: Another title\n"
        ]
        find_untitled_features(feature_file_names, feature_file_contents, self.test_csv_filename)
        output = self.held_output.getvalue().strip().split('\n')
        self.assertIn("+---------------+---------------+----------------+", output[0])
        self.assertIn("| Filename      |   Line Number | Matched Line   |", output[1])
        self.assertIn("+===============+===============+================+", output[2])
        self.assertIn("| file1.feature |             1 | Feature:       |", output[3])
        self.assertIn("+---------------+---------------+----------------+", output[4])
        self.assertIn("| file3.feature |             1 | Feature:       |", output[5])
        self.assertIn("+---------------+---------------+----------------+", output[6])
        self.assertIn("Results saved to test_untitled_feature.csv.", output[7])

    def test_csv_creation(self):
        feature_file_names = ["file1.feature"]
        feature_file_contents = ["Feature:\nScenario: A scenario"]
        find_untitled_features(feature_file_names, feature_file_contents, self.test_csv_filename)
        self.assertTrue(os.path.exists(self.test_csv_filename))  # Check if CSV file was created
        with open(self.test_csv_filename, 'r', encoding='utf-8') as csvfile:
            csv_content = csvfile.read()
            self.assertIn("Filename,Line Number,Matched Line", csv_content)  # Check CSV header
            self.assertIn("file1.feature,1,Feature:", csv_content)  # Check CSV content

if __name__ == '__main__':
    unittest.main()
