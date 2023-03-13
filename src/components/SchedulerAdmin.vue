<template>

    <div class="row heading">
        <el-button @click="visible = true">Advanced Configuration</el-button>
    </div>


    <div>
         <el-drawer
    ref="drawerRef"
    v-model="visible"
    title="Advanced Configuration"
    :before-close="handleClose"
    direction="ltr"
    class="demo-drawer"
  >
    <div class="demo-drawer__content">
      <el-form :model="form">


                <el-form-item label="Template" :label-width="formLabelWidth">
                  <el-select
                    v-model="config.template"
                    placeholder="Please select activity area"
                    @change="updateConfig"

                  >

                     <el-option
                                 v-for="item in email_template_options"
                                 :key="item.value"
                                 :label="item.label"
                                 :value="item.value">
                               </el-option>

                  </el-select>
              </el-form-item>




                        <el-form-item label="Range" :label-width="formLabelWidth">

                          <el-slider
                                                                   @change="updateConfig"
                                                               v-model="config.lookahead_days"
                                                               :min="2"
                                                               :max="15"
                                                                   :step="1"
                                                          :format-tooltip="formatTooltip"	/>

                        </el-form-item>





                         <el-form-item label="Duration" :label-width="formLabelWidth">
                                            <el-slider
                                                                   @change="updateConfig"
                                                               v-model="config.duration"
                                                               :min="15"
                                                               :max="60"
                                                                   :step="5"

                                                          :format-tooltip="formatDurationTooltip"	/>
                        </el-form-item>


        <el-form-item :label-width="formLabelWidth">
                                     <el-checkbox v-model="config.send_message_confirmation" label="Send Email Confirmation" size="large" /><br>

                  <el-space fill>
                      <el-alert type="info" show-icon :closable="false">
                        <p>(ICS file not being generated as of yet)</p>
                      </el-alert>
                </el-space>
          </el-form-item>


                  <el-form-item :label-width="formLabelWidth">
                                         <el-checkbox v-model="config.notify_participants" label="Notify Participants" size="large" /><br>

                  <el-space fill>
                      <el-alert type="info" show-icon :closable="false">
                        <p>Email confirmation will require an attached ICS file <br>
                      <a href="https://developer.nylas.com/docs/calendar/using-the-calendar-api/#notify-participants">Nylas Documentation</a>

</p>
                      </el-alert>
                </el-space>
          </el-form-item>


          <el-form-item label="Calendar" :label-width="formLabelWidth">
                   <el-radio-group v-model="config.calendar" class="ml-4">
                         <el-radio label="primary" size="large">Primary Calendar (Alex Li)</el-radio>
                         <el-radio label="alt" size="large">Alt Calendar (Alex Li)</el-radio>
                       </el-radio-group>
          </el-form-item>

            <el-form-item label="Description" :label-width="formLabelWidth">
                  <el-input
                           v-model="config.description"
                           :rows="2"
                           type="textarea"
                           placeholder="Event Description (ignore template)"
                           />
          </el-form-item>

      </el-form>
      <div class="demo-drawer__footer">



              <div class="">
                <p>This project should be considered WIP and <b>not</b> neccessarily production ready.<br>
                This project demonstrates using Nylas' calendar API's to build a custom scheduling solution.
                    <br>
            </p>
                  <ul>
                      <b>Documentation Links:</b>
                <li><a href="https://developer.nylas.com/docs/api/#post/calendars/availability">Availability Request</a></li>
                <li><a href="https://developer.nylas.com/docs/api/#post/events">Event Creation</a></li>
                <li><a href="https://developer.nylas.com/docs/calendar/autocreate-meetings/#prerequisites-1">Google Meet Auto-Conferencing</a></li>
                <li><a href="https://developer.nylas.com/docs/api/#post/events/to-ics">Generate ICS file from event ID</a></li>
                <li><a href="https://developer.nylas.com/docs/api/#post/send">Send Email Confirmation</a></li>
            </ul>

    </div>
      </div>
    </div>
  </el-drawer>




    </div>



</template>

<script>

import { ElButton, ElDrawer } from 'element-plus'
import { CircleCloseFilled } from '@element-plus/icons-vue'


    export default {
        name:'SchedulerAdminComponent',
        props:['default_config'],
        mounted() {
            console.log('admin component')
            this.config = this.default_config;


        },
        data() {

            return {
                formLabelWidth:'80px',
                visible:false,

                config: {
                    lookahead_days:0,
                    duration:0,
                    template:'',
                    send_message_confirmation:true,
                    description:'',
                    calendar: '',
                    notify_participants:true
                },

                email_template_options:[
                    {label:'Template One', value:'template1.html'},
                    {label:'Template Two', value:'template2.html'},
                    {label:'Template Three', value:'template3.html'}
                ],
            }
        },
        methods: {
            formatDurationTooltip(val) {
                return `${val} minutes`;
            },
            formatTooltip	(val) {
                return `${val} days`;
            },

            updateConfig(event) {
                console.log('config changed');
                this.$emit("configchanged", this.config);
            },
            handle_close() {
                console.log('handle close')
            }
        }
    }
</script>
