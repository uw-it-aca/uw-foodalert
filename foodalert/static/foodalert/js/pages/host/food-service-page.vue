<template>
    <generic-page>
        <template #heading>
            Food service information
        </template>
        <template #body>
            <p>
                Let's determine you eligibility for using Hungry Husky. Select all that apply.
            </p>
            <b-form-group>
                <b-form-checkbox
                    v-model="selected"
                    key="preparedByAuth"
                    value="preparedByAuth"
                    :disabled="selected.includes('none')">
                    My food was prepared by UW Housing &amp; Food Services or Bay Laurel Catering.
                </b-form-checkbox>
                <b-form-checkbox
                    v-model="selected"
                    key="hasPermit"
                    value="hasPermit"
                    :disabled="selected.includes('none')">
                    I have a UW Temporary Food Service Permit.
                    <b-link herf="#" v-b-toggle.perm-info> Learn More</b-link>
                </b-form-checkbox>
                <collapse-text-box bid="perm-info">
                    When providing food to the public (anyone beyond staff/faculty of your unit), UW offices are required to secure a Temporary Food Permit through <a href="#">UW Environmental Health &amp; Safety</a> to help ensure food service providers meet safety reulation and the food itself is safe for consumption.
                </collapse-text-box>
                <b-form-checkbox
                    v-model="selected"
                    key="none"
                    value="none"
                    :disabled="selected.includes('hasPermit') || selected.includes('preparedByAuth')">
                    None of the above.
                </b-form-checkbox>
            </b-form-group>
        </template>
        <template #navigation>
            <div class="mt-5">
               <b-row align-h="between">
                 <b-col md="4" lg="3" order-md="2">
                   <b-button class="mb-3" type="submit" block size="lg" variant="primary" @click="getNextPage()">Continue</b-button>
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
                if (this.selected.includes('hasPermit')) {
                    this.$router.push({ name: 'h-responsibilities' });
                } else if (this.selected.includes('preparedByAuth')) {
                    this.$router.push({ name: 'h-need-permit' });
                } else if (this.selected.includes('none')) {
                    this.$router.push({ name: 'h-categories' });
                }
            },
            getBackPage() {
                this.$router.push({ name: 'h-welcome' });
            }
        },
        data() {
            return {
                selected: [],
            }
        }
    }
</script>
