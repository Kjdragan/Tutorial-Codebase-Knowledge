# Chapter 9: Organizing the Details - Headers

In [Chapter 8: The Handshake Invitation and Reply - Request / Response (HTTP/1.1)](08_request___response__http_1_1_.md), we saw that the WebSocket handshake uses special `Request` and `Response` messages. We also learned that these messages contain important details called "headers" – things like `Host`, `Upgrade`, `Connection`, and the special WebSocket keys.

You might think, "Headers are just key-value pairs, like `Host: example.com`. Couldn't we just use a standard Python dictionary (`dict`) to store them?" That's a great question! While a dictionary seems close, HTTP headers have a couple of tricky rules that make a regular `dict` not quite suitable. Let's see why.

## What Problem Does `Headers` Solve?

Imagine you have a filing cabinet for storing notes about a project. You want to organize these notes using folder labels (like header names) and put pieces of paper inside (like header values). A standard Python dictionary is like a basic filing cabinet, but it has two limitations when dealing with HTTP headers:

1.  **Case-Insensitivity:** In the world of HTTP, the *name* of a header doesn't care about uppercase or lowercase letters. The header `Host` is considered exactly the same as `host` or `HOST`. A standard Python dictionary, however, *is* case-sensitive (`my_dict['Host']` is different from `my_dict['host']`). If we used a regular dictionary, we might accidentally store both `Host` and `host` as separate entries, which would be wrong according to HTTP rules.

2.  **Multiple Values for the Same Name:** Sometimes, a single HTTP message needs to include the same header name multiple times with different values. A common example is the `Set-Cookie` header used to send multiple cookies from a server to a browser. During the WebSocket handshake, the client might propose multiple protocols using `Sec-WebSocket-Protocol: chat, superchat`, or the server might list multiple supported protocols. A standard Python dictionary only allows one value per key – if you set the same key twice, the second value simply replaces the first.

We need a smarter filing cabinet! One that automatically treats "Host", "host", and "HOST" as the same folder label, and allows us to put multiple pages (values) inside a single folder if needed.

This is exactly what the `Headers` object in the `websockets` library does. It's a specialized, dictionary-like data structure designed specifically to handle the quirks of HTTP headers correctly.

## Meet the `Headers` Object: The Smart Filing Cabinet

The `Headers` object acts like a Python dictionary but with these superpowers:

*   **Case-Insensitive Keys:** When you look up a header, `headers['Host']` will find the value regardless of whether it was originally stored as `Host`, `host`, or `hOsT`.
*   **Multiple Value Support:** It remembers *all* values associated with a header name, keeping them in the order they appeared.

It's used internally by the [Request](08_request___response__http_1_1_.md) and [Response](08_request___response__http_1_1_.md) objects to store the headers for the handshake messages.

## How to Use `Headers` (Mostly for Reading)

You typically won't create `Headers` objects yourself unless you're doing very advanced customization. Most often, you'll interact with them when you inspect the handshake details attached to your connection object, like we saw briefly in Chapter 8.

Let's revisit that server example where we wanted to read headers sent by the client during the handshake:

```python
# example/asyncio/server_read_headers.py (Handler focus)
import asyncio
from websockets.asyncio.server import serve
# Import the Headers class (though often you just use the object you get)
from websockets.datastructures import Headers
from websockets.exceptions import MultipleValuesError

async def handler(websocket):
    # 'websocket' is the ServerConnection
    initial_request = websocket.request
    if initial_request:
        # Access the headers - this IS our Headers object!
        client_headers: Headers = initial_request.headers
        print(f"Client connected from path: {initial_request.path}")

        # --- Accessing Headers ---

        # 1. Get a single value (case-insensitive)
        #    This works whether the client sent 'Host' or 'host'
        try:
            host_header = client_headers['Host']
            print(f"  Host header value: {host_header}")
        except KeyError:
            print("  Host header not found.")
        except MultipleValuesError:
            # This shouldn't happen for 'Host', but good practice for others
            print("  Host header found multiple times (unexpected!).")

        # 2. Safely get a single value using .get()
        #    Returns None if not found, avoiding KeyError
        user_agent = client_headers.get('User-Agent') # Case doesn't matter
        if user_agent:
            print(f"  Client User-Agent: {user_agent}")
        else:
            print("  User-Agent header not found.")

        # 3. Get ALL values for a header (useful for duplicates)
        #    Imagine client sent: Sec-WebSocket-Protocol: chat, superchat
        #    Or two separate headers:
        #    Sec-WebSocket-Protocol: chat
        #    Sec-WebSocket-Protocol: superchat
        protocols = client_headers.get_all('Sec-WebSocket-Protocol')
        if protocols:
            print(f"  Client proposed protocols: {protocols}") # Output: ['chat', 'superchat']
        else:
            print("  Client didn't propose any subprotocols.")

        # 4. Iterate through all headers (name is original case, value is combined if multiple)
        print("\n  All Headers (name, value):")
        for name, value in client_headers.items():
            print(f"    {name}: {value}")
        # Note: .items() might combine multiple values into one string here.
        # For raw access preserving duplicates, use raw_items()

        print("\n  All Headers (raw name, raw value):")
        for raw_name, raw_value in client_headers.raw_items():
            print(f"    {raw_name}: {raw_value}")


    # ... rest of handler logic ...
    async for message in websocket:
        await websocket.send(message)

# ... (Server setup code) ...
```

**Explanation:**

1.  `client_headers = initial_request.headers`: We get the `Headers` object associated with the client's request.
2.  `client_headers['Host']`: Standard dictionary-like access. It's case-insensitive. Be aware it raises `KeyError` if the header isn't found and `MultipleValuesError` if the header exists more than once (use a `try...except` block).
3.  `client_headers.get('User-Agent')`: A safer way to get a single value. It returns `None` if the header isn't found or if it has multiple values (use `get_all` for multiple values). It's also case-insensitive.
4.  `client_headers.get_all('Sec-WebSocket-Protocol')`: The specific method to get *all* values associated with a header name. It always returns a list (which might be empty if the header wasn't present). This is crucial when you expect multiple values.
5.  `client_headers.items()`: Iterates through headers like a dictionary. Note that the *name* preserves its original casing from the first time it was added. The *value* might be a single value or potentially a combination if multiple existed.
6.  `client_headers.raw_items()`: Iterates through *all* header entries exactly as they were received or added, preserving duplicate names and their original casing. This gives you the most accurate view of the raw headers.

The same methods apply if you were inspecting `websocket.response.headers` on the client side.

## Under the Hood: The Dual Structure

How does the `Headers` object achieve both case-insensitive lookup *and* preservation of duplicates and order? It cleverly uses two internal data structures:

1.  **A List (`_list`):** It keeps a simple list of `(name, value)` tuples, exactly in the order headers were added. This preserves the original casing of names, the exact values, and allows for duplicate names. The `raw_items()` method iterates directly over this list.
2.  **A Dictionary (`_dict`):** It also maintains an internal dictionary where the keys are the *lower-cased* header names. The values in this dictionary are *lists* of all the values associated with that lower-cased name. This dictionary allows for fast, case-insensitive lookups. Methods like `__getitem__`, `get()`, and `get_all()` use this dictionary.

**Simplified Lookup Process (Conceptual):**

When you do `headers['Host']`:
1.  It takes `'Host'` and converts it to lowercase: `'host'`.
2.  It looks up `'host'` in the internal dictionary (`_dict`).
3.  If not found, raise `KeyError`.
4.  If found, it gets the list of associated values (e.g., `['example.com']`).
5.  It checks the length of this list.
6.  If the list has exactly one item, return that item (`'example.com'`).
7.  If the list has more than one item, raise `MultipleValuesError`.

When you do `headers.get_all('Sec-WebSocket-Protocol')`:
1.  It takes `'Sec-WebSocket-Protocol'` and converts it to lowercase: `'sec-websocket-protocol'`.
2.  It looks up `'sec-websocket-protocol'` in the internal dictionary (`_dict`).
3.  If not found, return an empty list `[]`.
4.  If found, return the list of associated values (e.g., `['chat', 'superchat']`).

**Code Glimpse:**

Let's look at the definition in `src/websockets/datastructures.py`:

```python
# src/websockets/datastructures.py (Simplified Structure)

from collections.abc import MutableMapping
from typing import Iterator, Union, Iterable, Mapping # ... and others

class MultipleValuesError(LookupError):
    """Raised when Headers has multiple values for a key."""
    # ... (error message formatting) ...

class Headers(MutableMapping[str, str]):
    """Efficient data structure for manipulating HTTP headers."""

    __slots__ = ["_dict", "_list"] # Optimization: defines allowed attributes

    def __init__(self, *args: HeadersLike, **kwargs: str) -> None:
        # Internal dictionary for quick, case-insensitive lookups.
        # Keys are lowercased names, values are lists of actual values.
        self._dict: dict[str, list[str]] = {}

        # Internal list to preserve order, casing, and duplicates.
        # Stores tuples of (original_name, value).
        self._list: list[tuple[str, str]] = []

        # Allow initialization like a regular dict (e.g., Headers({'Host': 'a'}))
        self.update(*args, **kwargs)

    # --- Main Access Methods ---

    def __getitem__(self, key: str) -> str:
        # 1. Look up lowercased key in the internal dict
        value_list = self._dict[key.lower()]
        # 2. Check how many values were found
        if len(value_list) == 1:
            return value_list[0] # Return the single value
        else:
            raise MultipleValuesError(key) # Too many values!

    def __setitem__(self, key: str, value: str) -> None:
        # 1. Add the value to the list associated with the lowercased key
        self._dict.setdefault(key.lower(), []).append(value)
        # 2. Add the (original_name, value) pair to the internal list
        self._list.append((key, value))

    def get_all(self, key: str) -> list[str]:
        """Return the (possibly empty) list of all values for a header."""
        # Directly return the list from the internal dict (or empty list)
        return self._dict.get(key.lower(), [])

    def raw_items(self) -> Iterator[tuple[str, str]]:
        """Return an iterator of all values as (name, value) pairs."""
        # Iterate over the internal list that preserves everything
        return iter(self._list)

    # --- Other dict-like methods ---

    def __contains__(self, key: object) -> bool:
        # Check existence using the lowercased key in the internal dict
        return isinstance(key, str) and key.lower() in self._dict

    def __iter__(self) -> Iterator[str]:
        # Iterate over the unique (lowercased) keys from the internal dict
        return iter(self._dict)

    def __len__(self) -> int:
        # Length is the number of unique (lowercased) keys
        return len(self._dict)

    def __delitem__(self, key: str) -> None:
        # 1. Remove from the internal dict
        key_lower = key.lower()
        del self._dict[key_lower]
        # 2. Rebuild the internal list excluding the deleted key (slow!)
        self._list = [(k, v) for k, v in self._list if k.lower() != key_lower]

    # ... other methods like update(), copy(), serialize(), __str__, __repr__ ...

    def serialize(self) -> bytes:
        # Helper to convert all headers back into bytes for sending
        # Uses the internal _list to preserve order and duplicates
        return str(self).encode() # str() method formats using _list

# Type hint for things that can initialize Headers
HeadersLike = Union[Headers, Mapping[str, str], Iterable[tuple[str, str]], ...]
```

This simplified view shows the two internal structures (`_dict`, `_list`) and how the key methods like `__getitem__`, `__setitem__`, `get_all`, and `raw_items` use them to provide the desired behavior.

## Conclusion

You've learned about the `Headers` object, the specialized "smart filing cabinet" used by `websockets` to handle HTTP headers during the handshake.

*   It solves the problems of **case-insensitivity** and **multiple values** for header names, which standard Python dictionaries don't handle correctly for HTTP.
*   It provides dictionary-like access (`headers['Name']`, `headers.get('Name')`) but is case-insensitive.
*   Use `headers.get_all('Name')` to correctly retrieve all values when duplicates are possible.
*   Use `headers.raw_items()` to see the headers exactly as they were received or added.
*   It works internally by using both a list (for order/duplicates) and a dictionary (for fast, case-insensitive lookup).
*   You primarily interact with it when reading `request.headers` or `response.headers` on a connection object.

Understanding `Headers` helps clarify how the library correctly parses and formats the critical details within the [Request / Response (HTTP/1.1)](08_request___response__http_1_1_.md) messages used in the handshake.

Now that we've covered the handshake details (Protocols, Request/Response, Headers), let's zoom out slightly and look at the core engine that actually interprets the WebSocket byte stream *after* the handshake is complete.

Up next: [Chapter 10: The Core Rules Engine - Protocol (Core)](10_protocol__core_.md)

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)