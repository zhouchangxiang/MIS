(function($){
    $.fn.tableRender = function(options){
        var $this = $(this)
        var defaluts = {
            tableName: '', //表名
            parentTableID: '', //父表ID
            parentTableLinkField: '', //父表关联的字段
        };
        options = $.extend(defaluts, options);
        var ModalID = "#" + options.tableName + "Modal" //弹框dom
        var toolbarID = "#" + options.tableName + "toolbar" //操作栏dom
        var FieldSetSearchID = "#" + options.tableName + "FieldSetSearchDom" //搜索字段的dom
        var columns = [] //表头对象
        var SingleSelect = false //默认复选，true时表格单选
        var toolbar = "" //表格操作栏dom
        var addbtn = "" //添加按钮dom
        var updatabtn = "" //修改按钮dom
        var deletebtn = "" //删除按钮dom
        //在配置数据表中或者tableName这条数据
        $.ajax({
            url: "http://127.0.0.1:5000/CUID",
            type: "get",
            async: false,
            data: {
                tableName: "CreateTableSet",
                field: "TableName",
                fieldvalue: options.tableName,
                limit: 100000000,
                offset: 0
            },
            success: function (data) {
                data = JSON.parse(data)
                if(data.rows == []){
                    //是否在第一列显示复选框
                    if(data.rows[0].ISFirstCheckBox == "True"){
                        columns = [{checkbox: true}]
                        //是否单选
                        if(data.rows[0].SingleSelect == "True"){
                            SingleSelect = true
                        }else if(data.rows[0].SingleSelect == "False"){
                            SingleSelect = false
                        }
                    }else if(data.rows[0].ISFirstCheckBox == "False"){
                        columns = [{checkbox: false}]
                    }
                    if(data.rows[0].IsAdd == "True"){
                        addbtn = '<button type="button" class="btn btn-info" data-add-btn>添加</button>'
                    }
                    if(data.rows[0].IsUpdate == "True"){
                        updatabtn = '<button type="button" class="btn btn-warning" data-updata-btn>编辑</button>'
                    }
                    if(data.rows[0].IsDelete == "True"){
                        deletebtn = '<button type="button" class="btn btn-danger" data-delete-btn>删除</button>'
                    }
                    toolbar = '<div id="'+ options.tableName + "toolbar" +'">' +
                        '<form class="form-inline">' +
                        '<div class="form-group">' +
                        '<div class="input-group">' +
                        '<select id="'+ options.tableName + "FieldSetSearchDom" +'" class="selectpicker" data-live-search="true"></select>' +
                        '</div> ' +
                        '<div class="input-group">' +
                        '<input type="text" class="form-control" data-field-search-value>' +
                        '</div> ' +
                        '<button type="button" class="btn btn-primary" data-search-btn>查询</button> ' +
                        addbtn + "&nbsp;" +
                        updatabtn + "&nbsp;" +
                        deletebtn + "&nbsp;" +
                        '</div>' +
                        '</form>' +
                        '</div>'

                }
            }
        })
        //在配置字段表中或者tableName这条数据
        $.ajax({
            url:"http://127.0.0.1:5000/CUID",
            type:"get",
            async: false,
            data:{
                tableName:"FieldSet",
                field:"TableName",
                fieldvalue:options.tableName,
                limit: 100000000,
                offset:0
            },
            success:function(data){
                data = JSON.parse(data)
                var ModalHtml = '<div id="'+ options.tableName + "Modal" +'" class="modal fade">'+
                    '<div class="modal-dialog">' +
                    '<div class="modal-content">' +
                    '<div class="modal-header">' +
                    '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>' +
                    '<h4 class="modal-title">配置信息</h4>' +
                    '</div>' +
                    '<div class="modal-body">' +
                    '<form class="form-horizontal" action="">' +
                    '<div class="form-group">' +
                    '<label for="ID" class="col-sm-3 control-label">ID</label>' +
                    '<div class="col-sm-9">' +
                    '<input type="text" class="form-control" name="ID" placeholder="" disabled="disabled">' +
                    '</div>' +
                    '</div>' +
                    '</form>' +
                    '</div>' +
                    '<div class="modal-footer"><button type="button" class="btn btn-primary" data-save-btn>保存</button></div>' +
                    '</div>' +
                    '</div>' +
                    '</div>'
                var ModalfieldHtml = ""
                if(data.rows == []) {
                    $.each(data.rows, function (i, value) {
                        //生成列头对象
                        var columnsField = {}
                        columnsField.field = data.rows[i].FieldName
                        columnsField.title = data.rows[i].TitleName
                        columnsField.inputType = data.rows[i].Edittype  //该字段输入类型
                        columnsField.DownTable = data.rows[i].Downtable //该字段下拉框加载的数据表
                        if (data.rows[i].Sortable == "True") {
                            columnsField.sortable = true
                            columnsField.order = "asc"
                        }
                        if (data.rows[i].Visible == "True") {
                            columnsField.visible = true
                        } else if (data.rows[i].Visible == "False") {
                            columnsField.visible = false
                        }
                        columns.push(columnsField)
                        //渲染模态框
                        if (data.rows[i].Isedit == "True") {
                            if (columnsField.inputType == "输入框") {
                                ModalfieldHtml += '<div class="form-group">' +
                                    '<label for="' + data.rows[i].FieldName + '" class="col-sm-3 control-label">' + data.rows[i].TitleName + '</label>' +
                                    '<div class="col-sm-9">' +
                                    '<input type="text" class="form-control" name="' + data.rows[i].FieldName + '" placeholder="">' +
                                    '</div>' +
                                    '</div>'
                            } else if (columnsField.inputType == "下拉框") {
                                ModalfieldHtml += '<div class="form-group">' +
                                    '<label for="' + data.rows[i].FieldName + 'selectField" class="col-sm-3 control-label">' + data.rows[i].TitleName + '</label>' +
                                    '<div class="col-sm-9">' +
                                    '<select id="' + data.rows[i].FieldName + 'selectField" class="selectpicker" data-live-search="true"></select>' +
                                    '</div>' +
                                    '</div>'
                            }
                        }
                    })
                }
                $("body").prepend(ModalHtml)
                $(ModalID).find(".form-horizontal").append(ModalfieldHtml)
            },
            error: function(data){
               console.log(data.responseText)
               bootbox.alert('获取表时请求失败')
            },
        })
        //表格渲染
        $this.bootstrapTable('destroy').bootstrapTable({
            url: "http://127.0.0.1:5000/CUID",
            method: 'get',
            queryParams:function(params){
                return {
                    tableName: options.tableName,
                    limit : params.limit,
                    offset : parseInt(params.offset/params.limit)
                };
            },
            pagination: true,
            toolbar:toolbar,
            pageNumber:1,
            pageSize: 10,
            pageList: [10, 20, 30, 40, 50],
            sidePagination: "server",
            paginationLoop:false,
            singleSelect:SingleSelect,
            clickToSelect:true,
            locale: "zh-CN",
            striped: true,
            showRefresh:true,
            columns: columns,
            responseHandler:function(res){
                res = JSON.parse(res)
                return res
            }
        })
        //搜索字段框渲染
        var resfreshFieldSelectOptions = ""
        $(toolbarID).find(FieldSetSearchID).html("")
        $.each(columns,function(i,value){
            if(columns[i].field){
                resfreshFieldSelectOptions += "<option value='"+ columns[i].field +"'>" + columns[i].title + "</option>";
            }
        })
        $(toolbarID).find(FieldSetSearchID).append(resfreshFieldSelectOptions)
        $(toolbarID).find(FieldSetSearchID).selectpicker("refresh")
        $(toolbarID).find(FieldSetSearchID).selectpicker("render")
        $(toolbarID).find(FieldSetSearchID).selectpicker("val", columns[0].title); //赋默认值
        //搜索按钮
        $(toolbarID).on("click","[data-search-btn]",function(){
            $this.bootstrapTable('refresh',{
                query:{
                    field: $(toolbarID).find(FieldSetSearchID).selectpicker("val"),
                    fieldvalue: $(toolbarID).find("[data-field-search-value]").val()
                }
            });
        })
        //添加按钮
        $(toolbarID).on("click","[data-add-btn]",function(){
            if(options.parentTableID != ""){
                var ParentTableRows = $(options.parentTableID).bootstrapTable("getAllSelections")
                if(ParentTableRows.length == 1){
                    $(ModalID).modal('show')
                    $.each(columns,function(i,value){
                        //判断输入框类型  为下拉框 则动态添加数据
                        if(columns[i].inputType == "输入框"){
                            $(ModalID).find(FieldSetSearchID).val("");
                        }else if(columns[i].inputType == "下拉框"){
                            $.ajax({
                                url:"http://127.0.0.1:5000/CUID",
                                type:"get",
                                data:{
                                    tableName:"FieldSet",
                                    field:"TableName",
                                    fieldvalue:columns[i].DownTable,
                                    limit: 100000000,
                                    offset:0
                                },
                                success:function(res){
                                    res = JSON.parse(res)
                                    var selectOptions = ""
                                    $(ModalID).find("#"+ columns[i].field +"selectField").html("");
                                    $.each(res.rows,function(i,value){
                                        selectOptions += "<option value='"+ res.rows[i].TitleName +"'>" + res.rows[i].TitleName + "</option>";
                                    })
                                    $(ModalID).find("#"+ columns[i].field +"selectField").append(selectOptions)
                                    $(ModalID).find("#"+ columns[i].field +"selectField").selectpicker("refresh")
                                    $(ModalID).find("#"+ columns[i].field +"selectField").selectpicker("render")
                                }
                            })
                        }
                    })
                }else{
                    bootbox.alert('请单选上级表格数据进行添加！');
                }
            }else{
                $(ModalID).modal('show')
                $.each(columns,function(i,value){
                    //判断输入框类型  为下拉框 则动态添加数据
                    if(columns[i].inputType == "输入框"){
                        $(ModalID).find("input[name="+ columns[i].field +"]").val("");
                    }else if(columns[i].inputType == "下拉框"){
                        $.ajax({
                            url:"http://127.0.0.1:5000/CUID",
                            type:"get",
                            data:{
                                tableName:"FieldSet",
                                field:"TableName",
                                fieldvalue:columns[i].DownTable,
                                limit: 100000000,
                                offset:0
                            },
                            success:function(res){
                                res = JSON.parse(res)
                                var selectOptions = ""
                                $(ModalID).find("#"+ columns[i].field +"selectField").html("");
                                $.each(res.rows,function(i,value){
                                    selectOptions += "<option value='"+ res.rows[i].TitleName +"'>" + res.rows[i].TitleName + "</option>";
                                })
                                $(ModalID).find("#"+ columns[i].field +"selectField").append(selectOptions)
                                $(ModalID).find("#"+ columns[i].field +"selectField").selectpicker("refresh")
                                $(ModalID).find("#"+ columns[i].field +"selectField").selectpicker("render")
                            }
                        })
                    }
                })
            }
        })
        //修改按钮
        $(toolbarID).on("click","[data-updata-btn]",function(){
            //判断是否有上级表格关联
            if(options.parentTableID != "") {
                var ParentTableRows = $(options.parentTableID).bootstrapTable("getAllSelections")
                if(ParentTableRows.length == 1){
                    var rows = $this.bootstrapTable('getAllSelections');
                    if (rows.length == 1) {
                        if (rows) {
                            $(ModalID).modal('show')
                            $.each(columns, function (i, value) {
                                if (columns[i].inputType == "输入框") {
                                    $(ModalID).find("input[name=" + columns[i].field + "]").val(rows[0][columns[i].field]);
                                } else if (columns[i].inputType == "下拉框") {
                                    $.ajax({
                                        url: "http://127.0.0.1:5000/CUID",
                                        type: "get",
                                        data: {
                                            tableName:"FieldSet",
                                            field:"TableName",
                                            fieldvalue:columns[i].DownTable,
                                            limit: 100000000,
                                            offset: 0
                                        },
                                        success: function (res) {
                                            res = JSON.parse(res)
                                            var selectOptions = ""
                                            $(ModalID).find("#" + columns[i].field +"selectField").html("")
                                            $.each(res.rows, function (i, value) {
                                                selectOptions += "<option value='" + res.rows[i].TitleName + "'>" + res.rows[i].TitleName + "</option>";
                                            })
                                            $(ModalID).find("#" + columns[i].field +"selectField").append(selectOptions)
                                            $(ModalID).find("#" + columns[i].field +"selectField").selectpicker("refresh")
                                            $(ModalID).find("#" + columns[i].field +"selectField").selectpicker("render")
                                            $(ModalID).find("#" + columns[i].field +"selectField").selectpicker('val', rows[0][columns[i].field])
                                        }
                                    })
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
                        $(ModalID).modal('show')
                        $.each(columns, function (i, value) {
                            if (columns[i].inputType == "输入框") {
                                $(ModalID).find("input[name=" + columns[i].field + "]").val(rows[0][columns[i].field]);
                            } else if (columns[i].inputType == "下拉框") {
                                $.ajax({
                                    url: "http://127.0.0.1:5000/CUID",
                                    type: "get",
                                    data: {
                                        tableName:"FieldSet",
                                        field:"TableName",
                                        fieldvalue:columns[i].DownTable,
                                        limit: 100000000,
                                        offset: 0
                                    },
                                    success: function (res) {
                                        res = JSON.parse(res)
                                        var selectOptions = ""
                                        $(ModalID).find("#" + columns[i].field +"selectField").html("")
                                        $.each(res.rows, function (i, value) {
                                            selectOptions += "<option value='" + res.rows[i].TitleName + "'>" + res.rows[i].TitleName + "</option>";
                                        })
                                        $(ModalID).find("#" + columns[i].field +"selectField").append(selectOptions)
                                        $(ModalID).find("#" + columns[i].field +"selectField").selectpicker("refresh")
                                        $(ModalID).find("#" + columns[i].field +"selectField").selectpicker("render")
                                        $(ModalID).find("#" + columns[i].field +"selectField").selectpicker('val', rows[0][columns[i].field])
                                    }
                                })
                            }
                        })
                    }
                } else {
                    bootbox.alert('请单选一条数据进行编辑！');
                }
            }
        })
        //删除按钮
        $(toolbarID).on("click","[data-delete-btn]",function(){
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
        $(ModalID).on("click","[data-save-btn]",function(){
            var idVal = $(ModalID).find("input[name=ID]").val();
            var requestType = ""
            if (idVal.length >= 1){
                requestType = "put"
            }else {
                requestType = "post"
            }
            var requestData = {} //请求参数的对象  获取表单内容
            requestData.tableName = options.tableName
            $.each(columns,function(i,value){
                if(columns[i].inputType == "输入框"){
                    requestData[columns[i].field] = $(ModalID).find("input[name="+ columns[i].field +"]").val();
                }else if(columns[i].inputType == "下拉框"){
                    requestData[columns[i].field] = $(ModalID).find("#"+ columns[i].field +"selectField").selectpicker("val");
                }
            })
            //判断是否有主表关联，有的话就额外传参
            if(options.parentTableID != ""){
                var parentTableClickRow = $(parentTableID).bootstrapTable("getAllSelections")
                requestData[options.parentTableLinkField] = parentTableClickRow[0][options.parentTableLinkField]
            }
            $.ajax({
                url:"http://127.0.0.1:5000/CUID",
                type:requestType,
                data:requestData,
                success:function(data){
                    if(data == "OK"){
                        $(ModalID).modal('hide')
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