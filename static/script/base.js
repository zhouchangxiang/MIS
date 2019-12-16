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
//highchart柱状图表渲染方法
function highchartsRender(id,xAxisArray,seriesData,unit){
    Highcharts.chart(id,{
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
        tooltip: {
            valueSuffix: " "+unit
        },
        yAxis: {
            title: {
                text: ''
            }
        },
        series:seriesData
    });
}

//highchart 实时数据趋势图 无x y轴线
function highchartsRealTimeNoTickRender(url,id,yKey,domID,totalKey,totalDom){
    var ws = new WebSocket(url);
    ws.onopen = function(){
        ws.send("");
        console.log("数据发送中...");
    };
    ws.onclose = function(){
        console.log("连接已关闭...");
    };
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    var chart = Highcharts.chart(id, {
        chart: {
            type: 'spline',
            marginRight: 10,
            backgroundColor:'#EFF5FB',
            events: {
                load: function () {
                    var series = this.series[0],
                        chart = this;
                    ws.onmessage = function (evt){
                        var received_msg = evt.data;
                        received_msg = JSON.parse(received_msg)
                        var x = new Date(received_msg.currentTime).getTime(),   // 返回时间
                            y = Math.floor(received_msg[yKey] * 100) / 100;       // 返回值
                        series.addPoint([x, y], true, true);
                        $("#"+ domID).html(y)
                        $("#"+ domID).siblings(".unit").html(received_msg.unit)
                        $("#"+ totalDom).html((parseInt(received_msg[totalKey] * 100 ) / 100 ).toFixed(2))
                        $("#"+ totalDom).siblings(".unit").html(received_msg.unit)
                    };
                }
            }
        },
        colors:["#8A8F97"],
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
            name: '实时数据',
            data: (function () {
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
                },
                colors:["#ffffff"],
            });
        }
    },function(){
        if($(this).find(".highcharts-item").attr("id") == id){
            chart.update({
                chart:{
                    backgroundColor:'#EFF5FB'
                },
                colors:["#8A8F97"],
            });
        }
    })
}

//highchart历史数据折线图渲染方法
function highchartsEnergyHistoryRender(id,seriesData,Unit){
    Highcharts.chart(id,{
        chart: {
            zoomType: 'x'
        },
        title: {
            text: null
        },
        credits: {
            enabled: false//不显示LOGO
        },
        plotOptions: {
			series: {
				showInLegend: true
			}
		},
        xAxis:{
            type: 'datetime',
            dateTimeLabelFormats: {
                millisecond: '%H:%M:%S.%L',
                second: '%H:%M:%S',
                minute: '%H:%M',
                hour: '%H:%M',
                day: '%m-%d',
                week: '%m-%d',
                month: '%Y-%m',
                year: '%Y'
            }
        },
        yAxis:{
            title: {
                text: ''
            },
        },
        tooltip: {
            valueSuffix: Unit,
            formatter: function () {
                return myTimeformatter(new Date(this.x)) + "<br>" + this.series.name + ":" + this.y + Unit
            }
		},
        series:seriesData
    });
}
//highchart区域排名柱状图渲染方法
function highchartsAreaBarRender(id,xAxisArray,seriesData,Unit){
    Highcharts.chart(id,{
        chart: {
            type: 'bar'
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
        tooltip: {
            valueSuffix: Unit
        },
        series:seriesData
    });
}

//highchart成本饼图
function highchartsPieRender(id,data){
    var chart = Highcharts.chart(id, {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            backgroundColor:'#EFF5FB',
            type: 'pie'
        },
        credits: {
            enabled: false//不显示LOGO
        },
        title: {
            text: null
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            name: '总成本',
		    colorByPoint: true,
            data:data
        }]
    });
    $(".costPieChart").hover(function(){
        chart.update({
            chart:{
                backgroundColor:'#07488E'
            }
        });
    },function(){
        chart.update({
            chart:{
                backgroundColor:'#EFF5FB'
            }
        });
    })
}
