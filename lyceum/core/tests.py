from django.test import TestCase

__all__ = []


class ContextTest(TestCase):
    fixtures = ['data.json']

    def check_instanse_fields(self, instance, loaded, prefetched, not_loaded):
        instance_dict = instance.__dict__

        for field in loaded:
            self.assertIn(field, instance_dict)

        for field in prefetched:
            self.assertIn(field, instance_dict['_prefetched_objects_cache'])

        for field in not_loaded:
            self.assertNotIn(field, instance_dict)
