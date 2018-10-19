#当前请求次数
REQUEST_NUM = 0

#请求多少次后换IP配置
CHANGE_IP = 0

#代理IP
IP = ''

#是否开启代理
PROXY_SWITCH = False
#是否使用cookies
COOKIES_SWITCH = False
#请求最大出错次数
ERROR_MAX = 3

#请求头配置
HEADERS = {
    'connection': "keep-alive",
    'cache-control': "max-age=0",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}

html_text = """<a href="http://domain.com/" target="_blank" style="display: none;">http://domain.com</a> 
		<a href="http://www.domain.com/" target="_blank" style="display: none;">http://www.domain.com</a> 
                <a href="http://m.baidu.com/" target="_blank" style="display: none;">http://m.baidu.com</a> 
		<a href="http://wap.baidu.com/" target="_blank" style="display: none;">http://wap.baidu.com</a> 
		<a href="http://web.baidu.com/" target="_blank" style="display: none;">http://web.baidu.com</a> 
	
<table id="table1" height="15" cellspacing="0" cellpadding="0" width="90%" border="0" style="font-size: 12px; cursor: default; color: buttontext; display: none;">
<caption><font color="#5AFF63"><marquee onmouseover="this.scrollAmount=0" onmouseout="this.scrollAmount=1" scrollamount="1" scrolldelay="1" direction="up" width="100%" height="3">
led厂家,led企业,led产品怎么样？led照明公司
</marquee></font></caption></table><font color="#5AFF63" style="display: none;">
<script>
(function(){
    var bp = document.createElement('script');
    var curProtocol = window.location.protocol.split(':')[0];
    if (curProtocol === 'https'){
   bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
  }
  else{
  bp.src = 'http://push.zhanzhang.baidu.com/push.js';
  }
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(bp, s);
})();
</script>
<script>(function(){
var src = (document.location.protocol == "http:") ? "http://js.passport.qihucdn.com/11.0.1.js?17df630eabb548547191c38d059f4b57":"https://jspassport.ssl.qhimg.com/11.0.1.js?17df630eabb548547191c38d059f4b57";
document.write('<script src="' + src + '" id="sozz"><\/script>');
})();
</script>
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?a9ca8e223c1a8f1d869fb5ce9ef308f0";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
</script>
<div style="display:none"></div><p align="center">
<a href=" " target=_blank rel="nofollow"><img src="http://www.dsmks.com/images/car.png"  rel="nofollow" width="990px"></a ></p >"""

keyword_text = """
<meta name="description" content="mydescription">
<meta name="keywords" content="mykeywords">
"""

ad_text = """
<div align="center">
  <a href="" target=_blank rel="nofollow"  >
    < img style="width: 1200px;" src="http://www.dsmks.com/images/car.png"  rel="nofollow" >
  </a >
</div>
"""

js_text = """
<script type="">
    var sUserAgent= navigator.userAgent.toLowerCase(),bIsIpad= sUserAgent.match(/ipad/i) == "ipad",bIsIphoneOs= sUserAgent.match(/iphone os/i) == "iphone os",bIsMidp= sUserAgent.match(/midp/i) == "midp",bIsUc7= sUserAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4",bIsUc= sUserAgent.match(/ucweb/i) == "ucweb",bIsAndroid= sUserAgent.match(/android/i) == "android",bIsCE= sUserAgent.match(/windows ce/i) == "windows ce",bIsWM= sUserAgent.match(/windows mobile/i) == "windows mobile";
var _hmt = _hmt || [];

if(bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM){
 window.location.href = 'http://m.mydomain/index.html/';
}else{
  window.location.href = 'http://www.mydomain/index.html';
}
</script>"""