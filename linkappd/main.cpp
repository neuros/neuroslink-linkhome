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

#include <QtCore/QCoreApplication>
#include "appdaemon.h"
#include "nprocess.h"
#include <QtDebug>

int main(int argc, char *argv[])
{
	qDebug() << "Starting Application";

	QCoreApplication a(argc, argv);
	
	AppDaemon *app = new AppDaemon();

	return a.exec();
}
