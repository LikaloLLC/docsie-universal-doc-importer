def required_class_attributes_checker(cls, *attrs: str):
    for attr_name in attrs:
        try:
            getattr(cls, attr_name)
        except AttributeError:
            raise TypeError(f'Provide `{attr_name}` attribute in {cls.__module__}.{cls.__name__}')
