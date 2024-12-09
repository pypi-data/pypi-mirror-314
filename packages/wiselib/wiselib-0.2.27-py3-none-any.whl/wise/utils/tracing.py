from functools import wraps
from typing import Callable

from django.conf import settings
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

resource = Resource(
    attributes={
        SERVICE_NAME: settings.ENV.tracing.service_name or settings.ENV.service_name
    }
)
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.ENV.tracing.url))
if settings.ENV.tracing.enabled:
    provider.add_span_processor(processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)


def with_trace(name: str) -> Callable:
    def func(f: Callable) -> Callable:
        @wraps(f)
        def wrapped(*args, **kwargs):
            with tracer.start_as_current_span(name) as span:
                span.set_attribute("args", str(args))
                span.set_attribute("kwargs", str(kwargs))
                ret = f(*args, **kwargs)
                span.set_attribute("return", str(ret))
                return ret

        return wrapped

    return func
