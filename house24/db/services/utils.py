import datetime


def generate_next_instance_number(model):
    """
    Generate next number depends on: 1) next pk number 2) current date
    :param model:
    :return:
    """
    last = model.objects.last()
    if last:
        next_number = last.pk + 1
    else:
        next_number = 1
    current_time = datetime.datetime.now()
    return f'{current_time.day}{current_time.month}{current_time.strftime("%y")}00{next_number}'
