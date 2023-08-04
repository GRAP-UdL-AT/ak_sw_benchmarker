/*
Project: Size Estimation
Author : Juan Carlos Miranda.https ://github.com/juancarlosmiranda
	Date : March 2022
	Description :
	Get calibration data from Azure Kinect devices

	Search references in https://microsoft.github.io/Azure-Kinect-Sensor-SDK/master/structk4a__calibration__t.html

	Use :

*/
#pragma comment(lib, "k4a.lib")
#include <k4a/k4a.h>
#include <k4a/k4atypes.h>
#include <k4arecord/record.h>
#include <k4arecord/playback.h>

#include <stdio.h>
#include <stdlib.h>
#include <iostream>


void print_calibration_data(k4a_calibration_camera_t  calibration_camera)
{
	printf("resolution_width = %d \n", calibration_camera.resolution_width);
	printf("resolution_height = %d \n", calibration_camera.resolution_height);
	printf("metric_radius = %f \n", calibration_camera.metric_radius);

	printf("Intrinsics parameters --> \n");
	printf("type = %d \n", calibration_camera.intrinsics.type);
	printf("focal_length_x_axis = %f \n", calibration_camera.intrinsics.parameters.param.fx);
	printf("focal_length_y_axis = %f \n", calibration_camera.intrinsics.parameters.param.fy);
	printf("principal_point_x = %f \n", calibration_camera.intrinsics.parameters.param.cx);
	printf("principal_point_y = %f \n", calibration_camera.intrinsics.parameters.param.cy);
	printf("k1_radial_distortion = %f \n", calibration_camera.intrinsics.parameters.param.k1);
	printf("k2_radial_distortion = %f \n", calibration_camera.intrinsics.parameters.param.k2);
	printf("k3_radial_distortion = %f \n", calibration_camera.intrinsics.parameters.param.k3);
	printf("k4_radial_distortion = %f \n", calibration_camera.intrinsics.parameters.param.k4);
	printf("k5_radial_distortion = %f \n", calibration_camera.intrinsics.parameters.param.k5);
	printf("k6_radial_distortion = %f \n", calibration_camera.intrinsics.parameters.param.k6);
	printf("center_of_distortion_in_Z=1_plane_x = %f \n", calibration_camera.intrinsics.parameters.param.codx);
	printf("center_of_distortion_in_Z=1_plane_y = %f \n", calibration_camera.intrinsics.parameters.param.cody);
	printf("tangential_distortion_coefficient_x = %f \n", calibration_camera.intrinsics.parameters.param.p1);
	printf("tangential_distortion_coefficient_y = %f \n", calibration_camera.intrinsics.parameters.param.p2);
	printf("metric_radius = %f \n", calibration_camera.intrinsics.parameters.param.metric_radius);

}

int main()
{
	int returnCode = 1;
	uint32_t number_devices_connected = k4a_device_get_installed_count(); //This obtain the number of devices connected

	if (number_devices_connected == 0)
	{
		printf("No k4a devices attached! \n");
		return 1;
	}
	else {
		printf("Count devices connected = %d \n", number_devices_connected);
	}

	k4a_device_t device = NULL;
	if (K4A_RESULT_SUCCEEDED != k4a_device_open(K4A_DEVICE_DEFAULT, &device))
	{
		printf("%d: Failed to open device\n", 1);
	}
	else {
		printf("Device opened: %d \n", device);
	}

	// ----------------------------------------------------------------------------
	// Get the size of the serial number
	size_t serial_size = 0;
	k4a_device_get_serialnum(device, NULL, &serial_size);

	// Allocate memory for the serial, then acquire it
	char* device_serial_number = (char*)(malloc(serial_size));
	k4a_device_get_serialnum(device, device_serial_number, &serial_size);
	printf("Opened device serial number: %s\n", device_serial_number);
	free(device_serial_number);
	// ----------------------------------------------------------------------------

	//---------------------------------------
	// My config TESTING
	// 30 FPS
	// MJPG
	// 1080P
	// NFOV Unbinned
	// WIRED_SYNC_MODE_STANDALONE
	//---------------------------------------
	k4a_device_configuration_t device_config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
	device_config.camera_fps = K4A_FRAMES_PER_SECOND_30;
	device_config.color_format = K4A_IMAGE_FORMAT_COLOR_MJPG;
	device_config.color_resolution = K4A_COLOR_RESOLUTION_1080P;
	device_config.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;
	device_config.wired_sync_mode = K4A_WIRED_SYNC_MODE_STANDALONE; //syncronized images like 
	device_config.synchronized_images_only = true; // true=ensures that return only completed images RGB+DEPTH+IR

	//---------------------------------------
	// Start the camera with the given configuration
	if (K4A_RESULT_SUCCEEDED != k4a_device_start_cameras(device, &device_config))
	{
		printf("Failed to start cameras!\n");
		k4a_device_close(device);
		return 1;
	}
	else {
		printf("CAMERA STARTED \n");
	}

	k4a_calibration_t calibration_data;  // = NULL;

	if (K4A_RESULT_SUCCEEDED == k4a_device_get_calibration(device, device_config.depth_mode, device_config.color_resolution, &calibration_data))
	{
		printf("----------------------- \n");
		printf("Color camera --> \n");
		printf("----------------------- \n");
		print_calibration_data(calibration_data.color_camera_calibration);

		printf("----------------------- \n");
		printf("ToF camera --> \n");
		printf("----------------------- \n");
		print_calibration_data(calibration_data.depth_camera_calibration);
		// ----------------------------------------------------------
	}
	else {
		printf("CALIBRATION FAILED-->");
	}
	// ----------------------------------------------------------------------------
	// Camera capture and application specific code would go here
	// Shut down the camera when finished with application logic
	printf("CAMERA STOPPED \n");
	k4a_device_stop_cameras(device);
	k4a_device_close(device);
	return 0;
}
