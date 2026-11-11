#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    int fd1[2], fd2[2], n;
    char filename[100], buffer[100];

    if (argc != 2) {
        printf("Usage: ./a.out filename\n");
        return 1;
    }

    pipe(fd1);  // Parent to Child
    pipe(fd2);  // Child to Parent

    pid_t p = fork();

    if (p > 0)
    {
        // Parent Process

        close(fd1[0]);
        close(fd2[1]);

        write(fd1[1], argv[1], 100);
        close(fd1[1]);

        wait(NULL);

        printf("File Content:\n");

        while ((n = read(fd2[0], buffer, 100)) > 0) {
            write(1, buffer, n);
        }

        close(fd2[0]);
    }
    else if (p == 0)
    {
        // Child Process

        close(fd1[1]);
        close(fd2[0]);

        read(fd1[0], filename, 100);
        close(fd1[0]);

        FILE *fp = fopen(filename, "r");

        if (fp == NULL) {
            perror("File not found");
            exit(1);
        }

        while ((n = fread(buffer, 1, 100, fp)) > 0) {
            write(fd2[1], buffer, n);
        }

        fclose(fp);
        close(fd2[1]);
    }

    return 0;
}
