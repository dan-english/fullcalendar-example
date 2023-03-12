<template>
   <div class="row heading">
          <div class="box col-md-12">
                      <h1>Scheduler (Admin) Settings</h1>

               <div >
                     <div class="box col-md-2">
                           <el-select v-model="config.template" placeholder="Select Email Template"  @change="updateTimezone()">
                                <el-option
                                  v-for="item in email_template_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                           </el-select>
                     </div>

                                        <div class="box col-md-2">
                                                     <div>
                                                            <el-slider
                                                                    @change="updateTimezone()"
                                                                v-model="config.lookahead_days"
                                                                :min="2"
                                                                :max="15"
                                                                    :step="1"
                                                           :format-tooltip="formatTooltip"	/>

                                                      </div>

                                         </div>


                                       <div class="box col-md-2">
                                                     <div class="slider-demo-block">

                                                            <el-slider
                                                                    @change="updateTimezone()"
                                                                v-model="config.duration"
                                                                :min="15"
                                                                :max="60"
                                                                    :step="5"

                                                           :format-tooltip="formatDurationTooltip"	/>

                                                      </div>

                                         </div>

                    <div class="box col-md-2">
                        <el-checkbox v-model="config.send_message_confirmation" label="Send Email Confirmation" size="large" />
                    </div>

                    <div class="box col-md-2">
                        <el-radio-group v-model="config.calendar" class="ml-4">
                          <el-radio label="primary" size="large">Primary Calendar (Alex Li)</el-radio>
                          <el-radio label="alt" size="large">Alt Calendar (Alex Li)</el-radio>
                        </el-radio-group>
                    </div>

                    <div class="box col-md-2">
                         <el-input
                            v-model="config.description"
                            :rows="2"
                            type="textarea"
                            placeholder="Event Description (ignore template)"
                            />
                    </div>
               </div>
          </div>
    </div>


</template>

<script>
    export default {
        name:'SchedulerAdminComponent',
        props:['default_config'],
        mounted() {
            console.log('admin component')
            this.config = this.default_config;
        },
        data() {
            return {
                config: {
                    lookahead_days:0,
                    duration:0,
                    template:'',
                    send_message_confirmation:true,
                    description:'',
                    calendar: ''
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

            updateTimezone(event) {
                this.$emit("configchanged", this.config);
            }
        }
    }
</script>
