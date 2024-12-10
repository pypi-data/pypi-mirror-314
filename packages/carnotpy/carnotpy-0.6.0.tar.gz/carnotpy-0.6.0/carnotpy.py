import pandas as pd
import datetime
import requests
from dateutil.relativedelta import relativedelta



def process_equipment(payload, equipment_name):
    if payload['filters'].get('equipment_name'):
        if payload.get('pipeline') and len(payload['pipeline']) > 0:
            for stage in payload['pipeline']:
                if stage['type'] == 'filter':
                    stage['filter_by'] = stage['filter_by'].replace(payload['filters']['equipment_name'] + ' - ',
                                                                    equipment_name + ' - ')
                elif stage.get('formula') and stage['formula'] != '':
                    stage['formula'] = stage['formula'].replace(payload['filters']['equipment_name'] + ' - ',
                                                                equipment_name + ' - ')
                elif stage['type'] == 'insert_series':
                    stage['name'] = stage['name'].replace(payload['filters']['equipment_name'] + ' - ',
                                                          equipment_name + ' - ')
                    if stage.get('filters') and stage['filters']['equipment_name'] == payload['filters'][
                        'equipment_name']:
                        stage['filters']['equipment_name'] = equipment_name
        payload['filters']['equipment_name'] = equipment_name


def process_date_range(payload, date_range):
    if payload.get('useCustomRange'):
        if payload.get('useCustomRelativeRange'):
            rel_range = payload.get('customRelativeRange', '30 days')
            new_range = None
            base_date = datetime.datetime.now()
            start_date = base_date - datetime.timedelta(days=30)
            if rel_range == 'current week':
                start_date = base_date - datetime.timedelta(days=base_date.weekday())
            elif rel_range == 'current month':
                start_date = base_date.replace(day=1)
            elif rel_range == 'today' or rel_range == "today full":
                start_date = base_date.replace(hour=0, minute=0, second=0, microsecond=0)
            elif rel_range == 'current year':
                start_date = base_date.replace(month=1, day=1)
            elif rel_range == 'last week':
                base_date = base_date - datetime.timedelta(weeks=1)
                end_date = base_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                start_date = end_date - datetime.timedelta(days=end_date.weekday())
            elif rel_range == 'last month':
                base_date = base_date.replace(day=1) - datetime.timedelta(days=1)
                end_date = base_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                start_date = end_date.replace(day=1)
            elif rel_range == 'yesterday':
                base_date = base_date - datetime.timedelta(days=1)
                end_date = base_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
            elif rel_range == 'last year':
                base_date = base_date.replace(year=base_date.year - 1, month=12, day=31)
                end_date = base_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                start_date = end_date.replace(year=base_date.year - 1, month=1, day=1)
            elif rel_range == 'today and tomorrow':
                start_date = base_date.replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = base_date + datetime.timedelta(days=1)
                base_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

            if rel_range in ['yesterday', 'today', 'today and tomorrow']:
                new_range = {
                    'start': start_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'end': base_date.strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                new_range = {
                    'start': start_date.strftime('%Y-%m-%d'),
                    'end': (base_date.strftime('%Y-%m-%d %H:%M:%S') if len(
                        base_date.strftime('%Y-%m-%d')) < 12 else base_date.strftime('%Y-%m-%d'))
                }
            if payload.get('customRelativeRangeStartOnly') and date_range and date_range['end']:
                payload['date_range'] = [new_range['start'], (
                    date_range['end'] + ' 23:59:59' if len(date_range['end']) < 12 else date_range['end'])]
            else:
                payload['date_range'] = [new_range['start'], (
                    new_range['end'] + ' 23:59:59' if len(new_range['end']) < 12 else new_range['end'])]

        elif payload.get('customRange'):
            if payload.get('customRangeStartOnly') and date_range and date_range['end']:
                payload['date_range'] = [payload['customRange']['start'], (
                    date_range['end'] + ' 23:59:59' if len(date_range['end']) < 12 else date_range['end'])]
            else:
                payload['date_range'] = [payload['customRange']['start'], (
                    payload['customRange']['end'] + ' 23:59:59' if len(payload['customRange']['end']) < 12 else
                    payload['customRange']['end'])]

    elif date_range:
        if payload.get('offsetRange') and payload.get('offsetType'):
            if payload['offsetRangeStartOnly']:
                if payload['offsetType'] in ['year', 'years'] and payload.get('offsetPreciseYear'):
                    payload['date_range'] = [
                        datetime.datetime.strptime(date_range['start'], '%Y-%m-%d').replace(
                            year=payload['offsetPreciseYear']).strftime('%Y-%m-%d'),
                        (date_range['end'] + ' 23:59:59' if len(date_range['end']) < 12 else date_range['end'])
                    ]
                elif payload['offsetType'] in ['month', 'months']:
                    offset = relativedelta(months=-payload['offsetAmount'])
                    payload['date_range'] = [
                        (datetime.datetime.strptime(date_range['start'], '%Y-%m-%d') + offset).strftime('%Y-%m-%d'),
                        (date_range['end'] + ' 23:59:59' if len(date_range['end']) < 12 else date_range['end'])
                    ]
                elif payload['offsetType'] in ['year', 'years']:
                    offset = relativedelta(years=-payload['offsetAmount'])
                    payload['date_range'] = [
                        (datetime.datetime.strptime(date_range['start'], '%Y-%m-%d') + offset).strftime('%Y-%m-%d'),
                        (date_range['end'] + ' 23:59:59' if len(date_range['end']) < 12 else date_range['end'])
                    ]
                else:
                    payload['date_range'] = [
                        (datetime.datetime.strptime(date_range['start'], '%Y-%m-%d') - datetime.timedelta(
                            **{payload['offsetType']: payload['offsetAmount']})).strftime('%Y-%m-%d'),
                        (date_range['end'] + ' 23:59:59' if len(date_range['end']) < 12 else date_range['end'])
                    ]
            else:
                if payload['offsetType'] in ['year', 'years'] and payload.get('offsetPreciseYear'):
                    payload['date_range'] = [
                        datetime.datetime.strptime(date_range['start'], '%Y-%m-%d').replace(
                            year=payload['offsetPreciseYear']).strftime('%Y-%m-%d'),
                        datetime.datetime.strptime(date_range['end'], '%Y-%m-%d').replace(
                            year=payload['offsetPreciseYear']).strftime('%Y-%m-%d') + ' 23:59:59'
                    ]
                elif payload['offsetType'] in ['month', 'months']:
                    offset = relativedelta(months=-payload['offsetAmount'])
                    payload['date_range'] = [
                        (datetime.datetime.strptime(date_range['start'], '%Y-%m-%d') + offset).strftime('%Y-%m-%d'),
                        (datetime.datetime.strptime(date_range['end'], '%Y-%m-%d') + offset).strftime(
                            '%Y-%m-%d') + ' 23:59:59'
                    ]
                elif payload['offsetType'] in ['year', 'years']:
                    offset = relativedelta(years=-payload['offsetAmount'])
                    payload['date_range'] = [
                        (datetime.datetime.strptime(date_range['start'], '%Y-%m-%d') + offset).strftime('%Y-%m-%d'),
                        (datetime.datetime.strptime(date_range['end'], '%Y-%m-%d') + offset).strftime(
                            '%Y-%m-%d') + ' 23:59:59'
                    ]
                else:
                    payload['date_range'] = [
                        (datetime.datetime.strptime(date_range['start'], '%Y-%m-%d') - datetime.timedelta(
                            **{payload['offsetType']: payload['offsetAmount']})).strftime('%Y-%m-%d'),
                        (datetime.datetime.strptime(date_range['end'], '%Y-%m-%d') - datetime.timedelta(
                            **{payload['offsetType']: payload['offsetAmount']})).strftime('%Y-%m-%d') + ' 23:59:59'
                    ]
        else:
            payload['date_range'] = [date_range['start'], (
                date_range['end'] + ' 23:59:59' if len(date_range['end']) < 12 else date_range['end'])]


class CarnotPy:

    def __init__(self, url, username, password, preset_token=None):
        self.url = url
        self.username = username
        self.password = password
        self.preset_token = preset_token

    def get_token(self):
        if self.preset_token is not None:
            return self.preset_token
        result = requests.post(self.url + "/login/", json={"user_name": self.username, "password": self.password})
        assert result.status_code == 200
        try:
            token = result.json()["token"]
            return token
        except KeyError:
            raise ValueError("Invalid username or password")

    def discover(self):
        """
        Get the point list of the facility
        :return: return a point list
        """
        # return a point list
        token = self.get_token()
        result = requests.post(self.url + "/point-discovery/",
                               headers={"Authorization": "Bearer " + token}
                               )
        assert result.status_code == 200
        return result.json()["result"]

    def get_notifications(self, facility_name, date_range=None, ignore_acknowledged=True):
        token = self.get_token()
        payload={
            "facility_name": facility_name,
            "date_range": date_range,
            "ignore_acknowledged": ignore_acknowledged
        }
        result = requests.post(
            self.url + "/notification/",
            json=payload,
            headers={"Authorization": "Bearer " + token, 'Content-Type': 'application/json'}
        )
        assert result.status_code == 200
        return result.json()["result"]

    def get_maintenance_records(self, facility_name, date_range=None, equipment_name=None):
        token = self.get_token()
        payload={
            "facility_name": facility_name,
            "date_range": date_range,
            "equipment_name": equipment_name
        }
        result = requests.post(
            self.url + "/maintenancerecord/",
            json=payload,
            headers={"Authorization": "Bearer " + token, 'Content-Type': 'application/json'}
        )
        assert result.status_code == 200
        return result.json()["result"]

    def read_history(self, sensor_ids, start_time, end_time):
        token = self.get_token()
        result = requests.post(
            self.url + "/historical-data/",
            json={
                "date_range": [start_time, end_time],
                "sensor_ids": sensor_ids
            },
            headers={"Authorization": "Bearer " + token, 'Content-Type': 'application/json'}
        )
        assert result.status_code == 200
        data = result.json()
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        df = pd.DataFrame(data)
        df = df.set_index('timestamp')
        return df

    def read_data3(self, payload, token=None):
        if token is None:
            token = self.get_token()
        result = requests.post(
            self.url + "/data3/",
            json=payload,
            headers={"Authorization": "Bearer " + token, 'Content-Type': 'application/json'}
        )
        assert result.status_code == 200
        data = result.json()
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        df = pd.DataFrame(data)
        df = df.set_index('timestamp')
        return df

    def read_data3_query(self, query, facility_name, date_range, equipment=None, on_only=False, parameters=None, data3_implementation=None):
        if data3_implementation is None:
            def get_read_data3_func():
                # return a function that reads data3 with the token already
                token = self.get_token()
                def my_read_data3(payload):
                    return self.read_data3(payload, token)
                return my_read_data3
            data3_implementation = get_read_data3_func()
        payload_array = query['data-payload']
        df = None
        index = None
        for payload in payload_array:
            payload['parameters'] = parameters
            process_date_range(payload, date_range)
            if 'facility_name' not in payload["filters"]:
                payload["filters"]["facility_name"] = facility_name
            if equipment is not None:
                process_equipment(payload, equipment)
            if on_only or payload.get('onOnly', False):
                if 'pipeline' not in payload:
                    payload['pipeline'] = []
                payload['pipeline'].append({
                                  "type": "filter",
                                  "filter_op": "eq",
                                  "filter_by": "* - on",
                                  "filter_value": 1,
                              })
            del(payload["seriesOverrides"])
            new_df = data3_implementation(payload)
            if index is None:
                index = new_df.index
            new_df.index = range(len(new_df))
            if df is None:
                df = new_df
            else:
                df = df.join(new_df)

        df.index = index
        return df

    def get_sensor_id(self, facility_name, equipment_name, sensor_name):
        token = self.get_token()
        result = requests.post(self.url + "/point/",
                               json={"facility_name": facility_name, "equipment_name": equipment_name},
                               headers={"Authorization": "Bearer " + token, 'Content-Type': 'application/json'}
                               )
        assert result.status_code == 200
        points = result.json()['result']
        for point in points:
            if point['sensor_name'] == sensor_name:
                return point['sensor_id']
        raise KeyError("Sensor not found")

    def write(self, sensor_id, value, priority, duration=None):
        token = self.get_token()
        result = requests.put(
            self.url + "/optimizationcontrol/",
            json={
                "sensor_id": sensor_id,
                "value": value,
                "priority": priority,
                "duration": duration
            },
            headers={"Authorization": "Bearer " + token, 'Content-Type': 'application/json'}
        )
        assert result.status_code == 200
        return result.json()

