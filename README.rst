
=====
exsim
=====

|  |Build Status|  |Docs|  |Coverage|  |PyPI|  |Python|
|  |PePY Downloads|  |PePY Monthly|

Introduction
------------

This is a simple financial exchange simulator.  It is intended for use
testing trading applications, protocol gateways, and the like.

It operates in two basic modes: standalone, or managed:

In standalone mode, the matching engine modules operate independently,
processing orders according to their implementation.  This mode is
intended for ad-hoc testing, demonstrations, etc.

In managed mode, the simulator is controlled by another process,
typically an integration test module, which can interact with the
matching engine to ensure that it implements a configured scenario
exactly.

Plugins
-------

The basic framework can be extended with new matching engine
behaviours and protocol mappings using plugins: Python modules that
provide derived classes specialising the default behaviours.

Once imported, these modules can be registered with the framework
(using a 'register' function), and are then available from the
standard factory functions.

Usage
-----

In a Python unittest module, you should import the exsim module, and
create an instance of the API class.

You can then load any additional (third-party) plugins before
configuring and creating a server instance.  The server instance is
created by forking the calling process, so any Python setup or
environment variables, etc, that exist are inherited by the service.
All subsequent interaction with the service uses IPC.

Design
------

* Run a basic event loop.
* Listen on one-or-more TCP sockets, and accept connections.
* Decode messages according to protocol module configured for that
  session.
* Dispatch messages via central dispatcher.
* Support for automatic test-requests/heartbeats.
* Messages can be queued for explicit handling in managed mode.
* Policy modules can be loaded for automatic message handling.
* Basic matching engine will manage books, publish data, and match
  orders.

Classes
^^^^^^^
Endpoint
  A listening socket, attached to a matching engine, and configured
  with a protocol to encode and decode received messages.

Session
  A socket connection, initiated by a client application.  Sessions
  are created by Endpoints, and inherit their Endpoint's Protocol and
  Engine.

Protocol
  An encoder and decoder that converts messages in a trading protocol
  (like, FIX or OUCH) into Python dictionaries that are passed to the
  matching engine for action.

  The protocol can optionally handle some of the "mechanics" of the
  communication: sequence numbers, heartbeats, etc.  But actual
  trading messages are simply translated and handed off to the engine.

Management Protocol
^^^^^^^^^^^^^^^^^^^
create_engine name class
  Create a matching engine of the specified class.

delete_engine name
  Delete a matching engine.

set_engine_property engine_name property_name value
  Configure the engine.

create_endpoint name engine protocol
  Create a listening protocol endpoint, using a specified protocol,
  and attach it to the specified engine.

delete_endpoint name
  Delete a listening endpoint.

set_protocol_property endpoint_name property_name value
  Configure the protocol module.

create_book name engine symbol
  Create a book within a matching for trading of the specified instrument.

delete_book name engine
  Delete a book from an engine.

create_quote quote_id engine book_name
  Create a (market maker) quote

set_quote_property quote_id name value
  Configure a quote

submit_quote quote_id
  Post a quote

delete_quote quote_id
  Remove a quote.

create_order order_id book_name
  Create an order

set_order_property order_id name value
  Configure an order

submit_order order_id
  Post an order.

delete_order order_id
  Manage an order.

match_orders book_name order_a order_b
  Match two orders.

The service starts with a control port listening for the management
protocol on a specified port.  The client API can connect to this
control port, and sends RPCs to the server.

There are no asynchronous events from the server: the client can poll
for queued events.  This simplifies the integration of the client API
with testing frameworks.

In managed mode, there is no configuration of the server other than via
the client API.  This ensures that test case code represents the
complete description of the required environment.

Roadmap
-------

M1
^^
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
^^
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
^^^^^^^

* Support acquiring instruments and pricing data from an external source.
   * Stream FIX (?) market data
   * Figure out how best to allow trading against those quotes/orders.
* Add ITCH/OUCH (with SOUP TCP) support to ensure the abstraction isn't
  too FIX-specific
* Add support for an RFQ workflow / matching engine.


License
-------
exsim is licensed under the GNU Public License.

While this is not legal advice, in short this means you're free to use
this code at no cost.  You may also change it and run the modifified
version, or integrate it with other code, but if you do you must not
distribute the changed code or a system that integrates this software
unless it is also made available under the GPL license.

Contributing
------------
Comments, suggestions, bug reports, bug fixes -- all contributions to
this project are welcomed.  See the project's `GitHub
<https://github.com/da4089/exsim>`_ page for access to the latest
source code, and please open an `issue
<https://github.com/da4089/exsim/issues>`_ for comments, suggestions,
and bugs.


.. |Build Status| image:: https://github.com/da4089/exsim/actions/workflows/build.yml/badge.svg?event=push
    :target: https://github.com/da4089/exsim/actions/workflows/build.yml
    :alt: Build status
.. |Docs| image:: https://readthedocs.org/projects/exsim/badge/?version=latest
    :target: http://exsim.readthedocs.io/en/latest/
    :alt: Docs
.. |Coverage| image:: https://coveralls.io/repos/github/da4089/exsim/badge.svg?branch=master
    :target: https://coveralls.io/github/da4089/exsim?branch=master
    :alt: Coverage
.. |PyPI| image:: https://img.shields.io/pypi/v/python-exsim.svg
    :target: https://pypi.python.org/pypi/python-exsim
    :alt: PyPI
.. |Python| image:: https://img.shields.io/pypi/pyversions/python-exsim.svg
    :target: https://pypi.python.org/pypi/python-exsim
    :alt: Python
.. |PePY Downloads| image:: https://pepy.tech/badge/exsim
    :target: https://pepy.tech/project/exsim
    :alt: PyPI Downloads
.. |PePY Monthly| image:: https://pepy.tech/badge/exsim/month
    :target: https://pepy.tech/project/exsim
    :alt: PyPI Monthly Downloads
