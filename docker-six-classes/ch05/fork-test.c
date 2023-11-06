#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/wait.h>

char* const argv_list[] = {
    "/bin/bash", 
    NULL
};

int main(void)
{
    printf("Parent - current PID: %d\n", getpid());
    pid_t pid = fork();

    if(pid == -1) {
        printf("can't fork, error occurred\n");
        exit(EXIT_FAILURE);
    } else if(pid == 0) {
        printf("I am child process with pid: %d\n", getpid());
        execv(argv_list[0], argv_list);
        exit(0);
    } else {
        printf("I am parent process with PID %d and my child is %d\n", getpid(), pid);
        waitpid(pid, NULL, 0);
        printf("Parent - stopped!\n");
    }

    return 0;
}