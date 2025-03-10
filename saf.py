import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class SafariCMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Safari CMS - MVP")
        self.testimonials = []  # In-memory storage for testimonials

        # Setup Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.tab_add = ttk.Frame(self.notebook)
        self.tab_view = ttk.Frame(self.notebook)
        self.tab_demo = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_add, text="Add Testimonial")
        self.notebook.add(self.tab_view, text="View Testimonials")
        self.notebook.add(self.tab_demo, text="Demo & Analysis")

        self.setup_tab_add()
        self.setup_tab_view()
        self.setup_tab_demo()

    def setup_tab_add(self):
        # Testimonial Input
        lbl_testimonial = ttk.Label(self.tab_add, text="Enter Testimonial:")
        lbl_testimonial.pack(pady=(10, 0))
        self.txt_testimonial = tk.Text(self.tab_add, height=10, width=50)
        self.txt_testimonial.pack(pady=(5, 10))

        # Email Input (Optional)
        lbl_email = ttk.Label(self.tab_add, text="Email (Optional):")
        lbl_email.pack(pady=(10, 0))
        self.entry_email = ttk.Entry(self.tab_add, width=50)
        self.entry_email.pack(pady=(5, 10))

        # Submit Button
        btn_submit = ttk.Button(self.tab_add, text="Submit Testimonial", command=self.submit_testimonial)
        btn_submit.pack(pady=(10, 10))

    def submit_testimonial(self):
        testimonial = self.txt_testimonial.get("1.0", tk.END).strip()
        email = self.entry_email.get().strip()
        if not testimonial:
            messagebox.showerror("Error", "Testimonial text cannot be empty.")
            return

        # Record submission time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"timestamp": timestamp, "email": email, "testimonial": testimonial}
        self.testimonials.append(entry)

        messagebox.showinfo("Success", "Testimonial submitted successfully!")
        self.txt_testimonial.delete("1.0", tk.END)
        self.entry_email.delete(0, tk.END)
        self.update_view_tab()
        self.update_demo_listbox()

    def setup_tab_view(self):
        # Treeview for displaying testimonials
        columns = ("timestamp", "email", "testimonial")
        self.tree = ttk.Treeview(self.tab_view, columns=columns, show="headings")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("email", text="Email")
        self.tree.heading("testimonial", text="Testimonial")
        self.tree.column("timestamp", width=150)
        self.tree.column("email", width=150)
        self.tree.column("testimonial", width=300)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Refresh Button
        btn_refresh = ttk.Button(self.tab_view, text="Refresh", command=self.update_view_tab)
        btn_refresh.pack(pady=10)

    def update_view_tab(self):
        # Clear and update the treeview with latest testimonials
        for item in self.tree.get_children():
            self.tree.delete(item)
        for testimonial in self.testimonials:
            self.tree.insert("", tk.END, values=(testimonial["timestamp"],
                                                 testimonial["email"],
                                                 testimonial["testimonial"]))

    def setup_tab_demo(self):
        # Information Label
        lbl_info = ttk.Label(self.tab_demo, text="Select a testimonial and click 'Analyze' to simulate LLM analysis.")
        lbl_info.pack(pady=(10, 5))

        # Listbox to display testimonial previews
        self.listbox_demo = tk.Listbox(self.tab_demo, width=80, height=10)
        self.listbox_demo.pack(padx=10, pady=5)
        self.update_demo_listbox()

        # Analyze Button
        btn_analyze = ttk.Button(self.tab_demo, text="Analyze Selected Testimonial", command=self.analyze_testimonial)
        btn_analyze.pack(pady=10)

        # Label to display simulated analysis result
        self.lbl_analysis_result = ttk.Label(self.tab_demo, text="Analysis result will appear here.", wraplength=600)
        self.lbl_analysis_result.pack(pady=10)

        # Refresh Button for Listbox
        btn_refresh_demo = ttk.Button(self.tab_demo, text="Refresh List", command=self.update_demo_listbox)
        btn_refresh_demo.pack(pady=5)

    def update_demo_listbox(self):
        self.listbox_demo.delete(0, tk.END)
        for idx, testimonial in enumerate(self.testimonials):
            preview = testimonial['testimonial'][:60].replace('\n', ' ') + "..."
            self.listbox_demo.insert(tk.END, f"{idx+1}. {preview}")

    def analyze_testimonial(self):
        try:
            index = self.listbox_demo.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "Please select a testimonial to analyze.")
            return

        testimonial_text = self.testimonials[index]["testimonial"]
        result = self.simulate_llm_analysis(testimonial_text)
        self.lbl_analysis_result.config(text=result)

    def simulate_llm_analysis(self, text):
        """
        A placeholder function simulating LLM analysis.
        It uses basic keyword checks to return a sentiment.
        """
        positive_keywords = ['good', 'great', 'excellent', 'amazing', 'fantastic']
        negative_keywords = ['bad', 'poor', 'terrible', 'awful', 'disappointing']
        text_lower = text.lower()
        pos_count = sum(text_lower.count(word) for word in positive_keywords)
        neg_count = sum(text_lower.count(word) for word in negative_keywords)

        if pos_count > neg_count:
            sentiment = "Positive"
        elif neg_count > pos_count:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        analysis = (f"Simulated Analysis:\n"
                    f"Sentiment: {sentiment}\n"
                    f"Positive keyword count: {pos_count}\n"
                    f"Negative keyword count: {neg_count}")
        return analysis

if __name__ == "__main__":
    root = tk.Tk()
    app = SafariCMSApp(root)
    root.mainloop()
