* website: <https://arrizza.com/python-gui-api-tkinter>
* installation: see <https://arrizza.com/setup-common>

## Summary

This module contains a set of simple base classes that can be
used for test or verification purposes on GUIs based on Tkinter.

A test harness can connect to this class using a TCPIP socket and
get the current screen content, press an x,y coordinate, and
invoke a menu item.

The typical scenario is to create a Tkinter GUI app and add the
gui-api-tkinter server into it. Then a test harness is built
using gui_api_harness and that is used by pytest (or whatever
other test driver you wish) to run tests against the GUI.

For a more detailed description of the available commands and
responses see gui_api.md

## Scripts

* See [Quick Start](https://arrizza.com/user-guide-quick-start) for information on using scripts.
* See [xplat-utils submodule](https://arrizza.com/xplat-utils) for information on the submodule.

## Sample code

See the sample directory for a sample client and server. Use
doit script to run the sample server.

```bash
./doit
```

This runs the code in the sample directory. The gui
subdirectory contains a sample Tkinter GUI app which has some
buttons and labels on it. The test harness is then used to
press buttons on the GUI and check that the GUI perform
s the expected behavior. The file sample/test_gui.py runs
those tests.

The pom/ subdirectory holds Page Object Model classes to
simplify the interactions between the test_gui code and the
GUI app.

For a more complex example, see ./ver directory. Invoke those tests using:

```bash
./do_ver
./do_ver -k tp001   # for the first test protocol
# etc.
```

## Other scripts and files

- do_doc: generates doxygen
- do_install: installs python environment
- do_lint: runs static analysis tools
- do_publish: publish the python module
- do_ver: runs verification scripts
- doit: runs a sample GUI client and a sample test harness
- srs.json: holds a list of requirements for the gui api and
  the test harness must adhere to
- todo.md known issues to fix/address
