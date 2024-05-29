import tkinter as tk
from tkinter import messagebox

class InvoiceGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice Generator")

        self.customer_name = tk.StringVar()
        self.customer_address = tk.StringVar()
        self.product_name = tk.StringVar()
        self.quantity = tk.DoubleVar()
        self.unit_price = tk.DoubleVar()
        self.gst_rate = tk.DoubleVar()

        self.create_widgets()

    def calculate_total(self):
        try:
            quantity = self.quantity.get()
            unit_price = self.unit_price.get()
            gst_rate = self.gst_rate.get()

            total_amount = quantity * unit_price
            gst_amount = (total_amount * gst_rate) / 100
            total_with_gst = total_amount + gst_amount

            return total_amount, gst_amount, total_with_gst
        except Exception as e:
            return None, None, None

    def generate_invoice(self):
        total_amount, gst_amount, total_with_gst = self.calculate_total()

        if total_amount is None:
            messagebox.showerror("Error", "Invalid input. Please check your values.")
            return

        invoice_text = f"Customer Name: {self.customer_name.get()}\n"
        invoice_text += f"Customer Address: {self.customer_address.get()}\n"
        invoice_text += f"Product: {self.product_name.get()}\n"
        invoice_text += f"Quantity: {self.quantity.get()}\n"
        invoice_text += f"Unit Price: {self.unit_price.get()}\n"
        invoice_text += f"GST Rate: {self.gst_rate.get()}%\n"
        invoice_text += f"Total Amount: {total_amount}\n"
        invoice_text += f"GST Amount: {gst_amount}\n"
        invoice_text += f"Total with GST: {total_with_gst}"

        with open("invoice.txt", "w") as file:
            file.write(invoice_text)

        messagebox.showinfo("Success", "Invoice generated successfully.")

    def create_widgets(self):
        # Create and arrange your GUI elements here
        # Example: labels, entry fields, buttons, etc.

        generate_button = tk.Button(self.root, text="Generate Invoice", command=self.generate_invoice)
        generate_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceGenerator(root)
    root.mainloop()
