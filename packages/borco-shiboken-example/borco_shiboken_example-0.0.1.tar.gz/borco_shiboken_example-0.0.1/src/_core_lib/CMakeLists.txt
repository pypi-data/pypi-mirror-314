set(LIB_NAME _core_lib)
set(LIB_COMPILE_DEFINITION _CORE_LIB_LIBRARY)

qt_add_library(${LIB_NAME} STATIC
    hellowidget.h
    hellowidget.cpp
)

target_include_directories(
    ${LIB_NAME} PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(
    ${LIB_NAME} PUBLIC
    Qt6::Widgets
)

target_compile_definitions(${LIB_NAME} PRIVATE ${LIB_COMPILE_DEFINITION})
