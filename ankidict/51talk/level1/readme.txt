1.每一课的图标
http://www.51talk.com/user/study_center_zx中的列表

课文音频
https://static.51talk.com/upload/efl_audio/zip/talk0793561.zip


预习页面
https://efl.51talk.com/efl/preview/793561

51talk使用的是Chivox做为语音方案，在预习页面上。
https://static.51talk.com/js/efl/chivox_preview2.0.js?v=1503544423739

页面上用这两个元素的播放和录音
<em class="play playOn"></em>
<em class="record recordOff"></em>

//听
function play_ref(type,row){
	if(row ==''){row =0;}
	if($(".record").hasClass("recordOn")){
		$(".record").addClass("disableRecord");
	}
	record_url(type, row);

	$('.play').click();
	
}
//说
function record_ref(type, row){
	record_url(type, row);
	$('#aiPanel .record').click();
}

网页中定义了word_ref和dialog_ref数组，保存了生词和对话的文本和音频地址。

<script>
    //变量初始化
    var www_url = "//static.51talk.com";
    var word_ref = [{"title":"how","url":"643dec2d25b7f2a1d6eb262ed80140d3_170516dbd.mp3","sentence1":"How does it work?","sentence1_url":"cc79145c49e70a9c9ffb86260a032857_170516c88.mp3","sentence2":"","sentence2_url":""},{"title":"fine","url":"da6cc7e1df4485289cc714d0a3eadd6e_170516160.mp3","sentence1":"I am fine.","sentence1_url":"263cde200196be82c7f38c532b70568f_170516e78.mp3","sentence2":"","sentence2_url":""},{"title":"what","url":"8243efd27049e2e4588e66138cede332_170516aa0.mp3","sentence1":"What is he doing?","sentence1_url":"c0c6c815479c3434bdf455081cdb2b43_170516701.mp3","sentence2":"","sentence2_url":""}];
    var dialog_ref = {"talk0":{"title":["Hello, Timmy. How are you?","Hello, Cindy. I am fine.","What are you doing?","I am listening to French music.","What are you doing?","I am singing French songs.","Cool! Let's play together.","Sure! Just come over."],"url":["14f1c4385420e3a75afd2360020f841f_170928be2.mp3","656e105248c01d0338e53e7492e5016f_170926b2f.mp3","317ef53e3ebd92126c9cf902d433dc11_170926bd0.mp3","e2cade9597a02405b3be030655ef5bdb_1709287ce.mp3","616282256e601d6c6f8e7cf7765e7cf9_1709265e7.mp3","6291cbddcd0ec340644b0ac4a362f11a_170926e80.mp3","bbc1df69304553b91893961641b613fd_170926e1d.mp3","a87d7d2b4f746c63b3268f104e97a707_170926744.mp3"]}};
    var sentence_ref = 0;
    var params = 793561;
    var snum = "U23057131136";
    var video_url = "https://static.51talk.com/upload/efl_video/prepar/bd3d6c4583118a1f753cb0440a6c1377_180601574.mp4";
</script>

收集这些数据，并下载相关的文件。

文件下载地址形如：
//static.51talk.com/upload/efl_audio/prepar/14f1c4385420e3a75afd2360020f841f_170928be2.mp3


定义了一个
<div id = "aiPanel">与17kouyu.js绑定



window.aiPanel = new _17kouyu.IPanel({...


登录url:
$.ajax({
	url: "//login.51talk.com/ajax/login",
	type: "post",
	async: !1,
	dataType: "json",
	data: n,
	success: function(o) {
		1e4 == o.code ? window.location.href = o.res.from_url : o.res.counter >= 3 ? t.showFn3(" \u5bc6\u7801\u9519\u8bef\uff0c\u8bf7\u7acb\u5373\u627e\u56de") : t.showFn1(o.message)
	}
})

n = {
auto_login:1,
client:1,
from_url:"https://www.51talk.com/efl/preview/793561",
group:0,
la:"Bhrt0rpPC"
password:"uxlSo0z+H7w5IPmOSV4CdpEBPHzjmfnyFUWlE3EL1q8qbSYvtpqO2ZMLETpV+WT03peVCxbmRKRBPjnD+kkIegyiO7T5ybdgUfNVX9UEWtwfdo6CmBiKxPPwySkOo0YdHzwXZGQ1DaVOMxGiiybFzGpSxsQcJ+tkkeHJWynytVM=",
user_name:"13316589693"
}

代码分析
            this.jsLginBtn.on("click", function() {
                var i = $(".js_loginBtn").filter(":visible").attr("id")
                  , n = {};
                if ("mobileLoginBtn" == i) {
                    if (n = {
                        auto_login: o.mobileAutoLogin,
                        user_name: o.mobile.val(),
                        mobile_code: o.code.val(),
                        la: o.loginLa.val()
                    },
                    "" == o.mobile.val())
                        return o.errorFn(o.mobile, "\u8bf7\u8f93\u5165\u624b\u673a\u53f7"),
                        !1;
                    if ("" == o.code.val())
                        return o.errorFn(o.code, "\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801"),
                        !1
                } else if ("accountLoginBtn" == i) {
                    o.publicKey.val() || o.getPublicKey();
                    var e = new JSEncrypt;
                    e.setPublicKey(o.publicKey.val());
                    var s = e.encrypt(o.password.val());
                    if (o.password2.val(s),
                    s && "false" != s || o.password2.val(hex_md5(o.password.val())),
                    n = {
                        auto_login: o.accounAutoLogin,
                        user_name: o.accountId.val(),
                        la: o.loginLa.val(),
                        password: o.password2.val()
                    },
                    "" == o.accountId.val())
                        return o.errorFn(o.mobile, "\u8bf7\u8f93\u5165\u624b\u673a\u53f7"),
                        !1;
                    "" == o.password.val() && "" == o.password1.val() && o.errorFn(o.password, "\u8bf7\u8f93\u5165\u5bc6\u7801")
                }
                n = $.extend(n, loginData),
                $("#code").blur(),
                $("#password").blur(),
                $.ajax({
                    url: "//login.51talk.com/ajax/login",
                    type: "post",
                    async: !1,
                    dataType: "json",
                    data: n,
                    success: function(o) {
                        1e4 == o.code ? window.location.href = o.res.from_url : o.res.counter >= 3 ? t.showFn3(" \u5bc6\u7801\u9519\u8bef\uff0c\u8bf7\u7acb\u5373\u627e\u56de") : t.showFn1(o.message)
                    }
                })
            }),
