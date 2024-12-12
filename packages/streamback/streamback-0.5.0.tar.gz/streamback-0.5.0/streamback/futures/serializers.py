import pickle
import base64


class Serializer(object):
    def serialize(self, obj):
        raise NotImplementedError()

    def deserialize(self, data):
        raise NotImplementedError()

    @property
    def name(self):
        return self.__class__.__name__


class PickleSerializer(Serializer):
    def serialize(self, obj):
        pickled_data = pickle.dumps(obj)
        encoded_data = base64.b64encode(pickled_data).decode("utf-8")
        return [self.name, encoded_data]

    def deserialize(self, data):
        pickled_data = base64.b64decode(data[1].encode("utf-8"))
        return pickle.loads(pickled_data)


class GenericSerializer(object):
    serializers = [PickleSerializer()]

    serializer_names = [serializer.name for serializer in serializers]

    def serialize(self, obj):
        if not obj:
            return obj

        if isinstance(obj, list) and not (obj[0] in self.serializer_names):
            return [self.serialize(value) for value in obj]

        if isinstance(obj, dict):
            return {key: self.serialize(value) for key, value in obj.items()}

        if hasattr(obj, "serializer"):
            serializer = obj.serializer
        else:
            serializer = PickleSerializer()

        return serializer.serialize(obj)

    def deserialize(self, data):
        if not data:
            return data

        if isinstance(data, list) and not (data[0] in self.serializer_names):
            return [self.deserialize(value) for value in data]

        if isinstance(data, dict):
            return {key: self.deserialize(value) for key, value in data.items()}

        if isinstance(data, list) and len(data) == 2:
            type = data[0]

            for serializer in self.serializers:
                if serializer.name == type:
                    return serializer.deserialize(data)

        return data
