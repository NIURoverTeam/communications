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
