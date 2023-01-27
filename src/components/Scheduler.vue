<template>
    <div class="row heading">
        <h1>Scheduler Example Using Live Data</h1>
        <div><a title="Response Data Set" target="_blank" href="/availability">Live Request via Flask Server</a></div>
        <div>
            Using <a target="_blank" href="https://fullcalendar.io/">FullCalendar.IO library</a> and <a target="_blank" href="https://developer.nylas.com/docs/api/#post/calendars/availability">Nylas Calendar data</a>
        </div>
    </div>
    <div>
          <div class="box col-md-5">
               <div>
                   <FullCalendar :options="calendarOptions" />
               </div>
          </div>
          <div class="col-md-2" v-if="selected_date">

                   <div  class="box" style="text-align:center">
                        <h5>Availability on <br>{{ formatSelectedDate() }}</h5>

                        <div style="text-align: center">
                            <div v-for="timeslot in timeslots_for_day" style="padding:5px;">
                                  <el-button
                                          style="width:90%"
                                        :id="(timeslot['start'])"
                                        type="primary"
                                        plain
                                        size="large"
                                        @click="selectedTime(timeslot['start'])">
                                      {{ humanTime(timeslot['start']) }}
                                  </el-button>

                            </div>
                        </div>
                   </div>

          </div>
          <div class="col-md-3">
                <div v-if="selected_time"  class="box" >
                    <h4>{{formatSelectedDate()}}</h4>
                    {{selected_time}} With an important person<br>Europe/London
            <div style="padding:5px;">
                <el-input placeholder="Your Name" v-model="name"></el-input>
            </div>
            <div style="padding:5px;">
                <el-input placeholder="Email" v-model="email"></el-input>
            </div>
            <el-button type="primary" plain style="width:200px" @click="confirmBooking()">Confirm Booking</el-button>

        </div>

          </div>
        </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import moment from 'moment';
import axios from 'axios';

    export default {
        components: {
            FullCalendar // make the <FullCalendar> tag available
        },
        mounted() {
            this.getAvailability();
        },
        data() {
            return {
                name:'',
                email:'',
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
                    initialDate:'2023-01-1',
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

                duration: 15,

            }
        },
        methods: {

            selectedTime(timeslot) {
                let app = this;
                console.groupCollapsed('New Time Slot Selected');
                console.log(timeslot);
                console.log(this.humanTime(timeslot));
                console.groupEnd();

               if(app.selected_epoch_time) {
                   document.getElementById(app.selected_epoch_time).classList.remove('active_timeslot_button');
                   app.selected_epoch_time = null;
               }

                document.getElementById(timeslot).classList.add('active_timeslot_button');

                app.selected_time = this.humanTime(timeslot)
                app.selected_epoch_time = timeslot;
            },

            formatSelectedDate() {
                let sdate = moment(this.selected_date['date']);
                return sdate.format('dddd') +', ' +sdate.format('MMMM')+' ' +sdate.format('Do')
            },

            humanTime(utcSeconds) {
                var date = new Date(utcSeconds * 1000);
                var day = moment.unix(utcSeconds);

                return day.format('H:mm');
            },

            highlightDays() {
                for(let i in this.availableDays) {
                    const el1 = document.querySelector('[data-date="'+this.availableDays[i]+'"]');
                    if(el1) {
                        el1.classList.add('available-timeslots-on-day')
                    }
                }
            },

            handleDateSelect(info) {
                let app = this;
                if(app.selected_epoch_time) {
                    let activeSlot = document.getElementById(app.selected_epoch_time);
                    activeSlot.classList.remove('active_timeslot_button')

                    app.selected_epoch_time = null;
                    app.selected_time = null;
                }

                // info.dayEl.style.backgroundColor = 'red';

                let timeslots = app.timeslot_data.filter(function (timeslot) {
                    return timeslot.day === info.dateStr;
                });

                app.timeslots_for_day = timeslots || null;
                app.selected_date = timeslots.length > 0 ? info : null;

                console.groupCollapsed('New Day Selected');
                console.log(info);
                console.log(timeslots)
                console.groupEnd();
            },

            getAvailability() {
                let app = this;
                axios.get('/availability').then((response)=>{
                    app.availableDays = response.data.days;
                    app.timeslot_data = response.data.time_slots;
                    console.groupCollapsed("Get Data From Nylas");
                    console.log(response.data);
                    console.groupEnd();
                }).then(()=>{
                    app.highlightDays();
                })

            },

            confirmBooking(){
                alert('confirm booking details')
            },

        }
    }
</script>
