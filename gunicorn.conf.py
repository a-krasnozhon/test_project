import multiprocessing

workers = 1
worker_class = 'uvicorn_server.GunicornUvicornWorker'
keepalive = 40
