from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from web.models import Device, Role


def bind_device_role(request):
    if request.method == 'POST':
        device_id = request.POST.get('device_id')
        tag_id = request.POST.get('tag_id')
        print("Device ID:", device_id)
        print("Tag ID:", tag_id)
        device = role = None
        try:
            device = get_object_or_404(Device, id=device_id)
            print("Device:", device)
        except Device.DoesNotExist:
            print("Device not found")

        try:
            role = get_object_or_404(Role, id=tag_id)
            print("Role:", role)
        except Role.DoesNotExist:
            print("Role not found")

        if device and role:
            device.character = role.role
            device.save()
            return JsonResponse({'success': True, 'message': 'Device role binding successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Device or role not found'})
