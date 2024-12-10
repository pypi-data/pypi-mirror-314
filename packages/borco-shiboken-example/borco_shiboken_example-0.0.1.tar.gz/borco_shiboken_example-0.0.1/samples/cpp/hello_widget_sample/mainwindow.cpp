#include "mainwindow.h"
#include "./ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), m_ui(new Ui::MainWindow)
{
    m_ui->setupUi(this);

    // connect some signals
    connect(m_ui->widgetNameEdit, &QLineEdit::textEdited, m_ui->widget, &HelloWidget::setName);
    connect(m_ui->widget, &HelloWidget::nameChanged, m_ui->widgetNameLabel, &QLabel::setText);

    // make sure we start with the correct name, if the widgetNameEdit was set in the .ui
    m_ui->widget->setName(m_ui->widgetNameEdit->text());
}

MainWindow::~MainWindow()
{
    delete m_ui;
}
