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
    export default {
        data() {
            return {
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

