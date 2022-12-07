#! /usr/bin/env python

import exsim


def main():

    # Server
    server = exsim.Server()
    port = server.get_port()
    print("Listening on port {0}".format(port))

    server.create_engine("default")
    server.create_endpoint("fix", 10101)
    server.set_endpoint_engine("fix", "default")

    server.load_protocol("fix42", "fix_protocol", "FixProtocol")
    server.set_endpoint_protocol("fix", "fix42")

    server.run()
    return


if __name__ == "__main__":
    main()
