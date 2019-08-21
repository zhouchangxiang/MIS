(function($){
    $.fn.tableRender = function(options){
        var defaluts = {
            tableName: '', //表名
            toolbar: '', //操作栏dom
            columns:[], //字段
            refreshDom:"", //搜索字段的dom
            fieldvalue: '', //搜索输入值
            Modal: '', //弹框dom
            ModalFieldStr: [], //弹框内录入的字段对象，field字段名，type字段输入类型，selectTableName下拉框数据表，selectField显示下拉框数据表的字段
            clickChildTableDom:"", //子表的dom
            clickChildTTableField:"", //搜索子表的字段
            clickParentTableDom:"", //根据父表搜索的表格dom
            clickParentTableField:"", //根据父表搜索的表的字段
        };
        var options = $.extend(defaluts, options);
        var $this = $(this)
        var singleSelect = false
        if(options.clickChildTableDom != ""){
            singleSelect = true
        }

        //搜索字段框渲染
        var columns = options.columns
        var resfreshFieldSelectOptions = ""
        $(options.toolbar).find(options.refreshDom).html("<option value=''>请选择列头搜索</option>")
        $.each(columns,function(i,value){
            if(columns[i].field){
                resfreshFieldSelectOptions += "<option value='"+ columns[i].field +"'>" + columns[i].title + "</option>";
            }
        })
        $(options.toolbar).find(options.refreshDom).append(resfreshFieldSelectOptions)
        $(options.toolbar).find(options.refreshDom).selectpicker("refresh")
        $(options.toolbar).find(options.refreshDom).selectpicker("render")
        $(options.toolbar).find(options.refreshDom).selectpicker("val", columns[0].title); //赋默认值
        //表格渲染
        $this.bootstrapTable({
            url: "http://127.0.0.1:5000/CUID",
            method: 'get',
            queryParams:function(params){
                return {
                    tableName: options.tableName,
                    field: $(options.toolbar).find(options.refreshDom).selectpicker("val"),
                    fieldvalue: $(options.toolbar).find(options.fieldvalue).val(),
                    limit : params.limit,
                    offset : parseInt(params.offset/params.limit)
                };
            },
            pagination: true,
            toolbar:options.toolbar,
            pageNumber:1,
            pageSize: 10,
            pageList: [10, 20, 30, 40, 50],
            sidePagination: "server",
            paginationLoop:false,
            singleSelect:singleSelect,
            clickToSelect:true,
            locale: "zh-CN",
            striped: true,
            showRefresh:true,
            columns: options.columns,
            responseHandler:function(res){
                res = JSON.parse(res)
                return res
            },
            onCheck:function(row, $element){
                if(options.clickChildTableDom != ""){
                    $(options.clickChildTableDom).bootstrapTable('refresh', {
                        query: {
                            field: options.clickChildTTableField,
                            fieldvalue: row[options.clickChildTTableField]
                        }
                    })
                }
            }
        })

        //搜索按钮
        $(options.toolbar).on("click","[data-search-btn]",function(){
            $this.bootstrapTable('refresh',{
                query:{
                    field: $(options.toolbar).find(options.refreshDom).selectpicker("val"),
                    fieldvalue: $(options.toolbar).find(options.fieldvalue).val()
                }
            });
        })
        //添加按钮
        $(options.toolbar).on("click","[data-add-btn]",function(){
            if(options.clickParentTableDom != ""){
                var ParentTableRows = $(options.clickParentTableDom).bootstrapTable("getAllSelections")
                if(ParentTableRows.length == 1){
                    $(options.Modal).modal('show')
                    $.each(options.ModalFieldStr,function(i,value){
                        var fieldstr = options.ModalFieldStr[i]
                        //判断输入框类型  为下拉框 则动态添加数据
                        if(fieldstr.type == "text"){
                            $(options.Modal).find("input[name="+ fieldstr.field +"]").val("");
                        }else if(fieldstr.type == "select"){
                            var selectField = fieldstr.selectField
                            if(fieldstr.selectUrl){ //有selectUrl就请求单独的路由获取数据
                                $.ajax({
                                    url:fieldstr.selectUrl,
                                    type:"get",
                                    data:{
                                        limit: 100000000,
                                        offset:0
                                    },
                                    success:function(res){
                                        res = JSON.parse(res)
                                        var selectOptions = ""
                                        $(options.Modal).find("#"+ fieldstr.field +"").html("")
                                        $.each(res.rows,function(i,value){
                                            selectOptions += "<option value='"+ res.rows[i][fieldstr.selectFieldID] +"'>" + res.rows[i][selectField] + "</option>";
                                        })
                                        $(options.Modal).find("#"+ fieldstr.field +"").append(selectOptions)
                                        $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("refresh")
                                        $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("render")
                                        if(fieldstr.selectDefault != ""){
                                            $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("val",fieldstr.selectDefault)
                                        }
                                    }
                                })
                            }else if(fieldstr.selectTableName){ //用selectTableName表名获取数据
                                $.ajax({
                                    url:"http://127.0.0.1:5000/CUID",
                                    type:"get",
                                    data:{
                                        tableName:fieldstr.selectTableName,
                                        limit: 100000000,
                                        offset:0
                                    },
                                    success:function(res){
                                        res = JSON.parse(res)
                                        var selectOptions = ""
                                        $(options.Modal).find("#"+ fieldstr.field +"").html("")
                                        $.each(res.rows,function(i,value){
                                            selectOptions += "<option value='"+ res.rows[i][fieldstr.selectFieldID] +"'>" + res.rows[i][selectField] + "</option>";
                                        })
                                        $(options.Modal).find("#"+ fieldstr.field +"").append(selectOptions)
                                        $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("refresh")
                                        $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("render")
                                        if(fieldstr.selectDefault != ""){
                                            $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("val",fieldstr.selectDefault)
                                        }
                                        if(fieldstr.selectLinkedFieldID){ //有selectLinkedFieldID属性就下拉时对其属性下拉框动态加载表字段
                                            //默认选中状态，给子下拉框添加数据
                                            var selectVal = $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("val")
                                            $.ajax({
                                                url:"http://127.0.0.1:5000/CUID",
                                                type:"get",
                                                data:{
                                                    tableName:"FieldSet",
                                                    field:"TableName",
                                                    fieldvalue:selectVal,
                                                    limit: 100000000,
                                                    offset:0
                                                },
                                                success:function(res) {
                                                    res = JSON.parse(res)
                                                    var linkSelectOptions = ""
                                                    $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").html("")
                                                    $.each(res.rows,function(i,value){
                                                        linkSelectOptions += "<option value='"+ res.rows[i][fieldstr.selectLinkedShowField] +"'>" + res.rows[i][fieldstr.selectLinkedShowField] + "</option>";
                                                    })
                                                    $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").append(linkSelectOptions)
                                                    $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("refresh")
                                                    $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("render")
                                                }
                                            })
                                            $(options.Modal).find("#"+ fieldstr.field +"").on("change",function(){
                                                selectVal = $(this).selectpicker("val")
                                                $.ajax({
                                                    url:"http://127.0.0.1:5000/CUID",
                                                    type:"get",
                                                    data:{
                                                        tableName:"FieldSet",
                                                        field:"TableName",
                                                        fieldvalue:selectVal,
                                                        limit: 100000000,
                                                        offset:0
                                                    },
                                                    success:function(res) {
                                                        res = JSON.parse(res)
                                                        var linkSelectOptions = ""
                                                        $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").html("")
                                                        $.each(res.rows,function(i,value){
                                                            linkSelectOptions += "<option value='"+ res.rows[i][fieldstr.selectLinkedShowField] +"'>" + res.rows[i][fieldstr.selectLinkedShowField] + "</option>";
                                                        })
                                                        $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").append(linkSelectOptions)
                                                        $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("refresh")
                                                        $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("render")
                                                    }
                                                })
                                            })
                                        }
                                    }
                                })
                            }
                        }
                    })
                }else{
                    bootbox.alert('请单选上级表格数据进行添加！');
                }
            }else{
                $(options.Modal).modal('show')
                $.each(options.ModalFieldStr,function(i,value){
                    var fieldstr = options.ModalFieldStr[i]
                    //判断输入框类型  为下拉框 则动态添加数据
                    if(fieldstr.type == "text"){
                        $(options.Modal).find("input[name="+ fieldstr.field +"]").val("");
                    }else if(fieldstr.type == "select"){
                        var selectField = fieldstr.selectField
                        if(fieldstr.selectUrl){ //有selectUrl就请求单独的路由获取数据
                            $.ajax({
                                url:fieldstr.selectUrl,
                                type:"get",
                                data:{
                                    limit: 100000000,
                                    offset:0
                                },
                                success:function(res){
                                    res = JSON.parse(res)
                                    var selectOptions = ""
                                    $(options.Modal).find("#"+ fieldstr.field +"").html("")
                                    $.each(res.rows,function(i,value){
                                        selectOptions += "<option value='"+ res.rows[i][fieldstr.selectFieldID] +"'>" + res.rows[i][selectField] + "</option>";
                                    })
                                    $(options.Modal).find("#"+ fieldstr.field +"").append(selectOptions)
                                    $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("refresh")
                                    $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("render")
                                    if(fieldstr.selectDefault != ""){
                                        $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("val",fieldstr.selectDefault)
                                    }
                                }
                            })
                        }else if(fieldstr.selectTableName){ //用selectTableName表名获取数据
                            $.ajax({
                                url:"http://127.0.0.1:5000/CUID",
                                type:"get",
                                data:{
                                    tableName:fieldstr.selectTableName,
                                    limit: 100000000,
                                    offset:0
                                },
                                success:function(res){
                                    res = JSON.parse(res)
                                    var selectOptions = ""
                                    $(options.Modal).find("#"+ fieldstr.field +"").html("")
                                    $.each(res.rows,function(i,value){
                                        selectOptions += "<option value='"+ res.rows[i][fieldstr.selectFieldID] +"'>" + res.rows[i][selectField] + "</option>";
                                    })
                                    $(options.Modal).find("#"+ fieldstr.field +"").append(selectOptions)
                                    $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("refresh")
                                    $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("render")
                                    if(fieldstr.selectDefault != ""){
                                        $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("val",fieldstr.selectDefault)
                                    }
                                    if(fieldstr.selectLinkedFieldID){ //有selectLinkedFieldID属性就下拉时对其属性下拉框动态加载表字段
                                        //默认选中状态，给子下拉框添加数据
                                        var selectVal = $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("val")
                                        $.ajax({
                                            url:"http://127.0.0.1:5000/CUID",
                                            type:"get",
                                            data:{
                                                tableName:"FieldSet",
                                                field:"TableName",
                                                fieldvalue:selectVal,
                                                limit: 100000000,
                                                offset:0
                                            },
                                            success:function(res) {
                                                res = JSON.parse(res)
                                                var linkSelectOptions = ""
                                                $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").html("")
                                                $.each(res.rows,function(i,value){
                                                    linkSelectOptions += "<option value='"+ res.rows[i][fieldstr.selectLinkedShowField] +"'>" + res.rows[i][fieldstr.selectLinkedShowField] + "</option>";
                                                })
                                                $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").append(linkSelectOptions)
                                                $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("refresh")
                                                $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("render")
                                            }
                                        })
                                        $(options.Modal).find("#"+ fieldstr.field +"").on("change",function(){
                                            selectVal = $(this).selectpicker("val")
                                            $.ajax({
                                                url:"http://127.0.0.1:5000/CUID",
                                                type:"get",
                                                data:{
                                                    tableName:"FieldSet",
                                                    field:"TableName",
                                                    fieldvalue:selectVal,
                                                    limit: 100000000,
                                                    offset:0
                                                },
                                                success:function(res) {
                                                    res = JSON.parse(res)
                                                    var linkSelectOptions = ""
                                                    $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").html("")
                                                    $.each(res.rows,function(i,value){
                                                        linkSelectOptions += "<option value='"+ res.rows[i][fieldstr.selectLinkedShowField] +"'>" + res.rows[i][fieldstr.selectLinkedShowField] + "</option>";
                                                    })
                                                    $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").append(linkSelectOptions)
                                                    $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("refresh")
                                                    $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("render")
                                                }
                                            })
                                        })
                                    }
                                }
                            })
                        }
                    }
                })
            }
        })
        //修改按钮
        $(options.toolbar).on("click","[data-updata-btn]",function(){
            //判断是否有上级表格关联
            if(options.clickParentTableDom != "") {
                var ParentTableRows = $(options.clickParentTableDom).bootstrapTable("getAllSelections")
                if(ParentTableRows.length == 1){
                    var rows = $this.bootstrapTable('getAllSelections');
                    if (rows.length == 1) {
                        if (rows) {
                            $(options.Modal).modal('show')
                            $.each(options.ModalFieldStr, function (i, value) {
                                var fieldstr = options.ModalFieldStr[i]
                                if (fieldstr.type == "text") {
                                    $(options.Modal).find("input[name=" + fieldstr.field + "]").val(rows[0][fieldstr.field]);
                                } else if (fieldstr.type == "select") {
                                    var selectField = fieldstr.selectField
                                    if(fieldstr.selectUrl) {
                                        $.ajax({
                                            url:fieldstr.selectUrl,
                                            type: "get",
                                            data: {
                                                limit: 100000000,
                                                offset: 0
                                            },
                                            success: function (res) {
                                                res = JSON.parse(res)
                                                var selectOptions = ""
                                                $(options.Modal).find("#" + fieldstr.field + "").html("")
                                                $.each(res.rows, function (i, value) {
                                                    selectOptions += "<option value='" + res.rows[i][fieldstr.selectFieldID] + "'>" + res.rows[i][selectField] + "</option>";
                                                })
                                                $(options.Modal).find("#" + fieldstr.field + "").append(selectOptions)
                                                $(options.Modal).find("#" + fieldstr.field + "").selectpicker("refresh")
                                                $(options.Modal).find("#" + fieldstr.field + "").selectpicker("render")
                                                $(options.Modal).find("#" + fieldstr.field + "").selectpicker('val', rows[0][fieldstr.field])
                                            }
                                        })
                                    }else if(fieldstr.selectTableName){
                                        $.ajax({
                                            url: "http://127.0.0.1:5000/CUID",
                                            type: "get",
                                            data: {
                                                tableName: fieldstr.selectTableName,
                                                limit: 100000000,
                                                offset: 0
                                            },
                                            success: function (res) {
                                                res = JSON.parse(res)
                                                var selectOptions = ""
                                                $(options.Modal).find("#" + fieldstr.field + "").html("")
                                                $.each(res.rows, function (i, value) {
                                                    selectOptions += "<option value='" + res.rows[i][fieldstr.selectFieldID] + "'>" + res.rows[i][selectField] + "</option>";
                                                })
                                                $(options.Modal).find("#" + fieldstr.field + "").append(selectOptions)
                                                $(options.Modal).find("#" + fieldstr.field + "").selectpicker("refresh")
                                                $(options.Modal).find("#" + fieldstr.field + "").selectpicker("render")
                                                $(options.Modal).find("#" + fieldstr.field + "").selectpicker('val', rows[0][fieldstr.field])
                                                if(fieldstr.selectLinkedFieldID){ //有selectLinkedFieldID属性就下拉时对其属性下拉框动态加载表字段
                                                    //默认选中状态，给子下拉框添加数据
                                                    var selectVal = $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("val")
                                                    $.ajax({
                                                        url:"http://127.0.0.1:5000/CUID",
                                                        type:"get",
                                                        data:{
                                                            tableName:"FieldSet",
                                                            field:"TableName",
                                                            fieldvalue:selectVal,
                                                            limit: 100000000,
                                                            offset:0
                                                        },
                                                        success:function(res) {
                                                            res = JSON.parse(res)
                                                            var linkSelectOptions = ""
                                                            $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").html("")
                                                            $.each(res.rows,function(i,value){
                                                                linkSelectOptions += "<option value='"+ res.rows[i][fieldstr.selectLinkedShowField] +"'>" + res.rows[i][fieldstr.selectLinkedShowField] + "</option>";
                                                            })
                                                            $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").append(linkSelectOptions)
                                                            $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("refresh")
                                                            $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("render")
                                                            $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID + "").selectpicker('val', rows[0][fieldstr.selectLinkedFieldID])
                                                        }
                                                    })
                                                    $(options.Modal).find("#"+ fieldstr.field +"").on("change",function(){
                                                        selectVal = $(this).selectpicker("val")
                                                        $.ajax({
                                                            url:"http://127.0.0.1:5000/CUID",
                                                            type:"get",
                                                            data:{
                                                                tableName:"FieldSet",
                                                                field:"TableName",
                                                                fieldvalue:selectVal,
                                                                limit: 100000000,
                                                                offset:0
                                                            },
                                                            success:function(res) {
                                                                res = JSON.parse(res)
                                                                var linkSelectOptions = ""
                                                                $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").html("")
                                                                $.each(res.rows,function(i,value){
                                                                    linkSelectOptions += "<option value='"+ res.rows[i][fieldstr.selectLinkedShowField] +"'>" + res.rows[i][fieldstr.selectLinkedShowField] + "</option>";
                                                                })
                                                                $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").append(linkSelectOptions)
                                                                $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("refresh")
                                                                $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("render")
                                                            }
                                                        })
                                                    })
                                                }
                                            }
                                        })
                                    }
                                }
                            })
                        }
                    } else {
                        bootbox.alert('请单选一条数据进行编辑！');
                    }
                }else{
                    bootbox.alert('请单选上级表格数据进行编辑！');
                }
            }else{
                var rows = $this.bootstrapTable('getAllSelections');
                if (rows.length == 1) {
                    if (rows) {
                        $(options.Modal).modal('show')
                        $.each(options.ModalFieldStr, function (i, value) {
                            var fieldstr = options.ModalFieldStr[i]
                            if (fieldstr.type == "text") {
                                $(options.Modal).find("input[name=" + fieldstr.field + "]").val(rows[0][fieldstr.field]);
                            } else if (fieldstr.type == "select") {
                                var selectField = fieldstr.selectField
                                if(fieldstr.selectUrl) {
                                    $.ajax({
                                        url:fieldstr.selectUrl,
                                        type: "get",
                                        data: {
                                            limit: 100000000,
                                            offset: 0
                                        },
                                        success: function (res) {
                                            res = JSON.parse(res)
                                            var selectOptions = ""
                                            $(options.Modal).find("#" + fieldstr.field + "").html("")
                                            $.each(res.rows, function (i, value) {
                                                selectOptions += "<option value='" + res.rows[i][fieldstr.selectFieldID] + "'>" + res.rows[i][selectField] + "</option>";
                                            })
                                            $(options.Modal).find("#" + fieldstr.field + "").append(selectOptions)
                                            $(options.Modal).find("#" + fieldstr.field + "").selectpicker("refresh")
                                            $(options.Modal).find("#" + fieldstr.field + "").selectpicker("render")
                                            $(options.Modal).find("#" + fieldstr.field + "").selectpicker('val', rows[0][fieldstr.field])
                                        }
                                    })
                                }else if(fieldstr.selectTableName){
                                    $.ajax({
                                        url: "http://127.0.0.1:5000/CUID",
                                        type: "get",
                                        data: {
                                            tableName: fieldstr.selectTableName,
                                            limit: 100000000,
                                            offset: 0
                                        },
                                        success: function (res) {
                                            res = JSON.parse(res)
                                            var selectOptions = ""
                                            $(options.Modal).find("#" + fieldstr.field + "").html("")
                                            $.each(res.rows, function (i, value) {
                                                selectOptions += "<option value='" + res.rows[i][fieldstr.selectFieldID] + "'>" + res.rows[i][selectField] + "</option>";
                                            })
                                            $(options.Modal).find("#" + fieldstr.field + "").append(selectOptions)
                                            $(options.Modal).find("#" + fieldstr.field + "").selectpicker("refresh")
                                            $(options.Modal).find("#" + fieldstr.field + "").selectpicker("render")
                                            $(options.Modal).find("#" + fieldstr.field + "").selectpicker('val', rows[0][fieldstr.field])
                                            if(fieldstr.selectLinkedFieldID){ //有selectLinkedFieldID属性就下拉时对其属性下拉框动态加载表字段
                                                //默认选中状态，给子下拉框添加数据
                                                var selectVal = $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("val")
                                                $.ajax({
                                                    url:"http://127.0.0.1:5000/CUID",
                                                    type:"get",
                                                    data:{
                                                        tableName:"FieldSet",
                                                        field:"TableName",
                                                        fieldvalue:selectVal,
                                                        limit: 100000000,
                                                        offset:0
                                                    },
                                                    success:function(res) {
                                                        res = JSON.parse(res)
                                                        var linkSelectOptions = ""
                                                        $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").html("")
                                                        $.each(res.rows,function(i,value){
                                                            linkSelectOptions += "<option value='"+ res.rows[i][fieldstr.selectLinkedShowField] +"'>" + res.rows[i][fieldstr.selectLinkedShowField] + "</option>";
                                                        })
                                                        $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").append(linkSelectOptions)
                                                        $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("refresh")
                                                        $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("render")
                                                        $(options.Modal).find("#" + fieldstr.selectLinkedFieldID + "").selectpicker('val', rows[0][fieldstr.selectLinkedFieldID])
                                                    }
                                                })
                                                $(options.Modal).find("#"+ fieldstr.field +"").on("change",function(){
                                                    selectVal = $(this).selectpicker("val")
                                                    $.ajax({
                                                        url:"http://127.0.0.1:5000/CUID",
                                                        type:"get",
                                                        data:{
                                                            tableName:"FieldSet",
                                                            field:"TableName",
                                                            fieldvalue:selectVal,
                                                            limit: 100000000,
                                                            offset:0
                                                        },
                                                        success:function(res) {
                                                            res = JSON.parse(res)
                                                            var linkSelectOptions = ""
                                                            $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").html("")
                                                            $.each(res.rows,function(i,value){
                                                                linkSelectOptions += "<option value='"+ res.rows[i][fieldstr.selectLinkedShowField] +"'>" + res.rows[i][fieldstr.selectLinkedShowField] + "</option>";
                                                            })
                                                            $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").append(linkSelectOptions)
                                                            $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("refresh")
                                                            $(options.Modal).find("#"+ fieldstr.selectLinkedFieldID +"").selectpicker("render")
                                                        }
                                                    })
                                                })
                                            }
                                        }
                                    })
                                }
                            }
                        })
                    }
                } else {
                    bootbox.alert('请单选一条数据进行编辑！');
                }
            }
        })
        //删除按钮
        $(options.toolbar).on("click","[data-delete-btn]",function(){
            var rows = $this.bootstrapTable('getAllSelections');
            if (rows.length > 0) {
                var jsonarray=[];
                bootbox.confirm({
                    message: "您确认要删除所选的记录吗？",
                    buttons: {
                        confirm: {
                            label: '删除',
                            className: 'btn-success'
                        },
                        cancel: {
                            label: '返回',
                            className: 'btn-danger'
                        }
                    },
                    callback: function (result) {
                        if(result){
                            for (var i = 0; i < rows.length; i++) {
                                var obj=createKeyIDObj(parseInt(rows[i].ID));
                                jsonarray.push(obj);
                            }
                            var a = JSON.stringify(jsonarray);
                            $.ajax({
                                url: 'http://127.0.0.1:5000/CUID',
                                method: 'DELETE',
                                data: {
                                    tableName: options.tableName,
                                    delete_data:a
                                },
                                success: function (data) {
                                    if(data == "OK"){
                                        var dialog = bootbox.dialog({
                                            message: '<p class="text-center mb-0"><i class="fa fa-spin fa-cog"></i>操作成功！</p>',
                                            closeButton: false
                                        });
                                        dialog.init(function(){
                                            setTimeout(function(){
                                                dialog.modal('hide');
                                            }, 2000);
                                        });
                                        $this.bootstrapTable('refresh');
                                    }
                                }
                            });
                        }
                    }
                });
            } else {
                bootbox.alert('请选择要删除的记录')
            }
        })
        //保存按钮
        $(options.Modal).on("click","[data-save-btn]",function(){
            var idVal = $(options.Modal).find("input[name=ID]").val();
            var requestType = ""
            if (idVal.length >= 1){
                requestType = "put"
            }else {
                requestType = "post"
            }
            var requestData = {} //请求参数的对象  获取表单内容
            requestData.tableName = options.tableName
            $.each(options.ModalFieldStr,function(i,value){
                var fieldstr = options.ModalFieldStr[i]
                if(fieldstr.type == "text"){
                    requestData[fieldstr.field] = $(options.Modal).find("input[name="+ fieldstr.field +"]").val();
                }else if(fieldstr.type == "select"){
                    requestData[fieldstr.field] = $(options.Modal).find("#"+ fieldstr.field +"").selectpicker("val");
                }
            })
            //判断是否有主表关联，有的话就额外传参
            if(options.clickParentTableDom != ""){
                var clickParentTableValue = $(options.clickParentTableDom).bootstrapTable("getAllSelections")
                requestData[options.clickParentTableField] = clickParentTableValue[0][options.clickParentTableField]
            }
            $.ajax({
                url:"http://127.0.0.1:5000/CUID",
                type:requestType,
                data:requestData,
                success:function(data){
                    if(data == "OK"){
                        $(options.Modal).modal('hide')
                        var dialog = bootbox.dialog({
                            message: '<p class="text-center mb-0"><i class="fa fa-spin fa-cog"></i>操作成功！</p>',
                            closeButton: false
                        });
                        dialog.init(function(){
                            setTimeout(function(){
                                dialog.modal('hide');
                            }, 2000);
                        });
                        $this.bootstrapTable('refresh');
                    } else {
                        bootbox.alert(data)
                    }
                },
                error: function(data){
                   console.log(data.responseText)
                   bootbox.alert('请求失败')
                },
            })
        })
    }
})(jQuery)
//封装id
function createKeyIDObj(keyID){
    return {
        id:keyID
    }
}