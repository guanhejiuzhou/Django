"""
HttpRequest封装的属性和方法:
1.COOKIES属性：该属性包含了HTTP请求携带的所有cookie‘
2.get_signed_cookie方法：获取带签名的cookie，如果签名验证失败，会产生BadSignature异常

HTTPResponse封装的方法：
1.set_cookie方法：该方法可以设置一组键值对，并将其最终写入浏览器
2.set_signed_cookie方法：和上面的方法作用相似，但是会对cookie进行签名来达到防篡改的作用

激活SessionMiddleware之后，每个HTTPRequest对象都会绑定一个session属性，它是一个类似字典的对象，除了保存
用户数据之外，还提供了检测浏览器是否支持cookie的方法，包括：
1.set_test_cookie方法：设置用于测试的cookie
2.test_cookie_worked方法：检测测试cookie是否工作
3.delete_test_cookie方法：删除用于测试的cookie
4.set_expiry方法：设置回话的过期时间
5.get_expire_age/get_expire_data方法：获取回话的过期时间
6.clear_expired方法：清理过期的会话

"""