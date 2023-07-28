=======
Roadmap
=======

* Structure
   * Daemon, able to emulate execution venues
      * PyInstaller executable?
      * Windows/Mac/Linux?
   * UI executable, able to manage the daemon
      * PyInstaller executable?
      * Windows/Mac/Linux?
      * PyQt5?
   * Python API module, able to manage the daemon
      * PyPI wheel?
   * Communicate via JSON over TCP?
* Entities
   * Venue
      * A venue trades a collection of Instruments
      * Offers one or more Endpoints
      * Defines a collection of features:
         * Order types
         * TIFs
         * etc
   * Instrument
      * A tradable thing.
      * Has only one asset class
      * Has one or more symbols
      * Has only one associated Book
   * Book
      * Maintains a collection of orders for an instrument
      * Matches orders to generate trades
      * Can generate market data
      * Can generate drop copies
      * Associated with only one Instrument
   * Bot
      * Performs automated trading activity
      * Associated with a Book
      * Can be implemented by a plugin
   * Session
      * A connection from a client to a venue
   * Endpoint
      * A network endpoint
      * The thing that a client will connect to
      * Hosts zero or more Sessions
      * Associated with only one Venue
* Add ability to define instruments
   * Different asset classes
      * Basic equity-style stuff
      * Options
      * Futures
      * FX spot
      * NDFs?
      * Crypto
   * Order types
      * Market
      * Limit
      * Pegs
      * Stops
      * Stop Limits
   * Various TIFs
   * Workflows
      * Taker
      * Maker
      * IOIs
      * RFQ/RFS
* Persist config
   * File?
   * Sqlite?
* Minimise work for v1.0

M1
==
* Basic FIX 4.x protocol module
   * Single orders only
   * Drop copy
   * Market data

* Basic simulation matching engine
   * Price-time matching
   * Taker workflow
   * Orders only (no quoting, etc)
   * Bots
      * Auto-fill
      * Auto-partial
      * Auto-reject
      * Auto-cancel
      * Partial-then-cancel
   * Activity levels
      * None (client application trading only)
      * Slow
      * Fast

* Read configuration from file
   * Basically a script of the same operations as possible via the
     (future) management protocol

M2
==
* Management protocol
   * REST?  WSS?
   * Logon authentication
   * Read and queue data for collection
   * Timeouts
   * Heartbeats

* Client-side API for Python
   * Use requests module?
      * Completely synchronous RPC-style.
   * Optionally, spawn simulator process in background

* Examples using unittest & pytest

Backlog
=======
* Support acquiring instruments and pricing data from an external source.
   * Stream FIX (?) market data
   * Figure out how best to allow trading against those quotes/orders.
* Add ITCH/OUCH (with SOUP TCP) support to ensure the abstraction isn't
  too FIX-specific
* Add support for an RFQ workflow / matching engine.
