exsim
=====

|  |Build Status|  |Code Health|  |Coverage|  |PyPI|  |Python|


Introduction
------------

# Exchange Simulator
#
# Run a basic event loop.
# Listen on a TCP socket, and accept connections.
# Decode messages according to protocol module for that session.
# Dispatch messages via central dispatcher.
# Support for automatic test-requests/heartbeats.
# Messages can be queued for manual handling.
# Policy modules can be loaded for automatic message handling.
# Basic matching engine will manage books, publish data, and match orders.


Usage
-----

In a Python unittest module, you should import the exsim module, and
create an instance of the API class.

You can then load any additional (third-party) plugins before
configuring and creating a server instance.  The server instance is
created by forking the calling process, so any Python setup or
environment variables, etc, that exist are inherited by the service.
All subsequent interaction with the service uses IPC.

Classes
-------

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

Plugins
-------

The basic framework can be extended with new matching engine
behaviours and protocol mappings using plugins: Python modules that
provide derived classes specialising the default behaviours.

Once imported, these modules can be registered with the framework
(using a 'register' function), and are then available from the
standard factory functions.


# Milestone 1
#
# - Accept protocol market data and trade flow connections
#   - Connect
#   - Disconnect
# - Accept management connections.
#   - Decide on a protocol.
#     - REST?
# - Read and queue data
# - Send data
# - Timeouts
# - Hearbeats
# - Logon & Logout
#
# This is sufficient to handle basic message flow to/from a venue.
# It's also basically a REST API on the side of RobotNPS ...

# Also needed is the client-side:
# - Use requests module.
#   - Completely synchronous RPC-style.
# - Spawn simulator process in background?

# Next thing needed is a pricing module: in order to generate a useful
# pricing stream, we need to have useful prices.  So that can either
# be managed directly via the API, or could track an externally
# sourced price stream.

The service starts with a control port listening for the management
protocol on a specified port.  The client API can connect to this
control port, and sends RPCs to the server.

There are no asynchronous events from the server: the client can poll
for queued events.  This simplifies the integration of the client API
with testing frameworks.

There is no configuration of the server other than via the client API.
This ensures that test case code represents the complete description
of the required environment.

Client Requests

create_engine name
delete_engine name
  Create or delete a matching engine.

set_engine_property engine_name property_name value
  Configure the engine.

create_endpoint name engine protocol
delete_endpoint name
  Create or delete a protocol endpoint, using a specified protocol,
  and attach it to the specified engine.

set_protocol_property endpoint_name property_name value
  Configure the protocol module.

create_book name engine symbol
delete_book name
  Create a book within a matching for trading of the specified instrument.

create_quote quote_id book_name
set_quote_property quote_id name value
submit_quote quote_id
delete_quote quote_id
  Manage a quote.

create_order order_id book_name
set_order_property order_id name value
submit_order order_id
delete_order order_id
  Manage an order.

match_orders book_name order_a order_b
  Match two orders.








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




.. |Build Status| image:: https://travis-ci.org/da4089/exsim.svg?branch=master
    :target: https://travis-ci.org/da4089/exsim
    :alt: Build status
.. |Code Health| image:: https://landscape.io/github/da4089/exsim/master/landscape.svg?style=flat
    :target: https://landscape.io/github/da4089/exsim/master
    :alt: Code Health
.. |Coverage| image:: https://coveralls.io/repos/github/da4089/exsim/badge.svg?branch=master
    :target: https://coveralls.io/github/da4089/exsim?branch=master
    :alt: Coverage
.. |PyPI| image:: https://img.shields.io/pypi/v/exsim.svg
    :target: https://pypi.python.org/pypi/exsim
    :alt: PyPI
.. |Python| image:: https://img.shields.io/pypi/pyversions/exsim.svg
    :target: https://pypi.python.org/pypi/exsim
    :alt: Python
