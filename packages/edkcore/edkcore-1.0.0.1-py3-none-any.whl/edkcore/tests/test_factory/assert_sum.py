from edkcore.support.abstract.abc_assert_action import AbcAssertAction


class AssertSum(AbcAssertAction):

    def assert_expect(self):
        assert self.context.count() == int(self.get_prop().expect("Sum"))
