#include <libssh/libssh.h>
#include <stdlib.h>
#include <stdio.h>


int main() {
    int verbosity = SSH_LOG_PROTOCOL;

    ssh_session my_ssh_session = ssh_new();

    ssh_options_set(my_ssh_session, SSH_OPTIONS_USER, "thomas");
    ssh_options_set(my_ssh_session, SSH_OPTIONS_HOST, "localhost");
    ssh_options_set(my_ssh_session, SSH_OPTIONS_LOG_VERBOSITY, &verbosity);

    int rc = ssh_connect(my_ssh_session);
    if(rc != SSH_OK) {
        fprintf(stderr, "Error connecting to localhost: %s\n",
                ssh_get_error(my_ssh_session));
        exit(-1);
    }

    // Authorized by the password.
    rc = ssh_userauth_password(my_ssh_session, "thomas", "5T6y7U8i9O");

}
