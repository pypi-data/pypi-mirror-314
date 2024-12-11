from nsanic.libs.base_timed import BaseTimed


class TestTImed(BaseTimed):

    def __init__(self):
        super().__init__()
        self.add_loop_task('test01', 10, self.test_01)
        self.add_timed_task('test02', ['*', '*', '*', '*', '*', 30], self.test_02)

    async def test_01(self):
        print('test_01')

    async def test_02(self):
        print('test_02')


a = TestTImed()
a.start()
