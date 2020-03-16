<template>
  <el-row style="background: #fff;">
    <el-col :span="24" style="padding: 15px;">
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
      <el-dialog title="添加日程" :visible.sync="dialogTableVisible" width="30%">
        <el-radio-group v-model="team" size="small">
          <el-radio-button v-for="(item,index) in teamList" :label="item.label" :value="item.value" :key="index"></el-radio-button>
        </el-radio-group>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogTableVisible = false">取消</el-button>
          <el-button type="primary" @click="addSave">确认</el-button>
        </div>
      </el-dialog>
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
  export default {
    name: "Calendar",
    components: {
      FullCalendar
    },
    data(){
      return {
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
        team:"",
        teamList:[
          {label:"a班组",value:"a"},
          {label:"b班组",value:"b"},
          {label:"c班组",value:"c"},
        ]
      }
    },
    mounted() {
      this.getData()
      this.team = this.teamList[0].label
    },
    methods:{
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
        },res =>{
          console.log("请求错误")
        })
      },
      handleDateClick(arg){  //点击日期
        this.start = arg.dateStr
        this.dialogTableVisible = true
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
        var newDate = e.event.start
        var oldDate = e.oldEvent.start
        console.log(e,newDate,oldDate)
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
      handleEventResize(event, dayDelta, minuteDelta, revertFunc, jsEvent, ui, view){  //拖动改变日程长度
        console.log(event)
      }
    }
  }
</script>

<style scoped>

</style>
