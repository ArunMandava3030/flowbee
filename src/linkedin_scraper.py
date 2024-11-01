# src/linkedin_scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from queue_manager import QueueManager
from data_handler import DataHandler

class LinkedInScraper:
    def __init__(self, driver_path, queue_manager, data_handler):
        self.driver_path = driver_path
        self.driver = webdriver.Chrome(self.driver_path)
        self.queue_manager = queue_manager
        self.data_handler = data_handler

    def login(self, username, password):
        # Login to LinkedIn (Update URL and selectors as necessary)
        self.driver.get("https://www.linkedin.com/login")
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]").click()
        time.sleep(2)

    def scrape_profile(self, profile_url):
        self.driver.get(profile_url)
        time.sleep(3)

        # Scrape posts
        posts = self.driver.find_elements(By.CSS_SELECTOR, "div.post-content-selector")
        for post in posts:
            post_data = {
                "date": post.find_element(By.CSS_SELECTOR, "time").text,
                "content": post.find_element(By.CSS_SELECTOR, "p.content").text,
                "likes": int(post.find_element(By.CSS_SELECTOR, "span.likes").text),
                "comments": int(post.find_element(By.CSS_SELECTOR, "span.comments").text),
                "has_media": bool(post.find_elements(By.CSS_SELECTOR, "img, video"))
            }
            self.data_handler.store_post_data(post_data)

    def start_scraping(self):
        while True:
            profile_url = self.queue_manager.get_next_profile()
            if profile_url:
                self.scrape_profile(profile_url)
                new_profiles = self._discover_profiles()
                self.queue_manager.add_profiles(new_profiles)

    def _discover_profiles(self):
        # Logic to discover additional profile URLs (e.g., from comments, likes)
        return ["https://linkedin.com/in/new-profile1", "https://linkedin.com/in/new-profile2"]

