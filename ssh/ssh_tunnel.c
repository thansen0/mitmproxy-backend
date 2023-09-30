/*  These guides were lifesavers
 *      https://api.libssh.org/stable/libssh_tutor_guided_tour.html
 *      https://api.libssh.org/stable/libssh_tutor_forwarding.html
 * 
 */

#include <libssh/libssh.h>
#include <iostream>
#include <errno.h>
#include <string.h>

#define BUFFER_SIZE 1024

int verify_knownhost(ssh_session session);
int direct_forwarding(ssh_session session);

int main() {
    ssh_session sshSession;
    int localPort = 8080;
    const char* remoteHost = "localhost";
    int remotePort = 8080;
    const char* remoteUser = "mitm";
    const char* remoteServer = "45.76.232.143";
    const int default_port = 22;
    int verbosity = SSH_LOG_PROTOCOL;

    // Initialize the SSH library
    ssh_init();

    // Create a new SSH session
    sshSession = ssh_new();
    if (sshSession == nullptr) {
        // Handle error
        printf("error; sshSession == nullptr\n");
        return 1;
    }

    // Set SSH options (e.g., host, port, user)
    ssh_options_set(sshSession, SSH_OPTIONS_HOST, remoteServer);
    ssh_options_set(sshSession, SSH_OPTIONS_PORT, &default_port); // SSH default port
    ssh_options_set(sshSession, SSH_OPTIONS_USER, remoteUser);
    ssh_options_set(sshSession, SSH_OPTIONS_LOG_VERBOSITY, &verbosity);

    // Connect to the remote SSH server
    int rc = ssh_connect(sshSession);
    if (rc != SSH_OK) {
        fprintf(stderr, "Error connecting to localhost: %s\n",
                ssh_get_error(sshSession));
        // Handle connection error
        ssh_free(sshSession);
        return 1;
    }

    // Verify the server's identity
    // For the source code of verify_knownhost(), check previous example
    if (verify_knownhost(sshSession) < 0) {
        fprintf(stderr, "Error verify host: %s\n",
                ssh_get_error(sshSession));
        ssh_disconnect(sshSession);
        ssh_free(sshSession);
        exit(-1);
    }
    printf("verified host\n");

    // Authenticate with password or other methods if needed
    const char *username = nullptr; // "mitm";
    //rc = ssh_userauth_none(sshSession, nullptr);
    rc = ssh_userauth_password(sshSession, nullptr, "");
    //rc = ssh_userauth_agent_pubkey(sshSession, username, NULL);
    // If keys are already shared, this will fail, and I need to use auth_none
    if (rc != SSH_AUTH_SUCCESS) {
        fprintf(stderr, "Error %i != SSH_AUTH_SUCCESS; %s\n",
                rc, ssh_get_error(sshSession));
        // Handle authentication error
        ssh_disconnect(sshSession);
        ssh_free(sshSession);
        return 1;
    }

    // Request local port forwarding
    //printf("about to enable channel listening\n");
    //rc = ssh_channel_listen_forward(sshSession, remoteHost, remotePort, &localPort);
    /*rc = ssh_channel_listen_forward(sshSession, NULL, 8080, NULL);
    if (rc != SSH_OK) {
        fprintf(stderr, "Error opening remote port: %s\n",
                ssh_get_error(sshSession));
        // Handle port forwarding error
        ssh_disconnect(sshSession);
        ssh_free(sshSession);
        return 1;
    }*/

    // Keep the program running until you want to terminate the tunnel
    //printf("press any key to continue:");
    //getchar();
    printf("about to enable direct forwarding (-L)\n");
    direct_forwarding(sshSession);

    // To terminate the tunnel, you can call:
    // ssh_channel_close_forward(sshSession, "localhost", localPort);

    printf("disconnecting and freeing resources\n");
    // Disconnect and free resources
    ssh_disconnect(sshSession);
    ssh_free(sshSession);

    return 0;
}


int verify_knownhost(ssh_session session) {
    enum ssh_known_hosts_e state;
    unsigned char *hash = NULL;
    ssh_key srv_pubkey = NULL;
    size_t hlen;
    char buf[10];
    char *hexa;
    char *p;
    int cmp;
    int rc;
 
    rc = ssh_get_server_publickey(session, &srv_pubkey);
    if (rc < 0) {
        return -1;
    }
 
    rc = ssh_get_publickey_hash(srv_pubkey,
                                SSH_PUBLICKEY_HASH_SHA1,
                                &hash,
                                &hlen);
    ssh_key_free(srv_pubkey);
    if (rc < 0) {
        return -1;
    }
 
    state = ssh_session_is_known_server(session);
    switch (state) {
        case SSH_KNOWN_HOSTS_OK:
            /* OK */
 
            break;
        case SSH_KNOWN_HOSTS_CHANGED:
            fprintf(stderr, "Host key for server changed: it is now:\n");
            ssh_print_hexa("Public key hash", hash, hlen);
            fprintf(stderr, "For security reasons, connection will be stopped\n");
            ssh_clean_pubkey_hash(&hash);
 
            return -1;
        case SSH_KNOWN_HOSTS_OTHER:
            fprintf(stderr, "The host key for this server was not found but an other"
                    "type of key exists.\n");
            fprintf(stderr, "An attacker might change the default server key to"
                    "confuse your client into thinking the key does not exist\n");
            ssh_clean_pubkey_hash(&hash);
 
            return -1;
        case SSH_KNOWN_HOSTS_NOT_FOUND:
            fprintf(stderr, "Could not find known host file.\n");
            fprintf(stderr, "If you accept the host key here, the file will be"
                    "automatically created.\n");
 
            /* FALL THROUGH to SSH_SERVER_NOT_KNOWN behavior */
 
        case SSH_KNOWN_HOSTS_UNKNOWN:
            hexa = ssh_get_hexa(hash, hlen);
            fprintf(stderr,"The server is unknown. Do you trust the host key?\n");
            fprintf(stderr, "Public key hash: %s\n", hexa);
            ssh_string_free_char(hexa);
            ssh_clean_pubkey_hash(&hash);
            p = fgets(buf, sizeof(buf), stdin);
            if (p == NULL) {
                return -1;
            }
 
            cmp = strncasecmp(buf, "yes", 3);
            if (cmp != 0) {
                return -1;
            }
 
            rc = ssh_session_update_known_hosts(session);
            if (rc < 0) {
                fprintf(stderr, "Error %s\n", strerror(errno));
                return -1;
            }
 
            break;
        case SSH_KNOWN_HOSTS_ERROR:
            fprintf(stderr, "Error %s", ssh_get_error(session));
            ssh_clean_pubkey_hash(&hash);
            return -1;
    }
 
    ssh_clean_pubkey_hash(&hash);
    return 0;
}

int direct_forwarding(ssh_session session) {
    printf("Started direct_forwarding function\n");


    ssh_channel forwarding_channel;
    int rc;
    char *http_get = "GET / HTTP/1.1\nHost: www.google.com\n\n";
    int nbytes, nwritten;
 
    forwarding_channel = ssh_channel_new(session);
    if (forwarding_channel == NULL) {
        fprintf(stderr, "Error making new channel; %s", ssh_get_error(session));
        return 1;
    }
 




    /* first site recommendation
    rc = ssh_channel_open_forward(forwarding_channel,
                                "www.google.com", 80,
                                "localhost", 5555);
    if (rc != SSH_OK) {
        fprintf(stderr, "Error %i != SSH_OK, %s", rc, ssh_get_error(session));
        ssh_channel_free(forwarding_channel);
        return rc;
    }
 
    nbytes = strlen(http_get);
    nwritten = ssh_channel_write(forwarding_channel,
                           http_get,
                           nbytes);
    if (nbytes != nwritten) {
        fprintf(stderr, "Error nbytes %i != nwritten %i, %s", nbytes, nwritten, ssh_get_error(session));
        ssh_channel_free(forwarding_channel);
        return SSH_ERROR;
    }

    std::cout << "nbytes " <<  nbytes << std::endl;
    std::cout << "nwritten " <<  nwritten << std::endl; // */
    // TODO look into exec command, maybe run the server this way? https://api.libssh.org/master/libssh_tutor_command.html




    // chatgpt recommendation
    const char *remote_host = "*";

    rc = ssh_channel_open_forward(forwarding_channel, remote_host, localPort, remote_host, remotePort);
    if (rc != SSH_OK) {
        fprintf(stderr, "Error %i != SSH_OK, %s", rc, ssh_get_error(session));
        ssh_channel_free(forwarding_channel);
        return rc;
    } // */

    // Main loop for data transfer
    char buffer[BUFFER_SIZE];
    //int nbytes;

    while (1) {
        // Read data from the local application (e.g., a web server)
        // and forward it through the SSH tunnel
        nbytes = fread(buffer, 1, sizeof(buffer), stdin);

        if (nbytes <= 0) {
            printf("nbytes %i <= 0 on read\n", nbytes);
            break; // End of input
        }

        ssh_channel_write(forwarding_channel, buffer, nbytes);

        // Read data from the remote server through the SSH tunnel
        nbytes = ssh_channel_read(forwarding_channel, buffer, sizeof(buffer), 0);

        if (nbytes <= 0) {
            printf("nbytes %i <= 0 on write\n", nbytes);
            break; // End of remote data
        }

        // Write the received data to the local application (e.g., a web browser)
        fwrite(buffer, 1, nbytes, stdout);
        fflush(stdout);
    }




    /* final looping option
    while (1) {
        nbytes = ssh_channel_read(forwarding_channel, buffer, sizeof(buffer), 0);
        if (nbytes < 0) {
            fprintf(stderr, "Error reading incoming data: %s\n",
                ssh_get_error(session));
            ssh_channel_send_eof(channel);
            ssh_channel_free(channel);
            return SSH_ERROR;
        }
    
        if (strncmp(buffer, "GET /", 5)) continue;
 
        nbytes = strlen(helloworld);
        nwritten = ssh_channel_write(forwarding_channel, helloworld, nbytes);
        if (nwritten != nbytes) {
            fprintf(stderr, "Error sending answer: %s\n",
                ssh_get_error(session));
            ssh_channel_send_eof(channel);
            ssh_channel_free(channel);
            return SSH_ERROR;
        }
        printf("Sent answer\n");
    }*/


 
    // Keep the program running until you want to terminate the tunnel
    printf("press any key to continue:");
    getchar();
 
    ssh_channel_free(forwarding_channel);
    return SSH_OK;
}
