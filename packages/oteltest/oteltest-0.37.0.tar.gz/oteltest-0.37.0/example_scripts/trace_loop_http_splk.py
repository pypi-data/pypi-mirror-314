from lib import trace_loop


if __name__ == "__main__":
    trace_loop(1)


class MyOtelTest:
    def requirements(self):
        return ("splunk-opentelemetry[all]",)

    def environment_variables(self):
        return {
            "OTEL_SERVICE_NAME": "my-otel-test",
            "OTEL_EXPORTER_OTLP_PROTOCOL": "http/protobuf",
        }

    def wrapper_command(self):
        return "splunk-py-trace"

    def on_start(self):
        return None

    def on_stop(self, telemetry, stdout: str, stderr: str, returncode: int) -> None:
        pass

    def is_http(self):
        return True
