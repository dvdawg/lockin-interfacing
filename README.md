# lockin-interfacing
Some code I wrote for interfacing with an SR510 Lock-In Amplifier. 

## Brief purpose overview
The interfacing is specifically geared for the **Spring 2024 ULAB** project I participated in, where a band-stop filter was connected to an LED to simulate the luminescence of an optically pumped NV-Center in the absence of Zeeman splitting. This luminescence was picked up by a photodiode circuit that filtered out a good amount of noise and passed current to the lock-in amplifier.

Here's a quick diagram of the circuit that the lock-in amplifier was connected to:
![The mock-NV and reading circuit](/README-assets/circuit.svg)
