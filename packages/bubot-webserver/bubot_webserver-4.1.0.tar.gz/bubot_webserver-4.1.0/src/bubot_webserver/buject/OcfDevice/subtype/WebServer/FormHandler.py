import json
import os.path
import re
from sys import path as syspath
from bubot.core.BubotHelper import BubotHelper

from aiohttp import web


class FormHandler(web.View):
    clear = re.compile('[^a-zA-Z0-9]')
    forms = dict()

    def __init__(self, request):
        web.View.__init__(self, request)
        if not self.forms:
            self.find_forms()

    async def get(self):
        def read_form(path):
            with open(path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    # await asyncio.sleep(1)
                    return web.json_response(data)
                except Exception as e:
                    return web.Response(status=500, text=str(e))

        device = self.request.match_info.get('device')
        obj_name = self.request.match_info.get('obj_name')
        form_name = self.request.match_info.get('form_name')
        subtype = self.request.match_info.get('subtype')
        package_name = BubotHelper.get_package_name('OcfDevice', device)
        # берем сначала формы приложения
        if subtype:
            try:
                file_name = self.forms[package_name][obj_name]['subtype'][subtype][f'{form_name}.form.json']
                return read_form(file_name)
            except KeyError:
                pass

        try:
            file_name = self.forms[package_name][obj_name][f'{form_name}.form.json']
            return read_form(file_name)
        except KeyError:
            pass

        # если таких нет берем глобальные объектов
        if subtype:
            try:
                file_name = self.forms['all'][obj_name]['subtype'][subtype][f'{form_name}.form.json']
                return read_form(file_name)
            except KeyError:
                pass

        try:
            file_name = self.forms['all'][obj_name][f'{form_name}.form.json']
            return read_form(file_name)
        except KeyError as key:
            return web.HTTPInternalServerError(text=f"Form not found ({key})")

    @classmethod
    def find_forms(cls, **kwargs):
        '''
        Ищем формы для каждого из предустановленных типов, в общем каталог и каталоге устройства
        :param kwargs:
        :return:
        '''
        buject_index = BubotHelper.init_buject_index()
        cls.forms = {'all': {}}
        for buject in buject_index:
            obj_name, subtype = buject.split('/')
            for package_name, package_path in buject_index[buject]:
                if subtype:
                    form_dir = os.path.normpath(f'{package_path}/buject/{obj_name}/subtype/{subtype}/form')
                else:
                    form_dir = os.path.normpath(f'{package_path}/buject/{obj_name}/form')
                if not os.path.isdir(form_dir):
                    continue
                cls._find_in_form_dir(package_name, obj_name, subtype, form_dir)

    @classmethod
    def _find_in_form_dir(cls, package_name, obj_name, subtype, form_dir):
        form_list = os.listdir(form_dir)
        for form_name in form_list:
            if form_name[-5:] != ".json":
                continue

            if package_name not in cls.forms:
                cls.forms[package_name] = {}
            if obj_name not in cls.forms[package_name]:
                cls.forms[package_name][obj_name] = {}
                cls.forms['all'][obj_name] = {}
            if subtype:
                if 'subtype' not in cls.forms[package_name][obj_name]:
                    cls.forms[package_name][obj_name]['subtype'] = {}
                    cls.forms['all'][obj_name]['subtype'] = {}
                if subtype not in cls.forms[package_name][obj_name]['subtype']:
                    cls.forms[package_name][obj_name]['subtype'][subtype] = {}
                    cls.forms['all'][obj_name]['subtype'][subtype] = {}
                cls.forms[package_name][obj_name]['subtype'][subtype][form_name] = os.path.normpath(
                    f'{form_dir}/{form_name}')
                cls.forms['all'][obj_name]['subtype'][subtype][form_name] = os.path.normpath(
                    f'{form_dir}/{form_name}')
            else:
                cls.forms[package_name][obj_name][form_name] = os.path.normpath(f'{form_dir}/{form_name}')
                cls.forms['all'][obj_name][form_name] = os.path.normpath(f'{form_dir}/{form_name}')
