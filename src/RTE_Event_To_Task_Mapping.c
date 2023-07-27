#ifdef __cplusplus
extern "C" {
#endif

extern void DcmSample_Provider_1000ms();
extern void DcmSample_Requester_1000ms();
extern void ASW1_10ms();
extern void ASW2_10ms();
extern void ASW3_10ms();

void OS_1Q1_1000ms_Task(){
	(void) DcmSample_Provider_1000ms();
	(void) DcmSample_Requester_1000ms();
}

void OS_1Q1_10ms_Task(){
	(void) ASW1_10ms();
	(void) ASW2_10ms();
	(void) ASW3_10ms();
}


#ifdef __cplusplus
}
#endif

