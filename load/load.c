#include <stdio.h>
#include <sys/time.h>

int main()
{
    struct timeval start, end;
    gettimeofday( &start, NULL );

    int a = 0;
    for(long i = 0; i < 10000000000; i++){
        a += i;
    }
    gettimeofday( &end, NULL );
    int timeuse = 1000000 * ( end.tv_sec - start.tv_sec ) + end.tv_usec - start.tv_usec;
    printf("time: %d us:%d\n", timeuse, a);

    return 0;
}
