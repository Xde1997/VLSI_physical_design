def id_generator(cls):
    class Wrapped(cls):
        _current_id = 0

        @classmethod
        def get_next_id(cls):
            id_to_return = cls._current_id
            cls._current_id += 1
            return id_to_return

    return Wrapped

@id_generator
class GlobalIDGenerator:
    pass