#! /usr/bin/env python

import exsim

def main():

    # Server
    server = exsim.Server(10101)
    server.run()

    return


if __name__ == "__main__":
    main()
