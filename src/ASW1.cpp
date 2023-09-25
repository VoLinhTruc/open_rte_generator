/*<RBHead>
*************************************************************************
* *
* ROBERT BOSCH GMBH *
* STUTTGART *
* *
* Alle Rechte vorbehalten - All rights reserved *
* *
*************************************************************************
*
*   __   __   ___  ___
*  /_ / /  / /__  /    /__/
* /__/ /__/ __ / /__  /  /
*
*
*************************************************************************
* Administrative Information (automatically filled in by eASEE) *
*************************************************************************
*
* $Filename__:$
*
* $Author____:$
*
* $Function__:$
*
*************************************************************************
* $Domain____:$
* $User______:$
* $Date______:$
* $Class_____:$
* $Name______:$
* $Variant___:$
* $Revision__:$
* $Type______:$
* $State_____:$
*
*************************************************************************
* List Of Changes
*
* $History___:
*
*
* $
*
*
***************************************************************************************************
</RBHead>*/

#include "ASW1.h"
#include "Arduino.h"
#include <WiFi.h>

const char* ssid     = "Bico";
const char* password = "11111111";
// const char* ssid     = "NGUYENDUCSAOLAU1.2G";
// const char* password = "28247467";
String html ="<!DOCTYPE html> <html> <head> <title>Mini Car Control</title> <style> body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f0f0f0; font-family: Arial, sans-serif; } .gameboy { border: 2px solid #222; border-radius: 10px; background-color: #ccc; width: 200px; /* height: 200px; */ padding: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3); } .gameboy-space { /* border: 2px solid #222; */ border-radius: 10px; /* background-color: #ccc; */ width: 50px; padding: 10px; /* box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3); */ } .button-container { display: flex; justify-content: space-between; margin: 10px 0; } .button { width: 45px; height: 45px; background-color: #fc7070; border: none; border-radius: 50%; color: #fff; /* font-size: 16px; */ cursor: pointer; box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.3); } .button-space { width: 20px; height: 45px; /* background-color: #444; */ border: none; border-radius: 50%; /* color: #fff; */ /* font-size: 16px; */ cursor: pointer; /* box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.3); */ } .slider-container { margin: 10px 0; } .slider { width: 100%; -webkit-appearance: none; appearance: none; height: 15px; border-radius: 5px; background-color: #64c4ff; outline: none; opacity: 0.7; -webkit-transition: .2s; transition: opacity .2s; } .slider::-webkit-slider-thumb { -webkit-appearance: none; appearance: none; width: 25px; height: 25px; border-radius: 50%; background: #ff2828; cursor: pointer; } .slider::-moz-range-thumb { width: 25px; height: 25px; border-radius: 50%; background: #444; cursor: pointer; } </style> </head> <body> <div class=\"gameboy\"> <div class=\"button-container\"> <div class=\"button-space\"></div> <button class=\"button\" onmousedown=\"sendCommand('up')\"></button> <div class=\"button-space\"></div> </div> <div class=\"button-container\"> <button class=\"button\" onmousedown=\"sendCommand('left')\"></button> <div class=\"button-space\"></div> <button class=\"button\" onmousedown=\"sendCommand('right')\"></button> </div> <div class=\"button-container\"> <div class=\"button-space\"></div> <button class=\"button\" onmousedown=\"sendCommand('down')\"></button> <div class=\"button-space\"></div> </div> </div> <div class=\"gameboy-space\"> </div> <div class=\"gameboy\"> <div class=\"slider-container\"> <input type=\"range\" min=\"0\" max=\"100\" value=\"50\" class=\"slider\" id=\"speedSlider\" oninput=\"updateSpeed()\"> </div> </div> <script> function sendCommand(command) { var xhr = new XMLHttpRequest(); xhr.open('GET', '/' + \"direction?\" + command, true); xhr.send(); } function updateSpeed() { var speedSlider = document.getElementById('speedSlider'); var speed = speedSlider.value; if (speed % 10 == 0) { var xhr = new XMLHttpRequest(); xhr.open('GET', '/' + \"speed?\" + speed, true); xhr.send(); } } </script> </body> </html>";

WiFiServer server(80);

void ASW1_10ms()
{
    static uint8 first_cycle_run_done = ASW1_FIRST_CYCLE_RUN_NOT_DONE;

    if (first_cycle_run_done == ASW1_FIRST_CYCLE_RUN_NOT_DONE)
    {
        // Implementation for the first cycle
        Serial.begin(115200);
        delay(10);
        
        Serial.println();
        Serial.println();
        Serial.print("Connecting to ");
        Serial.println(ssid);

        WiFi.begin(ssid, password);

        while (WiFi.status() != WL_CONNECTED) {
            delay(500);
            Serial.print(".");
        }

        Serial.println("");
        Serial.println("WiFi connected.");
        Serial.println("IP address: ");
        Serial.println(WiFi.localIP());
        
        server.begin();

        first_cycle_run_done = ASW1_FIRST_CYCLE_RUN_DONE;
    }
    else
    {
        // Cyclelic implementation
        WiFiClient client = server.available();

        if (client) 
        {        
            Serial.println("New Client.");
            String currentLine = "";
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();
            client.println(html);
            client.println();
            String client_response = "";
            while (client.available())
            {
                client_response += char(client.read());
                // Serial.write(client.read());
            }
            uint32 substring_start_index = client_response.indexOf("?") + 1;
            uint32 substring_end_index = client_response.indexOf(" ", substring_start_index);
            String extracted_value = client_response.substring(substring_start_index, substring_end_index);
            // Serial.println(extracted_value);
            static uint8 direction = 0; // 0:up, 1:right, 2:down, 3:left
            static uint8 speed = 0;
            if (extracted_value == "up")
            {
                direction = 0;
            }
            else if (extracted_value == "right")
            {
                direction = 1;
            }
            else if (extracted_value == "down")
            {
                direction = 2;
            }
            else if (extracted_value == "left")
            {
                direction = 3;
            }
            else
            {
                speed = extracted_value.toInt();
            }
            client.stop();
            Serial.println("Client Disconnected.");

            uint32 value_to_other_ASW = (uint32)0 | ((uint32)direction << 8) | (uint32)speed;
            Rte_Write_PP_ASW1_PP1_VDP_ASW1_Var1(value_to_other_ASW);

            Serial.println("ASW1_PP1_VDP_ASW1_Var1: " + String(value_to_other_ASW));
        }

        // static uint8 counter_for_1_second = 0;
        // counter_for_1_second = ++counter_for_1_second % 100;
        // if (counter_for_1_second == 0)
        // {
        //     static uint32 asw1_counter = 0;
        //     asw1_counter++;
        //     Rte_Write_PP_ASW1_PP1_VDP_ASW1_Var1(asw1_counter*22);
        //     Rte_Write_PP_ASW1_PP2_VDP_ASW1_Var2(asw1_counter*33);
            
        //     Serial.print("ASW2");
        //     Serial.print(" ");
        //     Serial.print(Rte_DRead_RP_ASW1_RP1_VDP_ASW2_Var1());
        //     Serial.print("\t");
        //     Serial.print("ASW3");
        //     Serial.print(" ");
        //     Serial.print(Rte_DRead_RP_ASW1_RP2_VDP_ASW3_Var1());
        //     Serial.println();
        // }
    }
}
