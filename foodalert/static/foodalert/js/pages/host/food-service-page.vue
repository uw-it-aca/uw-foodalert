<template>
    <generic-page>
        <template tabindex="0" #heading>
            Food service information
        </template>
        <template #body>
            <p>
                Let’s determine whether your food can be shared with the public. Please select all that apply.
            </p>
            <b-form-group>
                <b-form-checkbox
                    v-model="selected"
                    value="preparedByAuth"
                    @click.native="removeInput('none')">
                    <span>
                        My food was prepared by UW Housing &amp; Food Services or Bay Laurel Catering.
                    </span>
                </b-form-checkbox>
                <b-form-checkbox
                    v-model="selected"
                    class="mt-2"
                    value="hasPermit"
                    @click.native="removeInput('none')">
                    <span>
                        I have a UW Temporary Food Service Permit.
                        <b-link herf="#" v-b-toggle.perm-info> Learn more</b-link>
                    </span>
                </b-form-checkbox>
                <collapse-text-box bid="perm-info">
                    When providing food to the public (anyone beyond the staff or /faculty of your unit), UW offices are required to secure a Temporary Food Permit through <a href="#">UW Environmental Health &amp; Safety</a> to help ensure that food service providers meet safety regulations and the food itself is safe for consumption.
                </collapse-text-box>
                <b-form-checkbox
                    v-model="selected"
                    value="none"
                    class="mt-2"
                    @click.native="['preparedByAuth', 'hasPermit'].forEach(removeInput)">
                    <span>
                        None of these apply.
                    </span>
                </b-form-checkbox>
            </b-form-group>
        </template>
        <template #navigation>
            <div class="mt-5">
               <b-row align-h="between">
                 <b-col md="4" lg="3" order-md="2">
                   <b-button class="mb-3" type="submit" block size="lg" variant="primary" @click="getNextPage()" :disabled="selected.length == 0">Continue</b-button>
                 </b-col>
                 <b-col md="4" lg="3" order-md="1">
                   <b-button class="hh-back-button" type="submit" block size="lg" variant="outline-secondary" @click="getBackPage()">Back</b-button>
                 </b-col>
               </b-row>
            </div>
        </template>
    </generic-page>
</template>

<script type="text/javascript">
    import GenericPage from "../../components/generic-page.vue";
    import CollapseTextBox from "../../components/collapse-text-box.vue";
    export default {
        components:{
            "generic-page": GenericPage,
            "collapse-text-box": CollapseTextBox,
        },
        props: {
            bid: String,
        },
        methods: {
            getNextPage() {
                if (this.selected.includes('hasPermit') || this.selected.includes('preparedByAuth')) {
                    this.$router.push({ name: 'h-responsibilities' });
                } else { // if (this.selected.includes('none'))
                    this.$router.push({ name: 'h-categories' });
                }
            },
            getBackPage() {
                this.$router.push({ name: 'h-welcome' });
            },
            removeInput(str) {
                if(this.selected.includes(str)){
                    this.selected.splice(this.selected.indexOf(str), 1);
                }
            }
        },
        data() {
            return {
                selected: [],
            }
        },
        beforeMount() {
            axios.get("/notification/?host_netid=" + this.netID).then((result) => {
                result.data = result.data.filter((d)=>!d.ended)
                if(result.data.length)
                    this.$router.push({ name: 'h-update', params: {notificationText: "You already have an event running."}});
            }).catch((error) => this.showErrorPage(error.response, "h-food-service"));
        },
    }
</script>
