$(function () {
	//右上角用户信息
	$(".navUser").mouseover(function() {
		$(this).find(".navUserPanel").css("display", "block")
	}).mouseout(function (){
		$(this).find(".navUserPanel").css("display","none")
	})

    //点击主菜单加阴影效果
    $(".mainnav li a").on("click",function(){
        $(this).addClass("rootMenu").parent().siblings().find("a").removeClass("rootMenu")
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

	//装选项卡内容的高度设置
	$(window).resize(function () {
		$(".layui-tab-content").css("height",$(document).innerHeight() - 108)
	}).resize();

	//左右折叠导航
	$(".sideheadListBtn").on('click',function(){
		if($(".submenu").css("marginLeft") == "0px"){
			$(".submenu").animate({marginLeft:"-83%"})
            $(".contentRight").animate({marginLeft:"-16.6%",width:"96.6%"})
		}else{
            $(".submenu").animate({marginLeft:"0"})
            $(".contentRight").animate({marginLeft:"0",width:"80%"})
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
			//新增一个Tab项
			tabAdd: function(title,url,id){
				element.tabAdd('xbs_tab', {
					title: title,
					content: '<iframe tab-id="' + id + '" frameborder="0" src="' + url + '" class="x-iframe"></iframe>',
					id: id
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
		$('.site-tab-active').on('click', function(){
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