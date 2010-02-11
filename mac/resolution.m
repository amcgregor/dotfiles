/*
 * resolution.m
 * 
 * Alice Bevan-McGregor 2010-02-11
 *    Discovered via http://www.macosxhints.com/article.php?story=20090413120929454
 *    Updated with code provided in the comments to the article.
 * juanfc 2009-04-13 [setgetscreenres.m]
 * jawsoftware 2009-04-17
 * Based on newscreen
 *    Created by Jeffrey Osterman on 10/30/07.
 *    Copyright 2007 Jeffrey Osterman. All rights reserved. 
 *    PROVIDED AS IS AND WITH NO WARRANTIES WHATSOEVER
 *    http://forums.macosxhints.com/showthread.php?t=59575
 *
 * COMPILE UNIVERSAL:
 *    c++ resolution.m -framework ApplicationServices -o resolution -arch i386 -arch ppc
 *
 * COMPILE LEGACY:
 *    c++ resolution.m -framework ApplicationServices -o resolution -arch ppc -mmacosx-version-min=10.3.9
 *
 * COMPILE HOST-ONLY:
 *    c++ resolution.m -framework ApplicationServices -o resolution
 *
 * USAGE:
 *    setgetscreenres [ -l | 1..9] [ 1440 900 ]
 */

#include <ApplicationServices/ApplicationServices.h>

bool MyDisplaySwitchToMode (CGDirectDisplayID display, CFDictionaryRef mode);
void ListDisplays( CGDisplayCount dispCount, CGDirectDisplayID *dispArray );
void usage(const char *argv[]);
void GetDisplayParms(CGDirectDisplayID *dispArray,  CGDisplayCount dispNum, int *width, int *height, int *depth, int *freq);

int main (int argc, const char * argv[])
{
	int	h; 							// horizontal resolution
	int v; 							// vertical resolution
	int depth, freq;

	CFDictionaryRef switchMode; 	// mode to switch to
	CGDirectDisplayID theDisplay;  // ID of  display, display to set
	int displayNum; //display number requested by user
	
	CGDisplayCount maxDisplays = 10;
	CGDirectDisplayID onlineDspys[maxDisplays];
	CGDisplayCount dspyCnt;
	
	CGGetOnlineDisplayList (maxDisplays, onlineDspys, &dspyCnt);

	
	if (argc == 1) {
	    CGRect screenFrame = CGDisplayBounds(kCGDirectMainDisplay);
		CGSize screenSize  = screenFrame.size;
		printf("%.0f %.0f\n", screenSize.width, screenSize.height);
		return 0;
	}
	
	if (argc == 2) {
		if (! strcmp(argv[1],"-l")) {
			ListDisplays( dspyCnt, onlineDspys );
			return 0;
		}
		else if (! strcmp(argv[1],"-?")) {
			usage(argv);
			return 0;
		}
		else if (displayNum = atoi(argv[1])) {
			if (displayNum <= dspyCnt) {
				GetDisplayParms(onlineDspys, displayNum-1, &h, &v, &depth, &freq);
				printf("%d %d\n", h, v);
				return 0;
			}
			else {
				fprintf(stderr, "ERROR: display number out of bounds; displays on this mac: %d.\n", dspyCnt);
				return -1;
			}
		}
	}
	
	
	if (argc == 4 && (displayNum = atoi(argv[1])) && (h = atoi(argv[2])) && (v = atoi(argv[3])) ) {
		if (displayNum <= dspyCnt) {
			theDisplay= onlineDspys[displayNum-1];
		}
		else return -1;
	}
	else {
		if (argc != 3 || !(h = atoi(argv[1])) || !(v = atoi(argv[2])) ) {
			fprintf(stderr, "ERROR: syntax error.\n", argv[0]);
			usage(argv);
			return -1;
		}
		theDisplay = CGMainDisplayID();
	}


	switchMode = CGDisplayBestModeForParameters(theDisplay, 32, h, v, NULL);
	
	if (! MyDisplaySwitchToMode(theDisplay, switchMode)) {
	    fprintf(stderr, "Error changing resolution to %d %d\n", h, v);
		return 1;
	}
	
	return 0;
}


void ListDisplays( CGDisplayCount dispCount, CGDirectDisplayID *dispArray )
{
	int	h, v, depth, freq, i;
	CGDirectDisplayID mainDisplay = CGMainDisplayID();
	
		printf("Displays found: %d\n", dispCount);
		for	(i = 0 ; i < dispCount ;  i++ ) {

			GetDisplayParms(dispArray, i, &h, &v, &depth, &freq);
			printf("Display %d (id %d):  %d x %d x %d @ %dHz", i+1, dispArray[i], h, v, depth, freq);
			if ( mainDisplay == dispArray[i] ) 
				printf(" (main)\n");
			else
				printf("\n");
		}
}

void GetDisplayParms(CGDirectDisplayID *dispArray,  CGDisplayCount dispNum, int *width, int *height, int *depth, int *freq)
{
	CFDictionaryRef currentMode = CGDisplayCurrentMode (dispArray[dispNum]);
	CFNumberRef number = CFDictionaryGetValue (currentMode, kCGDisplayRefreshRate);
	CFNumberGetValue (number, kCFNumberLongType, freq);
	number = CFDictionaryGetValue (currentMode, kCGDisplayWidth);
	CFNumberGetValue (number, kCFNumberLongType, width);
	number = CFDictionaryGetValue (currentMode, kCGDisplayHeight);
	CFNumberGetValue (number, kCFNumberLongType, height);
	number = CFDictionaryGetValue (currentMode, kCGDisplayBitsPerPixel);
	CFNumberGetValue (number, kCFNumberLongType, depth);
}

bool MyDisplaySwitchToMode (CGDirectDisplayID display, CFDictionaryRef mode)
{
	CGDisplayConfigRef config;
	if (CGBeginDisplayConfiguration(&config) == kCGErrorSuccess) {
		CGConfigureDisplayMode(config, display, mode);
		CGCompleteDisplayConfiguration(config, kCGConfigureForSession );
		return true;
	}
	return false;
}


void usage(const char *argv[])
{
	printf("\nUsage: %s [-l | 1..9 ] [ hor_res vert_res]\n\n", argv[0]);
	printf("      -l  list resolution, depth and refresh rate of all displays\n");
	printf("    1..9  display # (default: main display)\n");
	printf(" hor_res  horizontal resolution\n");
	printf("vert_res  vertical resolution\n\n");
	printf("Examples:\n");
	printf("%s 800 600      set resolution of main display to 800x600\n", argv[0]);
	printf("%s 2 800 600    set resolution of secondary display to 800x600\n", argv[0]);
	printf("%s 3            get resolution of third display\n", argv[0]);
	printf("%s -l           get resolution, bit depth and refresh rate of all displays\n\n", argv[0]);
}