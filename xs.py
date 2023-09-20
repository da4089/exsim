#! /usr/bin/env python

import exsim


def main():

    # Server
    server = exsim.Server()
    port = server.get_port()
    print("Controller listening on port {0}".format(port))

    server.load_engine("default", "default_engine", "DefaultEngine")
    server.create_engine("default", "default")
    server.load_protocol("fix42", "fix_protocol", "FixProtocol")
    server.create_endpoint("fix", 10101, "fix42", "default")
    server.run()
    return


if __name__ == "__main__":
    main()
