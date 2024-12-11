import unittest

class Test(unittest.TestCase):
    def test_get_dates(self):
        from zhongwen.時 import 取日期
        from pandas import Timestamp
        self.assertEqual(取日期('1121231'), Timestamp('2023-12-31'))

    def test_get_periods(self):
        from zhongwen.時 import 取期間
        from pandas import Period, Timestamp
        self.assertEqual(取期間('112'), Period('2023', 'Y-DEC'))
        self.assertEqual(取期間('2024'), Period('2024', 'Y-DEC'))
        self.assertEqual(取期間('11310'), Period('202410', 'M'))
        self.assertEqual(取期間('113/10'), Period('202410', 'M'))
        self.assertEqual(取期間('113/1'), Period('202401', 'M'))
        self.assertEqual(取期間('2024-10'), Period('202410', 'M'))
        self.assertEqual(取期間('2020-01'), Period('202001', 'M'))
        self.assertEqual(取期間('2024Q2'), Period('2024Q2', 'Q-DEC'))
        self.assertEqual(取期間('2024Q2'), Period('2024Q2', 'Q-DEC'))
        self.assertEqual(取期間('99年年度'), Period('2010', 'Y-DEC'))
        self.assertEqual(取期間('112年年度'), Period('2023', 'Y-DEC'))
        self.assertEqual(取期間('112年第3季'), Period('2023Q3', 'Q-DEC'))
        self.assertEqual(取期間('112年上半年'), Period('2023-6', '6M'))

    def test_cut_period(self):
        from zhongwen.時 import 全年期別分割, 取期間
        from pandas import period_range
        import pandas as pd
        ps, rps = 全年期別分割(pd.Period('2024-06', freq='6M'))
        print(ps)
        print(rps)
        # print(period_range('2024Q1', periods=3, freq='Q'))

    def test_YOY(self):
        from zhongwen.時 import 去年同期, 取期間
        import pandas as pd
        p = 取期間('2024Q3')
        self.assertEqual(去年同期(p), 取期間('2023Q3'))
        p = pd.Period('2024-06', freq='6M')
        self.assertEqual(去年同期(p), pd.Period('2023-06', freq='6M'))

    def test_period(self):
        from zhongwen.時 import 上月, 上年度
        import pandas as pd
        self.assertIsInstance(上月(), pd.Period)
        self.assertIsInstance(上年度(), pd.Period)
        print(上年度())

    def test_iter_yearly(self):
        from zhongwen.時 import 自起始年底按年列舉至本年底
        from zhongwen.時 import 取日期
        import pandas as pd
        ds = 自起始年底按年列舉至本年底(111)
        ys = pd.date_range(取日期('1111231'), 取日期('1131231'), freq='YE')
        self.assertEqual(ds
                        ,list(pd.date_range(取日期('1111231'), 取日期('1131231'), freq='YE')))


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('googleclient').setLevel(logging.CRITICAL)
    logging.getLogger('matplotlib').setLevel(logging.CRITICAL)
    logging.getLogger('faker').setLevel(logging.CRITICAL)
    unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(Test('test_take_period'))  # 指定測試
    unittest.TextTestRunner().run(suite)
