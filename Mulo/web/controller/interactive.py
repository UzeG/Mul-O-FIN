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

    def control(self, template_data, template_odors):
        try:
            congestion = self.find_congest(int(template_data['id']))
            congestion.add_timeline()
            # p = int(template_data['port']) # float
            time_window = int(template_data['time_window'])
            threshold = int(template_data['threshold'])
            # d = int(template_data['duration']) # float
            output_device = template_data['output_device']
            m = len(congestion.congestion_control(time_window, threshold))
            print("nums:", time_window, threshold, output_device)
            if m == threshold:
                send_data = ""
                for odor in template_odors:
                    print(f"Odor: {odor.odor}, Port: {odor.port}, Start: {odor.start}, Duration: {odor.duration}, "
                          f"Intensity: {odor.intensity}")
                    # odor.start is not available.
                    # odor.intensity is pwm.
                    send_data += "{"+str(odor.odor)+","+str(odor.port)+","+str(odor.start)+","+str(odor.intensity) + "}"

                print(send_data)
                
                '''
                send_data = ("d" + str(output_device) + "p" + str(p) + "t" + str(d)).encode('utf-8')
                print(sockets)
                for client in sockets:
                    # 对字符串进行编码

                    try:
                        client.send(send_data)
                    except Exception as e:
                        print("admin_teaching_handle_restart:", e)
                        sockets.remove(client)
                '''
            return True

        except Exception as e:
            print(e)
            return False
