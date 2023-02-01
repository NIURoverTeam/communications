# communications
TCP server/client(s): Base station -> multiple Arduino devices (over ethernet, via Raspi/Jetson node)

## Notes / Scratchpad

### Controller Data Acquisition

#### GUI/Javascript Approach

https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API/Using_the_Gamepad_API

Do note that browsers cannot make vanilla TCP requests, only HTTP requests.  If we go this route, we will need to adapt the TCP server to accept HTTP requests and forward them over TCP.

#### Python/Server Approach

https://inputs.readthedocs.io/en/latest/user/quickstart.html

This lacks a true front-end, so a shell of a front end would be required.  The TCP server would have to be modified to send commands both over TCP and HTTP so that the browser can receive the data.


### Client/Server Assignment

Definitions: Fail-Safe: Assume all controls are set to zero if connection drop; Fail-Unsafe: Assume all controls remain the same if connection drop.

#### Polling Method 1

Jetson/Raspi is the client, and Base station is the server.

Client sends a request every 250ms to the base station requesting the full rover control state.

Client (Jetson/Raspi) determines Fail State: If no response from server, fail condition.

#### Polling Method 2

Base Station is the Client, and Jetson/Raspi is the Server.

Client sends a request every 250ms to the Jetson/Raspi with the full rover control state.

Server (Jetson/Raspi) determines Fail State: If client misses poll timeout, fail condition.

#### Instant Control Method

Base Station is the client, and Jetson/Raspi is the server.

Server sends a request whenever controller input is changed, could either be the full state or just the thing that changed.

Fail State is allways Unsafe: No way to determine fail condition.

#### Command Method

Base Station is the Client, and Jetson/Raspi is the Server.

Server sends a request indicating not the control state, but an approximation of what that control state would cause during 250ms; a command.
So, if the joystick is set to forwards, the command is "move forwards for 250ms at velocity 0.954".  The server then translates that to holding the joystick at that velocity for 250ms before resetting it to zero.

Fail State is allways Safe: Commands are scoped to a time limit.
