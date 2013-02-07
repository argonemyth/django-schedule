"""
This won't be necessry for Django 1.5
As we can get a list of updated field in post_save and pre_save signals.
"""

class DiffingMixin(object):
    def __init__(self, *args, **kwargs):
        super(DiffingMixin, self).__init__(*args, **kwargs)
        self._original_fields = dict(self.__dict__)

    def _get_changed_fields(self):
        """
        You need to call this function before saving.
        It return a list of fields that's changed.
        """
        missing = object()
        #result = {}
        result = [] 
        for key, value in self._original_fields.iteritems():
            if value != self.__dict__.get(key, missing):
                #result[key] = value
                result.append(key)
        return result
