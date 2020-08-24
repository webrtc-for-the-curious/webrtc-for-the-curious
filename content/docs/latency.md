# Latency

## Definition 

L = Δt = t`Observe` - t`Happen`

Latency is the time between an event actually happening and its observation. More specifically for video, latency is the time between an event happening to the receipt of a complete, understood frame displayed on a screen of a receiver.
For example: the sender points a web camera to a wall clock ticking, captures the clock to video frames, encodes them and transmits  video data over cellular and the receiver receives it over wired connection, decodes and displays on screen.

By this definition, the time from the hand ticking on the clock to it being displayed on receivers's monitor is end-to-end video latency.

The time from the transmission of a frame to reception of that frame is the sender-to-receiver time.

## Why is it important?
On one hand the purpose of live video stream can be just informing of the current state of the world while no decisions are being made based on the information received. On the other hand ultra low latency live video streams can be used to remotely control a device where presence of a human being is either impossible or cost prohibitive. 
Importance of keeping end-to-end latency to a minimum increases with the cost of a mistake of an untimely decision based on out of date information.

For example a weather station’s camera live streaming current weather conditions may be delayed by minutes whereas a remote controlled flying drone or a vehicle may not be safely operated at latencies above 500 milliseconds. In the later case the difference between low and  high latency may literally be life or death defining. 
Both extreme cases are here to demonstrate the spectrum of importance, however the most common case for live media now are web conferencing where high latency is rarely life threatening. However delayed video and/or audio creates impedance to productive conversation which is often uncomfortable enough to prevent people from using the internet as means for communication. Which in times of global pandemic (2020) may mean lost opportunities and revenues.

Thus measuring latency and providing real-time feedback to the remote operator may affect their decision, similarly we should also consider limiting the operator input affecting safety critical or otherwise high value decisions to a level where there is no human input as a human could not detect or deal with significantly delayed signal.

## How do you measure latency?

True latency is supposed to be measured end-to-end. That is, not just the latency of the network path between sender and receiver, but the latency combined latency of camera capture, frame encoding, transmission, receipt, decoding and display as well as  possible queueing between any of the steps. 

One way to measure end-to-end latency is when sender and receiver are in the same frame of reference.  

### Experiment 1 - Camera and end-to-end latency
[TODO]
Conclusion: changing camera intrinsic settings like auto exposure and content of image being shot affects latency in 84-185 msec range

### Experiment 2 - WebRTC on same wifi
[TODO]
Conclusion: Adding encode and transmission steps jumps latency to about 300 msec. Measuring approach works in the multihost case. 

### Experiment 3 - WebRTC over LTE
[TODO]
I am going to call myself on Zoom, but my laptop is going through an LTE hotspot on my phone.

Adding encode and transmission over LTE increases latency to 400-700 msec. Changing network conditions are captured by the measurement. 

I have demonstrated my approach to measuring latency. The main trick is to put both Event and its Observer in the same frame of reference and field of view. 
The upside of the approach is that it provides the most real-world “what you see is what you get” measurement, experiments are easy to conduct and results are obvious to audiences without specialized knowledge. It does not rely on expensive and unreliable time synchronization or any kind of time awareness on either sender or receiver. 

The approach has one HUGE drawback however - it is manual as well as it requires both sender and receiver to be located in the same place.
Let’s discuss automation ideas as next steps.

## Latency measurement automation
While one could theoretically measure latency of each component of a live video transmission pipeline separately and then sum all latencies in practice at least some components are either inaccessible for instrumentation or produce significantly different results when measured outside of such pipeline. Variable queue depths between pipeline stages, network topology and  camera exposure changes are just a few examples of components affecting end-to-end latency. 

## Good enough automatic latency measurement

If/when you can trade off some imprecision of latency measurements for automation you may use a method inspired by networking protocol for clock synchronization between computer systems over packet-switched, variable-latency data networks - the Network Time Protocol (NTP).

### Latency measurement with WebRTC built-in stats
[TODO: chrome does not implement all necessary WebRTC stats yet, refer to next chapter for the workaround method]
TODO: Talk about sender reports, NTP and RTP timestamps, how they are supposed to be exposed in WebRTC apis being discussed.

### Latency measurement with NTP inspired time synchronization
```
      tSV      tS                       tR
       |       |                        |
       |       |             <--(tR1)-- + [tR1]
       |       | <-----------           |
[tSV1] + [tS1] +                        |
       |       | ---->                  |
       |       |     --(tR1,tS1,tSV1)-> + [tR2]
       |       |                        |

RTT = tR2 - tR1
sender_local_clock_at_tR2 = tS1 + RTT / 2
```

Given a communication channel between sender and receiver (eg [DataChannel](https://webrtc.org/getting-started/data-channels)) receiver may create a model of the sender’ monotonic clock by following the below protocol.
1. At time `tR1` receiver sends a message its local monotonic clock timestamp. 
2. When received at sender local time `tS1` the sender responds with a copy of `tR1` as well as sender’s `tS1` and
 sender’s video track time `tSV1`. 
3. At time `tR2` on receiving end round trip time is calculated by subtracting the message’s  send and receive times. `RTT = tR2 - tR1`
4. Round trip time `RTT` together with sender local timestamp `tS1` is enough to create an estimation of sender's monotonic clock. Current time on sender at time `tR2` would be equal to `tS1` plus half of round trip time.  
5. Sender's local clock timestamp `tS1` paired with video track timestamp `tSV1` together with round trip time `RTT` is therefore enough to sync receiver video track time to sender video track. 

