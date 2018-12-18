<template>
     <div>
         <div>
             <b-dropdown text="Year" v-on:click.native="changeValue($event, 'Year')">
                <b-dropdown-item v-for="year in this.years">
                {{ year }}
                </b-dropdown-item>
             </b-dropdown>
             <b-dropdown text="Month" v-on:click.native="changeValue($event, 'Month')">
                <b-dropdown-item v-for="month in this.months">
                {{ month }}
                </b-dropdown-item>
             </b-dropdown>   
             <b-button style="float: right" @click="exportTable">Export</b-button>
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
        props: {
            items: {
                type: Array
            },
            years: {
                type: Array
            },
            months: {
                type: Array
            }
        },
        methods: {
            exportTable() {
                this.$emit('export');
            },
            changeValue(event, context) {
                this.$emit('updateValue', context, event.target.innerText);
            },
        }
    }   
</script>

