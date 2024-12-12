import inspect

from streamback.futures.serializers import GenericSerializer


class Future(object):
    def __init__(self, obj, streamback):
        self.obj = obj
        self.streamback = streamback
        self.method_path = []

    def __getattr__(self, item):
        self.method_path.append(item)
        return self

    def __call__(self, *args, **kwargs):
        frame = inspect.currentframe().f_back
        method = self.method_path.pop()
        current_obj = self.obj
        for attr in self.method_path:
            current_obj = getattr(current_obj, attr, None)
            if current_obj is None:
                raise AttributeError(
                    "'{0}' object has no attribute '{1}'".format(
                        self.obj.__class__.__name__, attr
                    )
                )
        if not callable(getattr(current_obj, method, None)):
            raise Exception("'{0}' is not callable on the object".format(method))
        serializer = GenericSerializer()
        payload = {
            "serialized_object": serializer.serialize(self.obj),
            "method_path": self.method_path,
            "method": method,
            "args": serializer.serialize(list(args)),
            "kwargs": serializer.serialize(kwargs),
        }
        return FutureStream(
            self.streamback.send(
                "streamback.futures.v%s" % self.streamback.futures_version or 1,
                payload,
            )
        )


class FutureStream(object):
    def __init__(self, streamback_feedback_lane, func=None):
        self.streamback_feedback_lane = streamback_feedback_lane
        self.func = func or (lambda value: value)

    def read(self):
        value = self.streamback_feedback_lane.read(
            self.streamback_feedback_lane.streamback.name
        )
        return self.func(GenericSerializer().deserialize(value))

    def then(self, func):
        return FutureStream(self.streamback_feedback_lane, func)


class FutureIterable(list):
    def foreach(self, func):
        return FutureIterable([func(obj) for obj in self])


def gather(streams):
    serializer = GenericSerializer()
    return [serializer.deserialize(stream.read()) for stream in streams]


def stream(streams):
    serializer = GenericSerializer()
    for stream in streams:
        yield serializer.deserialize(stream.read())
