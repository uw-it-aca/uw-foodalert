<template>
    <generic-page>
        <template #heading>
            Responsibilities
        </template>
        <template #body>
            <p>
                To ensure the safety of the food being shared, we'll need you yo agree to the following requirements.
            </p>
            <b-form-group>
                <b-form-checkbox
                    v-model="selected"
                    key="cond1"
                    value="cond1">
                    My office is responsible for the safety of this food.
                    <b-link herf="#" v-b-toggle.cond1-info> Learn More</b-link>
                </b-form-checkbox>
                <collapse-text-box bid="cond1-info">
                    You are responsible for food safety under the approval of the Temporary Food Permit, this same level of responsibility applies when using the Hungry Husky App.
                </collapse-text-box>
                <b-form-checkbox
                    v-model="selected"
                    key="cond2"
                    value="cond2">
                    For potrntially hazardous food, it has not benn out of heating or cooling for more than <strong>four hours</strong>.
                    <b-link herf="#" v-b-toggle.cond2-info> Learn More</b-link>
                </b-form-checkbox>
                <collapse-text-box bid="cond2-info">
                    Information is missing
                </collapse-text-box>
            </b-form-group>
        </template>
        <template #navigation>
            <div class="mt-5">
               <b-row align-h="between">
                 <b-col md="4" lg="3" order-md="2">
                   <b-button class="mb-3" type="submit" block variant="primary" @click="getNextPage()">Continue</b-button>
                 </b-col>
                 <b-col md="4" lg="3" order-md="1">
                   <b-button class="hh-back-button" type="submit" block variant="light" @click="getBackPage()">Back</b-button>
                 </b-col>
               </b-row>
            </div>
        </template>
    </generic-page>
</template>

<script type="text/javascript">
    import GenericPage from "../components/generic-page.vue";
    import CollapseTextBox from "../components/collapse-text-box.vue";
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
                if (this.selected.includes('cond1') && this.selected.includes('cond2')) {
                    this.$router.push({ name: 'form' });
                }
            },
            getBackPage() {
                this.$router.push({ name: 'food-service' });
            }
        },
        data() {
            return {
                selected: [],
            }
        }
    }
</script>