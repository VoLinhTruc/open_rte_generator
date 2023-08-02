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

    }
}
