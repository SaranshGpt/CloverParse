# CloverParse

This is compiler that compiles from a custom user-freidly data packet-matcher notation to a custom light-weight notation developed for my other project: Cloverwatch

## Context
 
My other project cloverwatch sits on a serial wire, and performs ECC (error correction) and pattern matching on the passing packets. For the pattern matching part, I developer a light-weight notation that the device could recieve from the user via a cli. 

The notation worked as expected but the problem I ran into was the notation proved far too cumbersome to use manually, even for early testing. I could make it easier to write but that would've required more processing power on the device side, which I wanted to avoid. So, I created a compiler that could convert from a more user-freindly format to the light-weight format, to make testing easier

## Notation Format

The notation format is given below, for both the device and the user side.

https://docs.google.com/document/d/1FwUk3ItxqC4IM4umB8sDmGDQ2atQy4gYsMCZP7TYH60/edit?usp=sharing