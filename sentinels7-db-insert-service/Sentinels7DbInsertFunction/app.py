import json
import os
import psycopg2
from SentinelS7Database import SentinelS7Database
# import requests

def get_fleet_table_no_modbus_publish_defaults():
    no_modbus_publish_defaults = (-999, -999, -999, 65535, 65535, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, 65535, 65535, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, 65535, 65535, -999, -999, 65535, 65535, -999, -999, 65535, 65535, -999, -999, 65535, 65535, -999, -999, 65535, 65535, -999, -999, 65535, 65535, -999, -999, 65535, 65535, -999, -999, 65535, 65535, -999, -999, 65535, 65535, -999, -999, 65535, 65535, -999, -999)
    # no_modbus_publish_values = ('2021-1-1T22:42:59.719436Z', '2044SBI17497', 98, 52, 999, -999, -999, -999)
    # print(str(len(no_modbus_publish_values + no_modbus_publish_defaults)))
    return no_modbus_publish_defaults

def get_fleet_table_columns():
    column_names = "published_at, device_id, cpu_usage_percent, ram_usage_percent, gps_lat, gps_lon, cellular_signal_strength, cellular_career, modbus_active, percent_load, actual_engine_percent_torque, engine_speed, total_engine_hours_lsb, total_engine_hours_msb, engine_coolant_temperature, engine_oil_temperature,  fuel_delivery_pressure, engine_oil_pressure,  coolant_level,  fuel_rate,  air_inlet_temperature,  boost_pressure, alternator_potential_voltage, electrical_potential_voltage, battery_potential_voltage, injector_metering_rail_1_pressure, injector_metering_rail_2_pressure, fuel_level, short_term_fuel_trim_bank_1, inlet_suction_pressure, outlet_discharge_pressure, flow_rate, superpump_level_control,superpump_pressure_control, key_position, flow_rate_sender, water_temperature_sender, flow_rate_total_lsb, flow_rate_total_msb, digital_input_1_state, digital_input_2_state, relay_output_1_state, relay_output_2_state, stop_red_lamp_state, warning_amber_lamp_state, mil_lamp_state, wait_to_start_lamp_state, def_tank_level, control_transducer_level, control_transducer_pressure, inlet_pressure, outlet_pressure, superpump_throttle_manual_auto_status, superpump_throttle_type, auto_start_state, number_of_sets_of_active_fault_codes, active_spn_1_lsb, active_spn_1_msb, active_fmi_1, active_occurrence_count_1, active_spn_2_lsb, active_spn_2_msb, active_fmi_2, active_occurrence_count_2, active_spn_3_lsb, active_spn_3_msb, active_fmi_3, active_occurrence_count_3, active_spn_4_lsb, active_spn_4_msb, active_fmi_4, active_occurrence_count_4, active_spn_5_lsb, active_spn_5_msb, active_fmi_5, active_occurrence_count_5,active_spn_6_lsb, active_spn_6_msb, active_fmi_6, active_occurrence_count_6, active_spn_7_lsb, active_spn_7_msb, active_fmi_7, active_occurrence_count_7, active_spn_8_lsb, active_spn_8_msb, active_fmi_8, active_occurrence_count_8, active_spn_9_lsb, active_spn_9_msb, active_fmi_9, active_occurrence_count_9, active_spn_10_lsb, active_spn_10_msb, active_fmi_10, active_occurrence_count_10"
    column_placeholders = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
    return [column_names, column_placeholders]

def get_fleet_vfd_x_600_table_columns():
    column_names = "published_at, device_id, cpu_usage_percent, ram_usage_percent, gps_lat, gps_lon, cellular_signal_strength, cellular_career, modbus_active, supply_voltage_1, suct_psi, disc_psi, sec_disc_psi, hz_input, manual_hz, max_pres, suc_pres_setpnt, kp, bias, working_maxpsi, flowmeter_1_flow, flowmeter_2_flow, flowmeter_1_total, flowmeter_2_total, pit_lvl_1, pit_lvl_2, temp_encl, hz_output, auto_mode_tog, vfd_run_relay, vfd_flt_reset_relay, vlvc_ctrl, ambr_litrelay, vfd_fault_di, vfd_run_di, vlv_closed, vlv_open, on_backup"
    column_placeholders = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
    return [column_names, column_placeholders]

def get_fleet_vfd_x_600_table_no_modbus_publish_defaults():
    no_modbus_publish_defaults = (-999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999, -999.999)
    # no_modbus_publish_values = ('2021-1-1T22:42:59.719436Z', '2044SBI18711', 98, 52, 999, -999, -999, -999)
    # print(str(len(no_modbus_publish_values + no_modbus_publish_defaults)))
    return no_modbus_publish_defaults

def get_fleet_table_insert_query(table_name):
    return "INSERT INTO {} ({}) VALUES ({});".format(table_name, get_fleet_table_columns()[0], get_fleet_table_columns()[1])

def get_fleet_vfd_x_600_table_insert_query(table_name):
    return "INSERT INTO {} ({}) VALUES ({});".format(table_name, get_fleet_vfd_x_600_table_columns()[0], get_fleet_vfd_x_600_table_columns()[1])

def lambda_handler(event, context):
    input_data_json = event
    table_name = event['table_name']
    modbus_active = event['modbus_active']
    print("Event is: ")
    print(event)
    
    db_insert = SentinelS7Database(None)
    db_insert_conn = db_insert.get_db_connection()
    db_insert_cursor = db_insert_conn.cursor()
    if 'vfd_x_600' in table_name:
        SQL = get_fleet_vfd_x_600_table_insert_query(table_name)
    else: #Assume controls inc. This should be refactored later
        SQL = get_fleet_table_insert_query(table_name)
    fleet_values = ()
    try:
        if modbus_active == 0: 
            print("Modbus is not available")
            #  If mobus is not available set missing params to -999 and populate the measures available
            no_modbus_publish_values = ()
            if 'vfd_x_600' in table_name:
                no_modbus_publish_defaults = get_fleet_vfd_x_600_table_no_modbus_publish_defaults()
            else: #Assume controls inc. This should be refactored later
                no_modbus_publish_defaults = get_fleet_table_no_modbus_publish_defaults()
            
            for measure_name in input_data_json:
                if measure_name not in ['table_name']:
                    measure_value = input_data_json[measure_name]
                    no_modbus_publish_values = no_modbus_publish_values + (measure_value,)
            fleet_values = no_modbus_publish_values + no_modbus_publish_defaults
        else:
            print("Modbus is available")
            for measure_name in input_data_json:
                if measure_name not in ['table_name']:
                    measure_value = input_data_json[measure_name]
                    fleet_values = fleet_values + (measure_value,)
        # Insert Row
        db_insert_cursor.execute(SQL, fleet_values)
    except (Exception, psycopg2.Error) as error:
        print(error)
    db_insert_conn.commit()
    db_insert_cursor.close()
    db_insert_conn.close()

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Inserted feed row successfully!')
    }

