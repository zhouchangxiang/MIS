<template>
  <el-row>
    <el-col :span="24">
      <div class="card-head">
        <span style="margin-left: 10px;" class="text-size-normol">工厂日历</span>
      </div>
      <el-col :span="24">
        <el-form :inline="true" :model="formParameters">
          <el-form-item label="月份：">
            <el-date-picker type="month" v-model="formParameters.startDate" size="mini" format="yyyy-MM" style="width: 120px;" :clearable="false"></el-date-picker>
          </el-form-item>
          <el-form-item label="开始班次：">
            <el-radio-group v-model="formParameters.team" fill="#082F4C" size="mini">
              <el-radio-button v-for="(item,index) in teamList" :key="index" :label="item.ShiftsName" :value="item.ShiftsName"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
      </el-col>
      <div class="platformContainer">
        <FullCalendar :plugins="calendarPlugins"
          locale="zh-cn"
          :header="header"
          :events="events"
          :editable="true"
          :selectable="true"
          :button-text="buttonText"
          @dateClick="handleDateClick"
          @eventClick="handleEventClick"
          @eventDrop="handleEventDrop"
          @eventResize="handleEventResize"
        />
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import FullCalendar from '@fullcalendar/vue'
  import dayGridPlugin from "@fullcalendar/daygrid";
  import timeGridPlugin from "@fullcalendar/timegrid";
  import interactionPlugin from "@fullcalendar/interaction";
  import '@fullcalendar/core/main.css';
  import '@fullcalendar/daygrid/main.css';
  import '@fullcalendar/timegrid/main.css';
  var moment = require('moment');
  export default {
    name: "Calendar",
    components: {
      FullCalendar
    },
    data(){
      return {
        formParameters:{
          startDate:moment(),
          team:"",
        },
        calendarPlugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        events:[],
        buttonText:{
          today:'今天',
          month: '月',
          week: '周',
          day: '天'
        },
        header:{
          left:'prev,next today',
          center:'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        dialogTableVisible:false,
        start:"",
        teamList:[]
      }
    },
    mounted() {
      this.getScheduling()
      this.getData()
    },
    methods:{
      getScheduling(){
        this.axios.get("/api/CUID",{
          params: {
            tableName: "Shifts",
            limit:100000000,
            offset:0
          }
        }).then(res =>{
          var data = JSON.parse(res.data)
          this.teamList = data.rows
        })
      },
      getData() {
        this.axios.get("/api/CUID",{
          params: {
            tableName: "plantCalendarScheduling",
            limit:100000000,
            offset:0
          }
        }).then(res =>{
          var data = JSON.parse(res.data)
          this.events = data.rows
        })
      },
      handleDateClick(arg){  //点击日期
        this.start = arg.dateStr

      },
      handleEventClick(e) {  //点击日程删除
        var ID = {
          id:e.event.extendedProps.ID
        }
        this.$confirm('此操作将永久删除该日程, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.delete("/api/CUID",{
            params: {
              tableName: "plantCalendarScheduling",
              delete_data:JSON.stringify(ID),
            }
          }).then(res =>{
            if(res.data == "OK"){
              this.getData()
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      handleEventDrop(e){   //拖动日程
        var startDate = moment(e.event.start).format('YYYY-MM-DD')
        var EndDate = moment(e.event.end).format('YYYY-MM-DD')
        var params = {
          tableName: "plantCalendarScheduling",
          ID:e.event.extendedProps.ID,
          title:e.event.title,
          start:startDate,
          end:EndDate,
          color:e.event.backgroundColor
        }
        this.axios.put("/api/CUID",this.qs.stringify(params)).then(res =>{
          if(res.data == "OK"){
            this.getData()
            this.$message({
              type: 'success',
              message: "修改成功"
            });
          }else{
            this.$message({
              type: 'info',
              message: res.data
            });
          }
        },res =>{
          console.log("请求错误")
        })
      },
      addSave(){
        var params = {
          tableName: "plantCalendarScheduling",
          title:this.team,
          start:this.start,
          color:"#00c3db"
        }
        this.axios.post("/api/CUID",this.qs.stringify(params)).then(res =>{
          if(res.data == "OK"){
            this.getData()
            this.dialogTableVisible = false
            this.$message({
              type: 'success',
              message: "添加成功"
            });
          }else{
            this.$message({
              type: 'info',
              message: res.data
            });
          }
        },res =>{
          console.log("请求错误")
        })
      },
      handleEventResize(e){  //拖动改变日程长度
        var startDate = moment(e.event.start).format('YYYY-MM-DD')
        var EndDate = moment(e.event.end).format('YYYY-MM-DD')
        var params = {
          tableName: "plantCalendarScheduling",
          ID:e.event.extendedProps.ID,
          title:e.event.title,
          start:startDate,
          end:EndDate,
          color:e.event.backgroundColor
        }
        this.axios.put("/api/CUID",this.qs.stringify(params)).then(res =>{
          if(res.data == "OK"){
            this.getData()
            this.$message({
              type: 'success',
              message: "修改成功"
            });
          }else{
            this.$message({
              type: 'info',
              message: res.data
            });
            this.getData()
          }
        },res =>{
          console.log("请求错误")
        })
      }
    }
  }
</script>

<style scoped>

</style>
