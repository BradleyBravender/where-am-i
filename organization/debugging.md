# Debugging
The purpose of this document is to track all encountered obstacles and solutions so that no problem must be solved twice.

Presented in the following format, with each obstacle block seperated by an empty line:

## Obstacle
### Problem
Problem explanation and error messages.
### Solution
Solution explanation.

---

## Obstacle
### Problem
When uploading a sketch, I received the error `avrdude: ser_open(): can't open device "/dev/ttyUSB0": Permission denied`.
### Solution
Run:
```sudo usermod -a -G tty <USERNAME>
sudo usermod -a -G dialout <USERNAME>
```
Then logout and log back in.

---
