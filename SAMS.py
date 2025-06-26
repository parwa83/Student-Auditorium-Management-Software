import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect("auditorium.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS Shows (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      date TEXT NOT NULL,
                      time TEXT NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Seats (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      show_id INTEGER NOT NULL,
                      seat_number TEXT NOT NULL,
                      seat_type TEXT NOT NULL, -- balcony or ordinary
                      status TEXT NOT NULL, -- available, booked, complimentary, vip
                      FOREIGN KEY (show_id) REFERENCES Shows(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Bookings (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      show_id INTEGER NOT NULL,
                      seat_number TEXT NOT NULL,
                      customer_name TEXT,
                      status TEXT NOT NULL, -- booked or canceled
                      FOREIGN KEY (show_id) REFERENCES Shows(id))''')
 
    conn.commit()
    conn.close()

class AuditoriumManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Auditorium Management Software")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f5")

        self.create_interface()

    def create_interface(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#333", pady=10)
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(header_frame, text="STUDENT AUDITORIUM MANAGEMENT SOFTWARE", 
                                font=("Arial", 16, "bold"), fg="white", bg="#333")
        header_label.pack()

        # Show Management Frame
        show_frame = tk.LabelFrame(self.root, text="Show Management", font=("Arial", 12, "bold"), 
                                   bg="#FFA500", padx=10, pady=10)
        show_frame.pack(padx=10, pady=10, fill="x")

        add_show_button = tk.Button(show_frame, text="Add Show", command=self.add_show, bg="#4CAF50", 
                                    fg="grey", font=("Arial", 10, "bold"))
        add_show_button.pack(pady=5, fill="x")

        view_shows_button = tk.Button(show_frame, text="View Shows", command=self.view_shows, bg="#4CAF50", 
                                      fg="grey", font=("Arial", 10, "bold"))
        view_shows_button.pack(pady=5, fill="x")

        # Seat Management Frame
        seat_frame = tk.LabelFrame(self.root, text="Seat Management", font=("Arial", 12, "bold"), 
                                   bg="#FFA500", padx=10, pady=10)
        seat_frame.pack(padx=10, pady=10, fill="x")

        view_seats_button = tk.Button(seat_frame, text="View Seats", command=self.view_seats, bg="#2196F3", 
                                      fg="grey", font=("Arial", 10, "bold"))
        view_seats_button.pack(pady=5, fill="x")

        book_seat_button = tk.Button(seat_frame, text="Book Seat", command=self.book_seat, bg="#2196F3", 
                                     fg="grey", font=("Arial", 10, "bold"))
        book_seat_button.pack(pady=5, fill="x")

        cancel_booking_button = tk.Button(seat_frame, text="Cancel Booking", command=self.cancel_booking, bg="#2196F3", 
                                          fg="grey", font=("Arial", 10, "bold"))
        cancel_booking_button.pack(pady=5, fill="x")

    def add_show(self):
        name = simpledialog.askstring("Show Name", "Enter show name:")
        date = simpledialog.askstring("Show Date", "Enter show date (YYYY-MM-DD):")
        time = simpledialog.askstring("Show Time", "Enter show time (HH:MM):")
    
        conn = sqlite3.connect("auditorium.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Shows (name, date, time) VALUES (?, ?, ?)", (name, date, time))
        show_id = cursor.lastrowid  # Get the ID of the newly created show
        conn.commit()
    
        # Initialize seats for the new show
        self.initialize_seats(show_id)
    
        conn.close()
        messagebox.showinfo("Success", "Show and seats added successfully.")


    def view_shows(self):
        conn = sqlite3.connect("auditorium.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Shows")
        shows = cursor.fetchall()
        conn.close()
        
        show_info = "\n".join([f"ID: {show[0]}, Name: {show[1]}, Date: {show[2]}, Time: {show[3]}" for show in shows])
        messagebox.showinfo("Shows", show_info)

    def view_seats(self):
        show_id = simpledialog.askinteger("Show ID", "Enter show ID to view seats:")
        
        conn = sqlite3.connect("auditorium.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Seats WHERE show_id = ?", (show_id,))
        seats = cursor.fetchall()
        conn.close()
        
        seat_info = "\n".join([f"Seat: {seat[2]}, Type: {seat[3]}, Status: {seat[4]}" for seat in seats])
        messagebox.showinfo("Seats", seat_info)

   
        seat = cursor.fetchone()
        
    def book_seat(self):
     try:
        show_id = simpledialog.askinteger("Show ID", "Enter show ID:")
        if not show_id:
            messagebox.showerror("Input Error", "Show ID is required.")
            return
        
        seat_number = simpledialog.askstring("Seat Number", "Enter seat number:")
        if not seat_number:
            messagebox.showerror("Input Error", "Seat number is required.")
            return
        
        customer_name = simpledialog.askstring("Customer Name", "Enter customer name:")
        if not customer_name:
            messagebox.showerror("Input Error", "Customer name is required.")
            return
        
        conn = sqlite3.connect("auditorium.db")
        cursor = conn.cursor()

        # Verify if the seat exists and is available
        cursor.execute("SELECT * FROM Seats WHERE show_id = ? AND seat_number = ? AND status = 'available'", 
                       (show_id, seat_number))
        seat = cursor.fetchone()
        
        if seat:
            # Seat is available, proceed with booking
            cursor.execute("UPDATE Seats SET status = 'booked' WHERE show_id = ? AND seat_number = ?", 
                           (show_id, seat_number))
            cursor.execute("INSERT INTO Bookings (show_id, seat_number, customer_name, status) VALUES (?, ?, ?, 'booked')", 
                           (show_id, seat_number, customer_name))
            conn.commit()
            messagebox.showinfo("Success", "Seat booked successfully.")
        else:
            # Seat is either not available or does not exist
            cursor.execute("SELECT * FROM Seats WHERE show_id = ? AND seat_number = ?", (show_id, seat_number))
            seat_check = cursor.fetchone()
            
            if seat_check:
                messagebox.showerror("Error", "Seat is already booked or reserved.")
            else:
                messagebox.showerror("Error", "Seat does not exist for this show. Please check the show ID and seat number.")
        
     except sqlite3.Error as e:
         messagebox.showerror("Database Error", f"An error occurred: {e}")
     finally:
        conn.close()


    


    def cancel_booking(self):
        booking_id = simpledialog.askinteger("Booking ID", "Enter booking ID to cancel:")
        
        conn = sqlite3.connect("auditorium.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE Bookings SET status = 'canceled' WHERE id = ?", (booking_id,))
        if cursor.rowcount > 0:
            conn.commit()
            messagebox.showinfo("Success", "Booking canceled successfully.")
        else:
            messagebox.showerror("Error", "Booking not found.")
        conn.close()

 


if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = AuditoriumManagementSystem(root)
    root.mainloop()
