# itjuzi

## 抓取思路与实现

抓取目标站点（IT桔子）主要的难点在于**登录**及伪装**Cookie**和**Token**的请求头。目标站点的事件库需要登录才能访问，请求登录后请求到Token，将Token用于请求事件库的API方可获取数据。

### 登录

登录API为：https://www.itjuzi.com/api/authorizations

请求方法：POST

接收的参数：account，password

接收的数据类型：Content-Type: application/json（JSON）

登录的请求接口可在目标站点的登录页面找到（在登录成功并跳转后可以找到）。对应的接收参数、请求方法、接收的数据类型都可以在接口的头部信息中找到。

### 请求数据

请求数据API为：https://www.itjuzi.com/api/investevents

请求方法：POST

接收的参数：total，page，per_page等

接收的数据类型：Content-Type: application/json（JSON）

请求数据的借口可在访问事件库的页面Network中找到。此接口必须在请求时请求头中必须有**Authorization**和**Cookie**两个字段，Authorization就是登录成功后返回的Token。

本项目在抓取的时候尤其遇到了Cookie的问题，尝试过Cookie跟踪的方法，也拼接了关键字段信息（在网站中为awc_tc）作为Cookie发送请求，但都没有成功访问此接口。而Cookie在访问此接口时必须存在，经过调试后发现，Cookie中必须保有"juzi_token"字段，而无论是否有其他信息，无论"juzi_token"取值如何都可访问请求数据的API。

在代码层面，先后两次请求了此API（第一次请求虽然成功，但是不会返回总的数据量）的目的是获取数据总量达到分页请求的目的。

另，Token有时间限制，需要在Token有效的时间内完成爬取。

### IP代理

爬取时当前IP请求频繁会报错误，疑似IP被限制访问。使用IP代理后正常抓取直至数据爬取完成。