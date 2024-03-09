# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /opt/homebrew/Cellar/cmake/3.28.3/bin/cmake

# The command to remove a file.
RM = /opt/homebrew/Cellar/cmake/3.28.3/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/build

# Include any dependencies generated for this target.
include core/CMakeFiles/apriltag_demo.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include core/CMakeFiles/apriltag_demo.dir/compiler_depend.make

# Include the progress variables for this target.
include core/CMakeFiles/apriltag_demo.dir/progress.make

# Include the compile flags for this target's objects.
include core/CMakeFiles/apriltag_demo.dir/flags.make

core/CMakeFiles/apriltag_demo.dir/apriltag_demo.c.o: core/CMakeFiles/apriltag_demo.dir/flags.make
core/CMakeFiles/apriltag_demo.dir/apriltag_demo.c.o: /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/core/apriltag_demo.c
core/CMakeFiles/apriltag_demo.dir/apriltag_demo.c.o: core/CMakeFiles/apriltag_demo.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object core/CMakeFiles/apriltag_demo.dir/apriltag_demo.c.o"
	cd /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/build/core && /Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT core/CMakeFiles/apriltag_demo.dir/apriltag_demo.c.o -MF CMakeFiles/apriltag_demo.dir/apriltag_demo.c.o.d -o CMakeFiles/apriltag_demo.dir/apriltag_demo.c.o -c /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/core/apriltag_demo.c

core/CMakeFiles/apriltag_demo.dir/apriltag_demo.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/apriltag_demo.dir/apriltag_demo.c.i"
	cd /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/build/core && /Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/core/apriltag_demo.c > CMakeFiles/apriltag_demo.dir/apriltag_demo.c.i

core/CMakeFiles/apriltag_demo.dir/apriltag_demo.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/apriltag_demo.dir/apriltag_demo.c.s"
	cd /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/build/core && /Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/core/apriltag_demo.c -o CMakeFiles/apriltag_demo.dir/apriltag_demo.c.s

# Object files for target apriltag_demo
apriltag_demo_OBJECTS = \
"CMakeFiles/apriltag_demo.dir/apriltag_demo.c.o"

# External object files for target apriltag_demo
apriltag_demo_EXTERNAL_OBJECTS =

apriltag_demo: core/CMakeFiles/apriltag_demo.dir/apriltag_demo.c.o
apriltag_demo: core/CMakeFiles/apriltag_demo.dir/build.make
apriltag_demo: lib/libapriltag.dylib
apriltag_demo: core/CMakeFiles/apriltag_demo.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable ../apriltag_demo"
	cd /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/build/core && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/apriltag_demo.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
core/CMakeFiles/apriltag_demo.dir/build: apriltag_demo
.PHONY : core/CMakeFiles/apriltag_demo.dir/build

core/CMakeFiles/apriltag_demo.dir/clean:
	cd /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/build/core && $(CMAKE_COMMAND) -P CMakeFiles/apriltag_demo.dir/cmake_clean.cmake
.PHONY : core/CMakeFiles/apriltag_demo.dir/clean

core/CMakeFiles/apriltag_demo.dir/depend:
	cd /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/core /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/build /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/build/core /Users/matthewmcauley/cornell/cup-robotics/cs-rereminibot/vision/apriltag-py/build/core/CMakeFiles/apriltag_demo.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : core/CMakeFiles/apriltag_demo.dir/depend

