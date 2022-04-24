import json
import datetime
import time
from SentinelS7Database import SentinelS7Database

class QueryDeviceTimescale:

    def __init__(self, client):
        self.client = client
        # self.paginator = client.get_paginator('query')

    def run_controls_inc_device_query(self, device_id, table_name):
            db = SentinelS7Database(None)
            column_names = "published_at,device_id,cpu_usage_percent,ram_usage_percent,gps_lat,gps_lon,cellular_signal_strength,cellular_career,modbus_active,percent_load,actual_engine_percent_torque,engine_speed,total_engine_hours_lsb,total_engine_hours_msb,engine_coolant_temperature,engine_oil_temperature,fuel_delivery_pressure,engine_oil_pressure,coolant_level,fuel_rate,air_inlet_temperature,boost_pressure,alternator_potential_voltage,electrical_potential_voltage,battery_potential_voltage,injector_metering_rail_1_pressure,injector_metering_rail_2_pressure,fuel_level,short_term_fuel_trim_bank_1,inlet_suction_pressure,outlet_discharge_pressure,flow_rate,superpump_level_control,superpump_pressure_control,key_position,flow_rate_sender,water_temperature_sender,flow_rate_total_lsb,flow_rate_total_msb,digital_input_1_state,digital_input_2_state,relay_output_1_state,relay_output_2_state,stop_red_lamp_state,warning_amber_lamp_state,mil_lamp_state,wait_to_start_lamp_state,def_tank_level,control_transducer_level,control_transducer_pressure,inlet_pressure,outlet_pressure,superpump_throttle_manual_auto_status,superpump_throttle_type,auto_start_state,number_of_sets_of_active_fault_codes,active_spn_1_lsb,active_spn_1_msb,active_fmi_1,active_occurrence_count_1,active_spn_2_lsb,active_spn_2_msb,active_fmi_2,active_occurrence_count_2,active_spn_3_lsb,active_spn_3_msb,active_fmi_3,active_occurrence_count_3,active_spn_4_lsb,active_spn_4_msb,active_fmi_4,active_occurrence_count_4,active_spn_5_lsb,active_spn_5_msb,active_fmi_5,active_occurrence_count_5,active_spn_6_lsb,active_spn_6_msb,active_fmi_6,active_occurrence_count_6,active_spn_7_lsb,active_spn_7_msb,active_fmi_7,active_occurrence_count_7,active_spn_8_lsb,active_spn_8_msb,active_fmi_8,active_occurrence_count_8,active_spn_9_lsb,active_spn_9_msb,active_fmi_9,active_occurrence_count_9,active_spn_10_lsb,active_spn_10_msb,active_fmi_10,active_occurrence_count_10"
            column_names_array = column_names.split(",")
            # print(column_names_array)
            
            query = "SELECT * FROM {} WHERE device_id = '{}' and published_at > now() - INTERVAL '{}' ORDER BY published_at DESC LIMIT 1;".format(table_name, device_id, '7 days')
            # print(query)
            device_results = db.get_select_query_all_results(query)

            device_results_formatted_json = None
            if len(device_results) > 0:
                device_results_row = device_results[0]
                published_at = device_results_row[0].isoformat().replace('+00:00', 'Z')
                device_results_json = {}
                for idx, device_results_col in enumerate(device_results_row):
                    # print(idx, device_results_col)
                    device_results_json[column_names_array[idx]] = device_results_col
                device_results_json.pop('published_at', None)
                device_results_json.pop('device_id', None)

                device_results_formatted_json = self.format_device_results(device_results_json)
                device_results_formatted_json = self.transform_device_results(device_results_formatted_json)
                device_results_formatted_json['published_at'] = published_at
            return device_results_formatted_json

    def run_vfd_x_600_device_query(self, device_id, table_name):
        db = SentinelS7Database(None)
        column_names = "published_at,device_id,cpu_usage_percent,ram_usage_percent,gps_lat,gps_lon,cellular_signal_strength,cellular_career,modbus_active,supply_voltage_1,suct_psi,disc_psi,sec_disc_psi,hz_input,manual_hz,max_pres,suc_pres_setpnt,kp,bias,working_maxpsi,flowmeter_1_flow,flowmeter_2_flow,flowmeter_1_total,flowmeter_2_total,pit_lvl_1,pit_lvl_2,temp_encl,hz_output,auto_mode_tog,vfd_run_relay,vfd_flt_reset_relay,vlvc_ctrl,ambr_litrelay,vfd_fault_di,vfd_run_di,vlv_closed,vlv_open,on_backup"
        column_names_array = column_names.split(",")

        query = "SELECT * FROM {} WHERE device_id = '{}' and published_at > now() - INTERVAL '{}' ORDER BY published_at DESC LIMIT 1;".format(table_name, device_id, '7 days')
        # print(query)
        device_results = db.get_select_query_all_results(query)

        device_results_formatted_json = None
        if len(device_results) > 0:
            device_results_row = device_results[0]
            published_at = device_results_row[0].isoformat().replace('+00:00', 'Z')
            device_results_json = {}
            for idx, device_results_col in enumerate(device_results_row):
                # print(idx, device_results_col)
                device_results_json[column_names_array[idx]] = device_results_col
            device_results_json.pop('published_at', None)
            device_results_json.pop('device_id', None)

            device_results_formatted_json = self.format_and_transform_vfd_x_600_device_results(device_results_json)
            device_results_formatted_json['published_at'] = published_at
        return device_results_formatted_json

    def run_device_query(self, device_id, table_name, device_type):
        result = None
        if device_type == 'VFD_X_600':
            result = self.run_vfd_x_600_device_query(device_id, table_name)
        else: # Default to controls inc query
            result = self.run_controls_inc_device_query(device_id, table_name)
        return result

    def run_multiple_devices_query(self, controls_inc_devices):
            db = SentinelS7Database(None)
            column_names = "published_at,device_id,cpu_usage_percent,ram_usage_percent,gps_lat,gps_lon,cellular_signal_strength,cellular_career,modbus_active,percent_load,actual_engine_percent_torque,engine_speed,total_engine_hours_lsb,total_engine_hours_msb,engine_coolant_temperature,engine_oil_temperature,fuel_delivery_pressure,engine_oil_pressure,coolant_level,fuel_rate,air_inlet_temperature,boost_pressure,alternator_potential_voltage,electrical_potential_voltage,battery_potential_voltage,injector_metering_rail_1_pressure,injector_metering_rail_2_pressure,fuel_level,short_term_fuel_trim_bank_1,inlet_suction_pressure,outlet_discharge_pressure,flow_rate,superpump_level_control,superpump_pressure_control,key_position,flow_rate_sender,water_temperature_sender,flow_rate_total_lsb,flow_rate_total_msb,digital_input_1_state,digital_input_2_state,relay_output_1_state,relay_output_2_state,stop_red_lamp_state,warning_amber_lamp_state,mil_lamp_state,wait_to_start_lamp_state,def_tank_level,control_transducer_level,control_transducer_pressure,inlet_pressure,outlet_pressure,superpump_throttle_manual_auto_status,superpump_throttle_type,auto_start_state,number_of_sets_of_active_fault_codes,active_spn_1_lsb,active_spn_1_msb,active_fmi_1,active_occurrence_count_1,active_spn_2_lsb,active_spn_2_msb,active_fmi_2,active_occurrence_count_2,active_spn_3_lsb,active_spn_3_msb,active_fmi_3,active_occurrence_count_3,active_spn_4_lsb,active_spn_4_msb,active_fmi_4,active_occurrence_count_4,active_spn_5_lsb,active_spn_5_msb,active_fmi_5,active_occurrence_count_5,active_spn_6_lsb,active_spn_6_msb,active_fmi_6,active_occurrence_count_6,active_spn_7_lsb,active_spn_7_msb,active_fmi_7,active_occurrence_count_7,active_spn_8_lsb,active_spn_8_msb,active_fmi_8,active_occurrence_count_8,active_spn_9_lsb,active_spn_9_msb,active_fmi_9,active_occurrence_count_9,active_spn_10_lsb,active_spn_10_msb,active_fmi_10,active_occurrence_count_10"
            column_names_array = column_names.split(",")
            # print(column_names_array)
            devices_ids = []
            for devices in controls_inc_devices:
                devices_ids.append(devices['device_serial']) 

            table_name = controls_inc_devices[0]['device_table_name']
            
            query = "SELECT DISTINCT ON (device_id) * FROM {} WHERE device_id in ({}) and published_at > now() - INTERVAL '{}' ORDER BY device_id,published_at DESC".format(table_name, ','.join(['%s'] * len(devices_ids)), '7 days')
            # print(query)
            device_results = db.get_select_query_all_results_with_params(query, devices_ids)
            
            multiple_devices_results_formatted = []
            device_results_formatted_json = None
            if len(device_results) > 0:
                # print(device_results)
                for device_results_row in device_results:
                    published_at = device_results_row[0].isoformat().replace('+00:00', 'Z')
                    device_id = device_results_row[1]
                    device_results_json = {}
                    for idx, device_results_col in enumerate(device_results_row):
                        # print(idx, device_results_col)
                        device_results_json[column_names_array[idx]] = device_results_col
                    device_results_json.pop('published_at', None)
                    device_results_json.pop('device_id', None)

                    device_results_formatted_json = self.format_device_results(device_results_json)
                    device_results_formatted_json = self.transform_device_results(device_results_formatted_json)
                    device_results_formatted_json['published_at'] = published_at
                    device_results_formatted_json['device_id'] = device_id
                    multiple_devices_results_formatted.append(device_results_formatted_json)
            
            return multiple_devices_results_formatted

    def run_vfd_x_600_multiple_devices_query(self, vfd_x_600_devices):
            db = SentinelS7Database(None)
            column_names = "published_at,device_id,cpu_usage_percent,ram_usage_percent,gps_lat,gps_lon,cellular_signal_strength,cellular_career,modbus_active,supply_voltage_1,suct_psi,disc_psi,sec_disc_psi,hz_input,manual_hz,max_pres,suc_pres_setpnt,kp,bias,working_maxpsi,flowmeter_1_flow,flowmeter_2_flow,flowmeter_1_total,flowmeter_2_total,pit_lvl_1,pit_lvl_2,temp_encl,hz_output,auto_mode_tog,vfd_run_relay,vfd_flt_reset_relay,vlvc_ctrl,ambr_litrelay,vfd_fault_di,vfd_run_di,vlv_closed,vlv_open,on_backup"
            column_names_array = column_names.split(",")
            # print(column_names_array)
            devices_ids = []
            for devices in vfd_x_600_devices:
                devices_ids.append(devices['device_serial']) 

            table_name = vfd_x_600_devices[0]['device_table_name']
            
            query = "SELECT DISTINCT ON (device_id) * FROM {} WHERE device_id in ({}) and published_at > now() - INTERVAL '{}' ORDER BY device_id,published_at DESC".format(table_name, ','.join(['%s'] * len(devices_ids)), '7 days')
            # print(query)
            device_results = db.get_select_query_all_results_with_params(query, devices_ids)
            
            multiple_devices_results_formatted = []
            device_results_formatted_json = None
            if len(device_results) > 0:
                # print(device_results)
                for device_results_row in device_results:
                    published_at = device_results_row[0].isoformat().replace('+00:00', 'Z')
                    device_id = device_results_row[1]
                    device_results_json = {}
                    for idx, device_results_col in enumerate(device_results_row):
                        # print(idx, device_results_col)
                        device_results_json[column_names_array[idx]] = device_results_col
                    device_results_json.pop('published_at', None)
                    device_results_json.pop('device_id', None)

                    device_results_formatted_json = self.format_and_transform_vfd_x_600_device_results(device_results_json)
                    device_results_formatted_json['published_at'] = published_at
                    device_results_formatted_json['device_id'] = device_id
                    multiple_devices_results_formatted.append(device_results_formatted_json)
            
            return multiple_devices_results_formatted

    def format_and_transform_vfd_x_600_device_results(self, device_results_json):
        db = SentinelS7Database(None)
        query = "select json_data from system_modbus_config_json where file_name = '{}' limit 1".format('read_vfd_x_600_registers_main_feed_query')
        device_formatted_json = db.get_select_query_all_results(query)[0][0]
        for holding_register in device_formatted_json['holding_registers']:
            register_name = holding_register['name']
            if register_name in device_results_json:
                holding_register['value'] = device_results_json[register_name]
            else:
                holding_register['value'] = 'Not Available'

        for holding_register in device_formatted_json['coils']:
            register_name = holding_register['name']
            if register_name in device_results_json:
                holding_register['value'] = device_results_json[register_name]
            else:
                holding_register['value'] = 'Not Available'

        for holding_register in device_formatted_json['discrete_inputs']:
            register_name = holding_register['name']
            if register_name in device_results_json:
                holding_register['value'] = device_results_json[register_name]
            else:
                holding_register['value'] = 'Not Available'

        # print(device_formatted_json)

        device_results_formatted_json = self.transform_device_results(device_formatted_json)
        # print(device_results_formatted_json)

        for register in device_results_formatted_json['holding_registers']:
            if register['value'] == -999.999:
                    register['value'] = "Not Available"
            if register['unit'] == "Boolean":
                if register['value'] == 0:
                    register['value'] = "Off"
                    register['unit'] = ""
                elif register['value'] == 1:
                    register['value'] = "On"
                    register['unit'] = ""
            register = self.remove_props(register)

        for register in device_results_formatted_json['coils']:
            if register['value'] == -999.999:
                    register['value'] = "Not Available"
            if register['unit'] == "Boolean":
                if register['value'] == 0:
                    register['value'] = "Off"
                    register['unit'] = ""
                elif register['value'] == 1:
                    register['value'] = "On"
                    register['unit'] = ""
            register = self.remove_props(register)

        for register in device_results_formatted_json['discrete_inputs']:
            if register['value'] == -999.999:
                    register['value'] = "Not Available"
            if register['unit'] == "Boolean":
                if register['value'] == 0:
                    register['value'] = "Off"
                    register['unit'] = ""
                elif register['value'] == 1:
                    register['value'] = "On"
                    register['unit'] = ""
            register = self.remove_props(register)
        
        return device_results_formatted_json

    def transform_device_results(self, device_results_formatted_json):
        for register in device_results_formatted_json['holding_registers']:
            # print(str(register))
            if 'value' in register:
                if isinstance(register['value'], list) and register['combine_operation'] == 'add':
                    register['value'] = (((register['value'][1] * 65536) + register['value'][0] ) / 10)
                    if register['value'] == 429496729.5:
                        register['value'] = "None"
                    register = self.remove_props(register)
                elif register['value'] == 999 or register['value'] == 999000000:
                    register['value'] = "Not Available"
                    register = self.remove_props(register)
                elif register['value'] == -999 or register['value'] == -999000000:
                    register['value'] = "Not Available"
                    register = self.remove_props(register)
                elif register['value'] == 65535:
                    register['value'] = "Not Available"
                    register = self.remove_props(register)
                    
                if 'enum' in register and register['value'] != "Not Available":
                    for item in register['enum']:
                        if item['original_value'] == register['value']:
                            register['value'] = item['display_value']
                            register = self.remove_props(register)
                elif 'operand' in register and register['value'] != "Not Available":
                    if register['operand'] == 'multiply':
                        if register['name'] == 'gps_lat' or register['name'] == 'gps_lon':
                            register['value'] = round(register['value'] * register['factor'], 6)
                        elif register['name'] == 'cellular_signal_strength':
                            register['value'] = self.get_signal_bars(register['value'])
                        elif register['name'] == 'modbus_active':
                            register['value'] = self.get_modbus_active_text(register['value'])
                        elif register['name'] == 'inlet_pressure':
                            # Add a special offset of -14.7
                            register['value'] = round((register['value'] - 147) * register['factor'], 2)
                            # register['value'] = self.get_modbus_active_text(register['value'])
                        else:
                            register['value'] = round(register['value'] * register['factor'], 2)
                        register = self.remove_props(register)
                    # print(register['value'])
        return device_results_formatted_json
        
    def remove_props(self, register):
        register.pop('factor', None)
        register.pop('operand', None)
        register.pop('address', None)
        register.pop('addresses', None)
        register.pop('name', None)
        register.pop('enum', None)
        register.pop('combine_operation', None)
        return register
        
    def get_modbus_active_text(self, msg):
        result = "Not Available"
        if msg == 1:
            result = "Available"
        return result
        
    def get_signal_bars(self, msg):
        result = -999
        if msg >= 0 and msg <= 0:
            result = 0
        elif msg >= 1 and msg <= 1:
            result = 1
        elif msg >= 2 and msg <= 6:
            result = 2
        elif msg >= 7 and msg <= 11:
            result = 3
        elif msg >= 12 and msg <= 16:
            result = 4
        elif msg >= 17 and msg <= 31:
            result = 5
        elif msg >= 32 and msg <= 100:
            result = 0
        elif msg >= 101 and msg <= 106:
            result = 1
        elif msg >= 107 and msg <= 116:
            result = 2
        elif msg >= 117 and msg <= 126:
            result = 3
        elif msg >= 127 and msg <= 136:
            result = 4
        elif msg >= 137 and msg <= 191:
            result = 5
        elif msg >= 192 and msg <= 199:
            result = 0
        return result
            
    def format_device_results(self, device_results_json):
        # print(device_results_json)
        # with open('read_controls_inc_holding_registers.json') as f:
        #     device_formatted_json = json.load(f)
        #     print(device_formatted_json)
        db = SentinelS7Database(None)
        query = "select json_data from system_modbus_config_json where file_name = '{}' limit 1".format('read_controls_inc_holding_registers_main_feed_query')
        device_formatted_json = db.get_select_query_all_results(query)[0][0]
        # print(device_formatted_json)
        # if len(device_results) > 0:
            
        for holding_register in device_formatted_json['holding_registers']:
            register_name = holding_register['name']
            # It's a list
            if isinstance(register_name, list):
                if register_name[0] in device_results_json and register_name[1] in device_results_json:
                    holding_register['value'] = [device_results_json[register_name[0]], device_results_json[register_name[1]]]
            elif register_name in device_results_json:
                holding_register['value'] = device_results_json[register_name]
            else:
                holding_register['value'] = 'Not Available'
        # print(device_formatted_json)
        return device_formatted_json

    def run_query(self, query_string):
        try:
            device_pages = []
            device_pages_flat = []
            page_iterator = self.paginator.paginate(QueryString=query_string)
            for page in page_iterator:
                device_pages.append(self._parse_query_result(page))
            
            for sublist in device_pages:
                for item in sublist:
                    device_pages_flat.append(item)
        
            return device_pages_flat
        except Exception as err:
            print("Exception while running query:", err)

    def _parse_query_result(self, query_result):
        query_status = query_result["QueryStatus"]

        progress_percentage = query_status["ProgressPercentage"]
        print(f"Query progress so far: {progress_percentage}%")

        bytes_scanned = float(query_status["CumulativeBytesScanned"]) / 1073741824
        print(f"Data scanned so far: {bytes_scanned} GB")

        bytes_metered = float(query_status["CumulativeBytesMetered"]) / 1073741824
        print(f"Data metered so far: {bytes_metered} GB")

        column_info = query_result['ColumnInfo']

        print("Metadata: %s" % column_info)
        print("Data: ")
        device_results = []
        for row in query_result['Rows']:
            device_result = self._parse_row(column_info, row)
            # print(device_result)
            device_results.append(device_result)
        return device_results

    def _parse_row(self, column_info, row):
        data = row['Data']
        row_output = []
        for j in range(len(data)):
            info = column_info[j]
            datum = data[j]
            row_output.append(self._parse_datum(info, datum))

        return row_output

    def _parse_datum(self, info, datum):
        if datum.get('NullValue', False):
            return "%s=NULL" % info['Name'],

        column_type = info['Type']

        # If the column is of TimeSeries Type
        if 'TimeSeriesMeasureValueColumnInfo' in column_type:
            return self._parse_time_series(info, datum)

        # If the column is of Array Type
        elif 'ArrayColumnInfo' in column_type:
            array_values = datum['ArrayValue']
            return "%s=%s" % (info['Name'], self._parse_array(info['Type']['ArrayColumnInfo'], array_values))

        # If the column is of Row Type
        elif 'RowColumnInfo' in column_type:
            row_column_info = info['Type']['RowColumnInfo']
            row_values = datum['RowValue']
            return self._parse_row(row_column_info, row_values)

        # If the column is of Scalar Type
        else:
            return datum['ScalarValue']

    def _parse_time_series(self, info, datum):
        time_series_output = []
        for data_point in datum['TimeSeriesValue']:
            time_series_output.append("{time=%s, value=%s}"
                                      % (data_point['Time'],
                                         self._parse_datum(info['Type']['TimeSeriesMeasureValueColumnInfo'],
                                                           data_point['Value'])))
        return "[%s]" % str(time_series_output)

    def _parse_array(self, array_column_info, array_values):
        array_output = []
        for datum in array_values:
            array_output.append(self._parse_datum(array_column_info, datum))

        return "[%s]" % str(array_output)

    @staticmethod
    def _parse_column_name(info):
        if 'Name' in info:
            return info['Name'] + "="
        else:
            return ""
