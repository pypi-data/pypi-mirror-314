import unittest
import tkinter as tk
from tkinter import ttk

class TestDesignPR_gui(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.gui = DesignPR(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_gui_components(self):
        self.gui.gui_setup()

        self.assertTrue(hasattr(self.gui, 'purpose_user'), "Purpose frame components are not properly set up.")
        self.assertTrue(hasattr(self.gui, 'seq_frame'), "Sequence frame is not properly set up.")
        self.assertTrue(hasattr(self.gui, 'method_var'), "Method frame components are not properly set up.")
        self.assertTrue(hasattr(self.gui, 'result_text'), "Result frame is not properly set up.")

    def test_gui_action_buttons(self):
        self.gui.gui_setup()

        buttons = [child for child in self.root.winfo_children() if isinstance(child, ttk.Button)]
        self.assertGreaterEqual(len(buttons), 2, "Action buttons are missing.")
        self.assertTrue(any(button.cget("text") == "Design Primers" for button in buttons), "Design Primers button is missing.")
        self.assertTrue(any(button.cget("text") == "Clear" for button in buttons), "Clear button is missing.")

    def test_create_purpose_frame_layout(self):
        self.gui.create_purpose_frame()

        self.assertEqual(self.gui.purpose_user.get(), "Insertion", "Default purpose should be 'Insertion'.")
        frame = [child for child in self.root.winfo_children() if isinstance(child, ttk.LabelFrame) and child.cget("text") == "Primers Purpose"]
        self.assertEqual(len(frame), 1, "Purpose frame is not properly created.")

    def test_create_purpose_frame_radio_buttons(self):
        self.gui.create_purpose_frame()

        frame = [child for child in self.root.winfo_children() if isinstance(child, ttk.LabelFrame) and child.cget("text") == "Primers Purpose"]
        self.assertEqual(len(frame), 1, "Purpose frame was not created correctly.")
        buttons = [child for child in frame[0].winfo_children() if isinstance(child, ttk.Radiobutton)]
        self.assertEqual(len(buttons), 4, "Radio buttons for all purposes are not properly created.")
        self.assertEqual(buttons[0].cget("text"), "Insertion", "First button should be 'Insertion'.")

    def test_create_sequence_frame_layout(self):
        self.gui.create_sequence_frame()

        self.assertTrue(hasattr(self.gui, 'seq_frame'), "Sequence frame is not properly created.")
        self.assertTrue(self.gui.seq_frame.winfo_children(), "Sequence frame should have children elements.")

    def test_create_sequence_frame_dynamic_update(self):
        self.gui.create_sequence_frame()

        initial_children = self.gui.seq_frame.winfo_children()
        self.gui.update_sequence_fields()
        updated_children = self.gui.seq_frame.winfo_children()

        self.assertGreater(len(updated_children), len(initial_children), "Sequence frame should update dynamically.")

    def test_create_method_frame_layout(self):
        self.gui.create_method_frame()

        frame = [child for child in self.root.winfo_children() if isinstance(child, ttk.LabelFrame) and child.cget("text") == "Cloning Method"]
        self.assertEqual(len(frame), 1, "Method frame is not properly created.")
        self.assertTrue(hasattr(self.gui, 'method_var'), "Method variable is not properly initialized.")

    def test_create_method_frame_default(self):
        self.gui.create_method_frame()

        self.assertEqual(self.gui.method_var.get(), "IVA", "Default cloning method should be 'IVA'.")

if __name__ == "__main__":
    unittest.main()
