import tkinter as tk
from tkinter import ttk, messagebox
import speedtest
import socket
import threading

class InternetSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")
        self.root.geometry("400x350")
        self.root.configure(bg="#2C3E50")  # Dark Blue Theme

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=5)

        # Title Label
        self.title_label = tk.Label(root, text="Internet Speed Test", font=("Arial", 16, "bold"), fg="white", bg="#2C3E50")
        self.title_label.pack(pady=10)

        # Labels for Speed Test Results
        self.download_label = tk.Label(root, text="Download Speed: -- Mbps", font=("Arial", 12), fg="white", bg="#2C3E50")
        self.download_label.pack(pady=5)

        self.upload_label = tk.Label(root, text="Upload Speed: -- Mbps", font=("Arial", 12), fg="white", bg="#2C3E50")
        self.upload_label.pack(pady=5)

        self.ping_label = tk.Label(root, text="Ping: -- ms", font=("Arial", 12), fg="white", bg="#2C3E50")
        self.ping_label.pack(pady=5)

        # Labels for Network Info
        self.ip_label = tk.Label(root, text="IP Address: --", font=("Arial", 12), fg="white", bg="#2C3E50")
        self.ip_label.pack(pady=5)

        self.isp_label = tk.Label(root, text="ISP: --", font=("Arial", 12), fg="white", bg="#2C3E50")
        self.isp_label.pack(pady=5)

        # Buttons
        self.test_button = ttk.Button(root, text="Run Speed Test", command=self.run_speed_test)
        self.test_button.pack(pady=10)

        self.refresh_button = ttk.Button(root, text="Refresh Network Info", command=self.get_network_info)
        self.refresh_button.pack(pady=5)

        # Load initial network info
        self.get_network_info()

    def get_network_info(self):
        """Fetch local and public IP addresses."""
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            self.ip_label.config(text=f"IP Address: {local_ip}")
        except Exception as e:
            self.ip_label.config(text="IP Address: Error")

    def run_speed_test(self):
        """Run a speed test in a separate thread to prevent UI freezing."""
        threading.Thread(target=self.perform_speed_test, daemon=True).start()

    def perform_speed_test(self):
        """Perform internet speed test and update labels."""
        try:
            self.test_button.config(state=tk.DISABLED, text="Testing...")
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            ping = st.results.ping
            isp = st.results.client.get("isp", "Unknown")

            # Update UI
            self.download_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")
            self.upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
            self.ping_label.config(text=f"Ping: {ping} ms")
            self.isp_label.config(text=f"ISP: {isp}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to test speed: {e}")

        finally:
            self.test_button.config(state=tk.NORMAL, text="Run Speed Test")

if __name__ == "__main__":
    root = tk.Tk()
    app = InternetSpeedTest(root)
    root.mainloop()
