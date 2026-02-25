# SXPL
X-Plane 12 remote control software

I'm working on making this FAA ATD compliant.

server.py should be running on the machine with X-Plane, and index.html should be used to communicate with it from the remote machine.

BATD requirement for variables to be controlled independently of the simulation (applicable to Cessna 172SP)

> The instructor must be able to pause the system at any time during the training simulation for the purpose of administering instruction or procedural recommendations.

* Aircraft geographic location,
* Aircraft heading,
* Aircraft airspeed,
* Aircraft altitude, and
* Wind direction, speed, and turbulence.

> The system must be capable of recording both a horizontal and vertical track of aircraft movement during the entire training session for later playback and review.

> The instructor must be able to disable any of the instruments prior to or during a training session and be able to simulate failure of any of the instruments without stopping or freezing the simulation to affect the failure. This includes simulated engine failures and the following aircraft systems failures: alternator or generator, vacuum or pressure pump, pitot static, electronic flight displays, or landing gear or flaps, as appropriate.

(AC 61-136B B.3.6.1-4)
