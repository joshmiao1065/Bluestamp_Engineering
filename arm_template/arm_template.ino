#include "src/CokoinoArm.h"

CokoinoArm arm;
int verL,horL,verR,horR;

void turnUD(void){ //detects vertical axis of left stick and determines how to move arm up and down
  if(!(verL > 450 && verL < 560)){ //controller deadzone 
    if(0<=verL && verL<=100){arm.up(10);return;}
    if(900<verL && verL<=1024){arm.down(10);return;} 
    if(100<verL && verL<=200){arm.up(20);return;}
    if(800<verL && verL<=900){arm.down(20);return;}
    if(200<verL && verL<=300){arm.up(25);return;}
    if(700<verL && verL<=800){arm.down(25);return;}
    if(300<verL && verL<=400){arm.up(30);return;}
    if(600<verL && verL<=700){arm.down(30);return;}
    if(400<verL && verL<=480){arm.up(35);return;}
    if(540<verL && verL<=600){arm.down(35);return;} 
    }
}

void turnLR(void){ //detects horizontal axis of left stick and determines how to move arm left and right
  if(!(horL > 450 && horL < 560)){ //controller deadzone 
    if(0<=horL && horL<=100){arm.right(0);return;}
    if(900<horL && horL<=1024){arm.left(0);return;}  
    if(100<horL && horL<=200){arm.right(5);return;}
    if(800<horL && horL<=900){arm.left(5);return;}
    if(200<horL && horL<=300){arm.right(10);return;}
    if(700<horL && horL<=800){arm.left(10);return;}
    if(300<horL && horL<=400){arm.right(15);return;}
    if(600<horL && horL<=700){arm.left(15);return;}
    if(400<horL && horL<=480){arm.right(20);return;}
    if(540<horL && horL<=600){arm.left(20);return;}
  }
}
void turnCO(void){ //detects vertical axis of right stick and determines how to open and close claw
  if(!(verR > 450 && verR < 560)){ //controller deadzone 
    if(0<=verR && verR<=100){arm.close(0);return;}
    if(900<verR && verR<=1024){arm.open(0);return;} 
    if(100<verR && verR<=200){arm.close(5);return;}
    if(800<verR && verR<=900){arm.open(5);return;}
    if(200<verR && verR<=300){arm.close(10);return;}
    if(700<verR && verR<=800){arm.open(10);return;}
    if(300<verR && verR<=400){arm.close(15);return;}
    if(600<verR && verR<=700){arm.open(15);return;}
    if(400<verR && verR<=480){arm.close(20);return;}
    if(540<verR && verR<=600){arm.open(20);return;} 
    }
}

//ensure only 1 command is read at a time 
void date_processing(int *x,int *y){
  if(abs(512-*x)>abs(512-*y))
    {*y = 512;}
  else
    {*x = 512;}
}

void setup() {
  Serial.begin(9600);
  //arm of servo motor connection pins
  arm.ServoAttach(4,5,6,7);
  //arm of joy stick connection pins : verL,horL,verR,horR
  arm.JoyStickAttach(A0,A1,A2,A3);
}

void loop() {
  //read 4 stick values

  //filter data so only 1 command at once
  

  //determine movement
  
}

