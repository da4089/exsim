

class PlugIn:
    """Defines the API between the simulator and a plugin module."""

    # The simulator can be customized using plugin modules to implement
    # order matching, and protocol implementations.  The APIs for these
    # functions are defined on a single interface, which can be partially
    # overridden as needed.
    #
    #

    # Order book
    #
    # A collection of orders, matched against each other.

    def add_order(self):
        pass

    def modify_order(self):
        pass

    def cancel_order(self):
        pass

    # Quote book
    #
    # A collection of quotes.  When an order matches a quote, send an
    # order request to the quote source, which can accept (send_order_filled)
    # or reject (send_order_canceled/send_order_rejected) the request.

    def add_or_update_quote(self):
        pass

    def withdraw_quote(self):
        pass

    def order_request(self):
        pass

    # Instrument master

    def instrument_definition(self):
        """Report the definition of an instrument."""
        pass

    def instrument_status_update(self):
        """Update the status of an instrument.

        Used for halts/resumes, etc."""
        pass

    # Order activity
    #
    # Used by order entry sessions to send acknowledgements and fills,
    # by order-based market data to publish book and trade updates, and
    # for drop copy sessions to publish trades.

    def send_login_response(self):
        """Accept or reject a login request."""
        pass

    def send_logout_response(self):
        """Accept or reject a logout request."""
        pass

    def send_order_added(self):
        """Confirm order added to book."""
        pass

    def send_order_modified(self):
        """Confirm order modified."""
        pass

    def send_order_canceled(self):
        """Confirm order canceled."""
        pass

    def send_order_filled(self):
        """Report a fill against an order."""
        pass

    def send_order_rejected(self):
        """Report an order being rejected."""
        pass

    def send_order_status(self):
        """Report current order status."""
        pass

    # Book events
    #
    # Used for quote-book style market data to report a change to the
    # book.

    def book_update(self):
        """Report change to level and side of order book."""
        pass
