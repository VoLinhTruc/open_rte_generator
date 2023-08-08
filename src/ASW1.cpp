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
        counter_for_1_second = ++counter_for_1_second % 100;
        if (counter_for_1_second == 0)
        {
            static uint32 asw1_counter = 0;
            asw1_counter++;
            Rte_Write_PP_ASW1_PP1_VDP_ASW1_Var1(asw1_counter*22);
            Rte_Write_PP_ASW1_PP2_VDP_ASW1_Var2(asw1_counter*33);
            
            Serial.print("ASW2");
            Serial.print(" ");
            Serial.print(Rte_DRead_RP_ASW1_RP1_VDP_ASW2_Var1());
            Serial.print("\t");
            Serial.print("ASW3");
            Serial.print(" ");
            Serial.print(Rte_DRead_RP_ASW1_RP2_VDP_ASW3_Var1());
            Serial.println();
        }
    }
}
