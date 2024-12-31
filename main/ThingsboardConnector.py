import tkinter as tk
from tkinter import messagebox
import logging
from tb_rest_client.rest_client_ce import RestClientCE
from tb_rest_client.rest import ApiException

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

class ThingsboardConnectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Thingsboard Connector")
        
        self.label = tk.Label(root, text="Thingsboard URL:")
        self.label.pack()
        
        self.url_entry = tk.Entry(root)
        self.url_entry.pack()

        self.user_id_label = tk.Label(root, text="User ID:")
        self.user_id_label.pack()
        
        self.user_id_entry = tk.Entry(root)
        self.user_id_entry.pack()
        
        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()
        
        self.connect_button = tk.Button(root, text="Connect", command=self.connect)
        self.connect_button.pack()
        
        self.device_listbox = tk.Listbox(root)
        self.device_listbox.pack()
        
        self.refresh_button = tk.Button(root, text="Refresh Devices", command=self.refresh_devices)
        self.refresh_button.pack()
        
        self.client = None  # Initialize the client as None initially
        
    def connect(self):
        url = self.url_entry.get()
        try:
            self.client = RestClientCE(base_url=url)
            self.client.login(username=self.user_id_entry.get(), password=self.password_entry.get())
            messagebox.showinfo("Info", "Connected to Thingsboard")
            logging.info("Connected to Thingsboard at %s", url)
        except ApiException as e:
            messagebox.showerror("Error", "Failed to connect to Thingsboard")
            logging.exception("Failed to connect to Thingsboard: %s", e)
        
    def refresh_devices(self):
        # Check if client is initialized before calling any methods
        if not self.client:
            messagebox.showerror("Error", "Please connect to Thingsboard first.")
            logging.error("Attempted to refresh devices without a valid client connection.")
            return

        try:
            devices = self.client.get_tenant_devices()
            self.device_listbox.delete(0, tk.END)
            for device in devices:
                self.device_listbox.insert(tk.END, device.name)
            logging.info("Devices refreshed successfully")
        except ApiException as e:
            messagebox.showerror("Error", "Failed to refresh devices")
            logging.exception("Failed to refresh devices: %s", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = ThingsboardConnectorApp(root)
    root.mainloop()
