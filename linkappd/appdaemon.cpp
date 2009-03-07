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

AppDaemon::AppDaemon()
{
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

void AppDaemon::appStart(const QString& fullpath, const QStringList& args, NProcess::Type option = NProcess::run_once, const QString& wd = "~/" )
{

	qDebug() << "Starting Application";

	NProcess *process = new NProcess(fullpath,args,option);
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
	else
	{
		qDebug() << "File was opened!";
	}
	while(!file.atEnd())
	{
		qDebug() << "End Not Found Yet";

		QByteArray line = file.readLine();
		if(!line.startsWith("#"))
		{
			QString conf(line);
			QStringList entry = conf.split(":",QString::SkipEmptyParts);
			if(entry.size() < 4)
				qDebug() << "Found whitespace, or config error";	
			else
			{
			qDebug() << "Config File List is: " + entry.at(0) + entry.at(1) + entry.at(2);
			
appStart(entry.at(0),entry.at(1),entry.at(2).split(","),entry.at(2).toInt())



			}

		}
		else
		{
			qDebug() << "Found line that starts with #";
		}

	}
}
