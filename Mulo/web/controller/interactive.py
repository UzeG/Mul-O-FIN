# 用户通信模块
from web.models import Template, Device
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
            time_window = int(template_data['time_window'])
            threshold = int(template_data['threshold'])
            output_device = template_data['output_device']
            m = len(congestion.congestion_control(time_window, threshold))
            print("Parameters - nums:", time_window, "threshold:", threshold, "output_device:", output_device)
            if m == threshold:
                send_data = ""
                for odor in template_odors:
                    print(f"Odor: {odor.odor}, Port: {odor.port}, Start: {odor.start}, Duration: {odor.duration}, "
                          f"Intensity: {odor.intensity}")
                    # odor.start is not available.
                    # odor.intensity is pwm.
                    send_data += ("{" + str(odor.odor) + "," + str(odor.port) + "," + str(odor.start) + "," + str(
                        odor.duration) + "," + str(odor.intensity) + "}")
                print(send_data)

                device_exists = Device.objects.filter(character=output_device).exists()
                if device_exists:
                    sockets.add(Device.objects.filter(character=output_device).first(), send_data)

        except Exception as e:
            print(e)
            return False
