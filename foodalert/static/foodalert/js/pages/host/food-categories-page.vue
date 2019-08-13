<template>
    <generic-page>
        <template #heading>
            Tell us more about your food
        </template>
        <template #body>
            <p>
                The following will help determine whether your food can be shared with the public.
            </p>
            <b-form-group>
                <b-form-checkbox
                    v-model="selected"
                    value="non-perishable"
                    @click.native="removeInput('none')">
                    <span>
                        My food is non-perishable.
                        <b-link herf="#" v-b-toggle.non-perishable> Examples</b-link>
                    </span>
                </b-form-checkbox>
                <collapse-text-box bid="non-perishable">
                Candy, beverages (pasteurized, canned, or bottled), chips, dips.
                </collapse-text-box>
                <b-form-checkbox
                    v-model="selected"
                    class="mt-3"
                    value="pre-packaged"
                    @click.native="['none', 'at-home'].forEach(removeInput)">
                    <span>
                        My food was commercially pre-packaged.
                        <b-link herf="#" v-b-toggle.pre-packaged> Examples</b-link>
                    </span>
                </b-form-checkbox>
                <collapse-text-box bid="pre-packaged">
                    Wrapped or boxed baked goods (cakes, pies), chips, store-bought ice cream.
                </collapse-text-box>
                <b-form-checkbox
                    v-model="selected"
                    class="mt-3"
                    value="at-home"
                    @click.native="['none', 'pre-packaged', 'non-perishable'].forEach(removeInput)">
                    My food was prepared at home.
                </b-form-checkbox>
                <b-form-checkbox
                    v-model="selected"
                    class="mt-3"
                    value="none"
                    @click.native="['non-perishable', 'pre-packaged', 'at-home'].forEach(removeInput)">
                    <span>
                        None of the above.
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
                if (this.selected.includes('non-perishable') || this.selected.includes('pre-packaged')) {
                    this.$router.push({ name: 'h-need-permit' });
                } else if (this.selected.includes('none') || this.selected.includes('atHome')) {
                    this.$router.push({ name: 'h-close' });
                }
            },
            getBackPage() {
                this.$router.push({ name: 'h-food-service' });
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
            }).catch((error) => this.showErrorPage(error.response, "h-welcome"));
        },
    }
</script>
