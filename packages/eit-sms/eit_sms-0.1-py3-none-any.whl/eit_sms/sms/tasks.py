from celery import shared_task


@shared_task
def sample_task():
    x_factor = 15
    y_factor = 30
    print("Multiplying {} by {}".format(x_factor, y_factor))
    return x_factor * y_factor
