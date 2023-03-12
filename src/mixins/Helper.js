import moment from "moment-timezone";

const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];

export const Helper = {

    methods: {
        formatShortDate(utcSeconds) {
            let date = new Date(utcSeconds * 1000);
            return date.getDate() + ' '+ months[date.getMonth()]
        },
       formatLongDate(utcSeconds) {
            let date = new Date(utcSeconds * 1000);
            return date.getDate() + ' '+ months[date.getMonth()] + ' ' + date.getFullYear() + ' ' +date.getHours()+ ':' +date.getMinutes()
        },

       formatAvailabilityDate(dateObject) {
            let day = weekday[dateObject.getDay()];
            let mon = month[dateObject.getMonth()];
            let date = dateObject.getDate();
            return (`${day}, ${date} ${mon}`);
       },


        humanReadableTime(utcSeconds) {
            return moment.unix(utcSeconds).format('H:mm');
        }

    }
};
