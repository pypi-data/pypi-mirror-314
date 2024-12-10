set(APP_NAME hello_widget_sample)

set(PROJECT_SOURCES
        main.cpp
        mainwindow.cpp
        mainwindow.h
        mainwindow.ui
)

qt_add_executable(
    ${APP_NAME}
    ${PROJECT_SOURCES}
)

target_link_libraries(
    ${APP_NAME} PRIVATE
    Qt6::Widgets
    _core_lib
)

# include(GNUInstallDirs)
install(TARGETS ${APP_NAME}
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
