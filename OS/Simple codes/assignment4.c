#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>

#define N 5

sem_t ch[N];
sem_t room;

void *philosopher(void *arg)
{
    int i = *(int *)arg;
    int left, right;

    left = i;
    right = (i + 1) % N;

    printf("\n%d philosopher is created", i);
    printf("\n%d philosopher is hungry", i);

    sem_wait(&room);

    sem_wait(&ch[left]);
    sem_wait(&ch[right]);

    printf("\n%d philosopher is eating", i);

    sleep(2);

    sem_post(&ch[right]);
    sem_post(&ch[left]);

    printf("\n%d philosopher has completed eating", i);

    sem_post(&room);

    return NULL;
}

int main()
{
    int i;
    int id[N];
    pthread_t pid[N];

    for(i = 0; i < N; i++)
        sem_init(&ch[i], 0, 1);

    sem_init(&room, 0, 4);

    for(i = 0; i < N; i++)
    {
        id[i] = i;
        pthread_create(&pid[i], NULL, philosopher, &id[i]);
    }

    for(i = 0; i < N; i++)
        pthread_join(pid[i], NULL);

    for(i = 0; i < N; i++)
        sem_destroy(&ch[i]);

    sem_destroy(&room);

    return 0;
}
