#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include "protos/connection.pb.h"
#include "protos/connection.grpc.pb.h"


class ClassifyTextServicer {
public:
    ClassifyTextServicer() {
        printf("obj created\n");
    }

};

int run_server() {

    ClassifyTextServicer *textServicer = new ClassifyTextServicer();

}

int main() {
    printf("Hello world!\n");


    while (true) {
        try {
            run_server();
            return 0;
        } catch (const std::exception& e) {
            std::cout << "Exception caught, restarting server: " << e.what() << std::endl;
        } catch (...) {
            std::cout << "Caught unknown exception, restarting server" << std::endl;
        }
    }
}
