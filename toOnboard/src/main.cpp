//System Headers
#include <stdio.h>
#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>
#include <fstream>

//DJI Linux Application Headers
#include "/home/odroid/Onboard-SDK/platform/LinuxSerialDevice.h"
#include "LinuxThread.h"
#include "LinuxSetup.h"
#include "LinuxCleanup.h"
#include "ReadUserConfig.h"
#include "LinuxMobile.h"
#include "LinuxFlight.h"
#include "LinuxInteractive.h"
#include "LinuxWaypoint.h"

//DJI OSDK Library Headers
#include <DJI_Follow.h>
#include <DJI_Flight.h>
#include <DJI_Version.h>
#include <DJI_WayPoint.h>

using namespace std;
using namespace DJI;
using namespace DJI::onboardSDK;

//! Main function for the Linux sample. Lightweight. Users can call their own API calls inside the Programmatic Mode else on Line 68. 
int main(int argc, char *argv[])
{
	//! ONBOARD_Instantiate a serialDevice, an API object, flight and waypoint objects and a read thread.
	LinuxSerialDevice* serialDevice = new LinuxSerialDevice(UserConfig::deviceName, UserConfig::baudRate);
	CoreAPI* api = new CoreAPI(serialDevice);
	Flight* flight = new Flight(api);
	LinuxThread read(api, 2);

	//! ONBOARD_Setup
	int setupStatus = setup(serialDevice, api, &read);
	if (setupStatus == -1){std::cout << "Setup Failed. \n";}
	//! Set broadcast Freq Defaults
	unsigned short broadcastAck = api->setBroadcastFreqDefaults(1);
	ackReturnData takeControlStatus;
	//ackReturnData goHomeStatus;
	ackReturnData landingStatus;
	float v_x=0;
	float v_y=0;
	float v_z=0;
	int land=0;
	int stop=0;
	uint8_t flag = 0x43; //Velocity Control
	
	cout.flush();
	
	//! Programmatic Mode - execute everything here without any interactivity. Useful for automation.
	while(stop==0)
	{
		//Attempt Take Control
		//cout.setstate(std::ios_base::failbit);
		cin >> v_x >> v_y >> v_z >> land >> stop;
		takeControlStatus = takeControl(api);
		cout.flush();
		//Return Home
		//goHomeStatus = goHome(flight,blockingTimeout); 
		if(takeControlStatus.status==1)
		{
			if(land==0) 
			{
				flight->setMovementControl(flag, v_x, v_y, v_z, 0);			
			}
			else
			{
				landingStatus = landing(api,flight,1); //last parameter is blocking timeout
			}
		}
		usleep(20000);
	}
	//! Cleanup
	int cleanupStatus = cleanup(serialDevice, api, flight, &read);
	if (cleanupStatus == -1)
	{
		std::cout << "Unable to cleanly destroy OSDK infrastructure. There may be residual objects in the system memory.\n";
		return 0;
	}
	std::cout << "Program exited successfully." << std::endl;
	return 0;
}

