#include <QtDBus>
#include <QApplication>
#include <QList>
#include <QString>
#include <QStringList>

int main(int argc, char *argv[])
{
	QString path = "/usr/bin/gqview";
	QStringList args;
	QString wd = "/home";
	QList<QVariant> argslist;
//	args.append("http://www.slashdot.org");

	argslist.append(path);
	argslist.append(args);
	argslist.append(wd);
	QApplication app(argc,argv);

	QDBusConnection dbus = QDBusConnection::sessionBus();
	QDBusMessage message = QDBusMessage::createMethodCall("tv.neuros.LinkHome","/LinkHome","tv.neuros.LinkHome","AppStart");
	message.setArguments(argslist);

	dbus.send(message);



	return app.exec();
}
