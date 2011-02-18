def get_source_ip(request):
    if request.META.has_key('REMOTE_ADDR'):
        return {'from_ip': request.META.get('REMOTE_ADDR'), 'excluded_ip': request.excluded_ip }
    else:
        return {}
