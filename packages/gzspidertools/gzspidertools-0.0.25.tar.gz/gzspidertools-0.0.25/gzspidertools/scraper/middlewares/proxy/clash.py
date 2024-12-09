class ProxyMiddleware:
    def process_request(self, request, spider):
        name = spider.name
        request.meta['proxy'] = 'http://127.0.0.1:7890'
