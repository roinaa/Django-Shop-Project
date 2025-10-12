import time

def request_timing_middleware(get_response):
    def middleware(request):

        if request.path == '/':
            start_time = time.time()

            response = get_response(request)

            duration = time.time() - start_time
            print(f"Main page request took {duration:.4f} seconds")
        else:
            response = get_response(request)

        return response
    return middleware