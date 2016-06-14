#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from time import sleep
from faker import Faker
from flask import Flask, request, Response, jsonify, g
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# config here temp

default_selenium_host = 'selenium'



app = Flask(__name__)
app.config['DEBUG'] = True
faker = Faker()


SELENIUM_DRIVER_HOST = os.environ.get('PW_SELENIUM_DRIVER', default_selenium_host)
selenium_url = "http://%s:4444/wd/hub" % SELENIUM_DRIVER_HOST
print('>>>> ', selenium_url)


@app.route("/_health", methods=['GET'])
def check_health():
    return 'I am OK!'


@app.route("/_sg_cookie", methods=['POST'])
def get_sg_cookie():
    """
    :return: String of Sogou Cookie
    """
    # default_cookie = 'SUV=1387161004695182; lastdomain=null; ssuid=1407346305; pgv_pvi=5216948224; pgv_si=s6847528960; pid=ask.xgzs.lddj; cid=w.search.yjjlink; GOTO=Af90017; ss_pidf=1; ss_cidf=1; SEID=000000004658860A2AFF0B10000B66B8; CXID=0A522AD3998C91A8993D3877F703A871; SUID=F2F4C66F506C860A5667DB8B000E648F; PHPSESSID=b7oek1dhh4ks6dl3fk453hisa7; ABTEST=8|1461035006|v1; weixinIndexVisited=1; JSESSIONID=aaaqBvaz15csY4qZ9lPqv; IPLOC=CN1100; ad=MQpZyZllll2QBdmalllllVtkynYlllllbDb1Dkllll9lllllpZlll5@@@@@@@@@@; ld=kyllllllll2gaIxElllllVtm647lllllToVlakllll9llllljllll5@@@@@@@@@@; SNUID=4F20E0BE6165532C39712CD46183AAFA; sct=141'
    # resp_data = {'sg_cookie': default_cookie}
    # return jsonify(resp_data)
    #--------

    username = request.form['email']
    password = request.form.get('password', 'guoku1@#')
    driver = g.driver

    if not username:
        return 'username is required!'

    driver.get('https://account.sogou.com/web/webLogin')
    try:
        quit_button = driver.find_element_by_css_selector("li.logout a")
        quit_button.click()
        sleep(3)
        driver.get('https://account.sogou.com/web/webLogin')
    except NoSuchElementException as e:
        pass

    app.logger.info("Will try to login as %s." % username)
    try:
        sleep(5)
        driver.find_element_by_css_selector('input[name="username"]').clear()
        driver.find_element_by_css_selector('input[name="username"]').send_keys(
            username)
        driver.find_element_by_css_selector('input[name="password"]').clear()
        driver.find_element_by_css_selector('input[name="password"]').send_keys(
            password)
        driver.find_element_by_css_selector(
            'form#Login button[type=submit]').click()
        app.logger.info("login as %s.", username)

        sleep(2)
        driver.get('http://weixin.sogou.com/')
        print('visited weixin.sogou.com')
        sleep(2)
        driver.get('http://weixin.sogou.com/weixin?type=1&query=shenyebagua818')
        print('searched by weixin.sogou.com')
        sleep(2)
        # try:
        #     driver.find_element_by_css_selector("div.results div").click()
        #     print 'clicked'
        #     print driver.window_handles
        # except NoSuchElementException as e:
        #     print e.message
        #     pass
        app.logger.info("getting cookies......")
        cookie = '; '.join(
            '{}={}'.format(c['name'], c['value'])
            for c in driver.get_cookies())
        resp_data = {'sg_cookie': cookie}
        app.logger.info("got cookies success")
        app.logger.info(resp_data)
        return jsonify(resp_data)
    except BaseException as e:
        app.logger.error("sogou login failed! %s", e.message)

@app.route("/userlink", methods=['POST'])
def get_user_link():
    weixin_id = request.args.get('query')
    driver = g.driver
    sleep(1)
    try:
        driver.get('http://weixin.sogou.com/weixin?type=1&query=%s' % weixin_id)
        obj = driver.find_element_by_id('sogou_vr_11002301_box_0')    #Todo 这个ID名字可能不能写死
        user_link = obj.get_attribute('href')
        app.logger.info(user_link)
        return jsonify({'user_link' :user_link})
    except Exception as e:
        app.logger.info(e)


@app.route("/", methods=['POST'])
def fetch():
    """ Fetching a page via PhantomJS.

    :Args:
        url : Url to be fetched of a page.
        expected_element: Wait for until this element been lo.
        time_out: Number of seconds before timing out.
    """

    url = request.form['url']
    driver = g.driver
    expected_element = request.form.get('expected_element', 'body')
    timeout = request.form.get('timeout', 15)
    timeout = float(timeout)
    if not url:
        return

    app.logger.info(">> Start to fetching %s" % url)
    driver.get(url)

    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, expected_element)))
        app.logger.info(">> Page is ready!")
    except TimeoutException:
        app.logger.info(">> Loading took too much time!")

    app.logger.info(">> Phantom have fetched the web page.")
    html = driver.page_source.encode('utf-8')
    return Response(html, mimetype='text/xml')


@app.before_request
def before_request():
    driver = webdriver.Remote(
        command_executor=selenium_url,
        desired_capabilities=DesiredCapabilities.CHROME.copy()

    )
    g.driver = driver


@app.teardown_request
def teardown_request(exception):
    print('>>  shut down. %s: ', getattr(g, 'driver', 'none.'))
    if hasattr(g, 'driver'):
        g.driver.close()
        g.driver.quit()


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
