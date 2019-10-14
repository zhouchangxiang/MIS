//监听div大小变化
(function($, h, c) {
   var a = $([]),
   e = $.resize = $.extend($.resize, {}),
   i,
   k = "setTimeout",
   j = "resize",
   d = j + "-special-event",
   b = "delay",
   f = "throttleWindow";
   e[b] = 250;
   e[f] = true;
   $.event.special[j] = {
      setup: function() {
         if (!e[f] && this[k]) {
            return false;
         }
         var l = $(this);
         a = a.add(l);
         $.data(this, d, {
            w: l.width(),
            h: l.height()
         });
         if (a.length === 1) {
            g();
         }
      },
      teardown: function() {
         if (!e[f] && this[k]) {
            return false;
         }
         var l = $(this);
         a = a.not(l);
         l.removeData(d);
         if (!a.length) {
            clearTimeout(i);
         }
      },
      add: function(l) {
         if (!e[f] && this[k]) {
            return false;
         }
         var n;
         function m(s, o, p) {
            var q = $(this),
            r = $.data(this, d);
            r.w = o !== c ? o: q.width();
            r.h = p !== c ? p: q.height();
            n.apply(this, arguments);
         }
         if ($.isFunction(l)) {
            n = l;
            return m;
         } else {
            n = l.handler;
            l.handler = m;
         }
      }
   };
   function g() {
      i = h[k](function() {
         a.each(function() {
            var n = $(this),
            m = n.width(),
            l = n.height(),
            o = $.data(this, d);
            if (m !== o.w || l !== o.h) {
               n.trigger(j, [o.w = m, o.h = l]);
            }
         });
         g();
      },
      e[b]);
   }
})(jQuery, this);
//根据key匹配id  加入数据
function adddata(ids,res){
    $("#" + ids).html(res)
}
//根据key匹配id,加入数据到表单
function addInputData(ids,res){
    $("#" + ids).val(res)
    $(".FilterCheckbox").each(function(){
        if($(this).val() == 'false'){
            $(this).prop("checked",false)
        }else if($(this).val() == 'true'){
            $(this).prop("checked",true)
        }
    })
}
//获取页面传参
function getUrlParam(name) {
  var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
  var r = decodeURI(window.location.search).substr(1).match(reg); //匹配目标参数
  if (r != null) return unescape(r[2]); return null; //返回参数值
}
//时间格式转换
function Appendzero(obj){
    if(obj < 10){
        return "0" + obj
    }else{
        return obj
    }
}
function myYearformatter(date){
    var y = date.getFullYear();
    var m = date.getMonth()+1;
    var d = date.getDate();
    var h = date.getHours()
    var minutes = date.getMinutes()
    var s = date.getSeconds()
    return Appendzero(y);
}
function myMonthformatter(date){
    var y = date.getFullYear();
    var m = date.getMonth()+1;
    var d = date.getDate();
    var h = date.getHours()
    var minutes = date.getMinutes()
    var s = date.getSeconds()
    return Appendzero(y) + '-' + Appendzero(m);
}
function myDayformatter(date){
    var y = date.getFullYear();
    var m = date.getMonth()+1;
    var d = date.getDate();
    var h = date.getHours()
    var minutes = date.getMinutes()
    var s = date.getSeconds()
    return Appendzero(y) + '-' + Appendzero(m) + '-' + Appendzero(d);
}
function myformatter(date){
    var y = date.getFullYear();
    var m = date.getMonth()+1;
    var d = date.getDate();
    var h = date.getHours()
    var minutes = date.getMinutes()
    var s = date.getSeconds()
    return Appendzero(y) + '-' + Appendzero(m) + '-' + Appendzero(d) + ' ' + Appendzero(h) + ':' + Appendzero(minutes);
}
function myTimeformatter(date){
    var y = date.getFullYear();
    var m = date.getMonth()+1;
    var d = date.getDate();
    var h = date.getHours()
    var minutes = date.getMinutes()
    var s = date.getSeconds()
    return Appendzero(y) + '-' + Appendzero(m) + '-' + Appendzero(d) + ' ' + Appendzero(h) + ':' + Appendzero(minutes) + ':' + Appendzero(s);
}
//封装id
function createKeyIDObj(keyID){
    return {
        id:keyID
    }
}
//鼠标拖拽滚动
window.addEventListener("load", function() {
    var addEventListener = 'addEventListener';
    var elems = document.getElementsByClassName('dragscroll');
    for (var i = 0; i < elems.length;) {
        (function(elem, lastClientX, lastClientY, pushed) {
            elem[addEventListener]('mousedown', function(e) {
                pushed = 1;
                lastClientX = e.clientX;
                lastClientY = e.clientY;
                e.preventDefault();
                e.stopPropagation();
            }, 0);
            window[addEventListener]('mousemove', function(e) {
                if (pushed) {
                    elem.scrollLeft -=
                        (- lastClientX + (lastClientX=e.clientX));
                    elem.scrollTop -=
                        (- lastClientY + (lastClientY=e.clientY));
                }
            }, 0);
            window[addEventListener]('mouseup', function(){
                pushed = 0;
            }, 0);

         })(elems[i++]);
    }
}, 0);
// 数字滚动效果
function Digit(a) {
    function b(a, b) {
        var f, g, c = d(b),
            e = c.toString().length;
        for (f = 0; e > f; f++) g = document.createElement("div"), g.className = "," != c[f] && "." != c[f] ? "to__led-number" : "to__led-number to__led-number--no", g.innerHTML = c[f], a.appendChild(g)
    }

    function c(a, b, c) {
        function i() {
            return 9 == h ? h = 0 : h++, h
        }
        var e, f, g, h, j, k, d = a.childNodes.length - 1;
        for (e = 0; e < a.childNodes.length; e++) f = {}, f = "left" == c ? a.childNodes[e] : a.childNodes[d], g = f.innerHTML, h = 0, f.innerHTML = "", "," != g && "." != g && (b.timerTemp += b.single), j = .5 * b.timerTemp / b.speed, k = b.timerTemp - j, ! function(a, b) {
            setTimeout(function() {
                if (a.innerHTML = b, "," != b && "." != b) {
                    a.innerHTML = b;
                    var c = setInterval(function() {
                        a.innerHTML = i()
                    }, 50);
                    setTimeout(function() {
                        clearInterval(c), a.innerHTML = b
                    }, 1e3 * k)
                } else a.innerHTML = b
            }, 1e3 * j)
        }(f, g), d--
    }

    function d(a) {
        var c, d, f, g, h;
        for (a = a.toString(), c = a.split("."), d = c[0], f = "." + c[1], g = d, h = 1; h <= Math.floor((d.length - 1) / 3); h++)
            //g = e(g, d.length - 3 * h, ",");
        return c[1] && (g += f), g
    }

    function e(a, b, c) {
        return a.slice(0, b) + c + a.slice(b)
    }
    Digit.prototype.render = function() {
        var d = a.direction,
            e = a.finish,
            f = a.speed,
            g = a.number.toString().replace(".", "").length - 1,
            h = Number((e / g).toFixed(2)),
            i = {
                number: g,
                single: h,
                speed: f,
                timerTemp: 0
            };
        i.timerTemp -= i.single, b(a.dom, a.number), c(a.dom, i, d)
    }
}
//highchart全局配置
function HighchartsGlobalSettings(){
    Highcharts.setOptions({
        lang:{
           contextButtonTitle:"图表导出菜单",
           decimalPoint:".",
           downloadJPEG:"下载JPEG图片",
           downloadPDF:"下载PDF文件",
           downloadPNG:"下载PNG文件",
           downloadSVG:"下载SVG文件",
           drillUpText:"返回 {series.name}",
           loading:"加载中",
           months:["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"],
           noData:"没有数据",
           numericSymbols: [ "千" , "兆" , "G" , "T" , "P" , "E"],
           printChart:"打印图表",
           resetZoom:"恢复缩放",
           resetZoomTitle:"恢复图表",
           shortMonths: [ "Jan" , "Feb" , "Mar" , "Apr" , "May" , "Jun" , "Jul" , "Aug" , "Sep" , "Oct" , "Nov" , "Dec"],
           thousandsSep:",",
           weekdays: ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六","星期天"]
        }
    });
}
//highchart静态图表渲染方法
function highchartsRender(id,xAxisArray,seriesData){
    var chart = Highcharts.chart(id,{
        chart: {
            type: 'column'
        },
        title: {
            text: null
        },
        credits: {
            enabled: false//不显示LOGO
        },
        legend: {
			enabled: false //不显示图例
		},
        xAxis: {
            categories: xAxisArray
        },
        yAxis: {
            title: {
                text: ''
            }
        },
        series:seriesData
    });
}
//highchart实时数据 激活最后一个点的提示框
function activeLastPointToolip(chart) {
    var points = chart.series[0].points;
    chart.tooltip.refresh(points[points.length -1]);
}
//highchart 实时数据趋势图
function highchartsRealTimeRender(url,id,xData,yData){
    var ws = new WebSocket(url);
    websocket()
    function websocket(){
        ws.onopen = function(){
            ws.send("hello");
            console.log("数据发送中...");
        };
        ws.onclose = function(){
            console.log("连接已关闭...");
        };
    }
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    var chart = Highcharts.chart(id, {
        chart: {
            type: 'spline',
            marginRight: 10,
            events: {
                load: function () {
                    var series = this.series[0],
                        chart = this;
                    activeLastPointToolip(chart);
                    ws.onmessage = function (evt){
                        var received_msg = evt.data;
                        received_msg = JSON.parse(received_msg)
                        var x = new Date(received_msg[xData]).getTime(),   // 返回时间
                            y = received_msg[yData];       // 返回值
                        series.addPoint([x, y], true, true);
                        activeLastPointToolip(chart);
                    };
                }
            }
        },
        title: {
            text: null
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: null
            }
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                    Highcharts.numberFormat(this.y, 2);
            }
        },
        credits: {
            enabled: false//不显示LOGO
        },
        legend: {
            enabled: false //不显示图例
        },
        series: [{
            name: '随机数据',
            data: (function () {
                // 生成随机值
                var data = [],
                    i;
                for (i = -19; i <= 0; i += 1) {
                    data.push({
                        x: null,
                        y: 0
                    });
                }
                return data;
            }())
        }]
    });
}
//highchart 实时数据趋势图 无x y轴线
function highchartsRealTimeNoTickRender(url,id,xData,yData,domID){
    var ws = new WebSocket(url);
    websocket()
    function websocket(){
        ws.onopen = function(){
            ws.send("hello");
            console.log("数据发送中...");
        };
        ws.onclose = function(){
            console.log("连接已关闭...");
        };
    }
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    var chart = Highcharts.chart(id, {
        chart: {
            type: 'spline',
            marginRight: 10,
            backgroundColor:'#8A8F97',
            events: {
                load: function () {
                    var series = this.series[0],
                        chart = this;
                    ws.onmessage = function (evt){
                        var received_msg = evt.data;
                        received_msg = JSON.parse(received_msg)
                        var x = new Date(received_msg[xData]).getTime(),   // 返回时间
                            y = received_msg[yData];       // 返回值
                        series.addPoint([x, y], true, true);
                        $("#"+ domID).html(y)
                    };
                }
            }
        },
        colors:["#ffffff"],
        title: {
            text: null
        },
        xAxis: {
            lineWidth :0,//去掉x轴线
            tickWidth:0,//去掉刻度
            labels: {
                enabled: false
            },//去掉刻度数字
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            tickWidth:0,//去掉刻度
            gridLineWidth: 0,//去掉y轴方向的横线
            labels: {
                enabled: false
            },//去掉刻度数字
            title: {
                text: null
            }
        },
        credits: {
            enabled: false//不显示LOGO
        },
        legend: {
            enabled: false //不显示图例
        },
        plotOptions: {
            series: {
                marker: {
                    enabled: false  //关闭数据点
                }
            }
        },
        series: [{
            name: '随机数据',
            data: (function () {
                // 生成随机值
                var data = [],
                    i;
                for (i = -19; i <= 0; i += 1) {
                    data.push({
                        x: null,
                        y: 0
                    });
                }
                return data;
            }())
        }]
    });
    $(".trendsChartItem").hover(function(){
        if($(this).find(".highcharts-item").attr("id") == id){
            chart.update({
                chart:{
                      backgroundColor:'#07488E'
                }
            });
        }
    },function(){
        if($(this).find(".highcharts-item").attr("id") == id){
            chart.update({
                chart:{
                      backgroundColor:'#8A8F97'
                }
            });
        }
    })
}