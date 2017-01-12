#! /usr/bin/env python

import exsim

def main():

    # Server
    server = exsim.Server()
    #server.listen(11111)
    server.run()

    return
    

if __name__ == "__main__":
    main()
