#! /usr/bin/env python

import exsim

def main():

    # Server
    server = exsim.Server()
    server.listen(11111)

    server.run()

    return
    
    # Matching engine.
    engine = exsim.Engine()

    # FIX gateway.
    fix_gateway = exsim.fix.Gateway()
    fix_gateway.set_engine(engine)

    fix_gateway.listen(10155)
    fix_gateway.listen(10156)

    # Run.
    fix_gateway.run()
    return

if __name__ == "__main__":
    main()
