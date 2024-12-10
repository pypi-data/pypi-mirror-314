from lib import trace_loop

# WHL = "/Users/pcollins/github/signalfx/splunk-otel-python/dist/splunk_opentelemetry-0.0.1-py3-none-any.whl"
# WHL = "/Users/pcollins/github/signalfx/sop-worktree/dist/splunk_opentelemetry-1.20.0.dev0-py3-none-any.whl[otlp]"
# WHL = "/Users/pcollins/github/signalfx/splunk-otel-python/dist/splunk_opentelemetry-0.0.1-py3-none-any.whl[otlp]"
# WHL = "/Users/pcollins/github/signalfx/sop-worktree/dist/splunk_opentelemetry-1.20.0-py3-none-any.whl[otlp]"
# WHL = "/Users/pcollins/github/signalfx/sop-worktree/dist/splunk_opentelemetry-1.21.0-py3-none-any.whl[all]"
# WHL = "/Users/pcollins/github/signalfx/sop-v2/dist/splunk_opentelemetry-2.0.0a1-py3-none-any.whl"
# WHL = "/Users/pcollins/github/signalfx/splunk-otel-python/dist/splunk_opentelemetry-0.0.1-py3-none-any.whl"
WHL = "/Users/pcollins/github/signalfx/sop-v2-prs/dist/splunk_opentelemetry-2.0.0a1-py3-none-any.whl"

SERVICE_NAME = "my-otel-test"
NUM_ADDS = 12

if __name__ == "__main__":
    trace_loop(NUM_ADDS)


class MyOtelTest:
    def requirements(self):
        return (WHL,)

    def environment_variables(self):
        return {
            "OTEL_SERVICE_NAME": SERVICE_NAME,
        }

    def wrapper_command(self):
        return "opentelemetry-instrument"

    def on_start(self):
        return None

    def on_stop(self, telemetry, stdout: str, stderr: str, returncode: int) -> None:
        print(f"script completed with return code {returncode}")

    def is_http(self):
        return False
