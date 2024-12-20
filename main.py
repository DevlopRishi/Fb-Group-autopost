import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
import logging
import threading
import os

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FacebookAutomatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Group Poster")
        self.root.geometry("800x600")

        # Variables
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.group_file_path_var = tk.StringVar()
        self.content_file_path_var = tk.StringVar()
        self.image_path_var = tk.StringVar()
        self.headless_var = tk.BooleanVar()
        self.proxy_var = tk.StringVar()

        # Input Frames
        input_frame = tk.Frame(root)
        input_frame.pack(padx=10, pady=10, fill=tk.X)

        # Email and Password Input
        tk.Label(input_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, padx=5)
        tk.Entry(input_frame, textvariable=self.email_var, width=30).grid(row=0, column=1, sticky=tk.W, padx=5)
        tk.Label(input_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, padx=5)
        tk.Entry(input_frame, textvariable=self.password_var, show="*", width=30).grid(row=1, column=1, sticky=tk.W, padx=5)

        # Group URL File Input
        tk.Label(input_frame, text="Group URLs File:").grid(row=2, column=0, sticky=tk.W, padx=5)
        tk.Entry(input_frame, textvariable=self.group_file_path_var, state='disabled', width=30).grid(row=2, column=1, sticky=tk.W, padx=5)
        tk.Button(input_frame, text="Browse", command=self.browse_group_file).grid(row=2, column=2, sticky=tk.W, padx=5)

        # Content File Input
        tk.Label(input_frame, text="Content File:").grid(row=3, column=0, sticky=tk.W, padx=5)
        tk.Entry(input_frame, textvariable=self.content_file_path_var, state='disabled', width=30).grid(row=3, column=1, sticky=tk.W, padx=5)
        tk.Button(input_frame, text="Browse", command=self.browse_content_file).grid(row=3, column=2, sticky=tk.W, padx=5)
        
        # Image File Input
        tk.Label(input_frame, text="Optional Image File:").grid(row=4, column=0, sticky=tk.W, padx=5)
        tk.Entry(input_frame, textvariable=self.image_path_var, state='disabled', width=30).grid(row=4, column=1, sticky=tk.W, padx=5)
        tk.Button(input_frame, text="Browse", command=self.browse_image_file).grid(row=4, column=2, sticky=tk.W, padx=5)


        # Headless Checkbox
        tk.Checkbutton(input_frame, text="Headless Mode", variable=self.headless_var).grid(row=5, column=0, sticky=tk.W, padx=5)

        # Proxy Input
        tk.Label(input_frame, text="Proxy (ip:port):").grid(row=6, column=0, sticky=tk.W, padx=5)
        tk.Entry(input_frame, textvariable=self.proxy_var, width=30).grid(row=6, column=1, sticky=tk.W, padx=5)

        # Start Button
        start_button = tk.Button(root, text="Start Posting", command=self.start_posting)
        start_button.pack(pady=10)

        # Log Display
        log_frame = tk.Frame(root)
        log_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Save button
        save_button = tk.Button(root, text='Save Log', command=self.save_log)
        save_button.pack(pady=10)

    def log_message(self, message):
        """Logs message to GUI and console."""
        logging.info(message)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def browse_group_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.group_file_path_var.set(file_path)
    
    def browse_content_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.content_file_path_var.set(file_path)
    
    def browse_image_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.image_path_var.set(file_path)
    
    def save_log(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.log_text.get("1.0", tk.END))
                messagebox.showinfo("Save", "Log Saved Successfully")

    def load_content_from_file(self, file_path):
        """Loads content from a text file, with each line being a post variation."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return [line.strip() for line in file if line.strip()]
        except Exception as e:
            self.log_message(f"Error loading content file: {e}")
            return []
        
    def load_group_urls_from_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                 return [line.strip() for line in file if line.strip()]
        except Exception as e:
            self.log_message(f"Error loading group urls: {e}")
            return []

    def start_posting(self):
        email = self.email_var.get()
        password = self.password_var.get()
        group_file_path = self.group_file_path_var.get()
        content_file_path = self.content_file_path_var.get()
        image_path = self.image_path_var.get()
        headless = self.headless_var.get()
        proxy = self.proxy_var.get()
        
        # Check for empty values and alert the user
        if not email:
            messagebox.showerror('Error', 'Email is required.')
            return
        if not password:
            messagebox.showerror('Error', 'Password is required.')
            return
        if not group_file_path:
            messagebox.showerror('Error', 'Group URLs file is required.')
            return
        if not content_file_path:
            messagebox.showerror('Error', 'Content file is required.')
            return
        
        group_urls = self.load_group_urls_from_file(group_file_path)
        content_list = self.load_content_from_file(content_file_path)

        if not group_urls or not content_list:
                return

        # Start posting in a separate thread to not block the UI
        threading.Thread(target=self._post_thread, args=(email, password, group_urls, content_list, image_path, headless, proxy)).start()

    def _post_thread(self, email, password, group_urls, content_list, image_path, headless, proxy):
        driver = self._setup_webdriver(headless, proxy)
        try:
            self._login_to_facebook(driver, email, password)
            for group_url in group_urls:
                post_text = random.choice(content_list)
                self._post_to_group(driver, group_url, post_text, image_path=image_path)
                time.sleep(random.randint(5, 15)) # Vary delays between groups
        finally:
            if driver:
              driver.quit()

    def _setup_webdriver(self, headless, proxy):
        """Sets up the Selenium webdriver with options"""
        options = Options()
        if headless:
            options.add_argument("--headless")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        try:
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
             self.log_message(f"Error setting up webdriver {e}")
             return None
             

    def _login_to_facebook(self, driver, email, password):
         """Logs into Facebook."""
         try:
           driver.get("https://www.facebook.com/")
           email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
           password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
           email_field.send_keys(email)
           password_field.send_keys(password)
           password_field.send_keys(Keys.RETURN)
           WebDriverWait(driver, 10).until(EC.url_contains("facebook.com/home"))
           self.log_message("Logged in successfully")
         except Exception as e:
           self.log_message(f"Error logging into facebook {str(e)}")

    def _check_group_membership(self, driver, group_url):
        """Checks if the account is a member of the group."""
        driver.get(group_url)
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Join Group') or contains(text(), 'Unirse al grupo')]"))) #  or (contains(text(), 'Participar')) if the site is in portuguese
            self.log_message(f"Not a member of group: {group_url}")
            return False
        except:
            return True


    def _post_to_group(self, driver, group_url, post_text, delay=3, image_path=None):
        """Posts a text message in a given group."""
        if not self._check_group_membership(driver, group_url):
            return
        try:
             driver.get(group_url)
             post_field = WebDriverWait(driver, 10).until(
               EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Write a post...' or @aria-label='Create a post...']"))
             )
             # Click on the box if it is a button
             if post_field.get_attribute('aria-label') == 'Create a post...':
                 post_field.click()
                 time.sleep(2)
                 post_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Write a post...']"))
                  )

             # Type in the message
             post_field.send_keys(post_text)

             # Optionally, upload image
             if image_path:
                upload_button = WebDriverWait(driver, 10).until(
                 EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Photo/video' or @aria-label='Add photo or video']//input"))
                )
                upload_button.send_keys(image_path)
                time.sleep(5) # Give time for upload
             
             # Locate and click on the post button
             post_button = WebDriverWait(driver, 10).until(
               EC.element_to_be_clickable((By.XPATH, "//span[text()='Post' or text()='Publicar']"))
              )
             post_button.click()
             time.sleep(delay)  # Give time for post to complete
             self.log_message(f"Posted to group: {group_url}")

        except Exception as e:
             self.log_message(f"Error occurred for group {group_url}: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FacebookAutomatorGUI(root)
    root.mainloop()
