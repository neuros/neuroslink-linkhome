/****************************************************************************
**
** Copyright (C) 2009 Neuros Technology
**
** This file is part of the LinkHome Daemon project
**
** GNU Lesser General Public License Usage
** This file may be used under the terms of the GNU Lesser
** General Public License version 2.1 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL included in the
** packaging of this file.  Please review the following information to
** ensure the GNU Lesser General Public License version 2.1 requirements
** will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
**/

#include "appdaemon.h"
#include <QtDebug>
#include <QByteArray>
#include <QDBusConnection>
#include <stdlib.h>
#include <time.h>

AppDaemon::AppDaemon(QObject* parent)
: QObject(parent)
{
	new LinkHomeAdaptor(this);
	QDBusConnection dbus = QDBusConnection::sessionBus();
dbus.registerObject("/LinkHome",this);
	dbus.registerService("tv.neuros.LinkHome");

	// Read config file and setup first apps
	QFile configfile("/usr/lib/linkhome/linkappd.conf");
	if(configfile.exists())
	{

		qDebug() << "Processing config file";
		process_config(configfile);
	}
	else
	{

	}

	// Setup d-bus

}

void AppDaemon::AppStart(const QString& path, const QStringList& args, const QString& wd)
{
	qDebug() << "Application starting via dbus";
	start(path,args,NProcess::run_once,wd);
}

void AppDaemon::start(const QString& path, const QStringList& args, NProcess::Type option, const QString& wd)
{

	qDebug() << "Starting Application";

	NProcess *process = new NProcess(path,args,option);
	process->setWorkingDirectory(wd);
	if(process->start())
	{
		connect(process,SIGNAL(exited()),this,SLOT(appExited()));
	}
	else
	{
		appErrored();
		delete process;
	}
}

void AppDaemon::appErrored()
{
	// Send D-Bus statement saying application startup failed
	qDebug() << "App failed to start";
}

void AppDaemon::appExited()
{
	NProcess *process = (NProcess*)QObject::sender();

	if(process != NULL)
		delete process;

	qDebug() << "App has finished running";

}

void AppDaemon::appStarted()
{
	// Send D-Bus statement that the app started
		qDebug() << "App has started completely";
}


void AppDaemon::process_config(QFile& file)
{
	if(!file.open(QIODevice::ReadOnly | QIODevice::Text))
	{
		qDebug() << "Could not open config file: /usr/lib/linkhome/linkapp.conf";
		return;
	}

	while(!file.atEnd())
	{
		QByteArray line = file.readLine();
		if(!line.startsWith("#"))
		{
			QString conf(line);
			QStringList entry = conf.split(",",QString::SkipEmptyParts);
			if(entry.size() < 3)
			{
				qDebug() << "Found whitespace, or config error so doing nothing for this entry:" << conf;
			}
			else
			{
				QString workdir = entry.at(0);
				QString app = entry.at(1);
				QString option = entry.at( entry.size() - 2);
				QString sleeptime = entry.at(entry.size() - 1 );
				QStringList args;

				for(int i = 2; i < entry.size() - 2; i++)
				{
					args.append(entry.at(i));
				}
					
			
				start(app,args,(NProcess::Type)option.toInt(),workdir);
				
				// hardcode test to be sure linkhome did open.
				sleep(sleeptime.toInt());				

			}
		}
	}
}

void AppDaemon::Test()
{
	qDebug() << "Adaptor Test";
}
