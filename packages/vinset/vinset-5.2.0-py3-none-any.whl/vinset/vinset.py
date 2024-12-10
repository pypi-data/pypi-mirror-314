import json
import cv2
import csv
import time
import numpy as np
import sys
import math
import argparse
import importlib.metadata
from importlib.resources import files
import os
from pymediainfo import MediaInfo
import commentjson
from ehdg_tools.ehdg_functions import get_dict_from_csv, string_to_bgr_tuple
from PIL import ImageFont, Image, ImageDraw


# This function is to change frame count to time in millisecond
def frame_count_to_time(frame_count_input, frame_rate_input):
    return int((frame_count_input / frame_rate_input) * 1000)


# This function is to change frame count to time in second
def frame_count_to_display_time(frame_count_input, frame_rate_input):
    return round((frame_count_input / frame_rate_input), 6)


# This function is to change time in millisecond to frame count
def time_to_frame_count(time_to_calculate, frame_rate_input):
    return int((time_to_calculate / 1000) * frame_rate_input)


# This function is to read string to convert boolean value
def str_to_bool(input_bool_string):
    if str(input_bool_string).lower().strip() == "true":
        return True
    else:
        return False


def get_info_from_dict(dict_input, key_string):
    try:
        return_value = dict_input[key_string]
        return return_value
    except KeyError:
        return None
    except TypeError:
        return None
    except ValueError:
        return None


# This function is to get built-in config location with new library (from importlib.resources import files)
def get_config_location(module_name, config_file_name):
    config_dir = files(module_name).joinpath(config_file_name)
    return str(config_dir)


# This function is to get built-in file location of okntool
def get_resource_file_location(file_name_input):
    resource_file_dir = get_config_location("vinset", file_name_input)
    if os.path.isfile(resource_file_dir):
        return resource_file_dir
    else:
        return None


def get_font_file_location(string_input):
    file_location = get_resource_file_location(f"{string_input}.ttf")
    if file_location is not None:
        return file_location
    else:
        raise FileNotFoundError(f"Font family : \"{string_input}\" could not be found in vinset.")


# This function is to display the process progressing
def print_percent_done(index_input, total, bar_len=50, title_input='Please wait'):
    percent_done = (index_input + 1) / total * 100
    percent_done_round = round(percent_done, 1)

    done = int(round(percent_done_round / (100 / bar_len)))
    togo = bar_len - done

    done_str = '=' * done
    togo_str = '_' * togo

    sys.stdout.write(f'\r{title_input}: [{done_str}{togo_str}] {percent_done_round}% done')
    sys.stdout.flush()


# This function is to change color string to color tuple value
def change_string_to_color_tuple(input_string):
    if input_string is None:
        return None
    elif input_string.lower() == "none" or input_string.lower() == "hide" or input_string.lower() == "null":
        return None
    elif "(" in input_string and ")" in input_string:
        color_value_array = input_string.replace("(", "").replace(")", "").split(",")
        output_color_tuple = tuple(float(index) for index in color_value_array)
        return output_color_tuple
    elif input_string.lower() == "red":
        output_color_tuple = (0, 0, 250)
        return output_color_tuple
    elif input_string.lower() == "green":
        output_color_tuple = (0, 250, 0)
        return output_color_tuple
    elif input_string.lower() == "blue":
        output_color_tuple = (250, 0, 0)
        return output_color_tuple
    elif input_string.lower() == "yellow":
        output_color_tuple = (0, 250, 250)
        return output_color_tuple
    elif input_string.lower() == "black":
        output_color_tuple = (0, 0, 0)
        return output_color_tuple
    elif input_string.lower() == "white":
        output_color_tuple = (250, 250, 250)
        return output_color_tuple
    elif input_string.lower() == "magenta":
        output_color_tuple = (250, 0, 250)
        return output_color_tuple
    elif "#" in input_string.lower():
        value = input_string.lstrip('#')
        lv = len(value)
        if lv == 6:
            try:
                tem_arr = tuple(int(value[xx:xx + lv // 3], 16) for xx in range(0, lv, lv // 3))
                return tem_arr[::-1]
            except ValueError as e:
                print(e)
                raise
        else:
            print(f"The length of input hex string must be 6 character. But it is {lv}.")
            raise
    else:
        try:
            blue_index, green_index, red_index = string_to_bgr_tuple(input_string)
            return blue_index, green_index, red_index
        except ValueError:
            print(f"Input string {input_string} is not a valid color string input.")
            print("It can be red, green, blue, black, white or magenta.")
            print("It also can be hex color code.")
            return None


# This function is to get the positions in parent axes array
def get_position_of_parent(search_string_input, axes_array_input):
    idx_found = False
    return_idx = None
    for idx, val in enumerate(axes_array_input):
        if val["axe_name"] == search_string_input:
            idx_found = True
            return_idx = idx
            break

    if not idx_found:
        print(f"{search_string_input} can not be found!")

    return return_idx


# This function is to get the positions in given array
def get_position(search_input, array_in):
    idx_found = False
    return_idx = None
    for idx, val in enumerate(array_in):
        if val == search_input:
            idx_found = True
            return_idx = idx
            break

    if not idx_found:
        print(f"{search_input} can not be found!")

    return return_idx


# This function is to get index value from horizontal to vertical labelling
def get_vertical_position(frame_width_input, frame_height_input, put_text_input,
                          x_input, y_input, color_search_input, font_input, thick_input):
    # width = height and height = width when we rotate the image
    f_w = frame_height_input
    f_h = frame_width_input
    tem_image = np.zeros([int(f_w), int(f_h), 3], dtype=np.uint8)
    x_edit = int(frame_height_input - y_input)
    y_edit = x_input
    co_ord_input = (x_edit, y_edit)

    cv2.putText(tem_image, put_text_input, co_ord_input, cv2.FONT_HERSHEY_DUPLEX, font_input,
                color_search_input, thick_input)
    # rotate
    out_image = cv2.rotate(tem_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # capture position to return
    color_index_output = np.where(np.all(out_image == color_search_input, axis=-1))

    return color_index_output


# This function is to get the color index in given image
def get_color_position(image_input, color_in):
    color_index_output = np.where(np.all(image_input == color_in, axis=-1))

    return color_index_output


# This function is to create the data array in order to draw lines in graph
def get_data_array(csv_data_input, t_data_input, y_data_input, offset_input,
                   filter_input=False, filter_by_input=None):
    if filter_input:
        if "=" in filter_by_input:
            filter_name, filter_value, filter_value_type = get_filter_value(filter_by_input)
            data_array_output = []

            with open(csv_data_input, "r") as csv_file:
                csv_reader = (csv.reader(csv_file, delimiter=','))
                header_array = next(csv_reader)
                t_pos = get_position(t_data_input, header_array)
                y_pos = get_position(y_data_input, header_array)
                f_pos = get_position(filter_name, header_array)
                if filter_value_type == "float":
                    for row in csv_reader:
                        filter_check = float(row[f_pos])
                        if filter_check == filter_value:
                            time_value = (float(row[t_pos]) + offset_input) * 1000
                            y_value = float(row[y_pos])
                            data_array_output.append([time_value, y_value])
                elif filter_value_type == "int":
                    for row in csv_reader:
                        filter_check = int(row[f_pos])
                        if filter_check == filter_value:
                            time_value = (float(row[t_pos]) + offset_input) * 1000
                            y_value = float(row[y_pos])
                            data_array_output.append([time_value, y_value])
                else:
                    for row in csv_reader:
                        filter_check = str(row[f_pos])
                        if filter_check == filter_value:
                            time_value = (float(row[t_pos]) + offset_input) * 1000
                            y_value = float(row[y_pos])
                            data_array_output.append([time_value, y_value])

            return data_array_output

        elif "event" in filter_by_input:
            data_array_output = []
            experience_data = False
            first_value_record = False

            with open(csv_data_input, "r") as csv_file:
                csv_reader = (csv.reader(csv_file, delimiter=','))
                header_array = next(csv_reader)
                t_pos = get_position(t_data_input, header_array)
                y_pos = get_position(y_data_input, header_array)
                f_pos = get_position(filter_by_input, header_array)

                for row in csv_reader:
                    event_string_value = str(row[f_pos])
                    if event_string_value != " ":
                        experience_data = True
                        if not first_value_record:
                            first_time_value = (float(row[t_pos]) * 1000)
                            first_value_record = True
                        if event_string_value == "server_end_of_file_message":
                            experience_data = False
                    if experience_data and first_value_record:
                        original_time_value = (float(row[t_pos]) * 1000)
                        time_value = ((float(row[t_pos]) + offset_input) * 1000) - first_time_value
                        y_value = float(row[y_pos])
                        data_array_output.append([time_value, y_value, original_time_value])
            # print(len(data_array_output))
            return data_array_output

    else:
        data_array_output = []
        with open(csv_data_input, "r") as csv_file:
            csv_reader = (csv.reader(csv_file, delimiter=','))
            header_array = next(csv_reader)
            t_pos = get_position(t_data_input, header_array)
            y_pos = get_position(y_data_input, header_array)

            for row in csv_reader:
                time_value = (float(row[t_pos]) + offset_input) * 1000
                y_value = float(row[y_pos])
                data_array_output.append([time_value, y_value])

        return data_array_output


def get_profile_data_array(rows, t_data_input, column_array, minimum_col_name=None,
                           filter_input=False, filter_by_input=None):
    final_rows = rows
    if filter_input:
        if "=" in filter_by_input:
            filter_name, filter_value, filter_value_type = get_filter_value(filter_by_input)
            final_rows = []
            for row in rows:
                if filter_value_type == "float":
                    filter_check = float(row[filter_name])
                elif filter_value_type == "int":
                    filter_check = int(row[filter_name])
                else:
                    filter_check = str(row[filter_name])
                if filter_check == filter_value:
                    final_rows.append(row)

    first_time = None
    data_array_output = []

    nom_v = 0
    interval = 1 / len(column_array)
    x_data_array = []
    for x in range(len(column_array)):
        nom_v += interval
        round_nom_v = round(nom_v, 2)
        x_data_array.append(round_nom_v)

    for row in final_rows:
        time_value_raw = int((float(row[t_data_input])) * 1000)
        if first_time is None:
            first_time = time_value_raw
        time_value = time_value_raw - first_time
        y_data_array = []
        for col_name in column_array:
            y_data_array.append(int(float(row[col_name])))
        temp_dict = {}
        temp_dict["time_value"] = time_value
        temp_dict["x_data_array"] = x_data_array
        temp_dict["y_data_array"] = y_data_array
        if minimum_col_name is not None:
            temp_dict["minimum_value"] = float(row[minimum_col_name])
        data_array_output.append(temp_dict)

    return data_array_output


# This function is to create the data array in order to draw lines in graph
def get_data_array_v_5(rows, t_data_input, y_data_input,
                       filter_input=False, filter_by_input=None):
    if filter_input:
        if "=" in filter_by_input:
            filter_name, filter_value, filter_value_type = get_filter_value(filter_by_input)
            first_time = None
            data_array_output = []

            for row in rows:
                time_value_raw = int((float(row[t_data_input])) * 1000)
                if first_time is None:
                    first_time = time_value_raw
                time_value = time_value_raw - first_time
                if str(row[y_data_input]).lower() == "nan":
                    y_value = np.nan
                else:
                    try:
                        y_value = float(row[y_data_input])
                    except ValueError:
                        y_value = np.nan
                temp_dict = {}
                temp_dict["time_value"] = time_value
                temp_dict["y_value"] = y_value
                if filter_value_type == "float":
                    filter_check = float(row[filter_name])
                elif filter_value_type == "int":
                    filter_check = int(row[filter_name])
                else:
                    filter_check = str(row[filter_name])
                if filter_check == filter_value:
                    data_array_output.append(temp_dict)

            return data_array_output

        elif "event" in filter_by_input:
            first_time = None
            data_array_output = []

            for row in rows:
                time_value_raw = int((float(row[t_data_input])) * 1000)
                if first_time is None:
                    first_time = time_value_raw
                time_value = time_value_raw - first_time
                if str(row[y_data_input]).lower() == "nan":
                    y_value = np.nan
                else:
                    try:
                        y_value = float(row[y_data_input])
                    except ValueError:
                        y_value = np.nan
                temp_dict = {}
                temp_dict["time_value"] = time_value
                temp_dict["y_value"] = y_value
                data_array_output.append(temp_dict)

            return data_array_output

    else:
        first_time = None
        data_array_output = []

        for row in rows:
            time_value_raw = int((float(row[t_data_input])) * 1000)
            if first_time is None:
                first_time = time_value_raw
            time_value = time_value_raw - first_time
            if str(row[y_data_input]).lower() == "nan":
                y_value = np.nan
            else:
                try:
                    y_value = float(row[y_data_input])
                except ValueError:
                    y_value = np.nan
            temp_dict = {}
            temp_dict["time_value"] = time_value
            temp_dict["y_value"] = y_value
            data_array_output.append(temp_dict)

        return data_array_output


# This function is to get filter by value
def get_filter_value(string_input):
    filter_name, filter_value = str(string_input).split("=")
    if "." in filter_value:
        try:
            filter_value = float(filter_value)
            filter_value_type = "float"
        except ValueError:
            filter_value = str(filter_value)
            filter_value_type = "str"
    else:
        try:
            filter_value = int(filter_value)
            filter_value_type = "int"
        except ValueError:
            filter_value = str(filter_value)
            filter_value_type = "str"

    return filter_name, filter_value, filter_value_type


def get_info_from_csv(csv_dir_input):
    header_array_out = []
    rows_out = []
    try:
        file_to_open = open(csv_dir_input)
        csv_reader = csv.reader(file_to_open)

        count_one = 0
        for row_data in csv_reader:
            if count_one <= 0:
                header_array_out = row_data
                count_one += 1
            else:
                rows_out.append(row_data)
    except FileNotFoundError:
        print(f"{csv_dir_input} could not be found.")

    return header_array_out, rows_out


def time_adjust_to_pixel(data_array_input, interval_in_milli):
    upper_limit = interval_in_milli

    out_array = []
    temp_array = []
    for data in data_array_input:
        time_value = data["time_value"]
        if time_value <= upper_limit:
            temp_array.append(data)
        else:
            mean_data = get_mean_of_array(temp_array)
            if mean_data is not None:
                out_array.append(mean_data)
            temp_array = [data]
            upper_limit += interval_in_milli
    mean_data = get_mean_of_array(temp_array)
    if mean_data is not None:
        out_array.append(mean_data)

    return out_array


def get_mean_of_array(arr_input):
    if arr_input:
        if len(arr_input) <= 1:
            if len(arr_input) <= 0:
                return None
            else:
                return arr_input[0]
        else:
            t_array = []
            y_array = []
            for v in arr_input:
                t_val = v["time_value"]
                y_val = v["y_value"]
                t_array.append(t_val)
                y_array.append(y_val)
            temp_dict = {}
            temp_dict["time_value"] = np.nanmean(t_array)
            if np.isnan(y_array).all():
                temp_dict["y_value"] = np.nan
            else:
                temp_dict["y_value"] = np.nanmean(y_array)
            return temp_dict
    else:
        return None


def get_series_data_array(data_array_in, time_width_in):
    time_width_milli = int(time_width_in * 1000)
    if data_array_in:
        series_data_array = []
        temp_array = []
        for data in data_array_in:
            t_value = data["time_value"]
            if t_value < time_width_milli:
                temp_array.append(data)
            else:
                temp_dict = {}
                temp_dict["time_limit_milli"] = time_width_milli
                temp_dict["data_array"] = temp_array
                series_data_array.append(temp_dict)
                temp_array = [data]
                time_width_milli += int(time_width_in * 1000)
        temp_dict = {}
        temp_dict["time_limit_milli"] = time_width_milli
        temp_dict["data_array"] = temp_array
        series_data_array.append(temp_dict)
        return series_data_array
    else:
        return None


def draw_graph_by_profile_info(frame_input, check_timer_in, series_info):
    profile_data_array = series_info["profile_data_array"]
    lower_limit = series_info["lower_limit"]
    upper_limit = series_info["upper_limit"]
    ax_x = series_info["ax_x"]
    ax_y = series_info["ax_y"]
    ax_w = series_info["ax_w"]
    ax_h = series_info["ax_h"]
    line_color = series_info["line_color"]
    line_thickness = series_info["line_thickness"]
    x_pixel_offset = series_info["x_pixel_offset"]
    y_pixel_offset = series_info["y_pixel_offset"]
    minimum_pointer = series_info["minimum_pointer"]
    minimum_pointer_enabled = str_to_bool(minimum_pointer["enabled"])

    if minimum_pointer_enabled:
        pointer_color = change_string_to_color_tuple(minimum_pointer["color"])
        pointer_radius = minimum_pointer["radius"]
    else:
        pointer_color = None
        pointer_radius = None

    data_to_draw = None
    for draw_data in profile_data_array:
        tv = draw_data["time_value"]
        if check_timer_in <= tv:
            data_to_draw = draw_data
            break

    if data_to_draw:
        start_x = None
        start_y = None
        start_data = False
        x_array = data_to_draw["x_data_array"]
        y_array = data_to_draw["y_data_array"]
        minimum_value = data_to_draw["minimum_value"]
        pointer_pos = None
        for x_val, y_val in zip(x_array, y_array):
            scaled_step = int((x_val * ax_w) + x_pixel_offset)
            x_po = int(ax_x + scaled_step)
            scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, y_val)
            scaled_num = int(scaled_num - y_pixel_offset)
            y_po = int(ax_y + ax_h - scaled_num)
            if pointer_pos is None:
                if x_val >= minimum_value:
                    pointer_pos = (x_po, y_po)

            if not start_data:
                start_x = x_po
                start_y = y_po
                start_data = True
            else:
                end_x = x_po
                end_y = y_po
                cv2.line(frame_input, (start_x, start_y), (end_x, end_y),
                         line_color, line_thickness, cv2.LINE_AA)
                start_x = end_x
                start_y = end_y

        if minimum_pointer_enabled:
            cv2.circle(frame_input, pointer_pos, pointer_radius, pointer_color, -1)

    return frame_input


def draw_normal_series_graph(frame_input, check_timer_in, series_info):
    series_id = series_info["series_id"]
    series_name = series_info["series_name"]
    display_type = str(series_info["display_type"])
    series_data_array = series_info["series_data_array"]
    lower_limit = series_info["lower_limit"]
    upper_limit = series_info["upper_limit"]
    time_interval = series_info["time_interval"]
    ax_x = series_info["ax_x"]
    ax_y = series_info["ax_y"]
    # ax_w = series_info["ax_w"]
    ax_h = series_info["ax_h"]
    line_color = series_info["line_color"]
    line_thickness = series_info["line_thickness"]
    x_pixel_offset = series_info["x_pixel_offset"]
    y_pixel_offset = series_info["y_pixel_offset"]
    draw_pointer = series_info["draw_pointer"]
    draw_time_line = series_info["draw_time_line"]
    pointer_color = series_info["pointer_color"]
    pointer_radius = series_info["pointer_radius"]
    time_line_opacity = series_info["time_line_opacity"]
    time_line_color = series_info["time_line_color"]
    time_line_thickness = series_info["time_line_thickness"]
    draw_array = None
    draw_time_limit = None
    draw_array_index = 0

    for ind, series_dict in enumerate(series_data_array):
        time_width_milli = series_dict["time_limit_milli"]
        if time_width_milli > check_timer_in:
            draw_array = series_dict["data_array"]
            draw_time_limit = time_width_milli
            draw_array_index = ind
            break

    time_divider = int(draw_time_limit / (draw_array_index + 1))

    pointer_index_in_graph = 0
    current_time_value = 0
    if draw_array:
        if draw_pointer:
            for draw_index, draw_data in enumerate(draw_array):
                tv = draw_data["time_value"]
                if check_timer_in <= tv:
                    pointer_index_in_graph = draw_index
                    current_time_value = tv
                    break

            if pointer_index_in_graph <= 0 or pointer_index_in_graph >= (len(draw_array) - 1):
                # print("out of bound")
                pointer_drawable = False
            else:
                pre_pointer_data = draw_array[pointer_index_in_graph - 1]
                previous_time_value = pre_pointer_data["time_value"]
                if np.isnan(current_time_value) or np.isnan(previous_time_value):
                    # print("is nan")
                    pointer_drawable = False
                else:
                    pointer_drawable = True
        else:
            pointer_drawable = False
            for draw_index, draw_data in enumerate(draw_array):
                tv = draw_data["time_value"]
                if check_timer_in <= tv:
                    pointer_index_in_graph = draw_index
                    break

        start_x = None
        start_y = None
        pointer_is_drawn = False
        pointer_pos = None
        time_x_po = None
        for draw_index, draw_data in enumerate(draw_array):
            tv = draw_data["time_value"]
            yv = draw_data["y_value"]

            if draw_index <= 0:
                can_draw = False
            else:
                can_draw = True
            scaled_step = int((tv % time_divider) / time_interval) + x_pixel_offset
            x_po = int(ax_x + scaled_step)
            if time_x_po is None and draw_index == pointer_index_in_graph:
                time_x_po = x_po
            if np.isnan(yv):
                can_draw = False
                y_po = None
            else:
                scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, yv)
                scaled_num = int(scaled_num - y_pixel_offset)
                y_po = int(ax_y + ax_h - scaled_num)
            if can_draw:
                end_x = x_po
                end_y = y_po
                cv2.line(frame_input, (start_x, start_y), (end_x, end_y),
                         line_color, line_thickness, cv2.LINE_AA)

            if pointer_drawable and can_draw and draw_index == pointer_index_in_graph:
                if not pointer_is_drawn:
                    pointer_pos = (x_po, y_po)
                    pointer_is_drawn = True
                    if display_type == "pen":
                        break
            start_x = x_po
            if y_po is not None:
                start_y = y_po
            if display_type == "pen" and draw_index == pointer_index_in_graph:
                break
        if draw_time_line:
            time_line_start = (time_x_po, ax_y)
            time_line_end = (time_x_po, int(ax_y + ax_h))
            overlay_frame = frame_input.copy()
            cv2.line(overlay_frame, time_line_start, time_line_end, time_line_color, time_line_thickness)
            # Add opacity of line
            frame_input = cv2.addWeighted(overlay_frame, time_line_opacity, frame_input, 1 - time_line_opacity, 0)

        if pointer_pos is not None and draw_pointer:
            # print(pointer_pos)
            cv2.circle(frame_input, pointer_pos, pointer_radius, pointer_color, -1)
    else:
        print(f"Warning! There is nothing to draw in series_id: {series_id}, series_name : {series_name}")

    return frame_input


def draw_texts(frame_input, text_info, main_data_in,
               frame_count_in, display_time_in, time_checker):
    text_type = text_info["text_type"]
    text_position = text_info["text_position"]
    text_pos_x = text_position["x"]
    text_pos_y = text_position["y"]
    text_style = text_info["text_style"]
    text_font_family = text_style["font_family"]
    text_font_size = text_style["font_size"]
    text_color = change_string_to_color_tuple(text_style["color"])
    box_drawing = get_info_from_dict(text_info, "box")
    if box_drawing is None:
        box_drawing = False

    if text_type == "normal":
        text_string = text_info["text_string"]
        if box_drawing:
            box_dimension = text_info["box_dimension"]
            box_x = box_dimension["x"]
            box_y = box_dimension["y"]
            box_w = box_dimension["width"]
            box_h = box_dimension["height"]
            box_style = text_info["box_style"]
            box_fill = box_style["fill"]
            box_boundary_thickness = box_style["boundary_thickness"]
            if box_fill:
                box_boundary_thickness = -1
            box_color = change_string_to_color_tuple(box_style["color"])
            frame_input = cv2.rectangle(frame_input, (box_x, box_y),
                                        ((box_x + box_w), (box_y + box_h)),
                                        box_color, box_boundary_thickness)
        # frame_input = cv2.putText(frame_input, text_string, (text_pos_x, text_pos_y),
        #                           cv2.FONT_HERSHEY_DUPLEX, text_font_scale,
        #                           text_color, text_thickness)
        frame_input = pillow_put_text(frame_input, text_string, (text_pos_x, text_pos_y),
                                      text_font_family, text_font_size, text_color)
    elif text_type == "time":
        raw_time_string = str(display_time_in)
        if "." in raw_time_string:
            sec_str, milli_str = raw_time_string.split(".")
            if len(milli_str) < 6:
                display_t = sec_str + "." + milli_str + ("0" * (6 - len(milli_str)))
            else:
                display_t = raw_time_string
        else:
            display_t = f"{raw_time_string}.000000"
        time_text_string = f"T={display_t} F={frame_count_in}"
        if box_drawing:
            box_dimension = text_info["box_dimension"]
            box_x = box_dimension["x"]
            box_y = box_dimension["y"]
            box_w = box_dimension["width"]
            box_h = box_dimension["height"]
            box_style = text_info["box_style"]
            box_fill = box_style["fill"]
            box_boundary_thickness = box_style["boundary_thickness"]
            if box_fill:
                box_boundary_thickness = -1
            box_color = change_string_to_color_tuple(box_style["color"])
            frame_input = cv2.rectangle(frame_input, (box_x, box_y),
                                        ((box_x + box_w), (box_y + box_h)),
                                        box_color, box_boundary_thickness)
        frame_input = pillow_put_text(frame_input, time_text_string, (text_pos_x, text_pos_y),
                                      text_font_family, text_font_size, text_color)
    elif text_type == "data":
        time_column_name = text_info["time_column_name"]
        data_column_name = text_info["data_column_name"]
        extra_string = text_info["extra_string"]
        extra_string_pos = text_info["extra_string_pos"]
        text_filter = str_to_bool(str(text_info["filter"]))
        if text_filter:
            filter_by = text_info["filter_by"]
        else:
            filter_by = None
        data_format_type = text_info["data_format_type"]
        data_array = get_data_array_v_5(main_data_in, time_column_name,
                                        data_column_name, text_filter, filter_by)
        data_index_to_show = 0
        for data_index, data_dict in enumerate(data_array):
            tv = data_dict["time_value"]
            if time_checker <= tv:
                data_index_to_show = data_index
                break
        dict_to_show = data_array[data_index_to_show]
        if data_format_type == "float":
            decimal_place = text_info["decimal_place"]
            raw_data_string = str(round(float(dict_to_show["y_value"]), decimal_place))
        elif data_format_type == "int":
            raw_data_string = str(int(dict_to_show["y_value"]))
        else:
            raw_data_string = str(dict_to_show["y_value"])
        if extra_string_pos == "back":
            data_text_string = raw_data_string + extra_string
        else:
            data_text_string = extra_string + raw_data_string
        if box_drawing:
            box_dimension = text_info["box_dimension"]
            box_x = box_dimension["x"]
            box_y = box_dimension["y"]
            box_w = box_dimension["width"]
            box_h = box_dimension["height"]
            box_style = text_info["box_style"]
            box_fill = box_style["fill"]
            box_boundary_thickness = box_style["boundary_thickness"]
            if box_fill:
                box_boundary_thickness = -1
            box_color = change_string_to_color_tuple(box_style["color"])
            frame_input = cv2.rectangle(frame_input, (box_x, box_y),
                                        ((box_x + box_w), (box_y + box_h)),
                                        box_color, box_boundary_thickness)
        frame_input = pillow_put_text(frame_input, data_text_string, (text_pos_x, text_pos_y),
                                      text_font_family, text_font_size, text_color)
        pass
    else:
        raise ValueError(f"Invalid text type: {text_type}")

    return frame_input


# This function is to change the given number to scaled value
def number_to_scale(lower_limit_input, upper_limit_input, box_height_input, number_input):
    total_limit = upper_limit_input - lower_limit_input
    number_in_total = number_input - lower_limit_input
    number_output = int(box_height_input * (number_in_total / total_limit))

    return number_output


# This function is to check whether there must be zero line or not
def need_to_display_zero_line(low_limit, up_limit):
    if low_limit < 0 < up_limit:
        return True
    else:
        return False


# This function is to produce average value from array
def get_value_from_array(data_arr_input, low_li, up_li):
    new_arr = data_arr_input[:]
    length_array = len(new_arr)
    if length_array == 1:
        val = new_arr[0]
        return val

    elif length_array == 0:
        val = [((low_li + up_li) / 2), "nothing"]
        return val

    else:
        total_time = 0
        total_value = 0
        for d in new_arr:
            total_time += d[0]
            total_value += d[1]
        avg_time = total_time / length_array
        avg_value = total_value / length_array
        val = [avg_time, avg_value]
        return val


def overlay_graph(draw_able_input, config_info_input, input_video_file, csv_data_to_be_used,
                  output_video_file, show_preview_video=True):
    if draw_able_input and config_info_input:
        axes_array = config_info_input["axes"]
        series_array = config_info_input["series"]
        display_able = str_to_bool(str(config_info_input["display"]))
        if not show_preview_video:
            display_able = False

        input_video = cv2.VideoCapture(input_video_file)
        frame_width = input_video.get(cv2.CAP_PROP_FRAME_WIDTH)
        print("Frame width:", frame_width)
        frame_height = input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("Frame height:", frame_height)
        frame_rate = input_video.get(cv2.CAP_PROP_FPS)
        print("Frame rate:", frame_rate)
        frame_count = input_video.get(cv2.CAP_PROP_FRAME_COUNT)
        print("Frame count:", frame_count)

        draw_data_array = []
        pointer_info_dict = {}
        max_video_length = math.ceil(frame_count_to_time(frame_count, frame_rate))

        # for loop over series array and prepare the respected data
        for info in series_array:
            search_string = info["parent_axes"]
            parent_index = get_position_of_parent(search_string, axes_array)
            if parent_index is not None:
                axes_info = axes_array[parent_index]
                axes_pos = axes_info["position"]
                # axes_pos_x = axes_pos["x"]
                # axes_pos_y = axes_pos["y"]
                axes_pos_w = axes_pos["width"]
                # axes_pos_h = axes_pos["height"]
                series_name = info["name"]
                pointer_position_name = series_name + "_pointer_info"
                pointer_info_dict[pointer_position_name] = (0, 0)
                display_type = info["display_type"]
                t_limit = info["t-limit"]
                try:
                    t_offset = info["time_offset"]
                except KeyError:
                    t_offset = 0
                t_w = t_limit["width"]
                t_data = info["t_data"]
                y_data = info["y_data"]
                info_filter = str_to_bool(str(info["filter"]))
                filter_by = None
                if info_filter:
                    filter_by = info["filterBy"]
                if str(display_type).lower() == "pen":
                    # getting data from csv with or without filter
                    if info_filter:
                        data_arr = get_data_array(csv_data_to_be_used, t_data, y_data, t_offset, info_filter, filter_by)
                    else:
                        data_arr = get_data_array(csv_data_to_be_used, t_data, y_data, t_offset)
                    series_data_array = []
                    # calculate the max duration of time can be displayed in one pixel
                    time_interval_for_data = round(1000 / (axes_pos_w / t_w), 4)
                    # calculate how many display for the whole video
                    number_of_time_interval = math.ceil(max_video_length / time_interval_for_data)
                    # lower range starts with 0 and upper range starts with milliseconds
                    # calculated from time interval for data
                    lower_range = 0
                    upper_range = round((lower_range + time_interval_for_data), 2)
                    # calculate the length of 1 display in milliseconds
                    width_check = int(t_w) * 1000
                    box_data_array = []
                    for i in range(1, (number_of_time_interval + 1), 1):
                        raw_data_array = []
                        # input_data = None
                        for data in data_arr:
                            if lower_range <= data[0] < upper_range:
                                raw_data_array.append(data)
                        # get the average of value array because we only can draw 1 data at 1 pixel
                        input_data = get_value_from_array(raw_data_array, lower_range, upper_range)
                        box_data_array.append(input_data)
                        if max_video_length <= width_check:
                            if i == (number_of_time_interval - 1):
                                another_box_array = box_data_array[:]
                                series_data_array.append([int(width_check), another_box_array])
                        else:
                            if upper_range >= width_check:
                                another_box_array = box_data_array[:]
                                series_data_array.append([int(width_check), another_box_array])
                                box_data_array.clear()
                                width_check += (int(t_w) * 1000)
                        lower_range = upper_range
                        upper_range = round((upper_range + time_interval_for_data), 2)
                    draw_data_array.append({"series_name": series_name, "display_type": display_type,
                                            "series_data_array": series_data_array})

                elif str(display_type).lower() == "static":
                    # getting data from csv with or without filter
                    if info_filter:
                        data_arr = get_data_array(csv_data_to_be_used, t_data, y_data, t_offset, info_filter, filter_by)
                    else:
                        data_arr = get_data_array(csv_data_to_be_used, t_data, y_data, t_offset)
                    series_data_array = []
                    # calculate the max duration of time can be displayed in one pixel
                    time_interval_for_data = round(1000 / (axes_pos_w / t_w), 4)
                    # calculate how many display for the whole video
                    number_of_time_interval = math.ceil(max_video_length / time_interval_for_data)
                    # lower range starts with 0 and upper range starts with milliseconds
                    # calculated from time interval for data
                    lower_range = 0
                    upper_range = round((lower_range + time_interval_for_data), 2)
                    # calculate the length of 1 display in milliseconds
                    width_check = int(t_w) * 1000
                    box_data_array = []
                    for i in range(1, (number_of_time_interval + 1), 1):
                        raw_data_array = []
                        # input_data = None
                        for data in data_arr:
                            if lower_range <= data[0] < upper_range:
                                raw_data_array.append(data)
                        # get the average of value array because we only can draw 1 data at 1 pixel
                        input_data = get_value_from_array(raw_data_array, lower_range, upper_range)
                        raw_data_array.clear()
                        box_data_array.append(input_data)
                        if max_video_length <= width_check:
                            if i == (number_of_time_interval - 1):
                                another_box_array = box_data_array[:]
                                series_data_array.append([int(width_check), another_box_array])
                        else:
                            if upper_range >= width_check:
                                another_box_array = box_data_array[:]
                                series_data_array.append([int(width_check), another_box_array])
                                box_data_array.clear()
                                width_check += (int(t_w) * 1000)
                        lower_range = upper_range
                        upper_range = round((upper_range + time_interval_for_data), 2)
                    draw_data_array.append({"series_name": series_name, "display_type": display_type,
                                            "series_data_array": series_data_array})

        ret, frame = input_video.read()
        raw_image = None
        if ret:
            # get the frame and fill with black
            raw_image = frame
            raw_image.fill(0)
        box_color_array = []

        for info in series_array:
            search_string = info["parent_axes"]
            parent_index = get_position_of_parent(search_string, axes_array)
            if parent_index is not None:
                axes_info = axes_array[parent_index]
                box_color = axes_info["box_color"]
                axes_pos = axes_info["position"]
                box_title = axes_info["box_title"]
                title_x_position = axes_info["box_title_x_position"]
                title_y_position = axes_info["box_title_y_position"]
                title_color = axes_info["box_title_color"]
                box_color_array.append({"box_color": box_color, "title_color": title_color})
                box_color = change_string_to_color_tuple(box_color)
                title_color = change_string_to_color_tuple(title_color)
                title_font = float(axes_info["box_title_font_scale"])
                box_thickness = int(axes_info["box_thickness"])
                axes_pos_x = axes_pos["x"]
                axes_pos_y = axes_pos["y"]
                axes_pos_w = axes_pos["width"]
                axes_pos_h = axes_pos["height"]
                t_limit = info["t-limit"]
                t_w = t_limit["width"]
                t_name = info["t_label"]
                t_label_x_position = info["t_label_x_position"]
                t_label_y_position = info["t_label_y_position"]
                y_name = info["y_label"]
                y_label_x_position = info["y_label_x_position"]
                y_label_y_position = info["y_label_y_position"]
                label_thickness = int(info["label_thickness"])
                label_font_scale = float(info["label_font_scale"])
                # draw box and labels according to config
                raw_image = cv2.rectangle(raw_image, (axes_pos_x, axes_pos_y),
                                          ((axes_pos_x + axes_pos_w), (axes_pos_y + axes_pos_h)),
                                          box_color, box_thickness)
                title_x = int(axes_pos_x) + int(title_x_position)
                title_y = int(axes_pos_y) - int(title_y_position)
                cv2.putText(raw_image, box_title, (title_x, title_y), cv2.FONT_HERSHEY_DUPLEX, title_font,
                            title_color, box_thickness)
                t_label_x = int(axes_pos_x) + int(t_label_x_position)
                t_label_y = int(axes_pos_y) + int(t_label_y_position)
                cv2.putText(raw_image, t_name, (t_label_x, t_label_y), cv2.FONT_HERSHEY_DUPLEX, label_font_scale,
                            box_color, label_thickness)
                y_label_x_input = axes_pos_x - int(y_label_x_position)
                y_label_y_input = axes_pos_y - int(y_label_y_position)
                # getting the position of vertical label
                ver_color_index_array = get_vertical_position(frame_width, frame_height, y_name,
                                                              y_label_x_input, y_label_y_input,
                                                              box_color, label_font_scale, label_thickness)
                # use that position and draw vertical label in raw image
                for item in zip(ver_color_index_array[0], ver_color_index_array[1]):
                    item_tuple = tuple(item)
                    raw_image[item_tuple[0], item_tuple[1]] = box_color

                x_scale_interval_width = int(axes_pos_w / t_w)
                # start_point_x_scale = axes_pos_x
                # x_scale_level = axes_pos_y + axes_pos_h
                height_of_scale = 5

                # draw x axis / t axis interval points
                for i in range(0, t_w):
                    space_value = i * x_scale_interval_width
                    # end_point_x_scale_level = start_point_x_scale - height_of_scale
                    cv2.line(raw_image, (axes_pos_x + space_value,
                                         axes_pos_h + axes_pos_y),
                             (axes_pos_x + space_value,
                              axes_pos_h + axes_pos_y - height_of_scale),
                             box_color, box_thickness, cv2.LINE_AA)
                # after this points, the raw black image is filled with
                # all graphs and labels

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        v_writer = cv2.VideoWriter(output_video_file, fourcc, int(frame_rate), (int(frame_width), int(frame_height)))
        whole_t = time.time()
        count = 0
        drawing_graph = True

        while drawing_graph:

            # start_tt = time.time()
            ret, frame = input_video.read()
            # end_tt = time.time()
            print_percent_done(count, frame_count)
            check_timer = frame_count_to_time(count, frame_rate)

            if ret:
                for info in series_array:
                    search_string = info["parent_axes"]
                    parent_index = get_position_of_parent(search_string, axes_array)
                    if parent_index is not None:
                        axes_info = axes_array[parent_index]
                        axes_pos = axes_info["position"]
                        x = axes_pos["x"]
                        y = axes_pos["y"]
                        w = axes_pos["width"]
                        h = axes_pos["height"]
                        axes_bg = axes_info["background"]
                        bg_fill = axes_bg["fill"]
                        color_input = change_string_to_color_tuple(bg_fill)
                        bg_opacity = axes_bg["opacity"]
                        # copy a frame to draw boundary
                        overlay_frame = frame.copy()
                        boundary_space = axes_bg["space"]
                        # draw boundary to graph
                        cv2.rectangle(overlay_frame,
                                      (x - boundary_space, y - boundary_space),
                                      (x + w + boundary_space,
                                       y + h + boundary_space),
                                      color_input, -1)
                        # overlay by original frame
                        frame = cv2.addWeighted(overlay_frame, bg_opacity,
                                                frame, 1 - bg_opacity, 0)
                        # draw graphs and labels over the frame
                        # to avoid color opacity drops
                        for color in box_color_array:
                            box_color = change_string_to_color_tuple(color["box_color"])
                            title_color = change_string_to_color_tuple(color["title_color"])
                            box_draw_index = get_color_position(raw_image, box_color)
                            title_draw_index = get_color_position(raw_image, title_color)

                            for box_item in zip(box_draw_index[0], box_draw_index[1]):
                                box_item_tuple = tuple(box_item)
                                frame[box_item_tuple[0], box_item_tuple[1]] = box_color

                            for title_item in zip(title_draw_index[0], title_draw_index[1]):
                                title_item_tuple = tuple(title_item)
                                frame[title_item_tuple[0], title_item_tuple[1]] = title_color

                clone_frame = np.copy(frame)

                # for loop and draw the data on the clone frame
                for info in series_array:
                    if len(draw_data_array) > 0:
                        info_name = info["name"]
                        display_arr = None
                        for dic in draw_data_array:
                            if dic["series_name"] == info_name:
                                display_arr = dic["series_data_array"]
                                break
                        search_str = info["parent_axes"]
                        pointer_info = info["pointer_value"]
                        need_to_draw_pointer = bool(pointer_info["enabled"])
                        line_color = change_string_to_color_tuple(info["line_color"])
                        line_thickness = int(info["line_thickness"])
                        zero_display = str_to_bool(str(info["zero_line_display"]))
                        zero_line_thick = 0
                        if zero_display:
                            zero_line_thick = int(info["zero_line_thickness"])
                        show_type = str(info["display_type"])
                        info_y_limit = info["y-limit"]
                        info_limits = info_y_limit["limits"]
                        lower_limit = info_limits["lower"]
                        upper_limit = info_limits["upper"]
                        can_zero_line_be_drawn = need_to_display_zero_line(lower_limit, upper_limit)
                        info_t_limit = info["t-limit"]
                        t_width = info_t_limit["width"]
                        pointer_color = None
                        pointer_radius = None
                        if need_to_draw_pointer:
                            pointer_color = change_string_to_color_tuple(pointer_info["color"])
                            pointer_radius = pointer_info["radius"]
                        parent_index = get_position_of_parent(search_str, axes_array)
                        axes_info = axes_array[parent_index]
                        if show_type == "pen" and parent_index is not None:
                            ax_pos = axes_info["position"]
                            ax_x = ax_pos["x"]
                            ax_y = ax_pos["y"]
                            ax_w = ax_pos["width"]
                            ax_h = ax_pos["height"]
                            if can_zero_line_be_drawn:
                                zero_line_start_x = ax_x
                                zero_line_y_scale = int(number_to_scale(lower_limit, upper_limit, ax_h, 0))
                                zero_line_y = int(ax_y + ax_h - zero_line_y_scale)
                                zero_line_end_x = ax_x + ax_w
                            else:
                                zero_line_start_x = 0
                                # zero_line_y_scale = 0
                                zero_line_y = 0
                                zero_line_end_x = 0
                            time_in_pixel_value = round((t_width / ax_w), 20)
                            # print(time_in_pixel_value)
                            time_interval_for_data = round(1 / (ax_w / t_width), 20)
                            start_x = ax_x
                            start_y = 0
                            value_to_draw = False
                            display_count = int(check_timer / (t_width * 1000))
                            # total_display_count = int(max_video_length / (t_width * 1000))
                            # end_x = 0
                            # end_y = 0
                            final_display_arr = display_arr[display_count][1]
                            # pointer_x = 0
                            # pointer_y = 0
                            check_timer_input = check_timer - (display_count * t_width * 1000)
                            drawable_limit = ax_x + int((check_timer_input / (time_interval_for_data * 1000)))
                            # pen_draw = False
                            no_first_value = False
                            pointer_position_info_name = info_name + "_pointer_info"

                            if len(final_display_arr) > 0:
                                for ind, num in enumerate(final_display_arr):
                                    if zero_display:
                                        cv2.line(clone_frame, (zero_line_start_x, zero_line_y),
                                                 (zero_line_end_x, zero_line_y),
                                                 line_color, zero_line_thick, cv2.LINE_AA)
                                    if type(num[1]) == str:
                                        if ind == 0:
                                            no_first_value = True

                                    elif math.isnan(num[1]):
                                        value_to_draw = False

                                    else:
                                        if not value_to_draw:
                                            if no_first_value:
                                                scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, num[1])
                                                start_x = ax_x
                                                start_y = int(ax_y + ax_h - scaled_num)
                                                value_to_draw = True
                                                no_first_value = False
                                            else:
                                                scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, num[1])
                                                # scaled_step = int(round(((num[0] / 1000) / time_in_pixel_value), 0))
                                                scaled_step = math.ceil((num[0] / 1000) / time_in_pixel_value)
                                                start_x = ax_x + scaled_step - (display_count * ax_w)
                                                start_y = int(ax_y + ax_h - scaled_num)
                                                value_to_draw = True
                                        else:
                                            if start_x >= drawable_limit:
                                                pen_draw = False
                                            else:
                                                pen_draw = True
                                            if pen_draw:
                                                scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, num[1])
                                                # scaled_step = int(round(((num[0] / 1000) / time_in_pixel_value), 0))
                                                scaled_step = math.ceil((num[0] / 1000) / time_in_pixel_value)
                                                end_x = ax_x + scaled_step - (display_count * ax_w)
                                                end_y = int(ax_y + ax_h - scaled_num)
                                                cv2.line(clone_frame, (start_x, start_y), (end_x, end_y),
                                                         line_color, line_thickness, cv2.LINE_AA)
                                                if need_to_draw_pointer and round(num[0] / 100, 0) >= round(
                                                        check_timer / 100, 0):
                                                    pointer_info_dict[pointer_position_info_name] = (end_x, end_y)

                                                start_x = end_x
                                                start_y = end_y

                                pointer_position_tuple = pointer_info_dict[pointer_position_info_name]
                                pointer_x = pointer_position_tuple[0]
                                pointer_y = pointer_position_tuple[1]
                                if pointer_x == ax_x or pointer_x == (ax_x + ax_w) or \
                                        pointer_y == ax_y or pointer_y == (ax_y - ax_h):
                                    pass
                                else:
                                    cv2.circle(clone_frame, (pointer_x, pointer_y), pointer_radius, pointer_color, -1)

                        elif show_type == "static" and parent_index is not None:
                            ax_pos = axes_info["position"]
                            ax_x = ax_pos["x"]
                            ax_y = ax_pos["y"]
                            ax_w = ax_pos["width"]
                            ax_h = ax_pos["height"]
                            if can_zero_line_be_drawn:
                                zero_line_start_x = ax_x
                                zero_line_y_scale = int(number_to_scale(lower_limit, upper_limit, ax_h, 0))
                                zero_line_y = int(ax_y + ax_h - zero_line_y_scale)
                                zero_line_end_x = ax_x + ax_w
                            else:
                                zero_line_start_x = 0
                                # zero_line_y_scale = 0
                                zero_line_y = 0
                                zero_line_end_x = 0
                            time_in_pixel_value = round((t_width / ax_w), 4)
                            # time_interval_for_data = round(1 / (ax_w / t_width), 4)
                            start_x = ax_x
                            start_y = 0
                            value_to_draw = False
                            display_count = int(check_timer / (t_width * 1000))
                            total_display_count = int(max_video_length / (t_width * 1000))
                            # end_x = 0
                            # end_y = 0
                            final_display_arr = display_arr[display_count][1]
                            pointer_position_info_name = info_name + "_pointer_info"

                            if len(final_display_arr) > 0:
                                for ind, num in enumerate(final_display_arr):
                                    if zero_display:
                                        cv2.line(clone_frame, (zero_line_start_x, zero_line_y),
                                                 (zero_line_end_x, zero_line_y),
                                                 line_color, zero_line_thick, cv2.LINE_AA)
                                    if type(num[1]) == str:
                                        pass

                                    elif math.isnan(num[1]):
                                        value_to_draw = False

                                    else:
                                        if not value_to_draw:
                                            scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, num[1])
                                            scaled_step = int(round(((num[0] / 1000) / time_in_pixel_value), 0))
                                            start_x = ax_x + scaled_step - (display_count * ax_w)
                                            start_y = int(ax_y + ax_h - scaled_num)
                                            value_to_draw = True
                                        else:
                                            scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, num[1])
                                            scaled_step = int(round(((num[0] / 1000) / time_in_pixel_value), 0))
                                            if display_count != total_display_count and ind == (
                                                    len(final_display_arr) - 1):
                                                end_x = ax_x + ax_w
                                            else:
                                                end_x = ax_x + scaled_step - (display_count * ax_w)
                                            end_y = int(ax_y + ax_h - scaled_num)
                                            cv2.line(clone_frame, (start_x, start_y), (end_x, end_y),
                                                     line_color, line_thickness, cv2.LINE_AA)
                                            if need_to_draw_pointer and (round(num[0] / 5, 0)) * 5 == round(check_timer,
                                                                                                            0):
                                                pointer_info_dict[pointer_position_info_name] = (end_x, end_y)

                                            start_x = end_x
                                            start_y = end_y
                                pointer_position_tuple = pointer_info_dict[pointer_position_info_name]
                                pointer_x = pointer_position_tuple[0]
                                pointer_y = pointer_position_tuple[1]
                                if pointer_x == ax_x or pointer_x == (ax_x + ax_w) or \
                                        pointer_y == ax_y or pointer_y == (ax_y - ax_h):
                                    pass
                                else:
                                    cv2.circle(clone_frame, (pointer_x, pointer_y), pointer_radius, pointer_color, -1)

                    else:
                        print("\r")
                        print("Drawable graph data is not found.")
                        drawing_graph = False

                for info in series_array:
                    search_string = info["parent_axes"]
                    parent_index = get_position_of_parent(search_string, axes_array)
                    if parent_index is not None:
                        axes_info = axes_array[parent_index]
                        axes_pos = axes_info["position"]
                        x = axes_pos["x"]
                        y = axes_pos["y"]
                        w = axes_pos["width"]
                        h = axes_pos["height"]
                        # crop the clone frame to get the graph box
                        cropped_image = clone_frame[y:(y + h), x:(x + w)]
                        # replace on the original frame in order to avoid over drawn
                        frame[y:(y + h), x:(x + w)] = cropped_image

                if display_able:
                    cv2.imshow("Frame", frame)
                    # cv2.imshow("F", clone_frame)
                # vsr_t = time.time()
                v_writer.write(frame)
                # vso_t = time.time()
                count += 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                end_whole_t = time.time()
                print("\r")
                print(f"The whole process took {round((end_whole_t - whole_t), 4)} seconds.")
                print(f"{output_video_file} is successfully produced.")
                print("Thank you for using VINSET")
                break

        input_video.release()
        v_writer.release()
        cv2.destroyAllWindows()


def add_data_array_to_series(series_type_input, main_data_dict, info_input, id_input):
    if series_type_input == "profile":
        t_data = info_input["t_data"]
        column_array = info_input["column_array"]
        info_filter = str_to_bool(str(info_input["filter"]))
        filter_by = None
        if info_filter:
            filter_by = info_input["filter_by"]
        minimum_column_name = get_info_from_dict(info_input, "minimum_column_name")
        data_arr = get_profile_data_array(main_data_dict, t_data, column_array,
                                          minimum_column_name, info_filter, filter_by)
        info_input["profile_data_array"] = data_arr
        info_input["series_id"] = id_input
    else:
        axes_info = info_input["axes_info"]
        axes_pos = axes_info["position"]
        axes_pos_w = axes_pos["width"]
        series_name = info_input["name"]
        info_input["series_id"] = id_input
        # display_type = info["display_type"]
        t_limit = info_input["t-limit"]
        # try:
        #     t_offset = info["time_offset"]
        # except KeyError:
        #     t_offset = 0
        t_w = t_limit["width"]
        t_data = info_input["t_data_name"]
        y_data = info_input["y_data_name"]
        info_filter = str_to_bool(str(info_input["filter"]))
        filter_by = None
        if info_filter:
            filter_by = info_input["filter_by"]
        # getting data from csv with or without filter
        data_arr = get_data_array_v_5(main_data_dict, t_data, y_data, info_filter, filter_by)

        # calculate the max duration of time can be displayed in one pixel
        time_interval_for_data = int(1000 / (axes_pos_w / t_w))

        # adjust the num of data into displayable amount
        data_arr = time_adjust_to_pixel(data_arr, time_interval_for_data)

        series_data_array = get_series_data_array(data_arr, t_w)
        if series_data_array is None:
            raise ValueError(f"The series_data_array is None in series_name : {series_name}.")

        info_input["series_name"] = series_name
        info_input["series_data_array"] = series_data_array
        info_input["time_interval"] = time_interval_for_data


def draw_box_by_series_info(series_type_input, frame_input, info_input):
    if series_type_input == "profile":
        axes_info = info_input["axes_info"]
        axes_pos = axes_info["position"]
        x = axes_pos["x"]
        y = axes_pos["y"]
        w = axes_pos["width"]
        h = axes_pos["height"]
        # box_line_color = change_string_to_color_tuple(axes_info["box_line_color"])

        box_style = axes_info["box_style"]
        box_fill = str_to_bool(str(box_style["fill"]))
        if box_fill:
            box_thickness = -1
            fill_color = change_string_to_color_tuple(box_style["fill_color"])
        else:
            box_thickness = box_style["thickness"]
            fill_color = change_string_to_color_tuple(box_style["fill_color"])
        box_opacity = box_style["opacity"]
        # copy a frame to draw boundary
        overlay_frame = frame_input.copy()
        box_padding = box_style["padding"]
        box_left_padding = box_padding["left"]
        box_right_padding = box_padding["right"]
        box_top_padding = box_padding["top"]
        box_bottom_padding = box_padding["bottom"]
        # draw boundary to graph
        cv2.rectangle(overlay_frame,
                      (x - box_left_padding, y - box_top_padding),
                      (x + w + box_right_padding,
                       y + h + box_bottom_padding),
                      fill_color, box_thickness)
        # overlay by original frame
        frame_input = cv2.addWeighted(overlay_frame, box_opacity,
                                      frame_input, 1 - box_opacity, 0)
        # draw graphs and labels over the frame
        # to avoid color opacity drops and repeated
        axes_info = info_input["axes_info"]
        box_line_color = axes_info["box_line_color"]
        axes_pos = axes_info["position"]
        box_title = axes_info["box_title"]
        box_title_position = axes_info["box_title_position"]
        title_x_position = box_title_position["x"]
        title_y_position = box_title_position["y"]
        box_title_style = axes_info["box_title_style"]
        box_title_family = box_title_style["font_family"]
        box_title_font_size = box_title_style["font_size"]
        box_title_color = box_title_style["color"]
        box_line_color = change_string_to_color_tuple(box_line_color)
        box_title_color = change_string_to_color_tuple(box_title_color)
        box_line_thickness = int(axes_info["box_line_thickness"])
        axes_pos_x = axes_pos["x"]
        axes_pos_y = axes_pos["y"]
        axes_pos_w = axes_pos["width"]
        axes_pos_h = axes_pos["height"]
        x_limit = info_input["x-limit"]
        x_limit_type = x_limit["type"]
        if x_limit_type == "nom":
            x_w = 10
        else:
            x_w = x_limit["width"]
        x_name = info_input["x_label"]
        x_label_position = info_input["x_label_position"]
        x_label_x_position = x_label_position["x"]
        x_label_y_position = x_label_position["y"]
        x_label_style = info_input["x_label_style"]
        x_label_font_family = x_label_style["font_family"]
        x_label_font_size = x_label_style["font_size"]
        x_label_color = x_label_style["color"]
        y_name = info_input["y_label"]
        y_label_position = info_input["y_label_position"]
        y_label_x_position = y_label_position["x"]
        y_label_y_position = y_label_position["y"]
        y_label_style = info_input["y_label_style"]
        y_label_font_family = y_label_style["font_family"]
        y_label_font_size = y_label_style["font_size"]
        y_label_color = y_label_style["color"]
        # draw box and labels according to config
        if box_line_color is not None:
            frame_input = cv2.rectangle(frame_input, (axes_pos_x, axes_pos_y),
                                        ((axes_pos_x + axes_pos_w), (axes_pos_y + axes_pos_h)),
                                        box_line_color, box_line_thickness)
        title_x = int(axes_pos_x) + int(title_x_position)
        title_y = int(axes_pos_y) - int(title_y_position)
        frame_input = pillow_put_text(frame_input, box_title, (title_x, title_y), box_title_family,
                                      box_title_font_size, box_title_color)
        x_label_x = int(axes_pos_x) + int(x_label_x_position)
        x_label_y = int(axes_pos_y) + int(x_label_y_position)
        frame_input = pillow_put_text(frame_input, x_name, (x_label_x, x_label_y), x_label_font_family,
                                      x_label_font_size, x_label_color)
        y_label_x = int(axes_pos_x) + int(y_label_x_position)
        y_label_y = int(axes_pos_y) + int(y_label_y_position)
        frame_input = pillow_put_text(frame_input, y_name, (y_label_x, y_label_y), y_label_font_family,
                                      y_label_font_size, y_label_color)

        x_scale_interval_width = int(axes_pos_w / x_w)
        # start_point_x_scale = axes_pos_x
        # x_scale_level = axes_pos_y + axes_pos_h
        x_label_tick = info_input["x_label_tick"]
        draw_x_tick = str_to_bool(str(x_label_tick["enabled"]))
        if draw_x_tick:
            x_tick_color = change_string_to_color_tuple(x_label_tick["color"])
            x_tick_height = x_label_tick["height"]
            x_tick_thickness = x_label_tick["thickness"]
            # draw x axis / t axis interval points
            for i in range(0, x_w):
                space_value = i * x_scale_interval_width
                tick_start_pos = (axes_pos_x + space_value, axes_pos_h + axes_pos_y)
                tick_end_pos = (axes_pos_x + space_value, axes_pos_h + axes_pos_y - x_tick_height)
                cv2.line(frame_input, tick_start_pos, tick_end_pos, x_tick_color, x_tick_thickness, cv2.LINE_AA)
    else:
        axes_info = info_input["axes_info"]
        axes_pos = axes_info["position"]
        x = axes_pos["x"]
        y = axes_pos["y"]
        w = axes_pos["width"]
        h = axes_pos["height"]
        # box_line_color = change_string_to_color_tuple(axes_info["box_line_color"])

        box_style = axes_info["box_style"]
        box_fill = str_to_bool(str(box_style["fill"]))
        if box_fill:
            box_thickness = -1
            fill_color = change_string_to_color_tuple(box_style["fill_color"])
        else:
            box_thickness = box_style["thickness"]
            fill_color = change_string_to_color_tuple(box_style["fill_color"])
        box_opacity = box_style["opacity"]
        # copy a frame to draw boundary
        overlay_frame = frame_input.copy()
        box_padding = box_style["padding"]
        box_left_padding = box_padding["left"]
        box_right_padding = box_padding["right"]
        box_top_padding = box_padding["top"]
        box_bottom_padding = box_padding["bottom"]
        # draw boundary to graph
        cv2.rectangle(overlay_frame,
                      (x - box_left_padding, y - box_top_padding),
                      (x + w + box_right_padding,
                       y + h + box_bottom_padding),
                      fill_color, box_thickness)
        # overlay by original frame
        frame_input = cv2.addWeighted(overlay_frame, box_opacity,
                                      frame_input, 1 - box_opacity, 0)
        # draw graphs and labels over the frame
        # to avoid color opacity drops and repeated
        axes_info = info_input["axes_info"]
        box_line_color = axes_info["box_line_color"]
        axes_pos = axes_info["position"]
        box_title = axes_info["box_title"]
        box_title_position = axes_info["box_title_position"]
        title_x_position = box_title_position["x"]
        title_y_position = box_title_position["y"]
        box_title_style = axes_info["box_title_style"]
        box_title_family = box_title_style["font_family"]
        box_title_font_size = box_title_style["font_size"]
        box_title_color = box_title_style["color"]
        box_line_color = change_string_to_color_tuple(box_line_color)
        box_title_color = change_string_to_color_tuple(box_title_color)
        box_line_thickness = int(axes_info["box_line_thickness"])
        axes_pos_x = axes_pos["x"]
        axes_pos_y = axes_pos["y"]
        axes_pos_w = axes_pos["width"]
        axes_pos_h = axes_pos["height"]
        t_limit = info_input["t-limit"]
        t_w = t_limit["width"]
        t_name = info_input["t_label"]
        t_label_position = info_input["t_label_position"]
        t_label_x_position = t_label_position["x"]
        t_label_y_position = t_label_position["y"]
        t_label_style = info_input["t_label_style"]
        t_label_font_family = t_label_style["font_family"]
        t_label_font_size = t_label_style["font_size"]
        t_label_color = t_label_style["color"]
        y_name = info_input["y_label"]
        y_label_position = info_input["y_label_position"]
        y_label_x_position = y_label_position["x"]
        y_label_y_position = y_label_position["y"]
        y_label_style = info_input["y_label_style"]
        y_label_font_family = y_label_style["font_family"]
        y_label_font_size = y_label_style["font_size"]
        y_label_color = y_label_style["color"]
        # draw box and labels according to config
        if box_line_color is not None:
            frame_input = cv2.rectangle(frame_input, (axes_pos_x, axes_pos_y),
                                        ((axes_pos_x + axes_pos_w), (axes_pos_y + axes_pos_h)),
                                        box_line_color, box_line_thickness)
        title_x = int(axes_pos_x) + int(title_x_position)
        title_y = int(axes_pos_y) - int(title_y_position)
        frame_input = pillow_put_text(frame_input, box_title, (title_x, title_y), box_title_family,
                                      box_title_font_size, box_title_color)
        t_label_x = int(axes_pos_x) + int(t_label_x_position)
        t_label_y = int(axes_pos_y) + int(t_label_y_position)
        frame_input = pillow_put_text(frame_input, t_name, (t_label_x, t_label_y), t_label_font_family,
                                      t_label_font_size, t_label_color)
        y_label_x = int(axes_pos_x) + int(y_label_x_position)
        y_label_y = int(axes_pos_y) + int(y_label_y_position)
        frame_input = pillow_put_text(frame_input, y_name, (y_label_x, y_label_y), y_label_font_family,
                                      y_label_font_size, y_label_color)

        x_scale_interval_width = int(axes_pos_w / t_w)
        # start_point_x_scale = axes_pos_x
        # x_scale_level = axes_pos_y + axes_pos_h
        t_label_tick = info_input["t_label_tick"]
        draw_t_tick = str_to_bool(str(t_label_tick["enabled"]))
        if draw_t_tick:
            t_tick_color = change_string_to_color_tuple(t_label_tick["color"])
            t_tick_height = t_label_tick["height"]
            t_tick_thickness = t_label_tick["thickness"]
            # draw x axis / t axis interval points
            for i in range(0, t_w):
                space_value = i * x_scale_interval_width
                tick_start_pos = (axes_pos_x + space_value, axes_pos_h + axes_pos_y)
                tick_end_pos = (axes_pos_x + space_value, axes_pos_h + axes_pos_y - t_tick_height)
                cv2.line(frame_input, tick_start_pos, tick_end_pos, t_tick_color, t_tick_thickness, cv2.LINE_AA)

    return frame_input


def draw_graph_by_series_info(series_type_input, clone_frame_input, info_input, check_timer_input):
    if series_type_input == "profile":
        display_info = {**info_input}
        line_color = change_string_to_color_tuple(info_input["line_color"])
        line_thickness = int(info_input["line_thickness"])
        info_y_limit = info_input["y-limit"]
        info_limits = info_y_limit["limits"]
        lower_limit = info_limits["lower"]
        upper_limit = info_limits["upper"]
        x_pixel_offset = get_info_from_dict(info_input, "x_pixel_offset")
        if x_pixel_offset is not None:
            x_pixel_offset = int(x_pixel_offset)
        else:
            x_pixel_offset = 0
        y_pixel_offset = get_info_from_dict(info_input, "y_pixel_offset")
        if y_pixel_offset is not None:
            y_pixel_offset = int(y_pixel_offset)
        else:
            y_pixel_offset = 0
        axes_info = info_input["axes_info"]
        ax_pos = axes_info["position"]
        ax_x = ax_pos["x"]
        ax_y = ax_pos["y"]
        ax_w = ax_pos["width"]
        ax_h = ax_pos["height"]
        display_info["lower_limit"] = lower_limit
        display_info["upper_limit"] = upper_limit
        display_info["ax_x"] = ax_x
        display_info["ax_y"] = ax_y
        display_info["ax_w"] = ax_w
        display_info["ax_h"] = ax_h
        display_info["line_color"] = line_color
        display_info["line_thickness"] = line_thickness
        display_info["x_pixel_offset"] = x_pixel_offset
        display_info["y_pixel_offset"] = y_pixel_offset
        clone_frame_input = draw_graph_by_profile_info(clone_frame_input, check_timer_input, display_info)
    else:
        display_info = {**info_input}
        pointer_info = info_input["pointer_value"]
        time_line_info = get_info_from_dict(info_input, "vertical_time_line")
        need_to_draw_pointer = str_to_bool(pointer_info["enabled"])
        if time_line_info is None:
            need_to_draw_time_line = False
        else:
            need_to_draw_time_line = str_to_bool(time_line_info["enabled"])
        line_color = change_string_to_color_tuple(info_input["line_color"])
        line_thickness = int(info_input["line_thickness"])
        zero_display = str_to_bool(str(info_input["zero_line_display"]))
        if zero_display:
            zero_line_style = info_input["zero_line_style"]
            zero_line_thickness = int(zero_line_style["thickness"])
            zero_line_color = change_string_to_color_tuple(str(zero_line_style["color"]))
            zero_line_opacity = zero_line_style["opacity"]
        else:
            zero_line_thickness = 0
            zero_line_color = None
            zero_line_opacity = 0
        info_y_limit = info_input["y-limit"]
        info_limits = info_y_limit["limits"]
        lower_limit = info_limits["lower"]
        upper_limit = info_limits["upper"]
        x_pixel_offset = get_info_from_dict(info_input, "x_pixel_offset")
        if x_pixel_offset is not None:
            x_pixel_offset = int(x_pixel_offset)
        else:
            x_pixel_offset = 0
        y_pixel_offset = get_info_from_dict(info_input, "y_pixel_offset")
        if y_pixel_offset is not None:
            y_pixel_offset = int(y_pixel_offset)
        else:
            y_pixel_offset = 0
        can_zero_line_be_drawn = need_to_display_zero_line(lower_limit, upper_limit)
        if need_to_draw_pointer:
            pointer_color = change_string_to_color_tuple(pointer_info["color"])
            pointer_radius = pointer_info["radius"]
            display_info["draw_pointer"] = True
            display_info["pointer_color"] = pointer_color
            display_info["pointer_radius"] = pointer_radius
        else:
            display_info["draw_pointer"] = False
            display_info["pointer_color"] = None
            display_info["pointer_radius"] = None
        if need_to_draw_time_line:
            display_info["draw_time_line"] = True
            display_info["time_line_opacity"] = time_line_info["opacity"]
            display_info["time_line_color"] = change_string_to_color_tuple(time_line_info["color"])
            display_info["time_line_thickness"] = time_line_info["thickness"]
        else:
            display_info["draw_time_line"] = False
            display_info["time_line_opacity"] = None
            display_info["time_line_color"] = None
            display_info["time_line_thickness"] = None
        axes_info = info_input["axes_info"]
        ax_pos = axes_info["position"]
        ax_x = ax_pos["x"]
        ax_y = ax_pos["y"]
        ax_w = ax_pos["width"]
        ax_h = ax_pos["height"]
        if can_zero_line_be_drawn:
            zero_line_start_x = ax_x
            zero_line_y_scale = int(number_to_scale(lower_limit, upper_limit, ax_h, 0))
            zero_line_y = int(ax_y + ax_h - zero_line_y_scale)
            zero_line_end_x = ax_x + ax_w
        else:
            zero_line_start_x = 0
            # zero_line_y_scale = 0
            zero_line_y = 0
            zero_line_end_x = 0
        if zero_display:
            overlay_frame = clone_frame_input.copy()
            cv2.line(overlay_frame, (zero_line_start_x, zero_line_y),
                     (zero_line_end_x, zero_line_y),
                     zero_line_color, zero_line_thickness, cv2.LINE_AA)
            clone_frame = cv2.addWeighted(overlay_frame, zero_line_opacity,
                                          clone_frame_input, 1 - zero_line_opacity,
                                          0)
        display_info["lower_limit"] = lower_limit
        display_info["upper_limit"] = upper_limit
        display_info["ax_x"] = ax_x
        display_info["ax_y"] = ax_y
        display_info["ax_w"] = ax_w
        display_info["ax_h"] = ax_h
        display_info["line_color"] = line_color
        display_info["line_thickness"] = line_thickness
        display_info["x_pixel_offset"] = x_pixel_offset
        display_info["y_pixel_offset"] = y_pixel_offset
        clone_frame_input = draw_normal_series_graph(clone_frame_input, check_timer_input, display_info)

    return clone_frame_input


def overlay_graph_v_5(config_info_input, input_video_file, csv_to_be_used,
                      output_video_file, show_preview_video=True):
    axes_array = config_info_input["axes"]
    series_array = config_info_input["series"]
    display_able = str_to_bool(str(config_info_input["display"]))
    if not show_preview_video:
        display_able = False
    main_csv_data_dict = get_dict_from_csv(csv_to_be_used)

    input_video = cv2.VideoCapture(input_video_file)
    frame_width = input_video.get(cv2.CAP_PROP_FRAME_WIDTH)
    print("Frame width:", frame_width)
    frame_height = input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("Frame height:", frame_height)
    frame_rate = input_video.get(cv2.CAP_PROP_FPS)
    print("Frame rate:", frame_rate)
    frame_count = input_video.get(cv2.CAP_PROP_FRAME_COUNT)
    print("Frame count:", frame_count)

    # max_video_length = math.ceil(frame_count_to_time(frame_count, frame_rate))
    series_id = 1

    for info in series_array:
        search_string = info["parent_axes"]
        parent_index = get_position_of_parent(search_string, axes_array)
        if parent_index is not None:
            axes_info = axes_array[parent_index]
            info["axes_info"] = axes_info

    # for loop over series array and prepare the respected data
    for info in series_array:
        series_type = get_info_from_dict(info, "series_type")
        add_data_array_to_series(series_type, main_csv_data_dict, info, series_id)
        series_id += 1

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    v_writer = cv2.VideoWriter(output_video_file, fourcc, int(frame_rate), (int(frame_width), int(frame_height)))
    whole_t = time.time()
    count = 0
    drawing_graph = True

    while drawing_graph:

        # start_tt = time.time()
        ret, frame = input_video.read()
        # end_tt = time.time()
        print_percent_done(count, frame_count)
        check_timer = frame_count_to_time(count, frame_rate)
        display_time = frame_count_to_display_time(count, frame_rate)

        if ret:
            for info in series_array:
                series_type = get_info_from_dict(info, "series_type")
                frame = draw_box_by_series_info(series_type, frame, info)

            clone_frame = np.copy(frame)

            # for loop and draw the data on the clone frame
            for info in series_array:
                series_type = get_info_from_dict(info, "series_type")
                clone_frame = draw_graph_by_series_info(series_type, clone_frame, info, check_timer)

            for info in series_array:
                search_string = info["parent_axes"]
                parent_index = get_position_of_parent(search_string, axes_array)
                if parent_index is not None:
                    axes_info = axes_array[parent_index]
                    axes_pos = axes_info["position"]
                    x = axes_pos["x"]
                    y = axes_pos["y"]
                    w = axes_pos["width"]
                    h = axes_pos["height"]
                    # crop the clone frame to get the graph box
                    cropped_image = clone_frame[y:(y + h), x:(x + w)]
                    # replace on the original frame in order to avoid over drawn
                    frame[y:(y + h), x:(x + w)] = cropped_image

            texts_array = get_info_from_dict(config_info_input, "texts")
            if texts_array is not None:
                for text_info in texts_array:
                    frame = draw_texts(frame, text_info, main_csv_data_dict,
                                       count, display_time, check_timer)

            if display_able:
                cv2.imshow("Frame", frame)
                # cv2.imshow("F", clone_frame)
            # vsr_t = time.time()
            v_writer.write(frame)
            # vso_t = time.time()
            count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            end_whole_t = time.time()
            print("\r")
            print(f"The whole process took {round((end_whole_t - whole_t), 4)} seconds.")
            print(f"{output_video_file} is successfully produced.")
            print("Thank you for using VINSET")
            break

    input_video.release()
    v_writer.release()
    cv2.destroyAllWindows()


def overlay_text(draw_able_input, config_info_input, input_video_file,
                 output_video_file, timeline_file, show_preview_video=True):
    text_info = config_info_input["text_info"]
    va_text_color = text_info["va_text_color"]
    va_text_font_size = text_info["va_text_font_size"]
    va_text_color_tuple = change_string_to_color_tuple(va_text_color)
    va_text_thickness = text_info["va_text_thickness"]
    stimulus_text_color = text_info["stimulus_text_color"]
    stimulus_text_font_size = text_info["stimulus_text_font_size"]
    stimulus_text_color_tuple = change_string_to_color_tuple(stimulus_text_color)
    stimulus_text_thickness = text_info["stimulus_text_thickness"]
    timeline_info = None
    stimulus_text_display_location = config_info_input["stimulus_text_display_location"]
    va_text_display_location = config_info_input["va_text_display_location"]
    sti_x_position = stimulus_text_display_location["x"]
    sti_y_position = stimulus_text_display_location["y"]
    va_x_position = va_text_display_location["x"]
    va_y_position = va_text_display_location["y"]
    minimum_va_decimal = text_info["minimum_va_decimal"]
    extra_draw = config_info_input["base_draw"]
    if extra_draw:
        extra_draw_names = config_info_input["base_draw_names"]
        extra_draw_info = config_info_input["base_draw_info"]
    else:
        extra_draw_names = None
        extra_draw_info = None

    try:
        f = open(timeline_file)
        timeline_info = json.load(f)
        print(f"{timeline_file} is loaded successfully by json.")
        # print(timeline_info)
    except ValueError:
        draw_able_input = False
        print(f"{timeline_file} cannot be loaded by json.")

    if draw_able_input and config_info_input:
        display_able = str_to_bool(str(config_info_input["display"]))
        if not show_preview_video:
            display_able = False

        input_video = cv2.VideoCapture(input_video_file)
        frame_width = input_video.get(cv2.CAP_PROP_FRAME_WIDTH)
        print("Frame width:", frame_width)
        frame_height = input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("Frame height:", frame_height)
        frame_rate = input_video.get(cv2.CAP_PROP_FPS)
        print("Frame rate:", frame_rate)
        frame_count = input_video.get(cv2.CAP_PROP_FRAME_COUNT)
        print("Frame count:", frame_count)

        stimulus_level_array = get_logmar_level_array(timeline_info, text_info)

        final_stimulus_level_array = add_logmar_interval(stimulus_level_array, text_info)

        # for data in final_stimulus_level_array:
        #     print(data)
        # return

        max_video_length = math.ceil(frame_count_to_time(frame_count, frame_rate))
        print(f"Video length:{max_video_length / 1000} sec")

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        v_writer = cv2.VideoWriter(output_video_file, fourcc, int(frame_rate), (int(frame_width), int(frame_height)))
        whole_t = time.time()
        count = 0
        drawing_graph = True
        start_drawing = False
        stimulus_display_text = None
        sweep_order = None
        final_stimulus_level_array_length = len(final_stimulus_level_array)
        # print(final_stimulus_level_array_length)
        stimulus_index = 0

        while drawing_graph:
            # start_tt = time.time()
            ret, frame = input_video.read()
            # end_tt = time.time()
            print_percent_done(count, frame_count)
            check_timer = frame_count_to_time(count, frame_rate)

            if ret:
                if extra_draw_names and extra_draw_info:
                    for name in extra_draw_names:
                        info = get_extra_draw_info(name, extra_draw_info)
                        if info:
                            info_type = info["info_type"]
                            info_details = info["info_details"]
                            if info_type == "box":
                                boundary_space = info_details["boundary_space"]
                                x = info_details["x"]
                                y = info_details["y"]
                                w = info_details["w"]
                                h = info_details["h"]
                                color = info_details["color"]
                                opacity = info_details["opacity"]
                                color_input = change_string_to_color_tuple(color)
                                # copy a frame to draw boundary
                                overlay_frame = frame.copy()
                                # draw boundary to graph
                                cv2.rectangle(overlay_frame,
                                              (x - boundary_space, y - boundary_space),
                                              (x + w + boundary_space,
                                               y + h + boundary_space),
                                              color_input, -1)
                                # overlay by original frame
                                frame = cv2.addWeighted(overlay_frame, opacity,
                                                        frame, 1 - opacity, 0)

                if stimulus_index < final_stimulus_level_array_length:
                    stimulus_timestamp_to_check = final_stimulus_level_array[stimulus_index]["timestamp"] * 1000
                    if check_timer >= stimulus_timestamp_to_check:
                        start_drawing = True
                        stimulus_display_text = str(final_stimulus_level_array[stimulus_index]["logmar"])
                        sweep_order = final_stimulus_level_array[stimulus_index]["sweep_order"]
                        stimulus_index += 1

                if start_drawing:
                    nearest_stimulus_text = get_nearest_stimulus(stimulus_display_text)
                    cv2.putText(frame, f"showing {str(nearest_stimulus_text)} logMAR", (sti_x_position, sti_y_position),
                                cv2.FONT_HERSHEY_TRIPLEX, stimulus_text_font_size,
                                stimulus_text_color_tuple, stimulus_text_thickness, cv2.LINE_AA)
                    va_display_text = get_va_from_stimulus(str(stimulus_display_text), sweep_order, minimum_va_decimal)
                    cv2.putText(frame, f"{str(va_display_text)} logMAR", (va_x_position, va_y_position),
                                cv2.FONT_HERSHEY_TRIPLEX, va_text_font_size,
                                va_text_color_tuple, va_text_thickness, cv2.LINE_AA)
                    if sweep_order == "resting":
                        start_drawing = False

                if display_able:
                    cv2.imshow("Frame", frame)
                    # cv2.imshow("F", clone_frame)
                    # vsr_t = time.time()
                    v_writer.write(frame)
                    # vso_t = time.time()
                    count += 1
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            else:
                end_whole_t = time.time()
                print("\r")
                print(f"The whole process took {round((end_whole_t - whole_t), 4)} seconds.")
                print(f"{output_video_file} is successfully produced.")
                print("Thank you for using VINSET")
                break

        input_video.release()
        v_writer.release()
        cv2.destroyAllWindows()


def get_logmar_level_array(timeline_info_info, text_info_input):
    draw_data = []
    end_marker_indicator = text_info_input["end_marker_location"]
    end_marker_name = text_info_input["end_marker_name"]
    # tt = trial_type
    end_marker_tt = text_info_input["end_marker_trial_type"]
    tt_indicator = text_info_input["end_marker_trial_type_location"]
    text_indicator = text_info_input["text_marker_location"]
    time_indicator = text_info_input["time_marker_location"]
    first_text_indicator, second_text_indicator, third_text_indicator = str(text_indicator).split("->")
    first_end_indicator, second_end_indicator, third_end_indicator = str(end_marker_indicator).split("->")
    first_tt_indicator, second_tt_indicator, third_tt_indicator = str(tt_indicator).split("->")
    first_time_indicator, second_time_indicator, third_time_indicator = str(time_indicator).split("->")
    minimum_va_decimal = text_info_input["minimum_va_decimal"]
    stimulus_step = text_info_input["stimulus_step"]
    last_logmar = None
    second_last_logmar = None
    for event in timeline_info_info:
        first_attribute = str(list(event.keys())[0])
        try:
            second_attribute = str(list(event.keys())[1])
        except IndexError:
            second_attribute = None
        if first_attribute == first_text_indicator:
            event_info = event[first_attribute]
            time_value = event_info[second_time_indicator][third_time_indicator]
            text_value = str(round((float(event_info[second_text_indicator][third_text_indicator])), 2))
            text_value = check_and_add_decimal(text_value, minimum_va_decimal)
            if last_logmar:
                second_last_logmar = last_logmar
                last_logmar = text_value
            else:
                last_logmar = text_value
            data = {"marker_name": first_attribute, "timestamp": time_value, "logmar": text_value}
            draw_data.append(data)
        elif second_attribute is not None and second_attribute == first_end_indicator:
            event_info = event[second_attribute]
            end_marker_string = event_info[second_end_indicator][third_end_indicator]
            tt_string = event_info[second_tt_indicator][third_tt_indicator]
            if end_marker_string == end_marker_name and tt_string == end_marker_tt:
                time_value = event_info[second_time_indicator][third_time_indicator]
                if last_logmar < second_last_logmar:
                    text_value = str(round(float(last_logmar) - stimulus_step, 1))
                else:
                    text_value = str(round(float(last_logmar) + stimulus_step, 1))
                data = {"marker_name": second_attribute, "timestamp": time_value, "logmar": text_value}
                draw_data.append(data)
    # for d in draw_data:
    #     print(d)

    return draw_data


def add_logmar_interval(draw_data_array_input, text_info_input):
    va_logmar_interval = text_info_input["va_logmar_interval"]
    draw_data_array_length = len(draw_data_array_input)
    last_index = draw_data_array_length - 1
    # minimum_va_decimal = text_info_input["minimum_va_decimal"]

    final_data_array = []
    for index in range(draw_data_array_length):
        if index is not last_index:
            first_value = draw_data_array_input[index]
            second_value = draw_data_array_input[index + 1]
            first_logmar = float(first_value["logmar"])
            second_logmar = float(second_value["logmar"])
            first_timestamp = first_value["timestamp"]
            second_timestamp = second_value["timestamp"]
            first_marker = first_value["marker_name"]
            second_marker = second_value["marker_name"]

            if first_logmar > second_logmar:
                sweep_order = "descending"
            elif first_logmar < second_logmar:
                sweep_order = "ascending"
            else:
                sweep_order = None
            if sweep_order:
                if first_marker == "end":
                    first_value["sweep_order"] = "resting"
                    second_value["sweep_order"] = sweep_order
                    final_data_array.append(first_value)
                    final_data_array.append(second_value)
                elif second_marker == "end":
                    first_value["sweep_order"] = sweep_order
                    second_value["sweep_order"] = "resting"
                    logmar_diff = first_logmar - second_logmar
                    number_of_intervals = int(round(abs(logmar_diff), 1) / va_logmar_interval)
                    extra_data = number_of_intervals - 1
                    each_time_interval_duration = (second_timestamp - first_timestamp) / number_of_intervals
                    final_data_array.append(first_value)
                    for ind in range(extra_data):
                        time_value = first_timestamp + ((ind + 1) * each_time_interval_duration)
                        if sweep_order == "descending":
                            text_value = str(round((first_logmar - ((ind + 1) * va_logmar_interval)), 2))
                        else:
                            text_value = str(round(first_logmar + ((ind + 1) * va_logmar_interval), 2))
                        data = {"marker_name": second_marker, "timestamp": time_value, "logmar": text_value,
                                "sweep_order": sweep_order}
                        final_data_array.append(data)
                    final_data_array.append(second_value)
                else:
                    logmar_diff = first_logmar - second_logmar
                    number_of_intervals = int(round(abs(logmar_diff), 1) / va_logmar_interval)
                    first_value["sweep_order"] = sweep_order
                    second_value["sweep_order"] = sweep_order
                    extra_data = number_of_intervals - 1
                    each_time_interval_duration = (second_timestamp - first_timestamp) / number_of_intervals
                    final_data_array.append(first_value)
                    for ind in range(extra_data):
                        time_value = first_timestamp + ((ind + 1) * each_time_interval_duration)
                        if sweep_order == "descending":
                            text_value = str(round((first_logmar - ((ind + 1) * va_logmar_interval)), 2))
                        else:
                            text_value = str(round(first_logmar + ((ind + 1) * va_logmar_interval), 2))
                        data = {"marker_name": first_marker, "timestamp": time_value, "logmar": text_value,
                                "sweep_order": sweep_order}
                        final_data_array.append(data)
                    final_data_array.append(second_value)
    last_data = final_data_array[-1]
    last_data["sweep_order"] = "resting"
    final_data_array = list({dictionary['timestamp']: dictionary for dictionary in final_data_array}.values())

    return final_data_array


def check_and_add_decimal(string_input, min_decimal_input):
    decimal_count = str(string_input)[::-1].find('.')
    if 0 < decimal_count < min_decimal_input:
        num_of_zero_to_add = min_decimal_input - decimal_count
        string_input = string_input + "0" * num_of_zero_to_add
    return string_input


def get_va_from_stimulus(string_input, sweep_order_input, min_decimal_input):
    if sweep_order_input == "descending" or sweep_order_input == "resting":
        output = str(round((float(string_input) + 0.1), 2))
        output_string = check_and_add_decimal(output, min_decimal_input)
    else:
        output = string_input
        output_string = check_and_add_decimal(output, min_decimal_input)
    return output_string


def get_nearest_stimulus(string_input):
    point_index = str(string_input).find(".") + 2
    stimulus_value = float(string_input)
    if point_index > -1:
        string_input = string_input[:point_index]
        if float(string_input) == 0:
            string_input = "0.0"
        if float(string_input) < stimulus_value:
            string_input = str(round(float(string_input) + 0.1, 1))
    return string_input


def get_extra_draw_info(name_input, info_array_input):
    draw_info = None
    for info in info_array_input:
        info_name = info["info_name"]
        if info_name == name_input:
            draw_info = info
            break
    return draw_info


def is_it_video_file(video_dir_input):
    file_info = MediaInfo.parse(video_dir_input)
    for track in file_info.tracks:
        if track.track_type == "Video":
            return True
    return False


def load_commented_json(config_input):
    try:
        with open(config_input, 'r') as handle:
            out_info = commentjson.load(handle)
    except ValueError:
        out_info = None
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error : {type(err).__name__} in line number:{exc_tb.tb_lineno}.")
        out_info = None

    return out_info


def pillow_put_text(frame_in, text_in, text_pos_in, font_family_in, font_size_in, color_in):
    font_path = get_font_file_location(font_family_in)
    font = ImageFont.truetype(font_path, font_size_in)
    image_pil = Image.fromarray(frame_in)  # Convert OpenCV image to PIL image
    draw = ImageDraw.Draw(image_pil)
    draw.text(text_pos_in, text_in, font=font, fill=color_in)
    frame_in = np.array(image_pil)

    return frame_in


def main():
    parser = argparse.ArgumentParser(prog='vinset', description='VINSET package.')
    vinset_version = importlib.metadata.version('vinset')
    parser.add_argument('--version', action='version', version=vinset_version),
    parser.add_argument("-i", dest="input_file", required=True, default=None,
                        help="input mp4 file", metavar="input.mp4")
    parser.add_argument("-o", dest="output_file", required=True, default=None,
                        help="output mp4 file", metavar="output.mp4")
    parser.add_argument("-c", dest="config_file", required=True, default=None,
                        help="config json file", metavar="config.json")
    parser.add_argument("-d", dest="csv_data_input", required=False,
                        default=None, help="input csv data file", metavar="data.csv")
    parser.add_argument("-t", dest="overlay_type", required=False, default=None,
                        help="overlay type", metavar="graph or text")
    parser.add_argument("-tl", dest="timeline_file", required=False, default=None,
                        help="timeline file", metavar="timeline.json")
    parser.add_argument("-cpv", dest="close_preview_video", required=False,
                        help="close preview video", action="store_false")

    # get all input name in string
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    config_file = args.config_file
    csv_file = args.csv_data_input
    overlay_type = args.overlay_type
    timeline_file = args.timeline_file
    close_preview_video = args.close_preview_video

    # start whether the inputs are valid or not
    if os.path.isfile(input_file):
        if is_it_video_file(input_file):
            print(f"Input file: {input_file}.")
        else:
            print(f"Input file: {input_file} is not a video file.")
            return
    else:
        print(f"Input file: {input_file} does not exist.")
        return

    if str(output_file).endswith(".mp4"):
        print(f"Output file: {output_file}.")
    else:
        print(f"Output file: {output_file} is not a mp4 file.")
        return

    if os.path.isfile(config_file):
        if str(config_file).endswith(".json") or str(config_file).endswith(".config"):
            print(f"Config file: {config_file}.")
            config_info = load_commented_json(config_file)
            if config_info is None:
                print(f"Config file: {config_file} cannot be loaded.")
                return
            else:
                print(f"Config file: {config_file} is loaded successfully.")
        else:
            print(f"Config file: {config_file} is not a .json or .config file.")
            return
    else:
        print(f"Config file: {config_file} does not exist.")
        return

    if csv_file is None:
        print("There is csv file input.")
        print("Looking for \"csv_data\" name in config.")
        try:
            csv_filename_from_config = config_info["csv_data"]
        except KeyError:
            print(f"The \"csv_data\" name could not be found in the config.")
            return
        except TypeError:
            print(f"The \"csv_data\" name could not be found in the config.")
            return
        print(f"The \"csv_data\" name : {csv_filename_from_config} is found.")
        input_file_basename = os.path.basename(input_file)
        csv_file = str(input_file).replace(input_file_basename, csv_filename_from_config)

    if os.path.isfile(csv_file):
        if str(csv_file).endswith(".csv"):
            print(f"data csv file: {csv_file}.")
        else:
            print(f"data csv file: {csv_file} is not a csv file.")
            return
    else:
        print(f"data csv file: {csv_file} does not exist.")
        return

    if overlay_type:
        if str(overlay_type) == "graph" or str(overlay_type) == "text":
            print("Overlay type:", overlay_type)
            print("With overlay input, vinset will be using old version of graph drawing.")
            print("In the version above 5.0.0, vinset does not require overlay input.")
        else:
            print("Overlay type must be graph or text.")
            print("In the version above 5.0.0, vinset does not require overlay input.")
    else:
        pass

    if timeline_file:
        if os.path.isfile(timeline_file):
            if str(timeline_file).endswith(".json"):
                print(f"Timeline file: {timeline_file}.")
            else:
                print(f"Timeline file: {timeline_file} is not a .json file.")
                return
        else:
            print(f"Timeline file: {timeline_file} does not exist.")
            return

    if overlay_type is None:
        overlay_graph_v_5(config_info, input_file, csv_file, output_file, close_preview_video)
    elif str(overlay_type) == "graph":
        overlay_graph(True, config_info, input_file, csv_file, output_file, close_preview_video)
        pass
    elif str(overlay_type) == "text":
        if timeline_file:
            overlay_text(True, config_info, input_file, output_file, timeline_file, close_preview_video)
        else:
            print("There is no timeline input -tl in commandline.")
            print("Please add -tl argument in commandline in order to proceed.")
            return
    else:
        print("Invalid overlay type input. It must be graph or text.")
        return
