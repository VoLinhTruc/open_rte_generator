extern void DcmSample_Provider_1000ms();
extern void DcmSample_Requester_1000ms();

void OS_1Q1_1000ms_Task(){
	(void) DcmSample_Provider_1000ms();
	(void) DcmSample_Requester_1000ms();
}

