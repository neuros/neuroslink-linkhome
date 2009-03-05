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

#ifndef NPROCESS_H
#define NPROCESS_H

#include <QObject>
#include <QString>
#include <QStringList>

#include <QProcess>

class NProcess : public QObject
{

Q_OBJECT

public:

	enum Type { run_once, monitor, test };

	NProcess(const QString&, const QStringList&, Type);
	~NProcess();

	bool start();
	void setType(Type);

private slots:
	void restart(int,QProcess::ExitStatus);
	void ended(int,QProcess::ExitStatus);


private:
	QProcess *process;
	QString apppath;
	QStringList arguments;
	Type type;

signals:
	void error();
	void started();
	void exited();

};

#endif // NPROCESS_H
