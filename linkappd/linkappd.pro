# -------------------------------------------------
# Project created by QtCreator 2009-03-04T15:18:14
# -------------------------------------------------
QT += network \
    script \
    sql \
    xml \
    xmlpatterns \
    testlib \
    dbus
QT -= gui
TARGET = linkappd
CONFIG += console
CONFIG -= app_bundle
TEMPLATE = app
SOURCES += main.cpp \
    appdaemon.cpp \
    nprocess.cpp \
    linkhomeadaptor.cpp

HEADERS += appdaemon.h \
    nprocess.h \
    linkhomeadaptor.h
