# -*- coding: utf-8 -*-


def raise_type_exception(invalid_value, valid_types, failed_operation):
        invalid_value = type(invalid_value).__name__
        valid_types = [t.__name__ for t in valid_types]
        valid_types = ', '.join(valid_types)
        message = 'Invalid type \'{}\'. Can only {} \'{}\' types'
        message = message.format(invalid_value, failed_operation.lower().strip(), valid_types)
        raise TypeError(message)
