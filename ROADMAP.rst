=======
Roadmap
=======


* Structure
  * Daemon, able to emulate execution venues
  * UI executable, able to manage the daemon
  * Python API module, able to manage the daemon
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
   * Orders only (no quoting, etc)
   * Instrument types:
      * Standard
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
