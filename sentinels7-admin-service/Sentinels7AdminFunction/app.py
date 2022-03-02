import json
import os
import io
import psycopg2
from SentinelS7Database import SentinelS7Database
# import requests

def get_fleet_table_create_query(table_name):
    return """CREATE TABLE IF NOT EXISTS {} (
                                            published_at TIMESTAMPTZ NOT NULL,
                                            device_id VARCHAR(16),
                                            cpu_temp_deg_c BIGINT,
                                            cpu_usage_percent BIGINT,
                                            ram_usage_percent BIGINT,
                                            gps_lat BIGINT,
                                            gps_lon BIGINT,
                                            cellular_signal_strength BIGINT,
                                            cellular_career BIGINT,
                                            modbus_active BIGINT,
                                            percent_load BIGINT, 
                                            actual_engine_percent_torque BIGINT, 
                                            engine_speed BIGINT, 
                                            total_engine_hours_lsb BIGINT, 
                                            total_engine_hours_msb BIGINT, 
                                            engine_coolant_temperature BIGINT, 
                                            engine_oil_temperature BIGINT, 
                                            fuel_delivery_pressure BIGINT, 
                                            engine_oil_pressure BIGINT, 
                                            coolant_level BIGINT, 
                                            fuel_rate BIGINT, 
                                            air_inlet_temperature BIGINT, 
                                            boost_pressure BIGINT, 
                                            alternator_potential_voltage BIGINT, 
                                            electrical_potential_voltage BIGINT, 
                                            battery_potential_voltage BIGINT, 
                                            injector_metering_rail_1_pressure BIGINT, 
                                            injector_metering_rail_2_pressure BIGINT, 
                                            fuel_level BIGINT, 
                                            short_term_fuel_trim_bank_1 BIGINT, 
                                            inlet_suction_pressure BIGINT, 
                                            outlet_discharge_pressure BIGINT, 
                                            flow_rate BIGINT, 
                                            superpump_level_control BIGINT,
                                            superpump_pressure_control BIGINT, 
                                            key_position BIGINT, 
                                            flow_rate_sender BIGINT, 
                                            water_temperature_sender BIGINT, 
                                            flow_rate_total_lsb BIGINT, 
                                            flow_rate_total_msb BIGINT, 
                                            digital_input_1_state BIGINT, 
                                            digital_input_2_state BIGINT, 
                                            relay_output_1_state BIGINT, 
                                            relay_output_2_state BIGINT, 
                                            stop_red_lamp_state BIGINT, 
                                            warning_amber_lamp_state BIGINT, 
                                            mil_lamp_state BIGINT, 
                                            wait_to_start_lamp_state BIGINT, 
                                            def_tank_level BIGINT, 
                                            control_transducer_level BIGINT, 
                                            control_transducer_pressure BIGINT, 
                                            inlet_pressure BIGINT, 
                                            outlet_pressure BIGINT, 
                                            superpump_throttle_manual_auto_status BIGINT, 
                                            superpump_throttle_type BIGINT, 
                                            auto_start_state BIGINT, 
                                            number_of_sets_of_active_fault_codes BIGINT, 
                                            active_spn_1_lsb BIGINT, 
                                            active_spn_1_msb BIGINT, 
                                            active_fmi_1 BIGINT, 
                                            active_occurrence_count_1 BIGINT, 
                                            active_spn_2_lsb BIGINT, 
                                            active_spn_2_msb BIGINT, 
                                            active_fmi_2 BIGINT, 
                                            active_occurrence_count_2 BIGINT, 
                                            active_spn_3_lsb BIGINT, 
                                            active_spn_3_msb BIGINT, 
                                            active_fmi_3 BIGINT, 
                                            active_occurrence_count_3 BIGINT, 
                                            active_spn_4_lsb BIGINT, 
                                            active_spn_4_msb BIGINT, 
                                            active_fmi_4 BIGINT, 
                                            active_occurrence_count_4 BIGINT, 
                                            active_spn_5_lsb BIGINT, 
                                            active_spn_5_msb BIGINT, 
                                            active_fmi_5 BIGINT, 
                                            active_occurrence_count_5 BIGINT,
                                            active_spn_6_lsb BIGINT,
                                            active_spn_6_msb BIGINT,
                                            active_fmi_6 BIGINT,
                                            active_occurrence_count_6 BIGINT,
                                            active_spn_7_lsb BIGINT,
                                            active_spn_7_msb BIGINT,
                                            active_fmi_7 BIGINT,
                                            active_occurrence_count_7 BIGINT,
                                            active_spn_8_lsb BIGINT,
                                            active_spn_8_msb BIGINT,
                                            active_fmi_8 BIGINT,
                                            active_occurrence_count_8 BIGINT,
                                            active_spn_9_lsb BIGINT,
                                            active_spn_9_msb BIGINT,
                                            active_fmi_9 BIGINT,
                                            active_occurrence_count_9 BIGINT,
                                            active_spn_10_lsb BIGINT,
                                            active_spn_10_msb BIGINT,
                                            active_fmi_10 BIGINT,
                                            active_occurrence_count_10 BIGINT
                                            );""".format(table_name)

def add_new_hyper_table(connection, table_name):
    cursor = connection.cursor()

    # create fleet hypertable
    query_create_table = get_fleet_table_create_query(table_name)
    query_create_hypertable = "SELECT create_hypertable('{}', 'published_at');".format(table_name)
    query_index_published_at_device_id_hypertable = "CREATE INDEX ON {} (device_id, published_at DESC);".format(table_name)
    query_index_device_id_hypertable = "CREATE INDEX ON {} (device_id);".format(table_name)

    print("Creating Table : {}".format(table_name))
    cursor.execute(query_create_table)
    print("Making it Hyper Table : {}".format(table_name))
    cursor.execute(query_create_hypertable)
    print("Creating Index for device_id + published_at on : {}".format(table_name))
    cursor.execute(query_index_published_at_device_id_hypertable)
    print("Creating Index for device_id on : {}".format(table_name))
    cursor.execute(query_index_device_id_hypertable)
    cursor.close()
    print("{} created successfully!".format(table_name))

def add_system_company(connection, table_name, company_name):
    cursor = connection.cursor()
    print("Inserting new row to : {}".format(table_name))
    query = "INSERT INTO public.system_company(id, name, hypertable_name) VALUES (nextval('system_company_id_seq'), %s, %s);"
    values = (company_name, table_name)
    cursor.execute(query, values)
    cursor.close()
    print("{} Inserted row successfully!".format(table_name))

def add_system_user_app_config_contact(connection, company_name, email, phone_numbers, devices_data_partial_publish, devices_data_refresh_frequency, user_is_admin):
    cursor = connection.cursor()
    get_table_name_query = "SELECT id,hypertable_name from system_company where name = '{}';".format(company_name)
    cursor.execute(get_table_name_query)
    result = cursor.fetchall()
    if result and result[0] and result[0][0]:
        # print(result)
        company_id = result[0][0]
        table_name = result[0][1]
        # print(table_name)

        print("Inserting new row to : {}".format(table_name))
        query = "INSERT INTO public.system_user(id, email, company_id) VALUES (nextval('user_id_seq'), %s, %s) RETURNING id;"
        values = (email, company_id)
        cursor.execute(query, values)
        new_user_id = cursor.fetchone()[0]
        print("{} Inserted row successfully!".format(table_name))

        print("Inserting rows into : {}".format('system_user_app_config'))
        query1 = "INSERT INTO public.system_user_app_config(id, key, value, type, user_id) VALUES (nextval('user_app_config_id_seq'), 'devices_data_partial_publish', %s, 'boolean', %s);"
        values1 = (devices_data_partial_publish ,new_user_id)
        cursor.execute(query1, values1)
        query2 = "INSERT INTO public.system_user_app_config(id, key, value, type, user_id) VALUES (nextval('user_app_config_id_seq'), 'devices_data_refresh_frequency', %s, 'string', %s);"
        values2 = (devices_data_refresh_frequency ,new_user_id)
        cursor.execute(query2, values2)
        query3 = "INSERT INTO public.system_user_app_config(id, key, value, type, user_id) VALUES (nextval('user_app_config_id_seq'), 'default_device_id', %s, 'integer', %s);"
        values3 = (-1 ,new_user_id)
        cursor.execute(query3, values3)
        query4 = "INSERT INTO public.system_user_app_config(id, key, value, type, user_id) VALUES (nextval('user_app_config_id_seq'), 'user_is_admin', %s, 'boolean', %s);"
        values4 = (user_is_admin ,new_user_id)
        cursor.execute(query4, values4)
        print("{} Inserted rows successfully!".format('system_user_app_config'))

        print("Inserting rows into : {}".format('system_user_contact'))
        for number in phone_numbers:
            query = "INSERT INTO public.system_user_contact(id, phone_number, user_id) VALUES (nextval('system_user_contact_id_seq'), %s, %s)"
            values = (number, new_user_id)
            cursor.execute(query, values)
        print("{} Inserted row successfully!".format('system_user_contact'))
        cursor.close()

    else:
        print("Company name not found")

def add_system_device_and_notifications(connection, company_name, devices):
    cursor = connection.cursor()
    get_table_name_query = "SELECT id from system_company where name = '{}';".format(company_name)
    cursor.execute(get_table_name_query)
    result = cursor.fetchall()
    if result and result[0] and result[0][0]:
        company_id = result[0][0]
        # print(company_id)

    get_user_id_company = "SELECT id,email from system_view_user_company where name = '{}';".format(company_name)
    cursor.execute(get_user_id_company)
    results = cursor.fetchall()
    print(get_user_id_company)
    print(results)
    user_ids_emails = []
    if results and len(results) > 0:
        for result in results:
            user_ids_emails.append({"id":result[0], "email": result[1]})

    get_system_alarm_alias_field_ids_query = "SELECT id,field_name from system_alarm_alias_field;"
    cursor.execute(get_system_alarm_alias_field_ids_query)
    results = cursor.fetchall()
    alarm_alias_fields = []
    if results and len(results) > 0:
        for result in results:
            alarm_alias_fields.append({"id":result[0], "field_name": result[1]})

        for device in devices:
            serial_number = device['serial_number']
            alias = device['alias']
            print("Inserting new row to : {}".format('system_device'))
            query = "INSERT INTO public.system_device(id, serial_number, alias, company_id) VALUES (nextval('system_device_id_seq'), %s, %s, %s) RETURNING id;"
            values = (serial_number, alias, company_id)
            cursor.execute(query, values)
            new_device_id = cursor.fetchone()[0]
            print("{} Inserted row successfully!".format('system_device'))
            
            for alarm in device['alarms']:
                print("Inserting new row to : {}".format('system_device_alarm_field'))
                query = "INSERT INTO public.system_device_alarm_field(id, expected_value, operator, value_type, device_id, alarm_alias_field_id, alarm_enabled) VALUES (nextval('system_device_alarm_field_id_seq'), %s, %s, %s, %s, %s, %s)"
                alarm_alias_field_id = None
                for alarm_alias_field in alarm_alias_fields:
                    if alarm_alias_field['field_name'] == alarm['alarm_alias_field_name']:
                        alarm_alias_field_id = alarm_alias_field['id']
                values = (alarm['expected_value'], alarm['operator'], alarm['value_type'], new_device_id, alarm_alias_field_id, alarm['alarm_enabled'])
                cursor.execute(query, values)
                print("{} Inserted row successfully!".format('system_device_alarm_field'))

                print("Inserting new row to : {}".format('system_device_alarm_notify'))
                query = "INSERT INTO public.system_device_alarm_notify(id, alarm_alias_field_id, notified, device_id) VALUES (nextval('device_alarm_notify_id_seq'), %s, %s, %s)"
                values = (alarm_alias_field_id, False, new_device_id)
                cursor.execute(query, values)
                print("{} Inserted row successfully!".format('system_device_alarm_notify'))

            print(user_ids_emails)
            for email in device['notify_user_emails']:
                user_id = None
                for user_id_email in user_ids_emails:
                    if user_id_email['email'] == email:
                        user_id = user_id_email['id']
                print("Inserting new row to : {}".format('system_device_contact'))
                query = "INSERT INTO public.system_device_contact(id, device_id, user_id) VALUES (nextval('system_user_contact_id_seq'), %s, %s)"
                values = (new_device_id, user_id)
                cursor.execute(query, values)
                print("{} Inserted row successfully!".format('system_device_contact'))
                
    cursor.close()

def add_hyper_table_retention_policy(connection, table_name, days):
    cursor = connection.cursor()
    print("Adding data retention policy for Table : {} as {}".format(table_name, days))
    query_hypertable = "SELECT add_retention_policy('{}', INTERVAL '{} days');".format(table_name, days)
    cursor.execute(query_hypertable)
    cursor.close()
    print("{} Added data retention policy of {} days successfully!".format(table_name, days))

def lambda_handler(event, context):
    result = None
    add_new_company= event.get('add_new_company', False)
    company_name= event.get('company_name', False)
    hyper_table_name = event.get('hyper_table_name', None)
    data_retention_policy_in_days = event.get('data_retention_policy_in_days', None)
    add_new_user= event.get('add_new_user', False)
    email= event.get('email', None)
    phone_numbers= event.get('phone_numbers', [])
    devices_data_partial_publish= event.get('devices_data_partial_publish', "false")
    devices_data_refresh_frequency= event.get('devices_data_refresh_frequency', 'high_frequency')
    user_is_admin= event.get('user_is_admin', "false")
    add_new_devices = event.get('add_new_devices', False)
    devices = event.get('devices', [])
    # print(event)
    
    admin = SentinelS7Database(None)
    admin_conn = admin.get_db_connection()

    try:
        if add_new_company:
            print("Running add_new_hyper_table")
            add_new_hyper_table(admin_conn, hyper_table_name)
            print("Finished Running add_new_hyper_table")

            print("Running add_hyper_table_retention_policy")
            add_hyper_table_retention_policy(admin_conn, hyper_table_name, data_retention_policy_in_days)
            print("Finished Running add_hyper_table_retention_policy")

            print("Running add_system_company")
            add_system_company(admin_conn, hyper_table_name, company_name)
            print("Finished Running add_system_company")

        if add_new_user:
            print("Running add_system_user_app_config_contact")
            add_system_user_app_config_contact(admin_conn, company_name, email, phone_numbers, devices_data_partial_publish, devices_data_refresh_frequency, user_is_admin)
            print("Finished Running add_system_user_app_config_contact")

        if add_new_devices:
            print("Running add_system_device")
            add_system_device_and_notifications(admin_conn,company_name, devices)
            print("Finished Running add_system_device")

        result = True

    except (Exception, psycopg2.Error) as error:
        print(error)
        result = error
    admin_conn.commit()
    admin_conn.close()

    # TODO implement
    return {
        'statusCode': 200,
        'body': result
    }

