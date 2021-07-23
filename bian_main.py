# 格式机器不规范，写的很丑，有大佬看到了可以帮萌新改一下吗
from selenium import webdriver
from time import sleep
from lxml import etree
import requests

# 定义页面网址
main_url = 'http://www.netbian.com'  # 主url
main_page_url = 'http://www.netbian.com/index{}.htm'  # 页url

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
}  # 请求头


# 网页请求函数
def get_url(url):
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(5)
    source = driver.page_source
    driver.quit()
    return source


# 从主页解析子页
def get_sun_url(htmls):
    html_etree = etree.HTML(htmls)  # 构造HTML文本文件
    sun_url = html_etree.xpath('//div[@class="list"]//ul//li//a//@href')
    del sun_url[2]
    del sun_url[2]
    del sun_url[-1]
    return sun_url


# 提取子页面图片url
def get_img(htmls):
    html_etree = etree.HTML(htmls)
    img_urls = html_etree.xpath('//div[@class="pic"]//p//a//@src')
    img_titles = html_etree.xpath('//div[@class="pic"]//p//a//@alt')
    return img_urls, img_titles


if __name__ == '__main__':
    html = get_url(main_page_url.format('_47'))
    # 只有写了第一页的爬取，因为爬取太多网站会给验证码，技术不够故只能作罢，要爬取其他页的请输入_+你想爬取的页数
    urls = get_sun_url(html)
    for urls in urls:
        sub_url = main_url + urls
        # print(sub_url)
        sub_html = get_url(sub_url)
        # print(sub_html)
        img_url, img_title = get_img(sub_html)

        num = (0 - 1)
        num += 1
        url_num = img_url[num]
        url_num = str(url_num)
        title_num = img_title[num]
        title_num = str(title_num)

        img = requests.get(url_num, headers=header).content
        img_name = 'D:/Test/' + title_num + '.jpg'
        with open(img_name, 'wb') as save_object:
            save_object.write(img)
