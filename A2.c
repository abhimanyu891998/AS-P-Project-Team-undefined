#include <errno.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>


void sigint_handler(int signum) {
    printf("\n\nA signal SIGINT is caught, jack you're termianating this behemoth process\n\n");
}

int main(int argc, char **argv){
    int numberOfArguments=argc;
    
    int i;
    
    char *singleCommand[numberOfArguments-1];
    struct rusage used;
    for(i=0;i<numberOfArguments-1;i++){
        singleCommand[i]=argv[i+1];
    }
    
    

    pid_t pid;

    pid = fork();

    if (pid < 0) {
        printf("fork: error no = %s\n", strerror(errno));
        exit(-1);
    } else if (pid == 0) {
        signal(SIGINT,SIG_DFL);
        printf("I am the child process with PID: %d that needs to be swapped with the command \n", (int)getpid());
        sleep(2);
        printf("Kill me baby, I am the child process \n");
        printf("Now I am changing my context, hmu \n");
        printf("execlp: Press <enter> to execute the command");

        getchar();


        if (execvp(singleCommand[0], singleCommand) == -1) {
            printf("execvp: error no = %s\n", strerror(errno));
            exit(-1);
        }
        printf("This statement should never be executed");



    } else {
        signal(SIGINT, sigint_handler);
        printf("I am the parent process with PID : %d\n",(int) getpid());
        int status;
        waitpid(pid, &status, 0);  // wait for child to terminate

        if(WIFEXITED(status)){ //if terminates normally
            printf("Child Process with PID %d terminated properly with exit status code %d, DAMN!! \n",(int) getpid(),(int) WEXITSTATUS(status));
        }else if (WIFSIGNALED(status)){ //this means that the child process was terminated with a signal, get signal details
            printf("Child process exited, with a status : %d and code %s \n", (int)WTERMSIG(status),strsignal(WTERMSIG(status)));
            getrusage(RUSAGE_CHILDREN, &used);
            printf("The child had experienced %ld involuntary context switches\n", used.ru_nivcsw);
        }
        getchar();
        printf("Try killing me bitch, i am the parent\n");

    }

    
    
   
    
    

    
    
    
}
