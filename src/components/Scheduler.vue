<template>
    <div class="row heading">
        <h1>Scheduler Example Using Nylas Calendar APIs</h1>
        <div>
            Using <a target="_blank" href="https://fullcalendar.io/">FullCalendar.IO library</a> and <a target="_blank" href="https://developer.nylas.com/docs/api/#post/calendars/availability">Nylas Calendar data</a>
        </div>
        <div>
            <a id="github_repo_link" target="_blank"  href="https://github.com/dan-english/fullcalendar-example">Github Repo</a>
        </div>
    </div>


    <SchedulerAdmin
        :default_config="admin_config"
        v-on:configchanged="refreshData"
    />


    <div class="row">
          <div class="box col-md-5">
               <div >
                   <FullCalendar :options="calendarOptions" />
               </div>
          </div>
          <div class="col-md-2" v-if="selected_date">

                   <div  class="box" style="text-align:center">
                        <h5>{{ host_name }}'s availability on <br>{{ formatAvailabilityDate(this.selected_date['date']) }}</h5>

                        <div style="text-align: center">
                            <div v-for="timeslot in timeslots_for_day" style="padding:5px;">
                                  <el-button
                                          style="width:90%"
                                        :id="(timeslot['start'])"
                                        type="primary"
                                        plain
                                        size="large"
                                        @click="selectedTime(timeslot['start_time'])">
                                      {{  humanReadableTime(timeslot['start_time']) }}
                                  </el-button>
                            </div>
                        </div>
                   </div>
          </div>
          <div id="collect_details_and_confirm" class="col-md-3">

             <div v-if="selected_time"  class="box" >

                            <h4>{{ formatAvailabilityDate(this.selected_date['date']) }}</h4>
                            {{selected_time}} With {{host_name}}<br> {{host_timezone}}
                            <div style="padding:5px;">
                                <el-input placeholder="Your Name" v-model="participant_name"></el-input>
                            </div>
                            <div style="padding:5px;">
                                <el-input placeholder="Email" v-model="participant_email"></el-input>
                            </div>

                             <el-button type="primary" plain style="width:200px" @click="confirmBooking()">Confirm Booking</el-button>
             </div>

          </div>
    </div>

    <div id='Scheduler_Response' class='row' >
        <SchedulerResponse
                :confirmation_response="confirmation_data" >
        </SchedulerResponse>
    </div>

</template>

<script>

import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import moment from 'moment-timezone';
import axios from 'axios';
import { ElNotification } from 'element-plus'

import {Helper} from '../mixins/Helper'

    export default {
        name: 'SchedulerComponent',
        mixins: [Helper],
        inject: ['global_host_timezone','global_host_name','global_host_email','global_participant_name', 'global_participant_email'],

        components: {
            FullCalendar // make the <FullCalendar> tag available
        },
        mounted() {
              console.groupCollapsed('Scheduler Config Details');
              console.log(`Host Name: ${this.global_host_name}`);
              console.log(`Host Email: ${this.global_host_email}`);
              console.log(`Host Timezone: ${this.global_host_timezone}`);
              console.log(`Participant Name: ${this.global_participant_name}`);
              console.log(`Participant Email: ${this.global_participant_email}`);
              console.warn(`Timezone set to: ${this.global_host_timezone}`)
              console.groupEnd();

            moment.tz.setDefault(this.global_host_timezone);
            this.calendarOptions.timeZone = this.global_host_timezone
            this.calendarOptions.initialDate = moment().format("YYYY-MM-DD");

            this.host_name = this.global_host_name;
            this.host_email = this.global_host_email;
            this.host_timezone = this.global_host_timezone;


            this.participant_name = this.global_participant_name;
            this.participant_email = this.global_participant_email;

            this.refreshData();
        },
        data() {
            return {
                email_template:'template1.html',
                email_template_options:[
                    {label:'Template One', value:'template1.html'},
                    {label:'Template Two', value:'template2.html'},
                    {label:'Template Three', value:'template3.html'}
                ],
                admin_config:{
                    lookahead_days:14,
                    duration:48,
                    template:'template1.html',
                    send_message_confirmation:true,
                    notify_participants:true,
                    description:'',
                    calendar: 'primary'
                },

                host_name: 'default',
                host_email: 'default@email.com',
                host_timezone: undefined,

                participant_name:'',
                participant_email:'',

                eventSources: [],
                calendarOptions: {
                    plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
                    initialView: 'dayGridMonth',
                    weekends: false, // initial value
                    headerToolbar: {
                        left: 'prev',
                        center: 'title',
                        right: 'next'
                    },
                    eventClassNames: 'dan-class',
                    eventTimeFormat: {
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: false
                    },
                    // initialDate:'2023-01-1',
                    validRange: {
                        start: '2023-01-01',
                        end: '2023-12-31',
                    },
                    showNonCurrentDates: false,
                    dateClick: this.handleDateSelect,
                    height: "auto",
                    datesSet: this.highlightDays,
                },

                timeslot_data: [],
                availableDays: [],
                timeslots_for_day: [],

                selected_date: '',
                selected_time: '',
                selected_epoch_time:'',
                selected_day:'',


                //this holds the responses after creating the event/sending the message
                confirmation_data:{}


            }
        },
        watch: {

        },
        methods: {
            selectedTime(timeslot) {
                let app = this;
                console.groupCollapsed('New Time Slot Selected');
                console.log(timeslot);
                console.log(this.humanReadableTime(timeslot));
                console.groupEnd();

               if(app.selected_epoch_time) {
                   document.getElementById(app.selected_epoch_time).classList.remove('active_timeslot_button');
                   app.selected_epoch_time = null;
               }

                document.getElementById(timeslot).classList.add('active_timeslot_button');

                app.selected_time = this.humanReadableTime(timeslot)
                app.selected_epoch_time = timeslot;
            },

            highlightDays() {
                Array.from(document.querySelectorAll('.available-timeslots-on-day')).forEach((el) => el.classList.remove('available-timeslots-on-day'));
                Array.from(document.querySelectorAll('.selected_day')).forEach((el) => el.classList.remove('selected_day'));


                //identify the days on the calendar that have available time-slots
                for(let i in this.availableDays) {
                    const el1 = document.querySelector('[data-date="'+this.availableDays[i]+'"]');
                    if(el1) {
                        el1.classList.add('available-timeslots-on-day')
                    }
                }
            },

            handleDateSelect(info) {
                console.log(info)
                let app = this;
                let clicked_date =  info.dateStr;


                //if a date has previously been selected reset the styles on the calendar
                if (app.selected_date) {
                    document.querySelector('[data-date="'+app.selected_date.dateStr+'"]').classList.remove('selected_day');
                }
                //check if a timeslot has been selected too

              if(app.selected_epoch_time) {
                    document.getElementById(app.selected_epoch_time).classList.remove('active_timeslot_button');

                    app.selected_epoch_time = null;
                    app.selected_time = null;
                    //shift the focus to remove the hover state on the button
                    document.getElementById("github_repo_link").focus();
              }


                if(app.availableDays.includes(clicked_date)) {
                    document.querySelector('[data-date="' + clicked_date + '"]').classList.add('selected_day');
                }

                let timeslots = app.timeslot_data.filter(function (timeslot) {
                    return timeslot.day === info.dateStr;
                });

                app.timeslots_for_day = timeslots || null;
                app.selected_date = timeslots.length > 0 ? info : null;


            },

            getAvailability() {
                let app = this;
                axios.get('/availability').then((response) => {


                    //available days will be used to highlight possible days on the calendar
                    app.availableDays = response.data.days;

                    //timeslot_data will be used to display possible time-slots for a meeting.
                    app.timeslot_data = response.data.time_slots;


                    console.groupCollapsed("Get Data From Nylas");
                    console.log(response.data);
                    console.groupEnd();
                }).then(()=>{

                        open2();

                    app.highlightDays();
                })

            },


            refreshData(value) {
                let app = this;
                  if(value) {
                      app.admin_config = value;
                  }

                app.selected_epoch_time = null;
                app.selected_time = null;
                app.timeslots_for_day =  null;
                app.selected_date=null;
                app.timeslot_data=null;
                app.availableDays=[]
                app.highlightDays();

                //shift the focus to remove the hover state on the button
                document.getElementById("github_repo_link").focus();

                axios.post('/availability-data', app.admin_config).then((response) => {

                    console.log(response.data);
                    //available days will be used to highlight possible days on the calendar
                    app.availableDays = response.data.days;

                    //timeslot_data will be used to display possible time-slots for a meeting.
                    app.timeslot_data = response.data.time_slots;
                }).then(()=>{
                    console.log(app.timeslot_data)
                    app.highlightDays();

                    ElNotification({
                        title: "Success",
                        type: "success",
                        message: 'Time Slots Updated',
                        duration: 1500,
                        position: 'top-right',
                        showClose: false,
                    });

                })
            },

            confirmBooking(){
                let app = this;
                app.confirmation_data = {};

                const data = {

                    config:app.admin_config,

                    host_name:app.host_name,
                    host_email:app.host_email,
                    host_timezone:app.host_timezone,

                    participant_name:app.participant_name,
                    participant_email:app.participant_email,

                    selected_epoch:app.selected_epoch_time,

                    selected_time:app.selected_time, //used in the message template
                    selected_date:app.formatAvailabilityDate(this.selected_date['date']) //used in the message template


                }
                axios.post('/send-confirmation', data).then((response)=>{
                    console.groupCollapsed("Confirmation Processes");
                    console.log(response.data);
                    console.groupEnd();
                    app.confirmation_data = response.data
                    ElNotification({
                        title: "Success",
                        type: "success",
                        message: 'Event Created',
                        duration: 1500,
                        position: 'top-right',
                        showClose: false,
                    });
                })

            },

        }
    }
</script>
