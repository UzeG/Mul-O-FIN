import random
import re
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from django.forms import model_to_dict

from web.models import Template, Role, TemplateOdorModel


def validate_code(width=120, height=30, char_length=5, font_file='kumo.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rnd_char():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))
        # return str(random.randint(0, 9)) 生成随机数字

    def rnd_color():
        """
        生成随机颜色
        :return:
        """
        return random.randint(0, 255), random.randint(50, 255), random.randint(84, 255)

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rnd_char()
        code.append(char)
        h = random.randint(0, 4)
        draw.text((i * width / char_length, h), char, font=font, fill=rnd_color())

    # 写干扰点
    for i in range(20):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rnd_color())

    # 写干扰圆圈
    for i in range(10):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rnd_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rnd_color())

    # 画干扰线
    for i in range(1):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rnd_color())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)


def validate_email(email):
    regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return True
    else:
        return False


def get_template_tree(user_profile):
    def fn(node):
        nodes = Template.objects \
            .filter(parent_id=node['data']['id']) \
            .values('id', 'event_name', 'input_description', 'threshold', 'time_window', 'output_device__role',
                    'parent', 'total_time', 'valid_while_parent', 'uuid') \
            .order_by('id')
        if len(nodes) == 0:
            return
        for j, n in enumerate(nodes):
            odors_query = TemplateOdorModel.objects \
                    .filter(event_template_id=n['id']) \
                    .values('odor__odor')
            leaf_node = {
                'data': n,
                'odors': [o['odor__odor'] for o in odors_query],
                'nodes': [],
                'path': f"{node['path']}-{j + 1}"
            }
            fn(leaf_node)
            node['nodes'].append(leaf_node)

    tree = []
    roots = Template.objects \
        .filter(uuid=user_profile.uuid, parent_id=None) \
        .values('id', 'event_name', 'input_description', 'threshold', 'time_window', 'output_device__role', 'parent',
                'total_time', 'valid_while_parent', 'uuid') \
        .order_by('id')
    for i, root in enumerate(roots):
        odors_query = TemplateOdorModel.objects \
            .filter(event_template_id=root['id']) \
            .values('odor__odor')
        root_node = {
            'data': root,
            'odors': [o['odor__odor'] for o in odors_query],
            'nodes': [],
            'path': f'{i + 1}'
        }
        fn(root_node)
        tree.append(root_node)
    print(tree)
    return tree


def get_template_odors_by_tid(tid):
    # {odor_id: string, port_id: string, duration: number, intensity: number, start: number}[]
    odors = TemplateOdorModel.objects \
        .filter(event_template_id=tid) \
        .values('odor_id', 'port', 'start', 'duration', 'intensity')
    return list(odors)
