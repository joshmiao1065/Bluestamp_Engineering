# International Space Station Tracker

This project utilzies a pyportal which is an internet-capable microcontroller with a built in screen. The code calls an API that actively tracks the space station position to yield a latitude and longitude coordinate pair which then was mapped to x-y coordinates on a mercator projection. It also tracks the path of the space station as it orbits the earth every 90 or so minutes. The greatest challenge I faced was getting acquainted with the Pyportal's libraries and capabilities which was overcome just by scouring the documentation :(

| **Engineer** | **School** | **Area of Interest** | **Grade** |
|:--:|:--:|:--:|:--:|
| Josh M | Cooper Union | Electrical Engineering | Incoming Junior |

![Headstone Image](ISS_tracker.png)
  
# Final Milestone

<iframe width="485" height="862" src="https://www.youtube.com/embed/HKJfoPRewhY" title="BlueStamp Engineering International Space Station Tracker" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

For your final milestone, explain the outcome of your project. Key details to include are:
- What you've accomplished since your previous milestone
- What your biggest challenges and triumphs were at BSE
- A summary of key topics you learned about
- What you hope to learn in the future after everything you've learned at BSE



# Second Milestone

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

<iframe width="560" height="315" src="https://www.youtube.com/embed/y3VAmNlER5Y" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

For your second milestone, explain what you've worked on since your previous milestone. You can highlight:
- Technical details of what you've accomplished and how they contribute to the final goal
- What has been surprising about the project so far
- Previous challenges you faced that you overcame
- What needs to be completed before your final milestone 

# First Milestone

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

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

```c++
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Hello World!");
}

void loop() {
  // put your main code here, to run repeatedly:

}
```

# Bill of Materials
Here's where you'll list the parts in your project. To add more rows, just copy and paste the example rows below.
Don't forget to place the link of where to buy each component inside the quotation marks in the corresponding row after href =. Follow the guide [here]([url](https://www.markdownguide.org/extended-syntax/)) to learn how to customize this to your project needs. 

| **Part** | **Note** | **Price** | **Link** |
|:--:|:--:|:--:|:--:|
| Adafruit Pyportal | Microcontroller and screen | $54.95 | <a href="https://www.adafruit.com/product/4116"> Link </a> |
| Micro USB Cable | Connect computer to pyportal | $4.95 | <a href="https://www.adafruit.com/product/592"> Link </a> |

# Other Resources/Examples
Here is a <a href="https://docs.circuitpython.org/projects/pyportal/en/latest/api.html"> link </a> to the documentation for the standard Pyportal library to help get you started.

To watch the BSE tutorial on how to create a portfolio, click <a href="https://drive.google.com/file/d/1GIGxyskToY8Ep137GnfTcfMCH4LaB6MF/view"> here </a>.
