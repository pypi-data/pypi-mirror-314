from mecheye.profiler import *
from mecheye.shared import *
import numpy as np

pitch = 1e-3


def print_profiler_info(profiler_info: ProfilerInfo):
    print(".........................................")
    print("Profiler Model Name:           ", profiler_info.model, sep="")
    print("Controller Serial Number:      ",
          profiler_info.controller_sn, sep="")
    print("Sensor Serial Number:          ", profiler_info.sensor_sn, sep="")
    print("Profiler IP Address:           ", profiler_info.ip_address, sep="")
    print("Profiler IP Subnet Mask:       ", profiler_info.subnet_mask, sep="")
    print("Profiler IP Assignment Method: ", ip_assignment_method_to_string(
        profiler_info.ip_assignment_method), sep="")
    print("Hardware Version:              V",
          profiler_info.hardware_version.to_string(), sep="")
    print("Firmware Version:              V",
          profiler_info.firmware_version.to_string(), sep="")
    print(".........................................")
    print()


def find_and_connect(profiler: Profiler) -> bool:
    print("Find Mech-Eye 3D Laser Profilers...")
    profiler_infos = Profiler.discover_profilers()

    if len(profiler_infos) == 0:
        print("No Mech-Eye 3D Laser Profilers found.")
        return False

    for i in range(len(profiler_infos)):
        print("Mech-Eye device index :", i)
        print_profiler_info(profiler_infos[i])

    print("Please enter the device index you want to connect: ")
    input_index = 0

    while True:
        input_index = input()
        if input_index.isdigit() and 0 <= int(input_index) < len(profiler_infos):
            input_index = int(input_index)
            break
        print("Input invalid! Please enter the device index you want to connect: ")

    error_status = profiler.connect(profiler_infos[input_index])
    if not error_status.is_ok():
        show_error(error_status)
        return False

    print("Connect Mech-Eye 3D Laser Profiler Successfully.")
    return True


def find_and_connect_multi_profiler() -> list:
    print("Find Mech-Eye 3D Laser Profilers...")

    profiler_infos = Profiler.discover_profilers()

    if len(profiler_infos) == 0:
        print("No Mech-Eye 3D Laser Profilers found.")
        return []

    for i in range(len(profiler_infos)):
        print("Mech-Eye device index :", i)
        print_profiler_info(profiler_infos[i])

    indices = set()

    while True:
        print("Please enter the device index you want to connect: ")
        print("Enter the character 'c' to terminate adding devices")

        input_index = input()
        if input_index == 'c':
            break
        if input_index.isdigit() and 0 <= int(input_index) < len(profiler_infos):
            indices.add(int(input_index))
        else:
            print("Input invalid! Please enter the device index you want to connect: ")

    profilers = []
    for index in indices:
        profiler = Profiler()
        status = profiler.connect(profiler_infos[index])
        if status.is_ok():
            profilers.append(profiler)
        else:
            show_error(status)

    return profilers


def confirm_capture() -> bool:
    print("Do you want the profiler to capture image ? Please input y/n to confirm: ")
    while True:
        input_str = input()
        if input_str == "y" or input_str == "Y":
            return True
        elif input_str == "n" or input_str == "N":
            return False
        else:
            print("Please input y/n again!")


def print_profiler_status(profiler_status: ProfilerStatus):
    print(".....Profiler temperatures.....")
    print("Controller CPU: ",
          f"{profiler_status.temperature.controller_cpu_temperature:.2f}", "°C", sep="")
    print("Sensor CPU:     ",
          f"{profiler_status.temperature.sensor_cpu_temperature:.2f}", "°C", sep="")
    print("...............................")
    print()


def save_data_to_ply(file_name: str, profile_batch: ProfileBatch, x_unit: float, y_unit: float, use_encoder_values: bool, encoder_vals: np.array, is_organized: bool = True):
    data_width = profile_batch.width()
    with open(file_name, 'w') as file:
        depth = profile_batch.get_depth_map().data()
        vertex_count = depth.size if is_organized else depth[~np.isnan(
            depth)].size
        y, x = np.indices(depth.shape, dtype=np.uint16)

        file.write(f"""ply
format ascii 1.0
comment File generated
comment x y z data unit in mm
element vertex {vertex_count}
property float x
property float y
property float z
end_header
"""
                   )

        def depth_to_point(x, y, depth):
            if not np.isnan(depth):
                file.write("{} {} {}\n".format(
                    x * x_unit * pitch, y * y_unit * pitch, depth))
            elif is_organized:
                file.write("nan nan nan\n")

        np.vectorize(depth_to_point)(x, np.repeat(encoder_vals, data_width).reshape(
            depth.shape) if use_encoder_values else y, depth)


def save_data_to_csv(file_name: str, profile_batch: ProfileBatch, x_unit: float, y_unit: float, use_encoder_values: bool, encoder_vals: np.array, is_organized: bool = True):
    data_width = profile_batch.width()
    with open(file_name, 'w') as file:
        file.write("X,Y,Z\n")
        depth = profile_batch.get_depth_map().data()
        y, x = np.indices(depth.shape, np.uint16)

        def depth_to_point(x, y, depth):
            if not np.isnan(depth):
                file.write("{},{},{}\n".format(x * x_unit *
                           pitch, y * y_unit * pitch, depth))
            elif is_organized:
                file.write("nan,nan,nan\n")

        np.vectorize(depth_to_point)(x, np.repeat(encoder_vals, data_width).reshape(
            depth.shape) if use_encoder_values else y, depth)


def get_trigger_interval_distance() -> float:
    while True:
        print(
            "Please enter encoder trigger interval distance (unit: um, min: 1, max: 65535): ")
        trigger_interval_distance = input()
        if trigger_interval_distance.isdigit() and 1 <= float(trigger_interval_distance) <= 65535:
            return float(trigger_interval_distance)
        print("Input invalid!")


def save_point_cloud(profile_batch: ProfileBatch, user_set: UserSet, save_ply: bool = True, save_csv: bool = True, is_organized: bool = True):
    if profile_batch.is_empty():
        return

    error, x_unit = user_set.get_float_value(
        XAxisResolution.name)
    if not error.is_ok():
        show_error(error)
        return

    error, y_unit = user_set.get_float_value(YResolution.name)
    if not error.is_ok():
        show_error(error)
        return
    # # Uncomment the following line for custom Y Unit
    # y_unit = get_trigger_interval_distance()

    error, line_scan_trigger_source = user_set.get_enum_value(
        LineScanTriggerSource.name)
    if not error.is_ok():
        show_error(error)
        return
    use_encoder_values = line_scan_trigger_source == LineScanTriggerSource.Value_Encoder

    error, trigger_interval = user_set.get_int_value(
        EncoderTriggerInterval.name)
    if not error.is_ok():
        show_error(error)
        return

    encoder_vals = profile_batch.get_encoder_array().data().squeeze().astype(np.int64)
    encoder_vals = (encoder_vals - encoder_vals[0]) / trigger_interval

    print("Save the point cloud.")
    if (save_csv):
        save_data_to_csv("PointCloud.csv", profile_batch, x_unit, y_unit,
                         use_encoder_values, encoder_vals, is_organized)
    if (save_ply):
        save_data_to_ply("PointCloud.ply", profile_batch, x_unit,
                         y_unit, use_encoder_values, encoder_vals, is_organized)
