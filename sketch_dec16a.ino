#include <WiFi.h>
#include <Wire.h>

#include <Adafruit_SSD1306.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char *ssid = "saumya’s iPhone";
const char *password = "Soumyaxx";
const String api_key = "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";

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

String makeApiRequest(String prompt);

void setup() {
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }

  Serial.begin(115200);
  connectToWiFi();
}

void loop() {
  // Display prompt on OLED
  displayMessage("Ask your question ?", "");

  // Check for user input via Serial
  String question = Serial.readStringUntil('\n');

  // If a question is entered, proceed
  if (!question.isEmpty()) {
    Serial.println("Received question: " + question);

    // Display the question on the OLED screen
    displayMessage("Your Question:", question);

    // Send question to ChatGPT API
    String apiResponse = makeApiRequest(question);\/

    // Handle the API response as needed
    // You may want to parse and display the response on the OLED screen

    delay(1000); // Adjust delay as needed
  }

  // Add any additional logic or functionality here

  delay(100);
}

void connectToWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void displayMessage(const String &header, const String &message) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println(header);
  display.println(message);
  display.display();
}

String makeApiRequest(String prompt) {
  HTTPClient http;
  http.setTimeout(24000); // Set a longer timeout (in milliseconds)
  http.begin("https://api.openai.com/v1/chat/completions");

  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", "Bearer " + String(api_key));

  StaticJsonDocument<1024> jsonPayload;
  jsonPayload["model"] = "gpt-3.5-turbo";
  jsonPayload["temperature"] = 0.8;
  jsonPayload["max_tokens"] = 35;

  JsonArray messages = jsonPayload.createNestedArray("messages");
  JsonObject userMessage = messages.createNestedObject();
  userMessage["role"] = "user";
  userMessage["content"] = prompt;

  String payloadString;
  serializeJson(jsonPayload, payloadString);

  int httpResponseCode = http.POST(payloadString);

  if (httpResponseCode == HTTP_CODE_OK) {
    // Handle the response, if needed
    String response = http.getString();
    Serial.println("API Response: " + response);
    
    DynamicJsonDocument jsonDoc(1024);
    DeserializationError error = deserializeJson(jsonDoc, response);

    if (error) {
      Serial.println("Error parsing JSON: " + String(error.c_str()));
    } else {
      // Extract the content from the first choice
      String content = jsonDoc["choices"][0]["message"]["content"];

      displayMessage("ChatGPT Response:", content);
    }
    delay(15000);
  } else {
    Serial.println("Error in API request");
    Serial.println(httpResponseCode);

  }

  http.end();

  return payloadString; // You can modify this as needed
}
