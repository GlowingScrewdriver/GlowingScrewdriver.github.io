# Fast Charging Control on a Cable

## Why?
Modern charging tech can be scary. 100W of power seems needlessly (and dangerously) fast for a battery housed in something
that can fit one's palm. Fast charging is something I like to keep away from for the most part, especially since heat and
reduced longevity are well known to be side effects of fast charging.

There are means of restricting charging at the software level. Common methods on Android devices make use of sysfs nodes
exposed by the devices' own charging drivers. However, getting root access in order to employ such methods isn't always feasible.

## Fast Charging Negotiation and the Cable
Most, if not all, fast charging technologies require some kind of negotiation between the source (charger) and the sink (charged
device). There needs to be communication about what power modes the sink and source support, so that both can agree on and use the same charging
voltage and current. This is facilitated by the cable.

## Preventing Fast Charging
A USB cable has at least 4 lines within it: VBus and Ground for power supply, and D+ and D- for data transfer. D+ and D- carry complements of each
other (if the D+ signal is high, D- is low and vice-versa). The data lines are critical to the negotiation process prior to fast charging, so
simply cutting off one of them should prevent fast charging.

I tested this idea with my Nokia 6.1 (2018), a USB PD device, along with the original charger and cable. It worked!!


## Making it Cool
To make it a more useful hack, I soldered two pin connectors onto the two loose ends of the cut data line, so that I could
simply connect the loose ends whenever I wanted to use the cable for data transfer or the occasional fast charge requirement.
The cable eventually gave way, but with some effort it should have been possible to re-enforce and protect the soldered joints.
