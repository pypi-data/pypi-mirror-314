#include "hellowidget.h"

#include <QHBoxLayout>
#include <QLabel>

HelloWidget::HelloWidget(QWidget *parent) : QWidget{parent}, m_label{new QLabel(this)}
{
    setMinimumHeight(100);

    m_label->setAlignment(Qt::AlignCenter);
    m_label->setStyleSheet(R"(QLabel {font-size: 24px; background-color: #F4EA56})");

    auto layout = new QHBoxLayout();
    layout->setContentsMargins(0, 0, 0, 0);
    layout->addWidget(m_label);
    setLayout(layout);
}

QString HelloWidget::name() const
{
    return m_name;
}

void HelloWidget::setName(const QString &newName)
{
    if (m_name == newName)
        return;
    m_name = newName;
    m_label->setText(hello());
    emit nameChanged(m_name);
}

QString HelloWidget::hello() const
{
    return QString("Hello %1!").arg(m_name);
}
