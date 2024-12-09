* website: <https://arrizza.com/python-socket-oneline>
* installation: see <https://arrizza.com/setup-common>

## Summary

This module contains a simple base class for handling sockets

The communication protocol has these basic rules:

- socket based using TCPIP; only one server per port
- only one client connected at any time. When that client
  disconnects, another client is allowed to connect.
- a "packet" is terminated by a line feed (0x0A).
- a client sends a packet (aka "command") to the server.
- Alternatively the server may respond with zero, one or more
  packets (aka "responses")
- The server cannot initiate a response asynchronously by
  itself i.e. it must wait for an incoming command to send
  any packets to the client.
- the following commands are predefined:
    - "ping" : the server will respond with "pong". The client
      can use this to confirm that the socket and communication
      channel are alive and responsive
    - "disconnect" : the server will initiate a disconnect
      from the current client
    - "shutdown" : the server will disconnect and then
      shutdown
    - "invalid" - the server has caught an exception when
      converting the incoming packet to ASCII (e.g. decode
      ('utf-8'))

## More details

- The server reads the incoming characters from the client one
  character at a time.
- Once it sees the 0x0A character, it sets up a string
  buffer of all ASCII characters seen so far (less the 0x0A) and
  calls a callback function with that string.
- The user must define that callback function.
- The following is up to the user to define:
    - Which incoming commands are legal
    - What response to send if an illegal command is received
    - What response or responses should be sent for all legal
      commands
    - Determine whether an empty string is a legal command
    - How to handle the scenario when a linefeed needs to be
      part of a command
    - How to handle non-ASCII scenarios e.g. Unicode or byte
      strings.

## Scripts

* See [Quick Start](https://arrizza.com/user-guide-quick-start) for information on using scripts.
* See [xplat-utils submodule](https://arrizza.com/xplat-utils) for information on the submodule.

## Sample code

see the sample directory for a sample client and server. Use
doit script to run the sample server.

```
    ./doit
```

- starts a server as a background process
- starts a client and sends various commands to the server
- stops that client
- starts another client
- sends some additional commands to the server
- asks the server to shutdown

## Other scripts and files

- do_doc: generates doxygen
- do_install: installs python environment
- do_lint: runs static analysis tools
- do_publish: publish the python module
- do_ver: runs verification scripts
- doit: runs a sample client & server
- srs.json: holds a list of requirements the client/server
  must adhere to
- test_ver.py: run by do_ver to perform verification
- todo.md known issues to fix/address
