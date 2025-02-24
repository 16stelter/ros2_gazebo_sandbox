cmake_minimum_required(VERSION 3.8)
project(ros2_gazebo_sandbox)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(bitbots_msgs REQUIRED)
find_package(rosgraph_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(urdf REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(gz_plugin_vendor REQUIRED)
find_package(gz-plugin REQUIRED)
find_package(gz_sim_vendor REQUIRED)
find_package(gz-sim REQUIRED)

add_library(fake_flight_controller SHARED
  plugins/fake_flight_controller.cpp
)

target_link_libraries(fake_flight_controller
  gz-sim::core
  gz-plugin::core
)

install(
  TARGETS
    fake_flight_controller
  DESTINATION lib
)

set(INCLUDE_DIRS ${bitbots_msgs_INCLUDE_DIRS} ${rosgraph_msgs_INCLUDE_DIRS}
  ${std_msgs_INCLUDE_DIRS} ${ament_cmake_INCLUDE_DIRS} 
  ${urdf_INCLUDE_DIRS} ${nav_msgs_INCLUDE_DIRS}
  ${rclpy_INCLUDE_DIRS} ${sensor_msgs_INCLUDE_DIRS} ${gazebo_msgs_INCLUDE_DIRS})
include_directories(${INCLUDE_DIRS})

link_directories(${LIBRARY_DIRS})

set(LIBS ${bitbots_msgs_LIBRARIES} ${rosgraph_msgs_LIBRARIES}
  ${std_msgs_LIBRARIES} ${ament_cmake_LIBRARIES}
  ${urdf_LIBRARIES} ${nav_msgs_LIBRARIES} ${geometry_msgs_LIBRARIES} ${rclpy_LIBRARIES}
  ${sensor_msgs_LIBRARIES} ${gazebo_msgs_LIBRARIES})

ament_export_dependencies(bitbots_msgs)
ament_export_dependencies(rosgraph_msgs)
ament_export_dependencies(std_msgs)
ament_export_dependencies(ament_cmake)
ament_export_dependencies(urdf)
ament_export_dependencies(nav_msgs)
ament_export_dependencies(geometry_msgs)
ament_export_dependencies(rclpy)
ament_export_dependencies(sensor_msgs)
ament_export_dependencies(gazebo_msgs)
ament_export_include_directories(${INCLUDE_DIRS})

install(DIRECTORY robots  DESTINATION share/${PROJECT_NAME})
install(DIRECTORY worlds  DESTINATION share/${PROJECT_NAME})
install(DIRECTORY models  DESTINATION share/${PROJECT_NAME})
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})

ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/gz_sim_resource_path.dsv.in")
ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/gz_sim_system_plugin_path.dsv")

ament_python_install_package(${PROJECT_NAME})

ament_package()
