import random

first_num = random.randint(75, 99)
third_num = random.randint(0, 3200)
fourth_num = random.randint(0, 140)


class FakeChromeUA:
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]

    os_type_phone = [
        '(Linux; Android 6.0; Nexus 5 Build/MRA58N)', '(Linux; Android 11; Pixel 5)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    @classmethod
    def get_ua(cls):
        return ' '.join(['Mozilla/5.0', random.choice(cls.os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version, 'Safari/537.36']
                        )
        # return choice(pc_user_agent)

    @classmethod
    def get_ua_phone(cls):
        return ' '.join(['Mozilla/5.0', random.choice(cls.os_type_phone), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version, 'Mobile Safari/537.36']
                        )


if __name__ == '__main__':
    ua = FakeChromeUA.get_ua_phone()
    print(type(ua))
    print(ua)
