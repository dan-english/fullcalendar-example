<template>
<h1>Response</h1>
<div class="row">
         <div class="col-md-6">
                <pre><code class="json">{{ jsonFormat(event_confirmation_json) }}</code></pre>
         </div>
            <div class="col-md-6">
                <pre><code class="json">{{ jsonFormat(message_confirmation_json) }}</code></pre>
         </div>
</div>

</template>

<script>
    export default {
        name:'SchedulerResponseComponent',
        props:['confirmation_response'],
        mounted() {
            console.log('response component')
        },
        data() {
            return {
                event_confirmation_json: {},
                message_confirmation_json:{},
            }
        },
        watch:{
            confirmation_response() {
                this.event_confirmation_json = this.confirmation_response.event_response;
                this.message_confirmation_json = this.confirmation_response.send_response;
            }
        },
        methods: {

            jsonFormat(data) {
                    return JSON.stringify(data, null, 4);
            },
        }
    }
</script>
