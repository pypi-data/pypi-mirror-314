import json
import time
import requests
from MZAPI.APM import APMClient
from MZAPI.KVS import LogHandler
from MZAPI.LOG import PublicIPTracker
from MZAPI.bdai import baiduauth
from MZAPI.headers import CustomRequestHeaders
from datetime import datetime
from opentelemetry import trace


class BaiduAddressRecognition:
    """
    一个用于使用百度AI进行地址识别的类。

    属性:
        ak (str): 百度API密钥。
        sk (str): 百度密钥。
        auth (baiduauth.BaiduAuth): 百度AI的身份验证处理器。
        ip (PublicIPTracker): 公共IP地址跟踪器。
        log (LogHandler): 日志处理器。
        headers (dict): 请求的HTTP头。
        apm_client (APMClient): 应用性能监控客户端。
        tracer (opentelemetry.trace.Tracer): OpenTelemetry追踪器。
    """

    def __init__(self, ak, sk, client_name):
        """
        初始化BaiduAddressRecognition实例。

        参数:
            ak (str): 百度API密钥。
            sk (str): 百度密钥。
            client_name (str): APM客户端名称。
        """
        self.ak = ak
        self.sk = sk
        self.auth = baiduauth.BaiduAuth(self.ak, self.sk)
        self.ip = PublicIPTracker()
        self.log = LogHandler()
        M = CustomRequestHeaders()
        self.headers = M.reset_headers()
        self.apm_client = APMClient(
            client_name=client_name,
            host_name="https://aip.baidubce.com/rpc/2.0/nlp/v1/address",
            token="kCrxvCIYEzhZfAHETXEB",
            peer_service="百度AI地址识别",
            peer_instance="180.97.107.95:443",
            peer_address="180.97.107.95",
            peer_ipv6="240e:ff:e020:934:0:ff:b0dc:3636",
            http_host="https://aip.baidubce.com/rpc/2.0/nlp/v1/address",
            server_name="MZAPI",
        )
        self.tracer = self.apm_client.get_tracer()

    def recognize(self, Content):
        """
        使用百度AI识别并提取文本内容中的地址。
        参数:
            Content (str): 需要识别地址的文本内容。
        返回:
            dict: 包含识别结果的字典，包括trace ID、时间戳和响应数据。
        """
        with self.tracer.start_as_current_span("百度AI地址识别") as span:
            token = self.auth.get_access_token()
            headers = {"Content-Type": "application/json", **self.headers}
            url = (
                f"https://aip.baidubce.com/rpc/2.0/nlp/v1/address?access_token={token}"
            )
            data = {"text": Content}
            response = requests.post(url, headers=headers, json=data)
            current_timestamp = int(time.time())
            dt_object = datetime.fromtimestamp(current_timestamp)
            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            IP = self.ip.get_public_ip()
            span.set_attribute("id", current_timestamp)
            span.set_attribute("url", url)
            span.set_attribute(
                "response", json.dumps(response.json(), ensure_ascii=False)
            )
            span.set_attribute("HTTP_status_code", response.status_code)
            M = response.json()
            span.set_attribute("HTTP_response_size", len(json.dumps(M)))
            span.set_attribute("HTTP_response_content_type", "application/json")
            span.set_attribute("HTTP_request_size", len(json.dumps(Content)))
            span.set_attribute("Method", "POST")  # 确保请求方法为POST
            span.set_attribute(
                "http.user_agent", response.request.headers.get("User-Agent", "-")
            )
            span.set_attribute("http.server", response.headers.get("Server", "-"))
            span.set_attribute(
                "http.date", response.headers.get("Date", "-")
            )  # 确保响应头名称为Date
            span.set_attribute("HTTP_request_headers", json.dumps(self.headers))
            span.set_attribute("client_ip", IP)
            self.ip.start_track_log()
            current_span = trace.get_current_span()
            traceID = current_span.get_span_context().trace_id
            W = trace.format_trace_id(traceID)
            self.log.start_process_log(response.json(), "百度AI地址识别", W)
            M = response.json()
            W = {
                "id": current_timestamp,
                "traceID": W,
                "time": formatted_time,
                "response": M,
            }
            return W
