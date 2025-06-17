# Pulse Sensor with LCD Dispaly

This project reads heart rate from a pulse sensor and outputs it to a parallel LCD. An Elegeoo Uno R3 microcontroller and the Arduino IDE were utilized. The biggest challenge was deviating from the <a href="https://drive.google.com/file/d/1GIGxyskToY8Ep137GnfTcfMCH4LaB6MF/view"> guide </a> to implement a parallel LCD isntead of a serial one. 

| **Engineer** | **School** | **Area of Interest** | **Grade** |
|:--:|:--:|:--:|:--:|
| Josh M | Cooper Union | Electrical Engineering | Incoming Junior |

![Headstone Image](Sample_Picture.png)
  
# Final Milestone

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

I only completed the base project but the final milestone should show off all the cool modifications you made to your project. I've listed some examples under the modifications-biometric.md file in this directory!

<iframe width="485" height="862" src="https://www.youtube.com/embed/lpizojFzK8A" title="Bluestamp Heart Rate Monitor" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

For your final milestone, explain the outcome of your project. Key details to include are:
- What you've accomplished since your previous milestone
- What your biggest challenges and triumphs were at BSE
- A summary of key topics you learned about
- What you hope to learn in the future after everything you've learned at BSE



# Second Milestone

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

An example of a second milestone would be completing the base project and integrating the sensor into the arduino and circuit.

<iframe width="560" height="315" src="https://www.youtube.com/embed/y3VAmNlER5Y" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

For your second milestone, explain what you've worked on since your previous milestone. You can highlight:
- Technical details of what you've accomplished and how they contribute to the final goal
- What has been surprising about the project so far
- Previous challenges you faced that you overcame
- What needs to be completed before your final milestone 

# First Milestone

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

An example of a first milestone would be demonstrating the function of the Arduino and connecting it to some components on an LED; showing off that oyu can write Arduino code and know how to build circuits on a breadbord is an example.

<iframe width="560" height="315" src="https://www.youtube.com/embed/CaCazFBhYKs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

For your first milestone, describe what your project is and how you plan to build it. You can include:
- An explanation about the different components of your project and how they will all integrate together
- Technical progress you've made so far
- Challenges you're facing and solving in your future milestones
- What your plan is to complete your project

# Schematics 
Here's where you'll put images of your schematics. [Tinkercad](https://www.tinkercad.com/blog/official-guide-to-tinkercad-circuits) and [Fritzing](https://fritzing.org/learning/) are both great resoruces to create professional schematic diagrams, though BSE recommends Tinkercad becuase it can be done easily and for free in the browser. 

# Code
Here's where you'll put your code. The syntax below places it into a block of code. Follow the guide [here]([url](https://www.markdownguide.org/extended-syntax/)) to learn how to customize it to your project needs. 
I also commented it really thoroughly for your reference if you ever get stuck.

```c++
/*
tells pulse sensor library hardware interrupts for better timing accuracy isntead of
checking only when called in the main funciton. This is to ensure no sensor inputs are missed.
You generally want to use this unless you have many sensors in which the interrupts may cause 
other sensors inputs to be missed.
*/
#define USE_ARDUINO_INTERRUPTS 
#include <PulseSensorPlayground.h>
#include <LiquidCrystal.h>

// Define LCD pins: RS, E, D4, ..., D7
LiquidCrystal lcd(12, 11, 4, 5, 6, 7);

//Global Constants
const int PULSE_SENSOR_PIN = 0; //data pin for pulse sensor
const int LED_PIN = 13; //on-board LED pin so you know that code is running
const int THRESHOLD = 550; //[nanometer] (green)light wavelength threshold for detecting a hearbeat

PulseSensorPlayground pulseSensor; //create the pulse sensor playground object to interact with the Pulse sensor hardware

void setup() {
  Serial.begin(9600); //Initialize serial monitor with baud rate of 9600
  /*
  The serial monitor is like a terminal where the arduino and your comptuer can interact. you can use it to
  print data, debug your code, or send commands
  Baud rate is the maximum bits per seocnd that can be transferred 
  9600 is the defaulted because it is almost gauranteed to be supported by all hardware and is fast enough for most tasks
  */

  //Initialize LCD
  lcd.begin(16, 2); //Our LCD has 16 rows and 2 columns to display text
  lcd.clear(); //Clear whatever might already be on the LCD screen

  //configure the pulse sensor with a few functions and passing in arguments
  
  //this declares that our variable PULSE_SENSOR_PIN will be the value of the input pin on the arduino which collects inputs from the sensor
  pulseSensor.analogInput(PULSE_SENSOR_PIN); 
  pulseSensor.blinkOnPulse(LED_PIN); //sends the information to blnik every time a heartbeat is detected to pin 13, the onboard LED
  /*Whenever your heart beats, it sends out greater amount of hemoglobin then the surrounding blood. This hemoglobin reflects light
  in a distinct and measurable way. The pulse sensor has a green LED and a light sensor. Since the hemoglobin is distributed in a way
  which matches the frequency of heart beats, the light sensor can detect these periodic differneces in the amount of light received.
  Since your heart beats periodically, this naturally creates a waveform with the same frequency as your heartbeat. We set THRESHOLD
  as the minimum wavelength threshold since more hemoglobin reflects light that is more red which as a greater wavelength so 550nm 
  is the wavelength that must be exceeded in order to count as a heartbeat since 550nm is about the wavelength of green*/
  pulseSensor.setThreshold(THRESHOLD);

//if the pulse sensor has started correctly, intilize these things
  if(pulseSensor.begin())
    {
      Serial.println("PulseSensor object created successfully!"); //prints this to serial monitor to let us know Sensor object works
      lcd.setCursor(0, 0); //move the LCD cursor position to start printing from top left corner
      lcd.print("Sensor ready!"); //print this message onto the lcd
    }

}

void loop() {
  lcd.setCursor(0,0); //constantly ensure that the LCD prints starting from the top left of the screen
  lcd.print("Heart Rate      "); //print with padding of just enough spaces so that all 16 blocks in first row are filled so BPM can print second row
  
  //get the current BPM
  int currentBPM = pulseSensor.getBeatsPerMinute();

  //print outputs to serial monitor and lcd everytime a heartbeat is detected
  if(pulseSensor.sawStartOfBeat())
    {
      Serial.print("♥ A heart beat hapened!\n");
      Serial.print("BPM: ");
      Serial.println(currentBPM);

      lcd.setCursor(0, 1);
      lcd.print("BPM: ");
      lcd.print(currentBPM);
      lcd.print("     "); // Clear residual characters
      
    }
    
  delay(20); //[ms]add a small delay to reduce CPU usage and conserve power
}
```

# Bill of Materials
Here's where you'll list the parts in your project. To add more rows, just copy and paste the example rows below.
Don't forget to place the link of where to buy each component inside the quotation marks in the corresponding row after href =. Follow the guide [here]([url](https://www.markdownguide.org/extended-syntax/)) to learn how to customize this to your project needs. 

| **Part** | **Note** | **Price** | **Link** |
|:--:|:--:|:--:|:--:|
| Electronics Kit | Contains microcontroller, breadboard, wires, and LCD | $36 | <a href="https://www.amazon.com/Arduino-A000066-ARDUINO-UNO-R3/dp/B008GRTSV6/(https://www.amazon.com/ELEGOO-Project-Tutorial-Controller-Projects/dp/B01D8KOZF4?crid=3QZ6GDFTMJ4HN&dib=eyJ2IjoiMSJ9.RFo2tGe8A0OPhXjogzb7TBCkWVNh7COJTqrATj1ouITiva_Elww5Vpbbykog0XplQnXyWferr-rSMTODScUTWifSzPnMBrxSGkdN9Wopk4Y08TA2xrZTFP8VoWqE7FtqRSVgXt8OJoF4I2jZSM0U3gRZ8KMTInt_QkJQJowCdMSZ2EshFCmejpsO07nvUG8zwaNoD6criYcDwIfLARL8iFU5TNeCtZ9YHB4oc91X1dCqR-oX_wpZw27Ea6bgpj0gK70EOX2rwhl2oJVif3r2vavQ5Kk2kcN1xinwQYmQJx8.wBY7rNjc1WHiMobJXfKksrgk5vaVGgP3N8iB4Y6omeI&dib_tag=se&keywords=electronics+kit&qid=1748097298&sprefix=electronics+ki%2Caps%2C167&sr=8-7)"> Link </a> |
| Pulse Sensor | Reads heart rate | $25 | <a href="https://www.amazon.com/Arduino-A000066-ARDUINO-UNO-R3/dp/B008GRTSV6/(https://www.amazon.com/PulseSensor-com-Original-Pulse-Sensor-project/dp/B01CPP4QM0/ref=sr_1_3?crid=3S5MU849KDR61&dib=eyJ2IjoiMSJ9.YwI7wE5G5MsEDbKg7uOr1qzORna22Tv0AThAA46aH4ocMuZhqK3dHgQLtAh9_3cFQGqwSRIvAKzW73uMA_iAl9VWqI7NEWU3um94xnt0vzIFREkb8sk9hQTlFShs3KWIH59mL7XvTwNPfUDbR94xLY1WJHK6ZHZVf0sjTdF9b0IUa_DCgd5voP0RfCC7thOJWH7whfMB4rpv1O6MB9jjBFmsTNac_m1FEEcFIJZy8W8.6dtOV92uDQes4RbzmvNATAB5MYweSRREWn6T75B7b_c&dib_tag=se&keywords=pulse+sensor+arduino&qid=1748097353&sprefix=pulse+sensor+arduino%2Caps%2C148&sr=8-3)"> Link </a> |

# Other Resources/Examples
One of the best parts about Github is that you can view how other people set up their own work. Here are some past BSE portfolios that are awesome examples. You can view how they set up their portfolio, and you can view their index.md files to understand how they implemented different portfolio components.
- <a href="https://www.ti.com/lit/ta/sszt726/sszt726.pdf?ts=1749091165452&ref_url=https%253A%252F%252Fwww.bing.com%252F"> Here </a> is a great resource explaining how the optical pulse sensor works. 
- [Example 1](https://trashytuber.github.io/YimingJiaBlueStamp/)
- [Example 2](https://sviatil0.github.io/Sviatoslav_BSE/)
- [Example 3](https://arneshkumar.github.io/arneshbluestamp/)

To watch the BSE tutorial on how to create a portfolio, click <a href="https://drive.google.com/file/d/1GIGxyskToY8Ep137GnfTcfMCH4LaB6MF/view"> here </a>.
