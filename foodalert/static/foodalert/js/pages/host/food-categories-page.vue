<template>
    <generic-page>
        <template #heading>
            Tell us about your food
        </template>
        <template #body>
            <p>
                Select all that apply to your food.
            </p>
            <b-form-group>
                <b-form-checkbox
                    v-model="selected"
                    key="non-perishable"
                    value="non-perishable"
                    :disabled="selected.includes('none') || selected.includes('atHome')">
                    My food is non-perishable.
                    <b-link herf="#" v-b-toggle.non-perishable> Examples</b-link>
                </b-form-checkbox>
                <collapse-text-box bid="non-perishable">
                Candy, beverages (pasteruized, canned, or bottled), chips, dips.
                </collapse-text-box>
                <b-form-checkbox
                    v-model="selected"
                    key="pre-packaged"
                    value="pre-packaged"
                    :disabled="selected.includes('none') || selected.includes('atHome')">
                    My food was commercially pre-packaged.
                    <b-link herf="#" v-b-toggle.pre-packaged> Examples</b-link>
                </b-form-checkbox>
                <collapse-text-box bid="pre-packaged">
                    Wrapped or boxed baked goods (cakes, pies), chips, store-bought ice cream.
                </collapse-text-box>
                <b-form-checkbox
                    v-model="selected"
                    key="atHome"
                    value="atHome"
                    :disabled="selected.includes('non-perishable') || selected.includes('pre-packaged') || selected.includes('none')">
                    My food was prepared at home.
                </b-form-checkbox>
                <b-form-checkbox
                    v-model="selected"
                    key="none"
                    value="none"
                    :disabled="selected.includes('non-perishable') || selected.includes('pre-packaged') || selected.includes('atHome') ">
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
                if (this.selected.includes('non-perishable') || this.selected.includes('pre-packaged')) {
                    this.$router.push({ name: 'h-need-permit' });
                } else if (this.selected.includes('none') || this.selected.includes('atHome')) {
                    this.$router.push({ name: 'h-close' });
                }
            },
            getBackPage() {
                this.$router.push({ name: 'h-food-service' });
            }
        },
        data() {
            return {
                selected: [],
            }
        }
    }
</script>
