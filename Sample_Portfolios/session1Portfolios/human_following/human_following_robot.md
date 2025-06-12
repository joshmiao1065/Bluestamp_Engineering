# Human-Following Robot


This project detects the position of a human hand(or any IR reflecting object) relative to the car and orients itself to face the hand and move towards it. It Uses and Ultrasonic sensor to detect objects in front and a pair of IR sensors to detect objects at the side. The car was constructed from an acryllic frame, 2 motors driving a pair of wheels, and a universal wheel. An L9110S motor driver was used to couple the 2 driving motors. 

| **Engineer** | **School** | **Area of Interest** | **Grade** |
|:--:|:--:|:--:|:--:|
| Josh M| Cooper Union | Electrical Engineering | Incoming Junior |

**Replace the BlueStamp logo below with an image of yourself and your completed project. Follow the guide [here](https://tomcam.github.io/least-github-pages/adding-images-github-pages-site.html) if you need help.**

![Headstone Image](Human-Following.png)
  
# Final Milestone
**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

I only completed the base project but an example of a final milestone would be the modifications you make to the project. Checkout the modifications.md file in this repository for some suggestions!

<iframe width="474" height="843" src="https://www.youtube.com/embed/N6S5iMMxFXY" title="BlueStamp Human Following Robot Video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

For your final milestone, explain the outcome of your project. Key details to include are:
- What you've accomplished since your previous milestone
- What your biggest challenges and triumphs were at BSE
- A summary of key topics you learned about
- What you hope to learn in the future after everything you've learned at BSE



# Second Milestone

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

An example of a realistiic second milestone is successfully implementing all of the sensors and the motor driver to detect your hand and move towards it.

<iframe width="560" height="315" src="https://www.youtube.com/embed/y3VAmNlER5Y" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

For your second milestone, explain what you've worked on since your previous milestone. You can highlight:
- Technical details of what you've accomplished and how they contribute to the final goal
- What has been surprising about the project so far
- Previous challenges you faced that you overcame
- What needs to be completed before your final milestone 

# First Milestone

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

Since this is just a demo portfolio, I didn't complete any milestones but an example of a first milestone would be constructing the frame and writing some code to get the motors to move the car. However, this can be tailored to you. Embed a youtube video and fill out a description under the youtube video.

<iframe width="560" height="315" src="https://www.youtube.com/embed/CaCazFBhYKs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

For your first milestone, describe what your project is and how you plan to build it. You can include:
- An explanation about the different components of your project and how they will all integrate together
- Technical progress you've made so far
- Challenges you're facing and solving in your future milestones
- What your plan is to complete your project

# Schematics 
Here's where you'll put images of your schematics. [Tinkercad](https://www.tinkercad.com/blog/official-guide-to-tinkercad-circuits) and [Fritzing](https://fritzing.org/learning/) are both great resoruces to create professional schematic diagrams, though BSE recommends Tinkercad becuase it can be done easily and for free in the browser. 

![Headstone Image](Human-following-schematic.png)

# Code 
Here's where you'll put your code. The syntax below places it into a block of code. Follow the guide [here]([url](https://www.markdownguide.org/extended-syntax/)) to learn how to customize it to your project needs. 

```c++
const int A_1B = 5;  // Motor A backward pin (connected to L9110S IA1 or IB1)
const int A_1A = 6;  // Motor A forward pin
const int B_1B = 9;  // Motor B backward pin
const int B_1A = 10; // Motor B forward pin

const int rightIR = 7; // Right IR sensor input pin
const int leftIR = 8;  // Left IR sensor input pin

const int trigPin = 3; // Ultrasonic sensor trigger pin
const int echoPin = 4; // Ultrasonic sensor echo pin

void setup() {
  Serial.begin(9600); // Start the serial monitor at 9600 bits per second

  // Set motor pins as output so we can send signals to control them
  pinMode(A_1B, OUTPUT);
  pinMode(A_1A, OUTPUT);
  pinMode(B_1B, OUTPUT);
  pinMode(B_1A, OUTPUT);

  // Set IR sensor pins as input to receive signals from the environment
  pinMode(leftIR, INPUT);
  pinMode(rightIR, INPUT);
  
  // Set ultrasonic sensor pins
  pinMode(echoPin, INPUT);  // Echo receives reflected signal
  pinMode(trigPin, OUTPUT); // Trigger sends pulse
}

void loop() {
  // Get the distance in centimeters using the ultrasonic sensor
  float distance = readSensorData();

  // Read IR sensor values
  // LOW (0) means an object is detected; HIGH (1) means no object
  int left = digitalRead(leftIR);
  int right = digitalRead(rightIR);

  int speed = 150; // Set motor speed (0 to 255)

  // Decision logic for movement:
  if (distance > 5 && distance < 10) {
    moveForward(speed); // Move forward if there is space
  } else if (!left && right) {
    turnLeft(speed); // If left is blocked, turn left
  } else if (left && !right) {
    turnRight(speed); // If right is blocked, turn right
  } else {
    stopMove(); // If both blocked or too close, stop
  }
}

// Function to read distance using ultrasonic sensor
float readSensorData() {
  digitalWrite(trigPin, LOW); // Clear the trigger pin
  delayMicroseconds(2);       // Short delay
  digitalWrite(trigPin, HIGH); // Send out a pulse
  delayMicroseconds(10);       // Pulse duration
  digitalWrite(trigPin, LOW);  // End the pulse

  // Measure how long it takes the echo to come back
  float distance = pulseIn(echoPin, HIGH) / 58.00;
  // Convert the time into distance (cm); formula derived from speed of sound
  return distance; // Return the calculated distance
}

// Function to move forward
void moveForward(int speed) {
  analogWrite(A_1B, 0);       // Stop backward
  analogWrite(A_1A, speed);   // Move forward
  analogWrite(B_1B, speed);   // Move forward
  analogWrite(B_1A, 0);       // Stop backward
}

// Function to move backward (not used in loop but can be added)
void moveBackward(int speed) {
  analogWrite(A_1B, speed);   // Move backward
  analogWrite(A_1A, 0);       // Stop forward
  analogWrite(B_1B, 0);       // Stop forward
  analogWrite(B_1A, speed);   // Move backward
}

// Function to turn right
void turnRight(int speed) {
  analogWrite(A_1B, speed);   // Right wheel moves backward
  analogWrite(A_1A, 0);       // Stop forward
  analogWrite(B_1B, speed);   // Left wheel moves backward
  analogWrite(B_1A, 0);       // Stop forward
}

// Function to turn left
void turnLeft(int speed) {
  analogWrite(A_1B, 0);       // Stop backward
  analogWrite(A_1A, speed);   // Right wheel moves forward
  analogWrite(B_1B, 0);       // Stop backward
  analogWrite(B_1A, speed);   // Left wheel moves forward
}

// Function to stop all motor movement
void stopMove() {
  analogWrite(A_1B, 0);       // Stop all motors
  analogWrite(A_1A, 0);
  analogWrite(B_1B, 0);
  analogWrite(B_1A, 0);
}

```

# Bill of Materials
Here's where you'll list the parts in your project. To add more rows, just copy and paste the example rows below.
Don't forget to place the link of where to buy each component inside the quotation marks in the corresponding row after href =. Follow the guide [here]([url](https://www.markdownguide.org/extended-syntax/)) to learn how to customize this to your project needs. 

| **Part** | **Note** | **Price** | **Link** |
|:--:|:--:|:--:|:--:|
| Sunfounder 3-in-1 kit | Contains all items in biuld | $60 | <a href="https://www.amazon.com/SunFounder-Compatible-Tutorials-Including-Controller/dp/B0B778L1DZ/ref=sr_1_4?dib=eyJ2IjoiMSJ9.D9LrCZJnua_keVMLJz2FWndaKBvfLliNkX8pEpx-M5ocxl66rlIHHNxPx934jXYwNUopVM4uYhSLr4r6klPaljdv30IDsPEyrO7TVbLN0ac.S2vkH-CFKxogVOVkIbW92XUBWpqqOinX4PYbdsYGjcM&dib_tag=se&keywords=sunfounder+3+in+1+starter+kit&qid=1748096711&sr=8-4"> Link </a> |

# Other Resources/Examples
One of the best parts about Github is that you can view how other people set up their own work. Here are some past BSE portfolios that are awesome examples. You can view how they set up their portfolio, and you can view their index.md files to understand how they implemented different portfolio components.
- [Example 1](https://trashytuber.github.io/YimingJiaBlueStamp/)
- [Example 2](https://sviatil0.github.io/Sviatoslav_BSE/)
- [Example 3](https://arneshkumar.github.io/arneshbluestamp/)

To watch the BSE tutorial on how to create a portfolio, click <a href="https://drive.google.com/file/d/1GIGxyskToY8Ep137GnfTcfMCH4LaB6MF/view"> here </a>.
