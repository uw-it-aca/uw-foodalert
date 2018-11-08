<template>
     <div>
         <div>
             <b-dropdown text="Year">
             </b-dropdown>
             <b-dropdown text="Month">
             </b-dropdown>   
             <b-button style="float: right">Export</b-button>
         </div>
         <p></p>
         <b-table hover :items="items"></b-table>
     </div>
</template>

<script>
    const items = [
        { dateSent: '10/22/18', timeSent: '4:44PM', endTime: '5:32PM', updateTime: '5:10PM', host: 'netid@uw.edu', permitNumber: '12345678', foodAndEvent: 'A Food and Event', quantity: 'About 8 meals', location: 'HUB 101', contains: 'Dairy, Meat' }
    ]

    export default {
        data() {
            return {
                items: items
            }
        },
        components: {

        },
        computed: {

        },
        props: {
            items: {
                type: Array
            }
        }
    }   
</script>

