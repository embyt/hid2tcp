hid2tcp
=======

hid2tcp provides access to USB HID device using libhid via a TCP port.

To use this library you need to
- build libhid including its python binding
  - for this you need SWIG installed during build
  - some updates and fixes need to be applied to libhid to be able to build
    it successfully; they are commited into https://github.com/romor/libhid
