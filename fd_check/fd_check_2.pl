#!/usr/bin/perl

$idx =1;
while(1)
{   
    $fd_open = `adb shell ls -l /proc/$ARGV[0]/fd`;
	@values = split('\n', $fd_open);
    printf("*************[index:%d, count:%d]*************\n", $idx, scalar(@values));
    printf("%s",$fd_open);
	printf("\n");
    $idx += 1;
	sleep 1;
}