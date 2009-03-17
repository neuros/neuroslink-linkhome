/*
 * This file was generated by dbusxml2cpp version 0.6
 * Command line was: dbusxml2cpp -a linkhomeadaptor -c LinkHomeAdaptor tv.neuros.LinkHome.xml
 *
 * dbusxml2cpp is Copyright (C) 2008 Nokia Corporation and/or its subsidiary(-ies).
 *
 * This is an auto-generated file.
 * This file may have been hand-edited. Look for HAND-EDIT comments
 * before re-generating it.
 */

#ifndef LINKHOMEADAPTOR_H_1236498009
#define LINKHOMEADAPTOR_H_1236498009

#include <QtCore/QObject>
#include <QtDBus/QtDBus>
class QByteArray;
template<class T> class QList;
template<class Key, class Value> class QMap;
class QString;
class QStringList;
class QVariant;

/*
 * Adaptor class for interface tv.neuros.LinkHome
 */
class LinkHomeAdaptor: public QDBusAbstractAdaptor
{
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "tv.neuros.LinkHome")
    Q_CLASSINFO("D-Bus Introspection", ""
"  <interface name=\"tv.neuros.LinkHome\" >\n"
"    <signal name=\"errored\" />\n"
"    <signal name=\"exited\" />\n"
"    <signal name=\"started\" />\n"
"    <method name=\"Test\" />\n"
"    <method name=\"AppStart\" >\n"
"      <arg direction=\"in\" type=\"s\" name=\"path\" />\n"
"      <arg direction=\"in\" type=\"as\" name=\"args\" />\n"
"      <arg direction=\"in\" type=\"s\" name=\"wd\" />\n"
"    </method>\n"
"    <method name=\"AppStart\" >\n"
"      <arg direction=\"in\" type=\"s\" name=\"path\" />\n"
"      <arg direction=\"in\" type=\"as\" name=\"args\" />\n"
"    </method>\n"
"    <method name=\"AppStart\" >\n"
"      <arg direction=\"in\" type=\"s\" name=\"path\" />\n"
"    </method>\n"
"  </interface>\n"
        "")
public:
    LinkHomeAdaptor(QObject *parent);
    virtual ~LinkHomeAdaptor();

public: // PROPERTIES
public Q_SLOTS: // METHODS
    void AppStart(const QString &path);
    void AppStart(const QString &path, const QStringList &args);
    void AppStart(const QString &path, const QStringList &args, const QString &wd);
    void Test();
Q_SIGNALS: // SIGNALS
    void errored();
    void exited();
    void started();
};

#endif