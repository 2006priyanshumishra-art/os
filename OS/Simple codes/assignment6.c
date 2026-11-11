// reader
#include<stdio.h>
#include<string.h>
#include<fcntl.h>
#include<unistd.h>

#define FIFO_PIPE "xyz"

int main()
{
    int fd,i,c=0,w=0,l=0;
    char str[200];

    fd = open(FIFO_PIPE,O_RDONLY);
    read(fd,str,sizeof(str)-1);
    str[sizeof(str)-1] = '\0';

    for(i=0;str[i]!='\0';i++)
    {
        if(str[i] == ' ' || str[i] == '\n')
            w++;

        if(str[i] == '\n')
            l++;

        c++;
    }

    printf("\nNo of characters = %d",c);
    printf("\nNo of lines = %d",l+1);
    printf("\nNo of words = %d\n",w+1);

    close(fd);
    return 0;
}

// writer
#include<sys/types.h>
#include<sys/stat.h>
#include<stdio.h>
#include<string.h>
#include<fcntl.h>
#include<unistd.h>

#define FIFO_PIPE "xyz"

int main()
{
    int fd,i=0;
    char str[200],ch;

    mkfifo(FIFO_PIPE,0644);

    printf("\nPipe Successfully created\n");
    printf("\nEnter your message (press @ to terminate)\n");

    while((ch = fgetc(stdin)) != '@' && i < 198)
    {
        str[i++] = ch;
    }

    str[i] = '\0';

    fd = open(FIFO_PIPE,O_WRONLY);
    write(fd,str,strlen(str));

    close(fd);

    return 0;
}






