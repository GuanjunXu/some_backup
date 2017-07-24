#!/usr/bin/perl

while(1)
{
    $cnt = `adb shell ls -l /proc/$ARGV[0]/fd | wc -l`;
	printf("[%d] proceee FD open: %d", $ARGV[0], $cnt);
	printf("\n");
	sleep 1;
}