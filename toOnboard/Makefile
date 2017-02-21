LIBSRCS = DJI_API.cpp \
          DJI_App.cpp \
          DJI_Camera.cpp \
          DJI_Codec.cpp \
          DJI_Flight.cpp \
          DJI_Follow.cpp \
          DJI_HardDriver.cpp \
          DJI_HotPoint.cpp \
          DJI_Link.cpp \
          DJI_Memory.cpp \
          DJI_Mission.cpp \
          DJI_VirtualRC.cpp \
          DJI_WayPoint.cpp

SRCS = main.cpp \
       LinuxThread.cpp \
       LinuxSerialDevice.cpp \
       LinuxSetup.cpp \
       LinuxCleanup.cpp \
       LinuxMobile.cpp \
       LinuxFlight.cpp \
       LinuxWaypoint.cpp\
       LinuxInteractive.cpp\
       ReadUserConfig.cpp\
       $(LIBSRCS)

OBJS = $(SRCS:.cpp=.o)

TARGET = ../a

LIBDIR = /home/odroid/Onboard-SDK/lib

CC = g++
INC = -I$(LIBDIR)/inc -Iinc
CXXFLAGS = --std=c++11 $(INC) -I/usr/local/include -pthread -lrt -g 
LDFLAGS = -Wl,-rpath,./ -L./ -L/usr/local/lib/
VPATH = /home/odroid/Onboard-SDK/platform:src:inc:$(LIBDIR)/src:$(LIBDIR)/inc

$(TARGET) : $(addprefix objs/, $(OBJS))
	$(CC) -o $@ $(CXXFLAGS) $^ $(LDFLAGS)

objs/main.o : src/main.cpp
	$(CC) -o $@ -c $< $(CXXFLAGS)

objs/%.o : %.cpp %.h
	$(CC) -o $@ -c $< $(CXXFLAGS)

clean :
	rm -f objs/* $(TARGET)
