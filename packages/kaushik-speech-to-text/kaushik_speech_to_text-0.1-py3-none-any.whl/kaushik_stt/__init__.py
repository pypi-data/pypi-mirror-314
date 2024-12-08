import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from os import getcwd, path

# Initialize the recognizer
recognizer = sr.Recognizer()

# Set Chrome options (optional, if you still need to run it in the background)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")

# Initialize WebDriver (This will open Chrome, but you won't interact with it visually)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Set file paths for the HTML page (optional if you need to interact with HTML)
index_path = path.join(getcwd(), 'index.html')  # Get the path first
formatted_index_path = index_path.replace('\\', '/')  # Replace backslashes with forward slashes
website = f"file:///{formatted_index_path}"  # Now that the path is cleaned up, use it in the f-string

# Open the website (optional if you want to interact with HTML)
driver.get(website)
print("Website opened in background browser.")

# Speech recognition function for continuous listening
def listen_continuously():
    print("Starting continuous listening... Say 'stop' to stop listening.")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)  # Adjusts to ambient noise levels
                print("Listening for speech...")
                audio = recognizer.listen(source)  # Wait for speech input
                print("Recognizing speech...")
                text = recognizer.recognize_google(audio)  # Recognize speech using Google's API
                print(f"User said: {text}")

                # Check if the word "stop" is in the recognized speech
                if "stop" in text.lower():
                    print("Stopping speech recognition...")
                    break  # Stop the loop when "stop" is said
        
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
        except KeyboardInterrupt:
            print("\nProgram stopped by user.")
            break  # Break the loop if the user presses Ctrl+C
        except Exception as e:
            print(f"Error occurred: {e}")

# Run the continuous listening function
listen_continuously()

# Close the browser after speech recognition (optional)
driver.quit()
