# 用户通信模块
from threading import Lock
from web.models import Template
from django.db.models import Q
from web.controller.congestion import Congestion
from web.controller.sockets import sockets


def find_template(uuid, event_name):
    try:
        template = Template.objects.filter(
            Q(uuid=uuid) | Q(uuid=""),
            Q(event_name=event_name)
        ).first()
        return template
    except Template.DoesNotExist:
        return None


def convert_template(template):
    if isinstance(template, Template):
        fields = template._meta.get_fields()
        template_data = {}

        for field in fields:
            field_name = field.name
            field_value = getattr(template, field_name)
            template_data[field_name] = field_value

        return template_data
    else:
        return -1


class Interactive:
    def __init__(self):
        self.events = {}  # 创建一个空字典来存储 EventID 和 Congestion 的映射关系

    def find_congest(self, event_id):
        if isinstance(event_id, int):
            if not (event_id in self.events):
                self.events[event_id] = Congestion()
            return self.events[event_id]

        else:
            return -1

    def control(self, template_data):
        try:
            congestion = self.find_congest(int(template_data['id']))
            congestion.add_timeline()
            p = int(template_data['port'])
            t = int(template_data['time_window'])
            n = int(template_data['role_num'])
            d = int(template_data['duration'])
            m = len(congestion.congestion_control(t, n))
            print(p, t, n, m)
            if m == n:

                for client in sockets:
                    # 对字符串进行编码
                    send_data = ("d1" + "p" + str(p) + "t" + str(d)).encode('utf-8')
                    try:
                        client.send(send_data)
                    except Exception as e:
                        print("admin_teaching_handle_restart:", e)
                        sockets.remove(client)
            return True

        except Exception as e:
            print(e)
            return False
