from streamback.futures.serializers import GenericSerializer


class FutureRunner(object):
    def run(self, serialized_object, method_path, method, args, kwargs):
        serializer = GenericSerializer()

        args = serializer.deserialize(args)
        kwargs = serializer.deserialize(kwargs)
        obj = serializer.deserialize(serialized_object)

        for method_name in method_path:
            obj = getattr(obj, method_name, None)
            if not obj:
                raise NoCallableFound(
                    "Could not find callable {method_name} in {obj}".format(
                        method_name=method_name, obj=obj
                    )
                )

        callable_method = getattr(obj, method, None)
        if callable_method:
            result = getattr(obj, method)(*args, **kwargs)
            return serializer.serialize(result)
        else:
            raise NoCallableFound(
                "Could not find callable {method} in {obj}".format(
                    method=method, obj=obj
                )
            )


class NoCallableFound(Exception):
    pass
