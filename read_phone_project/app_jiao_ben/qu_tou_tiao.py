from app_jiao_ben import AppReadBase
import random
import uiautomator2
import time


class QuTouTiao(AppReadBase):
    def __init__(self, phone_serial, pp):
        super(QuTouTiao, self).__init__(phone_serial, pp)
        # self.pp = uiautomator2.connect_usb()
        self.pp.watcher('tip1').when('知道了').click()
        self.pp.watcher('tip2').when('残忍离开').click()
        self.pp.watcher.start(0.5)

    def jurisdiction(self):
        # 需要获取电话权限、通知权限
        # 获取app权限，仅首次启动app才会用到
        if self.pp(text='同意').exists(timeout=3):
            self.pp(text='同意').click_exists(timeout=3)
            self.pp(text='同意去开启').click_exists(timeout=10)
            self.pp(text='允许').click_exists(timeout=10)

    def sign_in(self):
        self.logger.info(f'开始登录')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        if self.pp(text='登录').exists(timeout=5):
            self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/bnl"]').click_exists(timeout=20)
        else:
            read_time = self.pp.xpath('//*[@resource-id="com.jifen.qukan.personal:id/ee"]').get_text()
            return read_time

    def qian_dao(self):
        self.logger.info(f'开始签到')
        if self.pp(text='签到').exists(timeout=5):
            self.pp(text='签到').click(offset=(random.random(), random.random()))
        if self.pp(text='恭喜获得').exists(timeout=3):
            self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/wj"]').click()

    def read_issue(self):
        self.logger.info(f'开始阅读文章')
        self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/n9"]/'
                                                 'android.widget.FrameLayout[1]').get().bounds)
        if self.pp(text='领取').exists:
            self.pp(text='领取').click(offset=(random.random(), random.random()))
            time.sleep(random.random() + 1)
        # 获取前5个栏目
        for j in range(5):
            lan_mu = self.pp.xpath(f'//*[@resource-id="com.jifen.qukan:id/ad_"]/android.widget.LinearLayout[1]/'
                                   f'android.widget.RelativeLayout[{j+1}]')
            self.click_random_position(lan_mu.bounds)
            time.sleep(random.random() + 1)
            for i in range(random.randint(8, 12)):  # 每个栏目下滑随机次
                # 每个栏目下的文章标题
                for title in self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/al8"]').all():
                    # 需要满足看文章概率
                    if random.random() >= self.probability_read_issue:
                        continue
                    self.click_random_position(title.bounds)
                    time.sleep(random.random() + 1)
                    # 如果有获取金币的图标，才看，没有就返回,
                    if self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/a3_"]').exists:
                        issue_time_start = time.time()  # 开始计时
                        read_issue_time = random.randrange(5, 125, 30)  # 看文章的随机时间
                        read_video_time = random.randrange(5, 185, 30)  # 看视频的随机时间
                        # 看下是视频还是文章，视频就停着看，文章就下滑看
                        if self.pp.xpath('//com.qukan.media.player.renderview.TextureRenderView').exists:
                            while True:
                                if self.pp(text='重播').exists or time.time() - issue_time_start > read_video_time:
                                    break
                                time.sleep(1)
                        else:
                            while True:
                                time.sleep(random.uniform(3, 5))
                                self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8),
                                              random.uniform(0.3, 0.6), random.uniform(0.2, 0.3),
                                              random.uniform(0.1, 0.3))
                                time.sleep(1)
                                if not self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/g3"]').exists:
                                    self.pp.press('back')
                                # self.pp(scrollable=True).scroll(steps=200)
                                if time.time() - issue_time_start > read_issue_time:
                                    break
                        # 按照设定的点赞概率，随机点赞
                        if self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/bla"]').exists and \
                                random.random() < self.probability_thumb_up:
                            self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/bla"]')
                                                       .get().bounds)
                        # 按照设定的评论概率，随机评论
                        if self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/bku"]').exists and \
                                random.random() < self.probability_commit:
                            while True:
                                self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/bku"]')
                                                           .get().bounds)
                                time.sleep(random.random() + 1)
                                if self.pp(text='我来说两句...').exists:
                                    self.pp(text='我来说两句...').click(offset=(random.random(), random.random()))
                                    break
                                elif self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/zq"]').exists:
                                    break
                            self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/zq"]').wait()
                            self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/zq"]'). \
                                set_text(random.choice(self.commit))
                            self.pp(text='发布').click(offset=(random.random(), random.random()))
                            time.sleep(random.random() + 1)
                    self.pp.press('back')
                    time.sleep(random.random() + 1)
                    self.pp(text='我的').click(offset=(random.random(), random.random()))
                    read_time = self.pp.xpath('//*[@resource-id="com.jifen.qukan.personal:id/ee"]').get_text()
                    if int(read_time) > 60:
                        return
                    else:
                        self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/n9"]/'
                                                                 'android.widget.FrameLayout[1]').get().bounds)
                        time.sleep(random.random() + 1)
                # 随机下滑2-4次
                for k in range(random.randint(2, 4)):
                    self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                                  random.uniform(0.2, 0.3), random.uniform(0.1, 0.3))
                    time.sleep(random.random())
            self.logger.info('看完这个栏目了，换个栏目')

    def get_read_reward(self):
        self.logger.info(f'开始获阅读文章的奖励')
        self.pp(text='任务').click(offset=(random.random(), random.random()))
        while True:
            while True:
                if not self.pp(text="阅读得大额奖励").exists or self.pp(text="阅读得大额奖励").center()[1] > \
                        self.pp.xpath('//*[@resource-id="com.jifen.qukan.taskcenter:id/g5"]').get().bounds[1]:
                    self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                                  random.uniform(0.2, 0.3), random.uniform(0.1, 0.3))
                    time.sleep(random.random())
                else:
                    break
            temp = self.pp.xpath('//*[@text="阅读得大额奖励"]/following-sibling::android.widget.TextView[3]')
            if temp.get_text() == '领取奖励':
                self.click_random_position(temp.get().bounds)
                if self.pp(text='关闭').exists(timeout=60):
                    self.pp(text='关闭').click(offset=(random.random(), random.random()))
                    time.sleep(random.random() + 1)
                self.pp.press('back')
                if self.pp(text='恭喜获得').exists(timeout=3):
                    self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.qukan.taskcenter:id/r"]')
                                               .get().bounds)
            else:
                break

    def get_advertisement_reward(self):  # 看广告的金币，收益低
        self.logger.info(f'开始看广告获金币')
        self.pp(text='任务').click(offset=(random.random(), random.random()))
        while True:
            while True:
                if not self.pp(text="看广告视频拿金币").exists or self.pp(text="阅读得大额奖励").center()[1] > \
                            self.pp.xpath('//*[@resource-id="com.jifen.qukan.taskcenter:id/g5"]').get().bounds[1]:
                    self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                                  random.uniform(0.2, 0.3), random.uniform(0.1, 0.3))
                    time.sleep(random.random())
                else:
                    break
            temp = self.pp.xpath('//*[@text="看广告视频拿金币"]/following-sibling::android.widget.TextView[2]')
            if temp.get_text() == '立即观看':
                self.click_random_position(temp.get().bounds)
                if self.pp(text='关闭').exists(timeout=60):
                    self.pp(text='关闭').click(offset=(random.random(), random.random()))
                    time.sleep(random.random() + 1)
                self.pp.press('back')
                if self.pp(text='恭喜获得').exists(timeout=3):
                    self.click_random_position(self.pp.xpath('//*[@resource-id="com.jifen.qukan.taskcenter:id/r"]')
                                               .get().bounds)
            else:
                break

    def clean_cache(self):
        self.logger.info(f'开始清理缓存')
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        while True:
            if not self.pp(text="设置").exists:
                self.pp.swipe(random.uniform(0.3, 0.6), random.uniform(0.7, 0.8), random.uniform(0.3, 0.6),
                              random.uniform(0.2, 0.3), random.uniform(0.1, 0.3))
                time.sleep(random.random())
            else:
                break
        self.pp(text="设置").click(offset=(random.random(), random.random()))
        self.pp(text="清除缓存").wait()
        self.pp(text="清除缓存").click(offset=(random.random(), random.random()))

    def coin_info(self):
        self.pp(text='我的').click(offset=(random.random(), random.random()))
        self.pp(text='我的金币').wait()
        self.pp(text='我的金币').click(offset=(random.random(), random.random()))
        self.pp(description='提现').wait()
        self.pp(description='提现').click(offset=(random.random(), random.random()))

    def main_do(self):
        # raise
        self.app_start('趣头条')
        self.jurisdiction()
        self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/pe"]').wait()
        self.pp.xpath('//*[@resource-id="com.jifen.qukan:id/pe"]').wait_gone()
        self.pp(text='我的').wait(timeout=30)
        read_time = self.sign_in()
        self.qian_dao()
        if float(read_time) < 60:
            self.read_issue()
        else:
            self.logger.info(f' 趣头条 今日已经获取{read_time}分钟阅读时间，不再阅读了')
        self.get_read_reward()
        self.get_advertisement_reward()
        self.clean_cache()
        # self.coin_info()
        self.app_end()