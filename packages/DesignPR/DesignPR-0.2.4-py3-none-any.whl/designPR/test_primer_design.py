import unittest
import tkinter as tk
from tkinter import ttk

class TestDesignPR(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.gui = DesignPR(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_checkSEQ_empty_entry(self):
        # Test the empty input error
        self.gui.seq_entry_1.delete('1.0', 'end')
        self.gui.seq_entry_2.delete('1.0', 'end')
        with self.assertRaises(messagebox.showerror):
            self.gui.checkSEQ()

    def test_checkSEQ_invalid_characters(self):
        # Test the non-base characters error
        self.gui.seq_entry_1.insert('1.0', 'ATCGX')
        self.gui.seq_entry_2.insert('1.0', 'ATCG')
        with self.assertRaises(messagebox.showerror):
            self.gui.checkSEQ()

    def test_reverse_complement(self):
        # Test with a sample sequence
        result = self.gui.reverse_complement('ATCG')
        self.assertEqual(result, 'CGAT')

    def test_reverse_complement_empty_sequence(self):
        # Test with an empty sequence
        result = self.gui.reverse_complement('')
        self.assertEqual(result, '')

    def test_design_primers_insertion(self):
        # Test primer design for insertion
        self.gui.seq_entry_1.insert('1.0', 'ATCGTACG')
        self.gui.seq_entry_2.insert('1.0', 'TACG')
        self.gui.purpose_user.set('Insertion')
        primers = self.gui.design_primers()
        self.assertTrue('forward' in primers, "Forward primer not generated.")
        self.assertTrue('reverse' in primers, "Reverse primer not generated.")

    def test_design_primers_deletion(self):
        # Test primer design for deletion
        self.gui.seq_entry_1.insert('1.0', 'ATCGTACG')
        self.gui.seq_entry_2.insert('1.0', 'TAC')
        self.gui.purpose_user.set('Deletion')
        primers = self.gui.design_primers()
        self.assertTrue('forward' in primers, "Forward primer not generated.")
        self.assertTrue('reverse' in primers, "Reverse primer not generated.")

if __name__ == "__main__":
    unittest.main()
