#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mount.h>
#include <sys/wait.h>
#include <unistd.h>

#define STACK_SIZE (1024 * 1024)

static char container_stack[STACK_SIZE];

int container_main(void *arg)
{
    printf("Container - inside the container!\n");

    if (mount("none", "/mnt", "tmpfs", 0, "") != 0)
    {
        fprintf(stderr, "Failed to mount tmpfs!\n");
        exit(1);
    }

    system("mount | grep /mnt");

    char *new_args[] = {"/bin/bash", NULL};
    execv(new_args[0], new_args);

    printf("Something's wrong!\n");
    return 1;
}

int main()
{
    printf("Parent - start a container!\n");

    int container_pid = clone(container_main, container_stack + STACK_SIZE, CLONE_NEWNS | SIGCHLD, NULL);

    printf("Parent - container PID: %d\n", container_pid);

    waitpid(container_pid, NULL, 0);
    printf("Parent - container stopped!\n");
    return 0;
}
