#pragma once

#include <QWidget>

class QLabel;

class HelloWidget : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged FINAL)

  public:
    explicit HelloWidget(QWidget *parent = nullptr);

    QString name() const;
    void setName(const QString &newName);

    QString hello() const;

  signals:
    void nameChanged(const QString& name);

  private:
    QString m_name;
    QLabel* m_label;
};
