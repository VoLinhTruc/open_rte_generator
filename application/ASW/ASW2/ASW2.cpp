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
#include "ASW2.h"

void ASW2_10ms()
{
    static uint8 first_cycle_run_done = ASW2_FIRST_CYCLE_RUN_NOT_DONE;

    if (first_cycle_run_done == ASW2_FIRST_CYCLE_RUN_NOT_DONE)
    {
        // Implementation for the first cycle

        first_cycle_run_done = ASW2_FIRST_CYCLE_RUN_DONE;
    }
    else
    {
        // Cyclelic implementation
        static uint8 counter_for_1_second = 0;
        counter_for_1_second = ++counter_for_1_second % 200;
        if (counter_for_1_second == 0)
        {
            static uint32 asw2_counter = 0;
            asw2_counter++;
            Rte_Write_PP_ASW2_PP1_VDP_ASW2_Var1(asw2_counter*2);
            
            Serial.print("ASW2 receive from ASW1");
            Serial.print(" ");
            Serial.print(Rte_DRead_RP_ASW2_RP1_VDP_ASW1_Var1());
            Serial.println();
        }
    }
}
