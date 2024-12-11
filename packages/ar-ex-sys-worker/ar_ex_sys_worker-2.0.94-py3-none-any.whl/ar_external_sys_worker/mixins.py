import requests
import json
import base64
import datetime

import wsqluse.wsqluse


class UrlsWorkerMixin:
    """ Миксина для работы с юрлами """
    link_host = None
    port = None

    def get_full_endpoint(self, link, host=None, port=None):
        if not host:
            host = self.link_host
        if not port:
            port = self.port
        if not port:
            return "".join((str(host), str(link)))
        return "".join((str(host), ':' + str(port), str(link)))


class ExSys:
    link_host = None
    link_auth = None
    port = None
    link_create_act = None
    ex_sys_id = None


class SignallMixin:
    link_host = "https://signall.qodex.tech"
    # link_host = "https://signalltestdev.qodex.tech"
    link_auth = '/v1/user/login'
    link_get_po_links = "/v1/gravity/get_po_clients"
    port = None
    link_create_act = '/v1/acts/create_act_with_inn_and_kpp'
    ex_sys_id = 1
    auth_key_in_headers = 'Authorization'
    response_token_key = 'token'
    login_key_to_ex_sys = 'email'
    pass_key_to_ex_sys = 'password'
    login_column_name = 'signall_login'
    pass_column_name = 'signall_pass'

    def set_signall_test(self):
        self.link_host = "https://signalltestdev.qodex.tech"


class TokenAuth():
    link_get_token = '/v1/gravity/get_gravity_token'
    gravity_ip = None
    gravity_port = None
    inn = None
    kpp = None

    def get_token_url(self, url):
        return requests.post(url, json={"ip": self.gravity_ip,
                                        "port": str(self.gravity_port),
                                        "inn": self.inn,
                                        "kpp": self.kpp})


class TokenDBAuth:
    sql_shell = None
    ex_sys_id = None
    platform_id = None

    @wsqluse.wsqluse.tryExecuteGetStripper
    def get_token_db(self):
        return self.sql_shell.try_execute_get(
            f"SELECT token FROM ex_sys_auth_tokens "
            f"WHERE ex_sys_id={self.ex_sys_id} "
            f"AND platform_id={self.platform_id} "
            f"AND active=true")

    @wsqluse.wsqluse.tryExecuteStripper
    def set_token_db(self, token):
        return self.sql_shell.try_execute(
            "INSERT INTO ex_sys_auth_tokens (ex_sys_id, platform_id, token) "
            f"VALUES ({self.ex_sys_id}, {self.platform_id}, '{token}') "
            f"ON CONFLICT (ex_sys_id, platform_id) DO UPDATE "
            f"SET ex_sys_id={self.ex_sys_id}, platform_id={self.platform_id}"
        )


class AsuMixin:
    link_host = 'https://bashkortostan.asu.big3.ru'
    link_auth = '/extapi/v2/token-auth/'
    port = 443
    link_create_act = '/extapi/v2/landfill-fact/'
    ex_sys_id = 4
    auth_key_in_headers = 'Authorization'
    response_token_key = 'token'
    login_key_to_ex_sys = 'username'
    pass_key_to_ex_sys = 'password'
    login_column_name = 'asu_api_login'
    pass_column_name = 'asu_api_pass'


class ActWorkerMixin():
    table_name = 'records'

    def get_json(self, car_number: str, ex_id: int, gross: int, tare: int,
                 cargo: int, time_in: str, time_out: str, alerts: list,
                 carrier: str, trash_cat: str, trash_type: str,
                 operator_comments: dict, photo_in: str,
                 photo_out: str, containers_plan, containers_fact, route_num,
                 platform_type, act_number: dict):
        data = locals()
        data.__delitem__('self')
        json_data = json.dumps(data)
        return json_data


class AuthMe(UrlsWorkerMixin):
    link_host = None
    link_auth = None
    headers = None
    login = None
    password = None
    auth_key_in_headers = None
    response_token_key = None
    login_key_to_ex_sys = None
    pass_key_to_ex_sys = None

    def make_auth(self):
        self.set_headers(self.get_headers())

    def get_headers(self):
        token = self.get_token()
        headers = {self.auth_key_in_headers: token}
        return headers

    def set_headers(self, headers):
        self.headers = headers
        return self.headers

    def auth_me(self):
        auth_data = self.get_auth_data()
        endpoint = self.get_full_endpoint(self.link_auth)
        response = self.send_auth_data(endpoint, auth_data)
        return response

    def send_auth_data(self, endpoint, auth_data, *args, **kwargs):
        auth_data_json = json.dumps(auth_data)
        return requests.post(endpoint, data=auth_data_json,
                             *args, **kwargs)

    def get_auth_data(self):
        data = {self.login_key_to_ex_sys: self.login,
                self.pass_key_to_ex_sys: self.password}
        return data

    def extract_token(self, auth_result_json):
        response = auth_result_json.json()
        # if 'error' in response:
        #    return response
        print(response)
        token = response[self.response_token_key]
        return token

    def get_token(self, **kwargs):
        response = self.auth_me()
        token = self.extract_token(response)
        return token


class SignallActsGetter:
    get_acts_url = '/v1/acts/get_acts'

    def get_acts_command(self, start_date: str, end_date: str,
                         polygon_name: str, page: int = 1):
        return {
            "car_number": "",
            "current_page": page,
            "date_start": start_date,
            "date_stop": end_date,
            "platform_name": polygon_name,
            "sorting_by": "",
            "transporter_name": "",
            "waste_category": 'tko'
        }


class SignallActDeletter:
    headers = None
    working_link = None
    signal_del_act_url = None

    def delete_act(self, signall_act_id):
        return requests.delete(self.signal_del_act_url.format(signall_act_id),
                               headers=self.headers)

    def delete_act_by_id(self, id_):
        return requests.delete(
            self.signal_del_act_url.format(id_),
            headers=self.headers)


class SignallActUpdater:
    headers = None
    signall_update_act_link = None

    def update_act(self, signall_id, car_number, transporter_inn,
                   transporter_kpp, trash_cat, trash_type, comment,
                   client_inn=None, client_kpp=None):
        data_json = {
            'car_number': car_number,
            'carrier': {"inn": transporter_inn,
                        "kpp": transporter_kpp},
            "client": {"inn": client_inn,
                       "kpp": client_kpp},
            'comment': comment,
            'trash_cat': trash_cat,
            'trash_type': trash_type}
        data_json = json.dumps(data_json)
        response = requests.post(
            self.signall_update_act_link.format(signall_id),
            headers=self.headers,
            data=data_json)
        return response


class SignallGetCarriersPO:
    headers = None
    get_carriers_po_link = None

    def get_carriers_po(self):
        if not self.get_carriers_po_link:
            return {'error': 'There are not link for route get_carriers'}
        response = requests.get(self.get_carriers_po_link,
                                headers=self.headers)
        return response


class ARAPIWork:
    gravity_ip = None
    gravity_port = 8080

    def insert_client_to_gravity(self, name, inn, kpp, push_to_cm):
        return requests.post(
            url=f'http://{self.gravity_ip}:{self.gravity_port}/add_client',
            params=
            {'name': name,
             'inn': inn,
             'kpp': kpp,
             'push_to_cm': push_to_cm,
             })

    def make_client_tko_carrier(self, inn, push_to_cm, kpp):
        return requests.post(
            url=f'http://{self.gravity_ip}:{self.gravity_port}/make_client_tko_carrier',
            params=
            {
                'inn': inn,
                'push_to_cm': push_to_cm,
                'kpp': kpp
            })

    def make_client_region_operator(self, inn, kpp, push_to_cm):
        return requests.post(
            url=f'http://{self.gravity_ip}:{self.gravity_port}/make_client_region_operator',
            params=
            {
                'inn': inn,
                'push_to_cm': push_to_cm,
                'kpp': kpp
            })


class SignAllCarsGetter:
    headers = None
    working_link = None

    def get_cars(self, link=None):
        if not link:
            link = self.working_link
        response = requests.get(link,
                                headers=self.headers)
        return response.json()

    def get_cars_platform(self):
        pass

    def get_cars_ro(self):
        pass


class ExSysActIdExtractor:
    sql_shell = None
    ex_sys_id = None

    @wsqluse.wsqluse.tryExecuteGetStripper
    def extract_act_ex_id(self, local_id):
        command = "SELECT ex_sys_data_id FROM ex_sys_data_send_reports " \
                  f"WHERE local_id={local_id} and ex_sys_id={self.ex_sys_id} " \
                  f"order by id desc limit 1"
        return self.sql_shell.try_execute_get(command)


class SignallActDBDeletter:
    sql_shell = None

    @wsqluse.wsqluse.getTableDictStripper
    def get_unget_by_signall_acts(self):
        command = "SELECT * FROM ex_sys_data_send_reports esdsr " \
                  "WHERE esdsr.ex_sys_id=(SELECT id FROM external_systems where name='SignAll') " \
                  "AND (ex_sys_data_id is null " \
                  "OR ex_sys_data_id like '%carrier%' " \
                  "OR ex_sys_data_id like '%unable%')"
        return self.sql_shell.get_table_dict(command)

    def delete_act_from_send_reports(self, act_id):
        command = "DELETE FROM ex_sys_data_send_reports esdsr " \
                  "WHERE esdsr.local_id={} " \
                  "and esdsr.ex_sys_id=(SELECT id FROM external_systems where name='SignAll')"
        command = command.format(act_id)
        return self.sql_shell.try_execute(command)

    def delete_act_from_send_reports_sig_id(self, sig_act_id):
        command = "DELETE FROM ex_sys_data_send_reports esdsr " \
                  "WHERE esdsr.ex_sys_data_id='{}' " \
                  "and esdsr.ex_sys_id=(SELECT id FROM external_systems where name='SignAll')"
        command = command.format(sig_act_id)
        return self.sql_shell.try_execute(command)

    @wsqluse.wsqluse.tryExecuteGetStripper
    def select_signall_id_from_send_reports(self, local_id):
        command = "SELECT ex_sys_data_id FROM ex_sys_data_send_reports esdrs " \
                  "LEFT JOIN external_systems es ON (esdrs.ex_sys_id=es.id) " \
                  f"WHERE esdrs.local_id={local_id} and es.name='SignAll'"
        return self.sql_shell.try_execute_get(command)


class ActToJSONMixin:
    link_host = None
    link_create_act = None

    def get_json(self, car_number: str, ex_id: int, gross: int, tare: int,
                 cargo: int, time_in: str, time_out: str, alerts: list,
                 carrier: str, trash_cat: str, trash_type: str,
                 operator_comments: dict, photo_in: str,
                 photo_out: str):
        data = locals()
        data.__delitem__('self')
        json_data = json.dumps(data)
        return json_data


class VideoWorkerDB:
    sql_shell = None

    @wsqluse.wsqluse.getTableDictStripper
    def get_video_info(self, video_id):
        return self.sql_shell.get_table_dict(
            f"SELECT * FROM videos WHERE id={video_id}")


class PhotoEncoderMixin:
    def get_photo_data(self, photo_path):
        """ Извлечь из фото последовательность байтов в кодировке base-64 """
        try:
            print(photo_path)
            with open(photo_path, 'rb') as fobj:
                photo_data = base64.b64encode(fobj.read())
                return photo_data
        except FileNotFoundError:
            pass


class SignallPhotoEncoderMixin(PhotoEncoderMixin):
    def get_photo_data(self, photo_path):
        if not photo_path:
            return
        photo = super().get_photo_data(photo_path)
        if photo:
            data = photo.decode()
            return data


class DataBaseWorker:
    sql_shell = None

    def set_sqlshell(self, sql_shell):
        self.sql_shell = sql_shell

    @wsqluse.wsqluse.getTableDictStripper
    def get_photo_types(self, sql_shell):
        return

    @wsqluse.wsqluse.tryExecuteGetStripper
    def get_table_id_by_name(self, sql_shell, table_name):
        return sql_shell.try_execute_get(
            f"SELECT id FROM ex_sys_tables WHERE name='{table_name}'")


class Logger(ExSys):
    log_id = None
    table_name = None
    ex_sys_table_id = None
    sql_shell = None

    def log_ex_sys_sent(self, record_id: int, sent_time=None):
        if not sent_time:
            sent_time = datetime.datetime.now()
        command = "INSERT INTO ex_sys_data_send_reports (ex_sys_id, " \
                  "local_id, sent, table_id) VALUES " \
                  "({}, {}, '{}', " \
                  "(SELECT id FROM ex_sys_tables WHERE name='{}'))".format(
            self.ex_sys_id,
            record_id, sent_time,
            self.table_name)
        return self.sql_shell.try_execute(command)['info'][0][0]

    def log_ex_sys_get(self, ex_system_data_id,
                       log_id=None, get_time=None):
        if not get_time:
            get_time = datetime.datetime.now()
        if not log_id:
            log_id = self.log_id
        command = "UPDATE ex_sys_data_send_reports SET get='{}', " \
                  "ex_sys_data_id='{}' " \
                  "WHERE id={}".format(get_time, ex_system_data_id, log_id)
        return self.sql_shell.try_execute(command)

    def format_file_before_logging(self, data):
        return str(data)

    def log_ex_sys_data(self, data, log_id=None):
        if not log_id:
            log_id = self.log_id
        data = self.format_file_before_logging(data)
        command = "UPDATE ex_sys_data_send_reports SET data='{}' " \
                  "WHERE id={}".format(data, log_id)
        return self.sql_shell.try_execute(command)


class ActsSQLCommands:
    filters = []
    limit = 10
    sql_shell = None
    table_id = 9
    table_name = 'records'
    trash_cats_to_send = []
    time_start = None
    ex_sys_id = None
    trash_cats_blacklist_to_send = []

    def set_filters(self, *filters):
        self.filters.append(filters)

    def set_limit(self, limit: int):
        self.limit = limit

    def get_acts_all_command(self):
        command = "SELECT distinct on (r.id) r.id as ex_id, a.car_number, r.brutto as gross, " \
                  "r.tara as tare, r.cargo, r.time_in, r.time_out, " \
                  "carrier_cji.inn as carrier_inn, carrier_cji.kpp as carrier_kpp," \
                  "client_cji.inn as client_inn, client_cji.kpp as client_kpp," \
                  "tc.name as trash_cat, " \
                  "tt.name as trash_type, oc.gross as gross_comm," \
                  "oc.tare as tare_comm, oc.additional as add_comm, " \
                  "oc.changing as changing_comm, oc.closing as closing_comm," \
                  "oc.single as single_comm, " \
                  "dro.owner as polygon_id, ai.number as rfid, rri.route_num," \
                  "rri.containers_plan, rri.containers_fact, ra.alerts," \
                  "pol_objects.name as pol_object," \
                  "aprm.number as act_number, acts_packages.name as package_name " \
                  "FROM records r " \
                  "LEFT JOIN clients carriers ON (r.carrier=carriers.id) " \
                  "LEFT JOIN clients ON (r.client_id=clients.id) " \
                  "LEFT JOIN trash_cats tc ON (r.trash_cat=tc.id) " \
                  "LEFT JOIN trash_types tt ON (r.trash_type=tt.id) " \
                  "LEFT JOIN operator_comments oc ON (r.id=oc.record_id) " \
                  "LEFT JOIN auto a ON (a.id=r.auto) " \
                  "LEFT JOIN clients_juridical_info carrier_cji ON (carrier_cji.client_id=carriers.id) " \
                  "LEFT JOIN clients_juridical_info client_cji ON (client_cji.client_id=clients.id) " \
                  "LEFT JOIN ex_sys_data_send_reports esdsr ON (esdsr.local_id = r.id)" \
                  "LEFT JOIN duo_records_owning dro on r.id = dro.record " \
                  "LEFT JOIN auto_idents ai ON ai.id=a.identifier " \
                  "LEFT JOIN records_routes_info rri ON r.id=rri.record_id " \
                  "LEFT JOIN records_alerts ra ON ra.record_id=r.id " \
                  "LEFT JOIN records_pol_objects_mapping rpom ON rpom.record_id=r.id " \
                  "LEFT JOIN pol_objects ON rpom.object_id=pol_objects.id " \
                  "LEFT JOIN acts_packages_records_mapping aprm ON (aprm.record_id = r.id) " \
                  "LEFT JOIN acts_packages ON (aprm.package_id = acts_packages.id) " \
                  "WHERE not time_out is null "
        return command

    def get_alerts(self, record_id):
        alerts = [
            self.check_manual_pass(record_id)
        ]
        return alerts

    def check_manual_pass(self, record_id):
        command = "SELECT r.id, a.car_number, a.identifier, mps.manual_pass " \
                  "FROM manual_pass_control mps " \
                  "LEFT JOIN records r ON (mps.record_id=r.id) " \
                  f"LEFT JOIN auto a ON (r.auto=a.id) WHERE r.id={record_id}"
        res = self.sql_shell.try_execute_get(command)
        if not res:
            return
        res = res[0]
        identifier = res[2]
        manual_pass = res[3]
        if identifier and manual_pass:
            return 'Пропуск авто с меткой вручную'

    def get_acts_today_command(self):
        today = datetime.datetime.today()
        return self.get_acts_all_command() + " and time_in::date='{}'".format(
            today)

    def get_wdb_tonnage(self, where_clause):
        command = "select count(r.id), sum(cargo) from records r " \
                  "LEFT JOIN trash_cats tc ON (r.trash_cat=tc.id) " \
                  "where {}".format(where_clause)
        return self.sql_shell.get_table_dict(command)

    def get_acts_period(self, start_date, end_date, smth_else):
        command = self.get_acts_all_command() + " and time_in >= '{}' and time_out::date <= '{}' {}".format(
            start_date, end_date, smth_else)
        return self.sql_shell.get_table_dict(command)

    @wsqluse.wsqluse.getTableDictStripper
    def get_unsend_acts(self, record_id=None, limit=None):
        command = self.get_acts_all_command()
        if not limit:
            limit = self.limit

        command += "  and r.id NOT IN (SELECT local_id FROM " \
                   f"ex_sys_data_send_reports WHERE table_id={self.table_id} " \
                   f"and ex_sys_id = {self.ex_sys_id} and not get is null) "
        if record_id:
            command += f' and r.id={record_id} '
        else:
            command += f" and time_in::date>'{self.time_start}'"
        if self.trash_cats_blacklist_to_send:
            command += f" AND NOT tc.name in {self.trash_cats_blacklist_to_send}"
        elif self.trash_cats_to_send:
            command += f" AND tc.name in {self.trash_cats_to_send}"
        command += f" LIMIT {limit}"
        return self.sql_shell.get_table_dict(command)

    def get_one_unsend_act(self):
        try:
            return self.get_unsend_acts()[0]
        except:
            pass

    def get_filters_ready(self):
        filter_ready = ' and '.format(self.filters)
        return filter_ready


class DuoAcstSQLCommands(ActsSQLCommands):
    polygon_id = None
    table_id = None

    def get_unsend_command(self):
        return self.get_acts_all_command() + \
               "  and r.id NOT IN (SELECT local_id FROM " \
               "ex_sys_data_send_reports WHERE table_id={} and not get is null) " \
               "and tc.name='ТКО' and time_in::date>'2022.02.21' " \
               "and dro.owner={} LIMIT {} ".format(self.table_id,
                                                   self.limit,
                                                   self.polygon_id)


class AuthWorker(DataBaseWorker, AuthMe, ExSys):
    polygon_id = None

    def __init__(self):
        auth_data = self.get_auth_data_db()
        if not auth_data:
            return
        self.login = auth_data[0]['login']
        self.password = auth_data[0]['password']

    @wsqluse.wsqluse.getTableDictStripper
    def get_auth_data_db(self):
        command = "SELECT login, password FROM external_systems_auth_info " \
                  "WHERE external_system_id={} and polygon_id={}"
        command = command.format(self.ex_sys_id, self.polygon_id)
        response = self.sql_shell.get_table_dict(command)
        return response


class DbAuthInfoGetter:
    sql_shell = None
    login_column_name = None
    pass_column_name = None

    @wsqluse.wsqluse.tryExecuteGetStripper
    def get_login_from_db(self):
        command = "SELECT value FROM core_settings " \
                  f"where key='{self.login_column_name}'"
        return self.sql_shell.try_execute_get(command)

    @wsqluse.wsqluse.tryExecuteGetStripper
    def get_pass_from_db(self):
        command = "SELECT value FROM core_settings " \
                  f"where key='{self.pass_column_name}'"
        return self.sql_shell.try_execute_get(command)

    @wsqluse.wsqluse.tryExecuteGetStripper
    def get_db_value(self, key):
        command = "SELECT value FROM core_settings " \
                  f"where key='{key}'"
        return self.sql_shell.try_execute_get(command)

    def get_auth_info_from_db(self):
        return self.get_login_from_db(), self.get_pass_from_db()
