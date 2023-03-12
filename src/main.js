import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import './assets/main.css'

import SchedulerAdmin from './components/SchedulerAdmin.vue'
import Scheduler from './components/Scheduler.vue'
import SchedulerStatic from './components/SchedulerStatic.vue'
import SchedulerResponse from './components/SchedulerResponse.vue'


const app = createApp(App)

app.use(ElementPlus)

app.component('SchedulerAdmin', SchedulerAdmin)
app.component('Scheduler', Scheduler)
app.component('SchedulerStatic', SchedulerStatic)
app.component('SchedulerResponse', SchedulerResponse)

app.provide('global_host_timezone', import.meta.env.VITE_HOST_TIME_ZONE)
app.provide('global_host_name', import.meta.env.VITE_HOST_NAME)
app.provide('global_host_email', import.meta.env.VITE_HOST_EMAIL_ADDRESS)


app.provide('global_participant_name', import.meta.env.VITE_PARTICIPANT_NAME)
app.provide('global_participant_email', import.meta.env.VITE_PARTICIPANT_EMAIL_ADDRESS)


app.mount('#app')
