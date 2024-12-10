import Bio.SeqUtils
from Bio.SeqUtils import gc_fraction
from Bio.SeqUtils.MeltingTemp import Tm_NN
import tkinter as tk
from tkinter import ttk, messagebox


class DesignPR: 
    
    def __init__(self, root):
        self.root = root
        self.root.title("PCR Primer Design Tool")
        self.gui_setup()
        
    
    def gui_setup(self):   
        
        """""
        Purpose: 
        Sets up the GUI by calling all the functions 
        to initialize and arrange the GUI components
        
        Inputs: n/a
        
        """""
          
        self.create_purpose_frame()
        self.create_sequence_frame()
        self.create_method_frame()
        self.create_result_frame()
        self.create_action_buttons()
        
    
    def create_purpose_frame(self):
        
        """""
        Purpose: 
        Creates the button options for primer functions, 
        including insertion, deletion, point mutation and 2-fragment assembly as the options
        
        Inputs: n/a
        
        """""
        
        purpose_frame = ttk.LabelFrame(self.root, text="Primers Purpose")
        purpose_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.purpose_user = tk.StringVar(value="Insertion")
        purposes = ["Insertion", "Deletion", "Point Mutation", "2-Fragment Assembly"]
        for idx, purpose in enumerate(purposes):
            ttk.Radiobutton(purpose_frame, text=purpose, value=purpose, variable=self.purpose_user, command=self.update_sequence_fields).grid(row=0, column=idx, padx=5, pady=5)
    

    def create_sequence_frame(self):
        
        """""
        Purpose: 
        Creates the sequence entry boxes. This method updates actively based on the primer purpose choice
        the update_sequence_filed function is called for that. 
        
        Inputs: n/a
        
        """""
    
        self.seq_frame = ttk.Frame(self.root)
        self.seq_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.update_sequence_fields()
        
    def create_method_frame(self): 
        
        """""
        Purpose: 
        Creates the cloning method option list. Currently, this is only In vivo Assembly (IVA). 
        In the future, primers can be optimized to different cloning methods. 
        
        Inputs: n/a
        
        """""
        
        method_frame = ttk.LabelFrame(self.root, text="Cloning Method")
        method_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.method_var = tk.StringVar(value="IVA")
        self.method_list = ["IVA"]
        self.method_menu = ttk.OptionMenu(method_frame, self.method_var, "IVA", *self.method_list)
        self.method_menu.grid(row=0, column=0, padx=5, pady=5)
               
    
    def create_result_frame(self):
        
        """""
        Purpose: 
        Creates the output box where the resulting primers and optimized parameters 
        are revealed once the "Design Primers" button is pressed.
        
        Inputs: n/a
        
        """""
        
        result_frame = ttk.LabelFrame(self.root, text="Designed Primers")
        result_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.result_text = tk.Text(result_frame, height=10, width=60, state="disabled")
        self.result_text.grid(row=0, column=0, padx=5, pady=5)

    def create_action_buttons(self):
        
        """""
        Purpose: 
        Creates the two action buttons of the GUI.
        One for designing the primers after the user inputs the necessary sequences, which calls the design_primers method
        and another for clearing and restarting the GUI user inputs, which calls the clear method. 
        
        Inputs: n/a
        
        """""
        
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        ttk.Button(button_frame, text="Design Primers", command=self.design_primers).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_all).grid(row=0, column=1, padx=5, pady=5)
    
    
    def update_sequence_fields(self):
        
        """""
        Purpose: 
        Updates the sequence entry boxes based on the primer purpose choice defined by the user. 
        Specifically, it updates the title of each sequence entry box to guide the user inputs. 
       
       
        Inputs: n/a
        
        """""
        
       
        for widget in self.seq_frame.winfo_children():
            widget.destroy()


        purpose = self.purpose_user.get()
        first_frame_title = "DNA Sequence"
        second_frame_title = "Insert Sequence"

        if purpose == "Deletion":
            second_frame_title = "Sequence to Delete"  
        elif purpose == "Point Mutation":
            second_frame_title = "Mutation [original_codon;new_codon]"
        elif purpose == "2-Fragment Assembly": 
            first_frame_title = "Backbone Sequence"
        
        
        #Sequence frame 1
        seq_frame = ttk.LabelFrame(self.seq_frame, text=first_frame_title)
        seq_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(seq_frame, text="Sequence:").grid(row=0, column=0, padx=5, pady=5)
        self.seq_entry_1 = tk.Text(seq_frame, height=5, width=50)
        self.seq_entry_1.grid(row=0, column=1, padx=5, pady=5)
            
        #Sequence frame 2
        seq_frame = ttk.LabelFrame(self.seq_frame, text=second_frame_title)
        seq_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(seq_frame, text="Sequence:").grid(row=0, column=0, padx=5, pady=5)
        self.seq_entry_2 = tk.Text(seq_frame, height=5, width=50)
        self.seq_entry_2.grid(row=0, column=1, padx=5, pady=5)
        



    def checkSEQ(self): 
        
        """""
        Purpose: 
        Checks the sequence inputs from the user for 
        both non-base characters and empty entry boxes.
        
        
        Inputs: n/a
        
        """""
        
        
        seq_1 = self.seq_entry_1.get("1.0", tk.END).strip().upper()
        seq_2 = self.seq_entry_2.get("1.0", tk.END).strip().upper()
        seq_entries = [seq_1, seq_2]
        for seq in seq_entries: 
            if not seq:   
                messagebox.showerror("Input Error", "Please enter a valid DNA sequence.")
                return
            
            allowed_char = ["A", "T", "C", "G", ";"]
            for char in seq: 
                if char not in allowed_char: 
                    messagebox.showerror("Input Error", "Invalid characters found in sequence.")
                    return   
        
        return seq_entries    
    

    def reverse_complement(self, sequence):
        
        """""
        Purpose: 
        Takes primer sequences in the forward complement and turns them into 
        the reverse complement to generate reverse primers. 

        Inputs: primer sequence (forward complement)
        
        """""
        
        
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return ''.join(complement[base] for base in reversed(sequence))
    
    
    def design_primers(self):
        
        """""
        Purpose: 
        Using user input information such as primer purpose and sequences entries, this 
        method computes primer designs finding 
        1- homologous regions that aneal to the template sequences at a certain length
        2- adding inserts or removing sequences provided by the user
        3- overlap regions between two fragments 
        
        Once assembled the primers are sent to method display_primers for further optimization/generation.

        Inputs: n/a
        
        """""
        
        
        
        primer_purpose = self.purpose_user.get()
        seq_entries = self.checkSEQ()
        
        
        
        if(primer_purpose == "Insertion"):
            Backbone_seq = seq_entries[0]
            Ins_seq = seq_entries[1]
            
            if len(Ins_seq) > 15: 
                messagebox.showerror("Input Error", "Please use 2-Fragment Assembly for inserts longer than 15-bps.")
                return
                

            fwd_homologous = Backbone_seq[:15]
            rev_homologous = self.reverse_complement(Backbone_seq[-15:]+Ins_seq)
            
            
            fwd_primer = Ins_seq + fwd_homologous
            rev_primer = rev_homologous
            
            
            
            fwd_primer_optimized, fwd_primer_gc, fwd_primer_tm = self.analyze_primers(fwd_primer)
            rev_primer_optimized, rev_primer_gc, rev_primer_tm = self.analyze_primers(rev_primer)
            
            
            primers = {
                "forward": {fwd_primer_optimized},                
                "reverse": {rev_primer_optimized}, 
            }

            parameters = {
                "forward_gc": {fwd_primer_gc},
                "forward_tm":{fwd_primer_tm}, 
                
                
                "reverse_gc": {rev_primer_gc}, 
                "reverse_tm": {rev_primer_tm}
            }
        
        elif(primer_purpose == "Deletion"): 
            DNA_seq = seq_entries[0]
            delete_seq = seq_entries[1]
            
            fwd_start = len(delete_seq)
            fwd_end = 15+fwd_start
            print(fwd_start)
            
            if delete_seq in DNA_seq: 
                fwd_homologous = DNA_seq[fwd_start:fwd_end]
                rev_homologous = self.reverse_complement(DNA_seq[-15:]+ DNA_seq[fwd_start:fwd_end])
                
                fwd_primer = DNA_seq[-15:] + fwd_homologous
                rev_primer = rev_homologous
                
                
                fwd_primer_optimized, fwd_primer_gc, fwd_primer_tm = self.analyze_primers(fwd_primer)
                rev_primer_optimized, rev_primer_gc, rev_primer_tm = self.analyze_primers(rev_primer)
                
                
                parameters = {
                    "forward_gc": {fwd_primer_gc},
                    "forward_tm":{fwd_primer_tm}, 
                
                
                    "reverse_gc": {rev_primer_gc}, 
                    "reverse_tm": {rev_primer_tm}
                }
                
                primers = {
                    "forward": {fwd_primer},
                    "reverse": {rev_primer}
                }
            else: 
                messagebox.showerror("Input Error", "Sequence to delete not found in DNA sequence.")
                
        elif(primer_purpose == "2-Fragment Assembly"):
            BB_seq = seq_entries[0]
            INS_seq = seq_entries[1]
            
            fwd_BB_homologous = BB_seq[:15]
            fwd_BB_overlap = INS_seq[-12:]
            
            rev_BB_homologous = BB_seq[-15:]
            rev_BB_overlap = INS_seq[:12]
            
            fwd_BB = fwd_BB_overlap + fwd_BB_homologous
            rev_BB = self.reverse_complement(rev_BB_homologous + rev_BB_overlap)
            
            
            fwd_INS_homologous = INS_seq[:15]
            fwd_INS_overlap = BB_seq[-12:]
            
            rev_INS_homologous = INS_seq[-15:]
            rev_INS_overlap = BB_seq[:12]
            
            fwd_INS = fwd_INS_overlap + fwd_INS_homologous
            rev_INS = self.reverse_complement(rev_INS_homologous + rev_INS_overlap)
            
            

            fwd_BB_optimized, fwd_BB_gc, fwd_BB_tm = self.analyze_primers(fwd_BB)
            rev_BB_optimized, rev_BB_gc, rev_BB_tm = self.analyze_primers(rev_BB)
            
            fwd_INS_optimized, fwd_INS_gc, fwd_INS_tm = self.analyze_primers(fwd_INS)
            rev_INS_optimized, rev_INS_gc, rev_INS_tm = self.analyze_primers(rev_INS)
                
                
            parameters = {
                "forward_BB_gc": {fwd_BB_gc},
                "forward_BB_tm":{fwd_BB_tm}, 
                
                "reverse_BB_gc": {rev_BB_gc}, 
                "reverse_BB_tm": {rev_BB_tm}, 
                
                
                "forward_INS_gc": {fwd_INS_gc},
                "forward_INS_tm": {fwd_INS_tm}, 
                
                "reverse_INS_gc": {rev_INS_gc}, 
                "reverse_INS_tm": {rev_INS_tm}
            }
            
            
            primers = {
                "BB_forward": {fwd_BB_optimized},
                "BB_reverse": {rev_BB_optimized},
                
                "INS_forward": {fwd_INS_optimized},
                "INS_reverse": {rev_INS_optimized}
        
            }
        
        #for point mutations 
        else: 
            DNA_seq = seq_entries[0]
            original_codon, new_codon = seq_entries[1].split(";")
            
            fwd_point_homologous = DNA_seq[:15]
            fwd_point_overlap = DNA_seq[-12:]
            
            rev_point_homologous = DNA_seq[-15:] 
            rev_point_overlap = DNA_seq[:12]
            
            fwd_point_primer = fwd_point_overlap + new_codon + fwd_point_homologous
            rev_point_primer = self.reverse_complement(rev_point_homologous + rev_point_overlap)
            
            parameters = {}
            
            primers = {
                "mutation" : {original_codon + "-->" + new_codon},
                "forward": {fwd_point_primer},
                "reverse": {rev_point_primer}
            }

        self.display_primers(primers, parameters)

    
    def analyze_primers(self, primer):
        
        """"
        Purpose: 
        Analyzes a given primer sequence by optimizing its GC content and melting temperature (Tm),
        ensuring it meets specified thresholds for GC content, Tm, and length.

        Inputs:
        The DNA primer sequence to be analyzed.

        Returns:
        A tuple containing the optimized primer, its GC content, and Tm value.
        """
    
        thresholds = {
            "gc_low": 0.4,
            "gc_high": 0.7, 
            "tm_whole": 60, 
            "len_whole": 32
        }
  
        
        primer_optimized, primer_gc, primer_tm = self.optimize_primer(
            primer, 
            gc_low = thresholds["gc_low"],
            gc_high = thresholds["gc_high"],
            tm_threshold = thresholds["tm_whole"], 
            min_length= thresholds["len_whole"]
        )

        print(f"Analyze_primers: {primer_optimized}")
        
        return primer_optimized, primer_gc, primer_tm


    def optimize_primer(self, primer, gc_low, gc_high, tm_threshold, min_length): 
        
        """"
        Purpose:
        Optimizes a primer sequence by adjusting its length until it meets the minimum length,
        GC content, and Tm criteria.

        Inputs:
            primer (str): The DNA primer sequence to be optimized.
            gc_low (float): The minimum acceptable GC content.
            gc_high (float): The maximum acceptable GC content.
            tm_threshold (float): The minimum acceptable Tm value.
            min_length (int): The minimum acceptable length of the primer.

        Returns:
            A tuple containing the optimized primer, its GC content, and Tm value.
        
        """
        
        while len(primer) > min_length: 
            gc_content = gc_fraction(primer)
            tm = Tm_NN(primer)
        
            if gc_low <= gc_content <= gc_high and tm >= tm_threshold: 
                return primer, gc_content, tm
        
            primer = primer[:-1]
        
        return primer, gc_fraction(primer), Tm_NN(primer)



     
    def display_primers(self, primers, parameters):
        
        """
        Purpose: 
            Displays the details of primers based on the user's selected purpose.
            Formats and inserts primer sequences and their properties (e.g., GC content, Tm) into a result text box.

        Inputs:
            primers (dict): A dictionary containing primer sequences.
            parameters (dict): A dictionary containing calculated properties of the primers (GC content and Tm).
        """
        
        print(f"Displaying primers: {primers}")
        primer_purpose = self.purpose_user.get()
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        if primer_purpose == "2-Fragment Assembly":
            self.result_text.insert(tk.END, f"Backbone Forward Primer: {primers['BB_forward']}\n")
            self.result_text.insert(tk.END, f"Backbone Reverse Primer: {primers['BB_reverse']}\n")
            self.result_text.insert(tk.END, f"Insert Forward Primer: {primers['INS_forward']}\n")
            self.result_text.insert(tk.END, f"Insert Reverse Primer: {primers['INS_reverse']}\n")
            
            
            self.result_text.insert(tk.END, f"Backbone Forward Primer GC content: {parameters['forward_BB_gc']}\n")
            self.result_text.insert(tk.END, f"Backbone Forward Primer Tm: {parameters['forward_BB_tm']}\n")
            
            self.result_text.insert(tk.END, f"Backbone Reverse Primer GC content: {parameters['reverse_BB_gc']}\n")
            self.result_text.insert(tk.END, f"Backbone Reverse Primer Tm: {parameters['reverse_BB_tm']}\n")
            
            
            self.result_text.insert(tk.END, f"Insert Forward Primer GC content: {parameters['forward_INS_gc']}\n")
            self.result_text.insert(tk.END, f"Insert Forward Primer Tm: {parameters['forward_INS_tm']}\n")
            
            self.result_text.insert(tk.END, f"Insert Reverse Primer GC content: {parameters['reverse_INS_gc']}\n")
            self.result_text.insert(tk.END, f"Insert Reverse Primer Tm: {parameters['reverse_INS_tm']}\n")
       
        elif primer_purpose == "Point Mutation":
            self.result_text.insert(tk.END, f"Point Mutation: {primers['mutation']}\n")
            self.result_text.insert(tk.END, f"Forward Primer: {primers['forward']}\n")
            self.result_text.insert(tk.END, f"Reverse Primer: {primers['reverse']}\n")
            
            
        elif 'forward' in primers and 'reverse' in primers:
            self.result_text.insert(tk.END, f"Forward Primer: {primers['forward']}\n")
            self.result_text.insert(tk.END, f"Reverse Primer: {primers['reverse']}\n")
            
            self.result_text.insert(tk.END, f"Forward Primer GC content: {parameters['forward_gc']}\n")
            self.result_text.insert(tk.END, f"Forward Primer Tm: {parameters['forward_tm']}\n")
            
            
            self.result_text.insert(tk.END, f"Reverse Primer GC content: {parameters['reverse_gc']}\n")
            self.result_text.insert(tk.END, f"Reverse Primer Tm: {parameters['reverse_tm']}\n")
            
            
        else:
            print("Error: Missing primer data.")
        self.result_text.config(state="disabled")


    def clear_all(self):
        self.seq_entry_1.delete("1.0", tk.END)
        self.seq_entry_2.delete("1.0", tk.END)
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")


def main():
    root = tk.Tk()
    app = DesignPR(root)
    root.mainloop()

if __name__ == "__main__":
    main()
