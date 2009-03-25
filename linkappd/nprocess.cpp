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

#include "nprocess.h"
#include <QtDebug>

NProcess::NProcess(const QString& fullpath, const QStringList& args, NProcess::Type option):
process(NULL),apppath(fullpath),arguments(args),type(option),restarts(0),timer(NULL)
{
}

void NProcess::setType(NProcess::Type t)
{
	type = t;
}


bool NProcess::start()
{
	qDebug() << "Running NProcess::start()!";

	process = new QProcess();
	process->setWorkingDirectory(workingdir);
	process->closeWriteChannel();
	process->closeReadChannel(QProcess::StandardOutput);
	process->closeReadChannel(QProcess::StandardError);
	process->start(apppath,arguments);

	if(process->waitForStarted())
	{
		qDebug() << "NProcess:: Application Started!";
		emit started();

		if(type == NProcess::monitor)
		{
			qDebug() << "NProcess:: Use Monitor/Restart Slot";
			connect(process,SIGNAL(finished(int,QProcess::ExitStatus)),this,SLOT(restart(int,QProcess::ExitStatus)));
		}
		else
		{
			qDebug() << "NProcess:: Use Standard Slot";
			connect(process,SIGNAL(finished(int,QProcess::ExitStatus)),this,SLOT(ended(int,QProcess::ExitStatus)));
		}

		return true;
	}
	else
	{
		qDebug() << "NProcess:: Wait for Started Failed!";
		return false;
	}



}

void NProcess::restart(int code,QProcess::ExitStatus status )
{

	if( !timer.isActive())
	{
		qDebug() << "Init Timer !!!!!!!!!!!!!!!!!!!!!!!";
		timer.setSingleShot(true);
		timer.setInterval(10000);
		connect(&timer,SIGNAL(timeout()),this,SLOT(toManyRestarts() ) );
		timer.start();

	}

	qDebug() <<  "Restarted X times in 10 Seconds" << restarts;
	restarts++;

	qDebug() << "NProcess:: Restart Slot has Ran Codes are: Code: " + QString::number(code) + " Status: " + QString::number(status);

	if(process != NULL)
	{
		delete process;
	}

	start();
}

void NProcess::ended(int,QProcess::ExitStatus)
{
	emit exited();
}

NProcess::~NProcess()
{
	if(process != NULL)
		delete process;
}

void NProcess::setWorkingDirectory(const QString& dir)
{
	workingdir = dir;
}

void NProcess::toManyRestarts()
{
	if(restarts > 5)
	{
		qDebug() << "To Many Restarts!!!!!!!!!";

		disconnect(process);
	
		restarts = 0;
		emit exited();	

	}
	else
	{

		qDebug() << "Continue on my friend !!!!!!!!!";

		restarts = 0;
	}
}
