#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/capability.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define STACK_SIZE (1024 * 1024)

static char container_stack[STACK_SIZE];

int container_main(void *arg)
{
    printf("Container - inside the container!\n");

    if (setgid(0) != 0 || setuid(0) != 0)
    {
        fprintf(stderr, "Failed to set UID/GID!\n");
        exit(1);
    }

    printf("Container - UID: %d, GID: %d\n", getuid(), getgid());

    char *new_args[] = {"/bin/bash", NULL};
    execv(new_args[0], new_args);

    printf("Something's wrong!\n");
    return 1;
}

int main()
{
    printf("Parent - start a container!\n");

    int user_pid = clone(container_main, container_stack + STACK_SIZE, CLONE_NEWUSER | SIGCHLD, NULL);

    char uid_map[100];
    char gid_map[100];
    sprintf(uid_map, "0 %d 1", getuid());
    sprintf(gid_map, "0 %d 1", getgid());
    if (write(open("/proc/self/uid_map", O_WRONLY), uid_map, strlen(uid_map)) == -1 ||
        write(open("/proc/self/gid_map", O_WRONLY), gid_map, strlen(gid_map)) == -1)
    {
        fprintf(stderr, "Failed to write UID/GID map!\n");
        exit(1);
    }

    printf("Parent - container PID: %d\n", user_pid);

    waitpid(user_pid, NULL, 0);
    printf("Parent - container stopped!\n");
    return 0;
}
