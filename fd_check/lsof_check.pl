#!/usr/bin/perl

while(1)
{
    $cnt = `adb shell lsof | wc -l`;
	printf("Total FD open: %d", $cnt);
	printf("\n");
	sleep 1;
}