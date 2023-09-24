#include <libssh/libssh.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <iostream>

#define LOCAL_PORT 8080
#define REMOTE_HOST "45.76.232.143"
#define REMOTE_PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int local_socket;
    struct sockaddr_in local_address;
    char buffer[BUFFER_SIZE];
    int nbytes;

    // Create a local socket
    local_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (local_socket < 0) {
        perror("Failed to create local socket");
        return 1;
    }

    // Bind the local socket to the specified port
    local_address.sin_family = AF_INET;
    local_address.sin_port = htons(LOCAL_PORT);
    local_address.sin_addr.s_addr = INADDR_ANY;

    if (bind(local_socket, (struct sockaddr*)&local_address, sizeof(local_address)) < 0) {
        perror("Failed to bind local socket");
        close(local_socket);
        return 1;
    }

    // Listen for incoming connections
    if (listen(local_socket, 1) < 0) {
        perror("Failed to listen on local socket");
        close(local_socket);
        return 1;
    }

    printf("Listening on port %d...\n", LOCAL_PORT);

    // Initialize the SSH session and create a session instance
    ssh_session session;
    session = ssh_new();

    if (session == NULL) {
        fprintf(stderr, "Failed to create SSH session\n");
        close(local_socket);
        return 1;
    }

    // Set SSH options (hostname, username, and port)
    const char *hostname = REMOTE_HOST;
    const char *username = "mitm";
    int port = 22;

    ssh_options_set(session, SSH_OPTIONS_HOST, hostname);
    ssh_options_set(session, SSH_OPTIONS_USER, username);
    ssh_options_set(session, SSH_OPTIONS_PORT, &port);

    // Connect to the SSH server
    if (ssh_connect(session) != SSH_OK) {
        fprintf(stderr, "Failed to connect to SSH server\n");
        ssh_free(session);
        close(local_socket);
        return 1;
    }

    // Authenticate with the SSH server (you can use password or key-based authentication here)
    if (ssh_userauth_password(session, NULL, "") != SSH_AUTH_SUCCESS) {
        fprintf(stderr, "Authentication failed\n");
        ssh_disconnect(session);
        ssh_free(session);
        close(local_socket);
        return 1;
    }

    // Main loop for data transfer
    while (1) {
        socklen_t client_address_len;
        struct sockaddr_in client_address;
        int remote_socket;
        ssh_channel channel;

        client_address_len = sizeof(client_address);
        remote_socket = accept(local_socket, (struct sockaddr*)&client_address, &client_address_len);

        if (remote_socket < 0) {
            perror("Failed to accept connection");
            break;
        }

        printf("Accepted connection from %s:%d\n", inet_ntoa(client_address.sin_addr), ntohs(client_address.sin_port));

        // Open a forwarded channel (local socket to remote host)
        channel = ssh_channel_new(session);
        if (channel == NULL) {
            fprintf(stderr, "Error making new channel; %s", ssh_get_error(session));
        }

        // TODO pretty sure this line is wrong, check out https://api.libssh.org/stable/libssh_tutor_forwarding.html
        // TODO that was the issue, but still not connecting properly, keep working on it. block global is an issue again lol
        //if (ssh_channel_open_forward(channel, REMOTE_HOST, REMOTE_PORT, NULL, 0) != SSH_OK) {
        if (ssh_channel_open_forward(channel, REMOTE_HOST, REMOTE_PORT, "*", 8080) != SSH_OK) {
            fprintf(stderr, "Failed to open forwarded channel\n");
            ssh_channel_free(channel);
            close(remote_socket);
            continue;
        }

        // Forward data between local and remote sockets
        while ((nbytes = recv(remote_socket, buffer, sizeof(buffer), 0)) > 0) {
            std::cout << "Buffer: " << buffer << std::endl;
            ssh_channel_write(channel, buffer, nbytes);
            nbytes = ssh_channel_read(channel, buffer, sizeof(buffer), 0);
            if (nbytes <= 0) {
                break;
            }
            send(remote_socket, buffer, nbytes, 0);
        }

        // Close the forwarded channel and the remote socket
        ssh_channel_send_eof(channel);
        ssh_channel_free(channel);
        close(remote_socket);
        printf("Connection closed.\n");
    }

    // Disconnect and free the SSH session
    ssh_disconnect(session);
    ssh_free(session);

    // Close the local socket
    close(local_socket);

    return 0;
}

