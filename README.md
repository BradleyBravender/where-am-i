# where-am-i
Trilateration based localization for instances where SLAM and Differential GPS are not sufficient.

## Roadmap
A proposed roadmap for this project is as follows (adapted from the February 1 meeting minutes):

### Summer 2025
- [ ] Order the necessary microcontrollers, microphones, and speakers
- [ ] Develop a distance prediction method between a beacon and target
- [ ] Investigate the relationship between the number of back and forth pings and uncertainty (ex. does pinging back and forth x times and then dividing the total elapsed time by x reduce the uncertainty of the measurement?)
- [ ] Develop a handshake method between a beacon and target (using radio modules)
- [ ] Localize and handshake between 2 beacons and a target
- [ ] Localize and handshake betweeen 3 beacons and a target
- [ ] Creat a way to map each beacon relative to each other
- [ ] Create a mapping software
- [ ] Integrate with ROS for visualization

### Future Work
- [ ] If the project shows promise and fosters interest, find a professor to continue its development, especially in regards to a radio-wave version
- [ ] Develop a method of self localization in order for beacons to localize themselves with respect to each other (or an origin)
- [ ] Consider pursuing 3-D localization
- [ ] Develop a more sophisticated mapping system in ROS, perhaps with pseudo-GPS coordinates

