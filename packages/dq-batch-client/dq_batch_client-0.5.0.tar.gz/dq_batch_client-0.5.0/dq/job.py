# -*- coding: utf-8 -*-


class Job:

    def __init__(self, job_id, name, status, start_date, end_date,
                 source_records, processed_records, price):
        self.id = job_id
        self.name = name
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.source_records = source_records
        self.processed_records = processed_records
        self.price = price

    def __repr__(self):
        return str(vars(self))


class JobReport:

    def __new__(cls, *args, **kwargs):
        if 'code' in kwargs:
            return None
        return super().__new__(cls)

    def __init__(self, quality_issues, quality_names, results):
        self.quality_issues = quality_issues
        self.quality_names = quality_names
        self.results = results

    def __repr__(self):
        return str(vars(self))


class JobConfig:

    def __init__(self, name):
        self.name = name
        self._input_format = {
            "field_separator": ",",
            "text_delimiter": "\"",
            "code_page": "utf-8"
        }
        self._input_columns = {}
        self._extend = {
            "teryt": 0,
            "gus": 0,
            "geocode": 0,
            "building_info": 0,
            "diagnostic": 0,
            "area_characteristic": 0
        }
        self._module_std = {
            "address": 0,
            "names": 0,
            "contact": 0,
            "id_numbers": 0
        }
        self._client = {
            "name": "",
            "mode": ""
        }

        self._deduplication = {
            "on": 0,
            "incremental": 0
        }

    def input_format(self, field_separator=",", text_delimiter="\"",
                     code_page="utf-8"):
        self._input_format["field_separator"] = field_separator
        self._input_format["text_delimiter"] = text_delimiter
        self._input_format["code_page"] = code_page

    def input_column(self, idx, name, function):
        self._input_columns[idx] = {"no": idx, "name": name,
                                    "function": function}

    def extend(self, teryt=False, gus=False, geocode=False,
               building_info=False, diagnostic=False,
               area_characteristic=False):
        self._extend["teryt"] = self.__boolean_to_num(teryt)
        self._extend["gus"] = self.__boolean_to_num(gus)
        self._extend["geocode"] = self.__boolean_to_num(geocode)
        self._extend["building_info"] = self.__boolean_to_num(building_info)
        self._extend["diagnostic"] = self.__boolean_to_num(diagnostic)
        self._extend["area_characteristic"] = \
            self.__boolean_to_num(area_characteristic)

    def module_std(self, address=False, names=False, contact=False, id_numbers=False):
        self._module_std["address"] = self.__boolean_to_num(address)
        self._module_std["names"] = self.__boolean_to_num(names)
        self._module_std["contact"] = self.__boolean_to_num(contact)
        self._module_std["id_numbers"] = self.__boolean_to_num(id_numbers)

    def deduplication(self, on=False, incremental=False):
        self._deduplication["on"] = self.__boolean_to_num(on)
        self._deduplication["incremental"] = self.__boolean_to_num(incremental)

    def client(self, name, mode):
        self._client["name"] = name
        self._client["mode"] = mode

    @staticmethod
    def __boolean_to_num(value):
        return 1 if value else 0

    def data(self):
        return {
            "job_name": self.name,
            "input_format": self._input_format,
            "input_columns": list(self._input_columns.values()),
            "extend": self._extend,
            "module_std": self._module_std,
            "deduplication": self._deduplication,
            "client": self._client
        }
