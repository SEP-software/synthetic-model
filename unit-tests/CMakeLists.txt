cmake_minimum_required(VERSION 3.1)
project(buffers-utest)

set(GTEST_SRCDIR ${CMAKE_CURRENT_SOURCE_DIR}/../external/genericIO/external/buffers/external/googletest/googletest)
set(GTEST_BUILDDIR ${CMAKE_CURRENT_BUILD_DIR}/../external/genericIO/external/buffers/external/googletest/googlemock/gtest)
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/../libCXX")
include_directories("${GTEST_SRCDIR}/include")


#cmake_policy(SET CMP0083 NEW)
  if (APPLE)
    add_definitions(-DGTEST_USE_OWN_TR1_TUPLE)
    add_definitions(-D__GLIBCXX__)
  endif (APPLE)

add_executable(basicTest basicTest.cc)
target_link_libraries(basicTest   syntheticGenCXX gtest gtest_main gtest ${TCMALLOC_LIB})
add_test(NAME basic COMMAND  basicTest)

add_executable(depositTest depositTest.cc)
target_link_libraries(depositTest   syntheticGenCXX gtest gtest_main gtest ${TCMALLOC_LIB})
add_test(NAME deposit COMMAND  depositTest)




#add_exectuable(depositTest depositTest.cc)
#target_link_libraries(depositTest   syntheticGenCXX gtest gtest_main gtest ${TCMALLOC_LIB})
#add_test(NAME deposit COMMAND  depositTest)
#
#
#add_exectuable(riverTest riverTest.cc)
#target_link_libraries(riverTest   syntheticGenCXX gtest gtest_main gtest ${TCMALLOC_LIB})
#add_test(NAME river COMMAND  riverTest)
#

