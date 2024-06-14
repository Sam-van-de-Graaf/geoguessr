from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys
import json
import argparse
import requests
import io
import shutil
import os
from PIL import Image


def read_json_file(file_path):
    """
    Parse the info from a Json file. Used for extracting log in credentials
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"An error occurred while reading the JSON file: {e}")
        return None
    
class geobot:

    def __init__(self) -> None:
        """
        driver: Chrome webdriver for the bot
        highest_file: The highest file number stored to avoid extra overhead
        driver_wait: Sets the time with no actions until the webdriver will timeout
        """
        self.highest_file = None
        opts = ChromeOptions()
        opts.add_argument("--window-size=2560,1440")
        self.driver = webdriver.Chrome(options=opts)
        self.driver_wait = WebDriverWait(self.driver, 40)
        pass

    def sign_in(self) -> None:
        """
        Starts the webdriver and logs into geoguessr
        """

        self.driver.get("https://www.geoguessr.com/signin")
        time.sleep(2)

        file_path = 'credentials.json'
        json_data = read_json_file(file_path)

        email_field = self.driver_wait.until(EC.element_to_be_clickable((By.NAME, 'email')))
        email_field.send_keys(json_data["email"])

        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys(json_data["password"])

        enter_btn = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/main/div/div/form/div/div[3]/div[1]/div/button')
        enter_btn.click()

    def start_world_game(self) -> None:
        """
        Starts a world game on geoguessr
        """
        enter_btn = self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/main/div/div[2]/div[1]/div/div[2]/div/div/div/button')))
        enter_btn.click()

        enter_btn = self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[4]/div/div/div[1]/div/div[1]/div[4]/div/div/button')))
        enter_btn.click()

    def start_new_game(self) -> None:
        """
        Starts a new world game after a previous game has ended
        """
        time.sleep(1)
        self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/main/div[2]/div/div[2]/div/div[2]/div[3]/div/div/button')))
        element = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/main/div[2]/div/div[2]/div/div[2]/div[3]/div/div/button')
        element.click()
        pass

    def resize_image(self, input_path, output_path, size):
        """
        Resize an image to the specified size and save it to a new file.

        :input_path: Path to the input image file.
        :output_path: Path to save the resized image file.
        :size: Tuple (width, height) to resize the image to.
        """
        with Image.open(input_path) as img:
            # Resize the image
            resized_img = img.resize(size)
            
            # Save the resized image
            resized_img.save(output_path)

    def screenshot_canvas(self, file_name, directory, delay) -> None:
        '''
        Take a screenshot of the streetview canvas.
        '''
        self.driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'exCVRN-size-observer-view')))
        if delay >= 0:
            time.sleep(delay)
        pano = self.driver.find_element(By.CLASS_NAME, 'exCVRN-size-observer-view')

        file_number = self.get_next_file_number(file_name, directory)
        ss_name = file_name + "_" + str(file_number) + ".png"
        pano.screenshot(ss_name)
        new_path = directory + "/" + ss_name
        os.rename("./" + ss_name, directory + "/" + ss_name)
        self.resize_image(new_path, new_path, (900, 420))


        box = (90, 0, 732, 420)
        img = Image.open(new_path)
        img2 = img.crop(box)
        img2.save(new_path)

    def take_pano(self, file_name, directory, delay) -> None:
        """
        Combines four screenshots into a panarama
        file_name: The name of the new panarama
        directory: Where the panarama will be stored
        delay: The delay necesarry to let the game load
        """
        
        self.driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "guess-map_guessButton__iZNh5")))

        screenshots = []
        time.sleep(delay)
        for i in range(4):
            self.driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'exCVRN-size-observer-view')))
            element = self.driver.find_element(By.CLASS_NAME, 'exCVRN-size-observer-view')
            file_number = self.get_next_file_number(file_name, directory)
            ss_name = file_name + "_" + str(file_number) + ".png"

            element.screenshot(ss_name)

            new_path = directory + "/" + ss_name
            os.rename("./" + ss_name, directory + "/" + ss_name)
            screenshots.append(new_path)
            self.resize_image(new_path, new_path, (900, 420))

            if i != 3:
                self.rotate_canvas_value(470)
        
        self.highest_file = None

        box = (90, 0, 732, 420)
        for i in range(len(screenshots)):
            img = Image.open(screenshots[i])
            img2 = img.crop(box)
            img2.save(screenshots[i])
        
        width = box[2] - box[0]
        height = box[3] - box[1]
        new_image = Image.new('RGB',(4 * width, height))
        pano_name = screenshots[0]

        for i in range(4):
            image = screenshots[i]
            add_image = Image.open(image)
            new_image.paste(add_image, (i * width, 0))
            os.remove(image)

        new_image.save(pano_name)
        pass

    def rotate_canvas_value(self, rotation) -> None:
        '''
        Drag and click the <main> elem a few times to rotate us ~90 degrees.
        '''
        self.driver_wait.until(EC.presence_of_element_located((By.TAG_NAME, 'main')))
        main = self.driver.find_element(By.TAG_NAME, 'main')
        # for _ in range(0, 5):
        action = webdriver.common.action_chains.ActionChains(self.driver)
        action.move_to_element(main) \
            .click_and_hold(main) \
            .move_by_offset(rotation, 0) \
            .release(main) \
            .perform()
        action.move_to_element(main) \
            .click_and_hold(main) \
            .move_by_offset(rotation, 0) \
            .release(main) \
            .perform()

    def get_next_file_number(self, file_name, directory):
        """
        Finds the next available file number
        """

        if self.highest_file != None:
            self.highest_file += 1
            return self.highest_file
        else:
            for i in range(1000000):
                if not os.path.isfile(directory + "/" + file_name + "_" + str(i) + ".png"):
                    self.highest_file = i
                    return self.highest_file
        pass


    def rotate_canvas(self) -> None:
        '''
        Drag and click the <main> elem a few times to rotate us ~90 degrees.
        '''
        self.driver_wait.until(EC.presence_of_element_located((By.TAG_NAME, 'main')))
        main = self.driver.find_element(By.TAG_NAME, 'main')
        # for _ in range(0, 5):
        action = webdriver.common.action_chains.ActionChains(self.driver)
        action.move_to_element(main) \
            .click_and_hold(main) \
            .move_by_offset(400, 0) \
            .release(main) \
            .perform()
        action.move_to_element(main) \
            .click_and_hold(main) \
            .move_by_offset(400, 0) \
            .release(main) \
            .perform()
    
    def retrieve_game_data(self, game_code):
        """
        Retrieves the coordinates and contry for the specified game_code
        """

        game_link = "https://www.geoguessr.com/api/v3/games/" + game_code

        response = requests.get(game_link)
        data = io.StringIO(response.content.decode('utf-8')).readlines()

        data = [x.split("]") for x in data[0].split("[")]
        round_data = data[1][0].split("}", maxsplit=4)
            
        for ind, x in enumerate(round_data):
            x = x.split(",")
            if x[0] == '':
                x.pop(0)
            x = x[0] + ", " + x[1] + ", " + x[6] + "}"
            round_data[ind] = x
            map = eval(x)
        
        return(round_data)
    
    def write_game_data(self, game_code, num_screenshots, file_path):

        data = self.retrieve_game_data(game_code)

        try:
            with open(file_path, 'a') as file:
                for text in data:
                    for _ in range(num_screenshots):
                        file.write(text + '\n')
        except Exception as e:
            print(f"An error occurred: {e}")

        
    def get_game_code(self):
        time.sleep(1)
        code = self.driver.current_url.split("/")[-1]
        return code
    
    def make_guess(self):
        """
        Makes a prediction in the current geoguessr game
        """
        # time.sleep(1)
        self.driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "guess-map_canvas__cvpqv")))
        element = self.driver.find_element(By.CLASS_NAME, "guess-map_canvas__cvpqv")
        element.click()

        # time.sleep(1)
        self.driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "guess-map_guessButton__iZNh5")))
        element = self.driver.find_element(By.CLASS_NAME, "guess-map_guessButton__iZNh5")
        element.click()
        pass

    def exit_score_page(self) -> None:

        time.sleep(1)
        self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/main/div[2]/div/div[2]/div/div[2]/div[2]/div/button')))
        element = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/main/div[2]/div/div[2]/div/div[2]/div[2]/div/button')
        element.click()

    def collect_data(self, num_rounds) -> None:
        """
        Collects three screenshots from each location and saves the data

        This method is no longer necessary
        """

        self.sign_in()
        self.start_world_game()
        num_screenshots = 3
        
        for _ in range(num_rounds):
            for _ in range(5):
                for i in range(num_screenshots):
                    if i == 0:
                        self.screenshot_canvas("train", "./training_data/x_data", 2)
                    else:
                        self.screenshot_canvas("train", "./training_data/x_data", 0)
                    if (i != num_screenshots - 1):
                        self.rotate_canvas()
                self.make_guess()
                self.exit_score_page()
            game_code = self.get_game_code()
            self.write_game_data(game_code, num_screenshots, "./training_data/y_data/y_data.txt")
            self.start_new_game()
        
        time.sleep(10)

    def collect_data_pano(self, num_rounds) -> None:
        """
        Collects panoramas for the number of rounds specified
        """

        self.sign_in()
        self.start_world_game()
        num_screenshots = 1
        
        for _ in range(num_rounds):
            for _ in range(5):
                self.take_pano("train", "./training_data/x_data", 2)
                self.make_guess()
                self.exit_score_page()
            game_code = self.get_game_code()
            self.write_game_data(game_code, num_screenshots, "./training_data/y_data/y_data.txt")
            self.start_new_game()
        
        time.sleep(10)

if __name__ == "__main__":
    
    start_time = time.time()

    bot = geobot()
    bot.collect_data_pano(3)

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
    
    time.sleep(20)
    