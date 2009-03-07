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

#ifndef APPDAEMON_H
#define APPDAEMON_H



#include <QObject>
#include <QString>
#include <QStringList>
#include <QFile>

#include "nprocess.h"

class AppDaemon : public QObject
{

Q_OBJECT

public:
	AppDaemon();

public slots:
	void appStart(const QString&, const QStringList&, NProcess::Type);


private slots:
		void appExited();
		void appStarted();
		void appErrored();

private:
	void process_config(QFile&);

};

#endif // APPDAEMON_H
