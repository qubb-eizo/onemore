import time


class TimeLog:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time1 = time.time()
        # print(f'Time before - {time1}')
        response = self.get_response(request)
        time2 = time.time()
        # print(f'Time after - {time2}')
        print(f'TimeLog - {time2 - time1}')
        return response
