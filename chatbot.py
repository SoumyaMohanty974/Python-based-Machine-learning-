import network
import urequests as requests
import ujson as json
import time
from machine import Pin, SoftI2C
import ssd1306

# Define I2C pins
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# Initialize the OLED display
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Function to display scrolling text
def display_scrolling_text(text):
    text_width = len(text) * 8  # Assuming each character width is 8 pixels
    for i in range(text_width + oled_width):
        oled.fill(0)
        oled.text(text, oled_width - i, 0)
        oled.show()
        time.sleep(0.008)
        
        
def display_scrolling_text1(text):
    text_width = len(text) * 8  # Assuming each character width is 8 pixels
    # Calculate the starting position to center the text horizontally
    start_x = (oled_width - text_width) // 2
    # Calculate the starting position to center the text vertically
    start_y = (oled_height - 8) // 2  # Assuming each character height is 8 pixels
    for i in range(text_width + oled_width):
        oled.fill(0)
        # Calculate the current position of the text for scrolling effect
        current_pos = oled_width - i
        # If the current position is negative, adjust it to wrap around the display width
        if current_pos < -text_width:
            current_pos += oled_width
        # Render the text at the current position
        oled.text(text, current_pos, start_y)
        oled.show()
        time.sleep(0.001)  # Adjust scrolling speed as needed


def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.connect(ssid, password)

    while not wlan.isconnected():
        time.sleep(1)

    print("Connected to Wi-Fi")
    print("IP Address:", wlan.ifconfig()[0])

def make_api_request(prompt):
    api_key = ""  # Replace with your actual API key
    endpoint = ""
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.8,
        "max_tokens": 35,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            content = response_data["choices"][0]["message"]["content"]
            return content
        else:
            print("Error in API request:", response.status_code)
            return None
    except Exception as e:
        print("Exception:", e)
        return None

# Configure Wi-Fi credentials
wifi_ssid = "saumya’s iPhone"
wifi_password = "soumyaxx"

# Connect to Wi-Fi
connect_to_wifi(wifi_ssid, wifi_password)

# Main loop
while True:
    # Read input from Thonny IDE console
    oled.fill(0)
    a = "Ask any query?"
    oled.text(a, 0, 0)
    oled.show()
    input_text = input("Enter text to display (or 'exit' to quit): ")

    # Check if user wants to exit
    if input_text.lower() == 'exit':
        break

    # Display scrolling text
    display_scrolling_text(input_text)

    # Make API request
    response = make_api_request(input_text)
    if response:
        print("soumya's bot:", response)
        display_scrolling_text1(response)
    else:
        print("Failed to get ChatGPT response")

    # Wait for a moment before prompting again
    time.sleep(1)
