$(function () {
	//获取主菜单导航内容
	$.ajax({
        url: 'http://127.0.0.1:5000/CUID',
        method: 'get',
        data: {
            tableName: 'ModulMenus',
			field: 'MenuType',
            fieldvalue: '模块级',
            limit: 100000000,
            offset: 0
        },
        success: function (res) {
            res = JSON.parse(res)
			$(".sidebarLeftNav").html("")
			var sidebarLeftNavHtml = ""
			$.each(res.rows,function(i,value){
				sidebarLeftNavHtml += '<li><a href="javascript:;" class="sidebarLeftItem" rel="'+ res.rows[i].ID +'" title="'+ res.rows[i].ModulMenuName +'"><span class="'+ res.rows[i].MenuLogo +'"></span></a></li>'
			})
			$(".sidebarLeftNav").append(sidebarLeftNavHtml)
			$(".sidebarLeftNav li").eq(0).find("a").addClass("rootMenu").click()
        }
    })
	$(".sidebarLeftNav").on('click',".sidebarLeftItem",function(){
		var navID = $(this).attr("rel")
		var title = $(this).attr("title")
		$.ajax({
			url: 'http://127.0.0.1:5000/CUID',
			method: 'get',
			data: {
				tableName: 'ModulMenus',
				field: 'ParentNode',
				fieldvalue: navID,
				limit: 100000000,
				offset: 0
			},
			success: function (res) {
				res = JSON.parse(res)
				$(".sidebarRightNav").html("")
				var sidebarRightNavHtml = ""
				$.each(res.rows,function(i,value){
					sidebarRightNavHtml += '<li><a href="javascript:;" lay-href="'+ res.rows[i].ModulMenuRoute +'" class="site-tab"><span>'+ res.rows[i].ModulMenuName +'</span></a></li>'
				})
				$(".sidebarRightNav").append(sidebarRightNavHtml)
			}
		})
        $(this).addClass("rootMenu").parent().siblings().find("a").removeClass("rootMenu")
		$(".sidebarRight .sidebarRightHead").each(function(){
			if($(this).attr("data-menu-indet") == title){
				$(this).removeClass("hidden").siblings(".sidebarRightHead").addClass("hidden")
			}
		})
	})
	//添加修改cookie 用户信息
	var jobNumber = $("#userInfo").attr("data-job-number");
	var sesseionid = $("#userInfo").attr("data-sesseionid");
	setCookie("jobNumber",jobNumber)
	setCookie("sesseionid",sesseionid)
	//事实匹配sessionid 新用户登录后踢掉上一个用户
	function reqs() {
		$.ajax({
			url: 'http://127.0.0.1:5000/CUID',
			type: 'get',
			data:{
				tableName: 'User',
				field: 'WorkNumber',
				fieldvalue: jobNumber,
				limit: 100000000,
				offset: 0
			},
			success: function(res) {
				res = JSON.parse(res)
				console.log(res.rows[0].session_id)
				if(res.rows[0].session_id != getCookie("sesseionid")){
					bootbox.alert({
						message: "您的账号已在其他设备登录，请重新登录",
						callback: function () {
							window.location.href = "/account/logout"
						}
					})
				}
			},
			error: function() {
				bootbox.alert('请求sessionid失败');
			}
		});
	}
	setInterval(reqs, 5000);

	//右上角用户信息
	$(".navHead-item").mouseover(function() {
		$(this).find(".navUserPanel").css("display", "block")
	}).mouseout(function (){
		$(this).find(".navUserPanel").css("display","none")
	})

	//查看用户信息
	$("#seeUserMessage").on('click',function(){
		var html= ''
		$.ajax({
			url:'/user_manage/MyUser/Select',
			method: 'get',
			data:{
				id: '',
				Name:$(".navUserName").html(),
				limit : 1,
                offset : 0
			},
			success:function(res){
				res = JSON.parse(res)
				html = '<table class="table table-bordered"><tr><td>用户名</td><td>' + res.rows[0].Name +'</td></tr>'+
            	'<tr><td>工号</td><td>'+ res.rows[0].WorkNumber +'</td></tr><tr><td>所属部门</td><td>'+ res.rows[0].OrganizationName +'</td></tr>'+
            	'<tr><td>所属角色</td><td>'+ res.rows[0].RoleName +'</td></tr>'+
            	'<tr><td>创建用户</td><td>'+ res.rows[0].Creater +'</td></tr>'+
            	'<tr><td>创建时间</td><td>'+ res.rows[0].CreateTime +'</td></tr>'+
            	'<tr><td>上次登录时间</td><td>'+ res.rows[0].LastLoginTime +'</td></tr></table>'
				bootbox.alert(html)
			},
			error:function (data) {
				bootbox.alert("请求失败")
            }
		})
	})

	//全屏
	$(".navHead-riht").on("click","[data-fullscreen]",function(){
		var SCREEN_FULL = 'glyphicon-fullscreen',
      		SCREEN_REST = 'glyphicon-resize-small',
      		iconElem = $(this).find("i");
      	if(iconElem.hasClass(SCREEN_FULL)){
        	var elem = document.body;
        	if(elem.webkitRequestFullScreen){ //谷歌
          		elem.webkitRequestFullScreen();
        	} else if(elem.mozRequestFullScreen) { //火狐
          		elem.mozRequestFullScreen();
        	} else if(elem.msRequestFullscreen) { //IE11
          		elem.msRequestFullscreen();
        	}
        	iconElem.addClass(SCREEN_REST).removeClass(SCREEN_FULL);
      	} else {
        	var elem = document;
        	if(elem.webkitCancelFullScreen){ //谷歌
          		elem.webkitCancelFullScreen();
        	} else if(elem.mozCancelFullScreen) { //火狐
          		elem.mozCancelFullScreen();
        	} else if(elem.cancelFullScreen) {
          		elem.cancelFullScreen();
        	} else if(elem.exitFullscreen) {
          		elem.exitFullscreen();
        	}else if(elem.msExitFullscreen) {  //ie
          		elem.msExitFullscreen();
        	}
        	iconElem.addClass(SCREEN_FULL).removeClass(SCREEN_REST);
      	}
	})

	//装选项卡内容的高度设置
	$(window).resize(function () {
		$(".layui-tab-content").css("height",$(document).innerHeight() - 104)
	}).resize();

	//左右折叠导航
	$(".sidebarMoveBtn").on('click',function(){
		if($(".sidebarRight").css("left") == "60px"){
			$(".sidebarRight").animate({left:"-226px"})
            $(".contentRight").animate({marginLeft:"60px"})
            $(".contentLeft").animate({width:"60px"})
			$(".sidebarMoveBtn").css({background:"#ffffff",color:"#07488E"})
			$(".sidebarMoveBtn").find("i").removeClass("glyphicon-menu-left").addClass("glyphicon-menu-right")
		}else{
            $(".sidebarRight").animate({left:"60px"})
            $(".contentRight").animate({marginLeft:"346px"})
            $(".contentLeft").animate({width:"346px"})
			$(".sidebarMoveBtn").css({background:"#07488E",color:"#ffffff"})
			$(".sidebarMoveBtn").find("i").removeClass("glyphicon-menu-right").addClass("glyphicon-menu-left")
		}
	})

	var $body = $('body')
	//iframe选项卡
	layui.use('element', function(){
		var $ = layui.jquery,
			layer = layui.layer;
			element = layui.element;
		//触发事件
		var tab = {
			tabAdd: function(title,url,id){
				element.tabAdd('xbs_tab', {
					title: title,
					content: '<iframe tab-id="' + id + '" frameborder="0" src="' + url + '" class="x-iframe"></iframe>',
					id: id
				})
			},
			closeThisTabs:function(){
				if(!$(".layui-this").hasClass("layadminHome")){
					$(".layui-this").find(".layui-tab-close").trigger('click');
				}
			},
			closeOtherTabs:function(){
				$("#LAY_app_tabsheader li").each(function(){
					if(!$(this).hasClass("layui-this")){
						if(!$(this).hasClass("layadminHome")){
							$(this).find(".layui-tab-close").trigger('click');
						}
					}
				})
			},
			closeAllTabs:function(){
				$("#LAY_app_tabsheader li").each(function(){
					if(!$(this).hasClass("layadminHome")){
						$(this).find(".layui-tab-close").trigger('click');
					}
				})
			},
			tabDelete: function(othis,id){
				//删除指定Tab项
				element.tabDelete('xbs_tab', id);
				othis.addClass('layui-btn-disabled');
			},
			tabChange: function(id){
				//切换到指定Tab项
				element.tabChange('xbs_tab', id);
			}
		};
		//点击事件
	  	$body.on('click', '*[layadmin-event]', function(){
			var othis = $(this),
				attrEvent = othis.attr('layadmin-event');
			tab[attrEvent] && tab[attrEvent].call(this, othis);
	  	});
		//导航菜单点击增加到tabs选项卡
		$('.sidebarRightNav').on('click',".site-tab", function(){
			$(this).addClass("site-tab-active").parent().siblings().find(".site-tab").removeClass("site-tab-active")
			var url = $(this).attr('lay-href');
			var title = $(this).find("span").html();
			var index = $(this).attr('lay-href');
			for (var i = 0; i < $('.x-iframe').length; i++) {
				if($('.x-iframe').eq(i).attr('tab-id') == index){
					tab.tabChange(index);
					event.stopPropagation();
					return;
				}
			 };
			tab.tabAdd(title, url, index);
			tab.tabChange(index);
		});
		//选项卡右侧导航栏效果
		$(".layadmin-tabs-select").on("mouseover",function () {
			$(this).find(".layui-nav-child").addClass("layui-show")
        })
		$(".layadmin-tabs-select .layui-nav-child").on("mouseout",function () {
			$(this).find(".layui-nav-child").removeClass("layui-show")
        })
	});
})
//设置和获取cookie
function setCookie(name,value,iDay){
	var oDate=new Date();
		oDate.setDate(oDate.getDate()+iDay);
	document.cookie=name+'='+value+';expires='+oDate;
}
function getCookie(key){
	console.log(document.cookie)
	var startIndex = document.cookie.indexOf(name); //开始索引
    if (startIndex > -1) {
            var tempStr = document.cookie.substring(startIndex, document.cookie.length);
        var endIndex = tempStr.indexOf(";")//结束索引：第一个分号 索引
        var item = tempStr.substring(0, endIndex);
        return item.split("=")[1];
    }
    return "";
}