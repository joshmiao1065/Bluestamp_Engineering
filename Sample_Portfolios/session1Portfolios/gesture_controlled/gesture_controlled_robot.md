# Gesture-Controlled Robot

This project features a car robot that can be controlled by gestures on a glove. An accelerometer detects changes in speed (and directioln) of the glove component which corrresponds to different movement functions on the car. A pair of HC05 bluetooth modules communicicates instructions and feedback between the car and glove. An UNOR3 microcontroller controls the car's logic while an Arduino Micro controls the glove's logic. 

You should comment out all portions of your portfolio that you have not completed yet, as well as any instructions:
```HTML 
<!--- This is an HTML comment in Markdown -->
<!--- Anything between these symbols will not render on the published site -->
```

| **Engineer** | **School** | **Area of Interest** | **Grade** |
|:--:|:--:|:--:|:--:|
| Josh M | Cooepr Union | Electrical Engineering | Incoming Junior |

**Replace the BlueStamp logo below with an image of yourself and your completed project. Follow the guide [here](https://tomcam.github.io/least-github-pages/adding-images-github-pages-site.html) if you need help.**

![Headstone Image](gesture-controlled-robot.png)
  
# Final Milestone

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

I only completed the base project but the final milestone should include all of the awesome modifications you made! I've attached some mod ideas in the modification.md file in this directory!

<iframe width="560" height="315" src="https://www.youtube.com/embed/F7M7imOVGug" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

For your final milestone, explain the outcome of your project. Key details to include are:
- What you've accomplished since your previous milestone
- What your biggest challenges and triumphs were at BSE
- A summary of key topics you learned about
- What you hope to learn in the future after everything you've learned at BSE



# Second Milestone

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

An example of a second milestone is completing the base project and demonstrating the function and integration of all the components with the accelerometer, the bluetooth module, and the computer science concepts used to integrate them!

<iframe width="560" height="315" src="https://www.youtube.com/embed/y3VAmNlER5Y" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

For your second milestone, explain what you've worked on since your previous milestone. You can highlight:
- Technical details of what you've accomplished and how they contribute to the final goal
- What has been surprising about the project so far
- Previous challenges you faced that you overcame
- What needs to be completed before your final milestone 

# First Milestone

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

A good example of a first milestone is the completion of the frame of the car, deciding how you should mount what components(microcontroller,motor drivers, sensors, etc.) and where. You should also have integrated the motors and be able to drive the car with your arduino code, maybe integrate a sensor or two.

<iframe width="560" height="315" src="https://www.youtube.com/embed/CaCazFBhYKs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

For your first milestone, describe what your project is and how you plan to build it. You can include:
- An explanation about the different components of your project and how they will all integrate together
- Technical progress you've made so far
- Challenges you're facing and solving in your future milestones
- What your plan is to complete your project

# Schematics 
Here's where you'll put images of your schematics. [Tinkercad](https://www.tinkercad.com/blog/official-guide-to-tinkercad-circuits) and [Fritzing](https://fritzing.org/learning/) are both great resoruces to create professional schematic diagrams, though BSE recommends Tinkercad becuase it can be done easily and for free in the browser. 

Here's a sample schematic that uses an L298 motor driver instead of an L9110S:
![Headstone Image](gesture-controlled-robot-schematic.png)


# Code
Here's where you'll put your code. The syntax below places it into a block of code. Follow the guide [here]([url](https://www.markdownguide.org/extended-syntax/)) to learn how to customize it to your project needs. 

Here is the code for the hand module to control the robot:
```c++
#include <SoftwareSerial.h> // Include the SoftwareSerial library to use other digital pins for serial communication
SoftwareSerial BT_Serial(2, 3); // Create a Bluetooth serial connection on pins 2 (RX) and 3 (TX)

#include <Wire.h> // Include the Wire library for I2C communication

const int MPU = 0x68; // I2C address of the MPU6050 accelerometer/gyroscope module
int16_t AcX, AcY, AcZ; // Variables to hold raw accelerometer data for X, Y, and Z axes

int flag = 0; // A flag to prevent sending repeated commands

void setup() {
  Serial.begin(9600); // Start serial communication with the computer for debugging at 9600 baud

  // Initialize I2C communication with the MPU6050
  Wire.begin(); // Start I2C communication
  Wire.beginTransmission(MPU); // Begin talking to the MPU6050 at its I2C address
  Wire.write(0x6B); // Access the power management register
  Wire.write(0);    // Write 0 to wake up the MPU6050 (it starts in sleep mode)
  Wire.endTransmission(true); // Complete the transmission and release the I2C bus

  delay(500); // Give the MPU time to initialize
}

void loop() {
  Read_accelerometer(); // Call the function to read accelerometer values

  // If the device is tilted forward and no command has been sent yet
  if ((AcX < 60) && (flag == 0)) {
    flag = 1; // Set the flag so we don't send another command right away
    BT_Serial.write('f'); // Send the character 'f' to the Bluetooth device (usually means "forward")
  }

  // If the device is tilted backward and no command has been sent yet
  if ((AcX > 130) && (flag == 0)) {
    flag = 1; // Set the flag to prevent repeats
    BT_Serial.write('b'); // Send the character 'b' to the Bluetooth device (usually means "backward")
  }

  delay(100); // Wait 100 milliseconds before looping again
}

void Read_accelerometer() {
  // Tell the MPU we want to start reading from register 0x38 (which is not correct; it should be 0x3B for ACCEL_XOUT_H)
  Wire.beginTransmission(MPU);
  Wire.write(0x3B); // Starting register for accelerometer data (this line should actually use 0x3B for correct data)
  Wire.endTransmission(false); // End the transmission but keep connection open to request data
  Wire.requestFrom(MPU, 6, true); // Ask for 6 bytes of data (2 bytes each for X, Y, and Z axes)

  // Read high and low bytes for each axis and combine them into one 16-bit number
  AcX = Wire.read() << 8 | Wire.read(); // Combine high and low byte for X-axis
  AcY = Wire.read() << 8 | Wire.read(); // Combine high and low byte for Y-axis
  AcZ = Wire.read() << 8 | Wire.read(); // Combine high and low byte for Z-axis

  // Map raw accelerometer values from the range -17000 to 17000 into 0 to 180 degrees (approximate)
  AcX = map(AcX, -17000, 17000, 0, 180);
  AcY = map(AcY, -17000, 17000, 0, 180);
  AcZ = map(AcZ, -17000, 17000, 0, 180);

  // Print the mapped values to the Serial Monitor for debugging
  Serial.print(AcX);
  Serial.print("\t");
  Serial.print(AcY);
  Serial.print("\t");
  Serial.println(AcZ); 
}
```
Here is the code for the robot component;
``` c++
#include <SoftwareSerial.h> // Include the SoftwareSerial library to allow serial communication on digital pins
SoftwareSerial BT_Serial(2, 3); // Create a software serial port on pins 2 (RX) and 3 (TX) for Bluetooth communication

/*
L9110S motor driver setup:
Motor A (right motor): controlled using pins in1 and in2
Motor B (left motor): controlled using pins in3 and in4
*/

#define in1 9 // Set pin 9 as in1, which controls the right motor forward direction
#define in2 8 // Set pin 8 as in2, which controls the right motor backward direction
#define in3 7 // Set pin 7 as in3, which controls the left motor backward direction
#define in4 6 // Set pin 6 as in4, which controls the left motor forward direction

char bt_data; // Variable to store a single character received from the Bluetooth module
int Speed = 150; // Speed of the motors, from 0 (stopped) to 255 (full speed)

void setup() {
  Serial.begin(9600); // Start communication with the Serial Monitor at 9600 baud rate
  BT_Serial.begin(9600); // Start communication with the Bluetooth module at 9600 baud rate

  pinMode(in1, OUTPUT); // Set pin in1 as an output to control motor direction
  pinMode(in2, OUTPUT); // Set pin in2 as an output to control motor direction
  pinMode(in3, OUTPUT); // Set pin in3 as an output to control motor direction
  pinMode(in4, OUTPUT); // Set pin in4 as an output to control motor direction

  delay(200); // Wait 200 milliseconds to let everything initialize
}

void loop() {
  // Check if data has been received from the Bluetooth module
  if (BT_Serial.available() > 0) {
    bt_data = BT_Serial.read(); // Read the incoming character and store it in bt_data
    Serial.println(bt_data); // Print the received character to the Serial Monitor
  }

  // If the received character is 'f', move forward
  if (bt_data == 'f') {
    forward(); // Call the forward function
    Speed = 180; // Set motor speed to 180
  }
  // If the received character is 'b', move backward
  else if (bt_data == 'b') {
    backward(); // Call the backward function
    Speed = 180; // Set motor speed to 180
  }
  // If the received character is 'l', turn left
  else if (bt_data == 'l') {
    turnLeft(); // Call the turnLeft function
    Speed = 250; // Set motor speed to 250
  }
  // If the received character is 'r', turn right
  else if (bt_data == 'r') {
    turnRight(); // Call the turnRight function
    Speed = 250; // Set motor speed to 250
  }
  // If the received character is 's', stop all motors
  else if (bt_data == 's') {
    Stop(); // Call the Stop function
    Speed = 0; // Set speed to 0
  }
}

// Function to move the robot forward
void forward() {
  analogWrite(in1, Speed); // Right motor forward
  analogWrite(in2, 0);     // Right motor not moving backward
  analogWrite(in3, 0);     // Left motor not moving backward
  analogWrite(in4, Speed); // Left motor forward
}

// Function to move the robot backward
void backward() {
  analogWrite(in1, 0);     // Right motor not moving forward
  analogWrite(in2, Speed); // Right motor backward
  analogWrite(in3, Speed); // Left motor backward
  analogWrite(in4, 0);     // Left motor not moving forward
}

// Function to turn the robot to the right
void turnRight() {
  analogWrite(in1, 0);     // Right motor stopped
  analogWrite(in2, Speed); // Right motor backward
  analogWrite(in3, 0);     // Left motor stopped
  analogWrite(in4, Speed); // Left motor forward
}

// Function to turn the robot to the left
void turnLeft() {
  analogWrite(in1, Speed); // Right motor forward
  analogWrite(in2, 0);     // Right motor not moving backward
  analogWrite(in3, Speed); // Left motor backward
  analogWrite(in4, 0);     // Left motor not moving forward
}

// Function to stop all motors
void Stop() {
  analogWrite(in1, 0); // Right motor off
  analogWrite(in2, 0); // Right motor off
  analogWrite(in3, 0); // Left motor off
  analogWrite(in4, 0); // Left motor off
}

```


# Bill of Materials
Here's where you'll list the parts in your project. To add more rows, just copy and paste the example rows below.
Don't forget to place the link of where to buy each component inside the quotation marks in the corresponding row after href =. Follow the guide [here]([url](https://www.markdownguide.org/extended-syntax/)) to learn how to customize this to your project needs. 

| **Part** | **Note** | **Price** | **Link** |
|:--:|:--:|:--:|:--:|
| Car chassis | frame to hold components of car | $21.29 | <a href="https://www.amazon.com/perseids-Chassis-Encoder-Wheels-Battery/dp/B07DNXBFQN/ref=sr_1_10?crid=26TUUFVPI4E3P&dib=eyJ2IjoiMSJ9.b6A_uqlNY7c_XNSLuXfmFx3lnf3nSeLGG7KgC7ZRfC9FAK22FT6M83V1dTBEAvnkHgRE0NNpo0oADYqyV4P2HpY5BFGlLS5OXcRD4aEW4oZsKRGeNyx6VCcRs7hoENdwnlQ8hLuKGPpRNYNJns2n3xydphLJvzrAHjoARmRiwPmFpghbM1R-1qsX5oLcwUgeikl74r8tSpjraJ1ymDeFdq6Kf9PpSFMZnd112Ga4ex0Q4MCaQT605Nzcs1spfnEG27m1GZgqWH8y7CDjJa2srdlHjoSkiJWC8MTTn3ug0Zg.7oE32LVlD_UTGvu8buwQxem0Dpe5zyabMMu1Q39WiQs&dib_tag=se&keywords=robot%2Bchassis&qid=1715357415&s=toys-and-games&sprefix=robot%2Bchassi%2Ctoys-and-games%2C95&sr=1-10&th=1&qty=1&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D"> Link </a> |
| Screwdriver Kit | Screwdriver with bits to fasten components onto chassis | $5.94 | <a href="https://www.amazon.com/Small-Screwdriver-Set-Mini-Magnetic/dp/B08RYXKJW9/"> Link </a> |
| L9110S motor drivers | Couple the pairs of motors | $5.99 | <a href="https://www.amazon.com/Ferwooh-Stepper-Controller-2-5-12V-H-Bridge/dp/B0D17PJ2MS/ref=sr_1_1?crid=2OQ7UJ1VJLUHU&dib=eyJ2IjoiMSJ9.xPgxMG6cmxZRuRbSqT3QxSr9zBhiCzp3WpnCeGbZjJfW2wU1eHonQ9Yw7yZi2k6Q3PhHd4uR1wLLWBETfHe0SF_wYRGvOug585fW0fsZTX6ImNTMLCJR3VH7MrRlnR7uQ5g0XrAXnzyVOSTEAmuNKyuiUk_vhsIuCNv1HCMrPUyPtn7qKFCwz7vVMcvEXx5Ddy4TPQJlpbS_voU9at8F85yJM5O9Hp5bbg_xuIHUsuE2ePCbv4lATgHmgHzENtlSRiU4laurwSqTAEgEnv9gNIbmb5d2HT5qBLfNChqSyio.9Fh1mUFHx48E8QZCOAX5T2ZJxzbHHdu93PJ63MLUqpM&dib_tag=se&keywords=L9110S+DC&qid=1716940953&s=electronics&sprefix=l9110s+dc%2Celectronics%2C89&sr=1-1"> Link </a> |
| Elegeoo Uno R3 | Logic control for robot component | $14.98 | <a href="https://www.amazon.com/ELEGOO-Board-ATmega328P-ATMEGA16U2-Compliant/dp/B01EWOE0UU/ref=sr_1_2_sspa?crid=3A6NCD2X9JEMJ&dib=eyJ2IjoiMSJ9.AcWZy-Yg4mDTnhzEHozxzPZdVC5-KUL2tW-OQewDKpBB4brSpD-p4bn74WcXiW3KarYertgpNaLJ0VHKx0qsPqolKAhiz1GRG5BwJQl73cEvrlXIXNmqlpSvU7uu2aRVSwAZi9Gj2AjSPLM3esW1Gzy9xEiQ9oiR5LCNjh4MlYDx5mTm5sI4rsD4CFTipJnF572qXlickl35FRcCj8oMXQotumgqI4yEIq0HobOtIlEnNhtVB51JMBHhqtmmF_PC9WeHJ4ySUVVcv_gq3_VeG1aAEbdm4NXmmT6NOYPw4Qo.1PFdgFT22oqO5Mg6-6j_aUL_EV8tUPuaFrB5N9oaEX0&dib_tag=se&keywords=elegoo+arduino&qid=1716856465&s=electronics&sprefix=elegoo+arduino%2Celectronics%2C99&sr=1-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"> Link </a> |
| Motors | Drive the movement of the car | $11.98 | <a href="https://www.amazon.com/AEDIKO-Motor-Gearbox-200RPM-Ratio/dp/B09N6NXP4H/ref=sr_1_4?crid=1JP29NIWBLH2M&dib=eyJ2IjoiMSJ9.Wq3jKgOLbqtEP772vMD4pV5f-w3PLBdEpKqguykXOb0JFO14f4Dq0m_VDVUMUFtR8WFINUEticI3GXcoGqwXPqK9yIh04PhCktgccMz9zAUiKXMJPwmOTUp_6av3XuFD0lXo9WngN9iKI6YgZrhEEs9qnqbcB1GnvgntCdKz8Q1dFuNu61NgSE6Z8vBk3FRpaNcr1lCI7FApTiNi0Qce8gbfmMn6oUggZQHpIOKKZ6s.M7WsZ_ZZtm3rm93kKgw0NOxt1McVBYX6m55oGxu1xxI&dib_tag=se&keywords=dc+motor+with+gearbox&qid=1715911706&sprefix=dc+motor+with+gearbox%2Caps%2C126&sr=8-4"> Link </a> |
| Electronics kit | Additional sensors and wiring components | $14 | <a href="https://www.amazon.com/Smraza-Electronics-Potentiometer-tie-Points-Breadboard/dp/B0B62RL725/ref=sxts_b2b_sx_reorder_acb_business?content-id=amzn1.sym.f63a3b0b-3a29-4a8e-8430-073528fe007f%3Aamzn1.sym.f63a3b0b-3a29-4a8e-8430-073528fe007f&crid=2IC3T44H3U3WG&cv_ct_cx=breadboard+kit&dib=eyJ2IjoiMSJ9.TUd5tu2T8rmms7ZuJ0UzmbtpLL1zsu93bQM0PzwnP4E.sT0V0vL_QtbYv8ymVTCcRkhFNgBtRvRiT7G4FT1oGTE&dib_tag=se&keywords=breadboard+kit&pd_rd_i=B0B62RL725&pd_rd_r=67e1f4ff-e3b9-44e4-b441-b4ae282f036b&pd_rd_w=UjFaP&pd_rd_wg=0xRoC&pf_rd_p=f63a3b0b-3a29-4a8e-8430-073528fe007f&pf_rd_r=BFGP77H27ZN31W4PZAW6&qid=1715911733&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=breadboard+kit%2Caps%2C109&sr=1-2-9f062ed5-8905-4cb9-ad7c-6ce62808241a"> Link </a> |
| Breadboard Kit | Additional breadboards to connect component | $8.79 | <a href="https://www.amazon.com/Breadboards-Solderless-Breadboard-Distribution-Connecting/dp/B07DL13RZH/ref=sxts_b2b_sx_reorder_acb_business?content-id=amzn1.sym.f63a3b0b-3a29-4a8e-8430-073528fe007f%3Aamzn1.sym.f63a3b0b-3a29-4a8e-8430-073528fe007f&crid=1RAL6PA1TZ81Q&cv_ct_cx=breadboard+kit&dib=eyJ2IjoiMSJ9.TUd5tu2T8rmms7ZuJ0UzmbtpLL1zsu93bQM0PzwnP4E.sT0V0vL_QtbYv8ymVTCcRkhFNgBtRvRiT7G4FT1oGTE&dib_tag=se&keywords=breadboard+kit&pd_rd_i=B07DL13RZH&pd_rd_r=1e3e6f57-5578-4452-b230-90d43c79b5d3&pd_rd_w=rFN6B&pd_rd_wg=3mMuA&pf_rd_p=f63a3b0b-3a29-4a8e-8430-073528fe007f&pf_rd_r=JC9D7T4VYRDQ9HJVY5X8&qid=1715912837&s=electronics&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=breadboard+kit%2Celectronics%2C102&sr=1-1-9f062ed5-8905-4cb9-ad7c-6ce62808241a"> Link </a> |
| Arduino Micro | Logic control for the hand component | $20 | <a href="https://www.amazon.com/Arduino-Micro-Headers-A000053-Controller/dp/B00AFY2S56/ref=sxts_b2b_sx_reorder_acb_business?content-id=amzn1.sym.44ecadb3-1930-4ae5-8e7f-c0670e7d86ce%3Aamzn1.sym.44ecadb3-1930-4ae5-8e7f-c0670e7d86ce&cv_ct_cx=arduino%2Bmicro&keywords=arduino%2Bmicro&pd_rd_i=B00AFY2S56&pd_rd_r=3c265d26-c144-45b4-b645-a19f57187069&pd_rd_w=ZWCox&pd_rd_wg=dgTyS&pf_rd_p=44ecadb3-1930-4ae5-8e7f-c0670e7d86ce&pf_rd_r=SRN3W01Y55A8M3VF2PXJ&qid=1686186926&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sr=1-1-62d64017-76a9-4f2a-8002-d7ec97456eea&th=1"> Link </a> |
| Micro USB cable | Upload code to the microcontrollers | $5 | <a href="https://www.amazon.com/Charging-Transfer-Android-Trustable-MYFON/dp/B098DW7485/ref=sr_1_6?crid=3USJU0DMSZB2S&keywords=micro+usb&qid=1686187078&s=electronics&sprefix=micro+usb%2Celectronics%2C106&sr=1-6"> Link </a> |
| Accelerometer | Detects acceleration(gestures) of hand component  | $9 | <a href="https://www.amazon.com/Pre-Soldered-Accelerometer-Raspberry-Compatible-Arduino/dp/B0BMY15TC4/ref=sr_1_5?crid=8EDYBVQQY7E2&dib=eyJ2IjoiMSJ9.ID40hq0zMYWtG7Um61yZ63xnujgA2opJZN4n7Ear4a7PVz0kChoZQvMielgIQHXUTy4_yuQvwgK7S5aC7H8U6s5ChRMOd0Iba7IZDg_ySpKnO5uemH-09l_GS1vcaiACgMnHA4JltsdzdfsSBwKgUFAhFhLuvIKnY6G3lrVGfynAdqGHpq4kg53C83MmKTRP8583zcZvMNE8N9pGZr9m2_ctic429UEwmpvof0hrhug.bBXCol9-0Y3cd8LQBcW01jRrDORIYOXF6HAJOn6LUjY&dib_tag=se&keywords=accelerometer+arduino&qid=1715912788&sprefix=accelerometer+arduino%2Caps%2C110&sr=8-5"> Link </a> |
| HC05 Bluetooth module | Connect the microcontrolelrs between hand and robot | $9 | <a href="https://www.amazon.com/DSD-TECH-HC-05-Pass-through-Communication/dp/B01G9KSAF6/ref=sr_1_3?crid=2J833J7AYQJA&keywords=hc05&qid=1686187263&sprefix=hc0%2Caps%2C112&sr=8-3"> Link </a> |
| Breadboard power supply | Enables a 9V alkaline battery to power breadboard | $8 | <a href="https://www.amazon.com/ALAMSCN-Solderless-Breadboard-Battery-Arduino/dp/B08JYPMCZY/ref=sxts_b2b_sx_reorder_acb_business?content-id=amzn1.sym.f63a3b0b-3a29-4a8e-8430-073528fe007f%3Aamzn1.sym.f63a3b0b-3a29-4a8e-8430-073528fe007f&crid=Z2S8NZU0KN1S&cv_ct_cx=breadboard+power+supply&dib=eyJ2IjoiMSJ9.nJ_euybTOUu9E6yyDpnEqg.NgztCYPGkG96eXyyFxpvxOVw5ykdTUq6oziUQnvf51E&dib_tag=se&keywords=breadboard+power+supply&pd_rd_i=B08JYPMCZY&pd_rd_r=f2beb6df-6d77-44a3-8b72-83255f19ca20&pd_rd_w=r1wmq&pd_rd_wg=ToFNq&pf_rd_p=f63a3b0b-3a29-4a8e-8430-073528fe007f&pf_rd_r=R5ZMMGW4CXRBP3PWAYMA&qid=1715912515&s=electronics&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=breadboard+power+s%2Celectronics%2C114&sr=1-1-9f062ed5-8905-4cb9-ad7c-6ce62808241a"> Link </a> |
| 9V batteries | Supply power to components | $8.69 | <a href="https://www.amazon.com/Amazon-Basics-Performance-All-Purpose-Batteries/dp/B00MH4QM1S/ref=sr_1_5_pp?crid=3TQ7ANPH958JM&dib=eyJ2IjoiMSJ9.bmcV2Upj_vpB6G9CFlPPxYAryat512da7ekZjc52HecXSTmtx7PbJ50EgQFPCMqlAxjOUq-tL4vQTpozlHvH89bMwx-HJoyGcdz6EY8HrMxahTiqOXkoP7ewkDcgHoMhmHamdlQfW6FBHO0Gm-DYZZnnMuvEU3qOpemA8PGEvRhEx4-lGaBZhrvls039G1-9SizAW-YRGXZ2fFrdVDlREyyOhAuxXZaE5QqUxWesRQgP9UfGOYaInRWTTPwhDbXFa-RPzGbU1C_u4wq-NMqKBtWEQqR9-cA8O3FYOx3icEY.dtKJmI2T-iCmMM_bYnbiHUWzhKpJDRxS-bBmZIwYFKM&dib_tag=se&keywords=9v+batteries&qid=1720651326&rdc=1&s=electronics&sprefix=9v+batteries%2Celectronics%2C105&sr=1-5"> Link </a> |
| Velcro tape | attach components to hand component | $8 | <a href="https://www.amazon.com/Art3d-Sticky-Double-Sided-Command-Adhesive/dp/B0B58FGF8H/ref=sr_1_1_sspa?crid=2N0JOMEZLJ2DS&dib=eyJ2IjoiMSJ9.qGUGB_MXfmbL0MW7bqNJbxvZC9pzliDJ9KYyRNNrctnh03kCcUXONRrcPYdGeo7Jwzrm83HyF8Jsb1RkcdlLPAw-8RkxbTCMiW6UI1Fpnjv9GjXUg9VBOLxmLVUbmMp5J7gFXKKLTWQ-w_L4Q9rykEUqKmjv-v6GRykMMZLY2cVt__lLxMIlwr6qBnQLWpHiklifUJwjiURxO--TTt2VReYgmN0z7118ifSucrkvRrg.mwA0L4zMSlJP2RO8IBba7dVqwa1Lkr8KvY1JmeQEfCg&dib_tag=se&keywords=velcro+tape+pieces&qid=1716734034&sprefix=velcro+tape+piece%2Caps%2C89&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"> Link </a> |
| Digital multimeter | debugging tool | $11 | <a href="https://www.amazon.com/AstroAI-Digital-Multimeter-Voltage-Tester/dp/B01ISAMUA6/ref=sxin_17_pa_sp_search_thematic_sspa?content-id=amzn1.sym.e8da13fc-7baf-46c3-926a-e7e8f63a520b%3Aamzn1.sym.e8da13fc-7baf-46c3-926a-e7e8f63a520b&cv_ct_cx=digital+multimeter&dib=eyJ2IjoiMSJ9.5LQumrfBR8l0mKnJCJlRg73dxpou0gqYD_ffU3srgs0Utegwth8GcQCSVXVzeZeLSJx5J3itz5TLdmJHsrVITQ.-00jRPoT-bBy26YC4LzQ-S4cYdztgmSMGb83_WEm6HY&dib_tag=se&keywords=digital+multimeter&pd_rd_i=B01ISAMUA6&pd_rd_r=e1ff2570-7e4a-4906-bc55-6f819d48d1bc&pd_rd_w=h7HgL&pd_rd_wg=0ZcFH&pf_rd_p=e8da13fc-7baf-46c3-926a-e7e8f63a520b&pf_rd_r=R6YKX3NXTDQ1PQP4H8RM&qid=1715911879&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sr=1-1-7efdef4d-9875-47e1-927f-8c2c1c47ed49-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM&psc=1"> Link </a> |

# Other Resources/Examples
One of the best parts about Github is that you can view how other people set up their own work. Here are some past BSE portfolios that are awesome examples. You can view how they set up their portfolio, and you can view their index.md files to understand how they implemented different portfolio components.
- [Example 1](https://trashytuber.github.io/YimingJiaBlueStamp/)
- [Example 2](https://sviatil0.github.io/Sviatoslav_BSE/)
- [Example 3](https://arneshkumar.github.io/arneshbluestamp/)

To watch the BSE tutorial on how to create a portfolio, click here.
