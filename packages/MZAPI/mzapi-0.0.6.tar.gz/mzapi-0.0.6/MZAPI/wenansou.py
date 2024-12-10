import datetime
import time

import requests
from MZAPI.APM import APMClient
from MZAPI.KVS import LogHandler
from MZAPI.LOG import PublicIPTracker
from MZAPI.headers import CustomRequestHeaders
from opentelemetry import trace


class WenAnSou:
    def __init__(self, client_name):
        """
        初始化 WenAnSou 类。

        :param client_name: 客户端名称
        """
        self.ip = PublicIPTracker()
        self.log = LogHandler()
        M = CustomRequestHeaders()
        self.headers = M.reset_headers()
        self.apm_client = APMClient(
            client_name=client_name,
            host_name="https://www.hhlqilongzhu.cn/api/wenan_sou.php",
            token="kCrxvCIYEzhZfAHETXEB",
            peer_service="龙珠API",
            peer_instance="111.229.214.169:443",
            peer_address="111.229.214.169",
            peer_ipv6="-",
            http_host="https://www.hhlqilongzhu.cn/api/wenan_sou.php",
            server_name="米粥API",
        )
        self.tracer = self.apm_client.get_tracer()

    def get_response(self, Content):
        """
        发送请求并获取响应。

        :param Content: 搜索内容
        :return: 包含响应信息的字典
        """
        with self.tracer.start_as_current_span("wenansou") as span:
            url = f"https://www.hhlqilongzhu.cn/api/wenan_sou.php?msg={Content}"
            headers = {
                "Host": "www.hhlqilongzhu.cn",
                "Origin": self.headers.get("Referer"),
                **self.headers,
            }
            response = requests.get(url, headers=headers)
            current_timestamp = int(time.time())
            dt_object = datetime.datetime.fromtimestamp(current_timestamp)
            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            span.set_attribute("id", current_timestamp)
            span.set_attribute("url", url)
            span.set_attribute("response", response.text)
            span.set_attribute("HTTP_status_code", response.status_code)
            span.set_attribute("HTTP_response_content", response.text)
            span.set_attribute("HTTP_response_size", len(response.text))
            span.set_attribute(
                "http.response_time", response.elapsed.total_seconds() * 1000
            )
            span.set_attribute("http.method", "GET")
            span.set_attribute(
                "http.user_agent", response.request.headers.get("User-Agent", "-")
            )
            span.set_attribute(
                "http.content_type", response.headers.get("Content-Type", "-")
            )
            span.set_attribute("http.server", response.headers.get("Server", "-"))
            span.set_attribute("http.date", response.headers.get("Dat", "-"))
            self.ip.start_track_log()
            current_span = trace.get_current_span()
            traceID = current_span.get_span_context().trace_id
            W = trace.span.format_trace_id(traceID)
            self.log.start_process_log(response.text, "WenAnSou", W)
            M = response.text
            W = {
                "id": current_timestamp,
                "traceID": W,
                "time": formatted_time,
                "response": M,
            }
            return W
