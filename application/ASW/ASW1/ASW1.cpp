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

#include "Arduino.h"
#include "ASW1.h"

void ASW1_10ms()
{
    static uint8 first_cycle_run_done = ASW1_FIRST_CYCLE_RUN_NOT_DONE;

    if (first_cycle_run_done == ASW1_FIRST_CYCLE_RUN_NOT_DONE)
    {
        // Implementation for the first cycle
        Serial.begin(115200);
        first_cycle_run_done = ASW1_FIRST_CYCLE_RUN_DONE;
    }
    else
    {
        // Cyclelic implementation
        static uint8 counter_for_1_second = 0;
        counter_for_1_second = ++counter_for_1_second % 1000;
        if (counter_for_1_second == 0)
        {
            Serial.print("ASW1");
            Serial.print("\t");
            Serial.print(counter_for_1_second);
        }
    }
}
