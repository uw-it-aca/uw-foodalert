<template>
    <ended-template></ended-template>
</template>

<script>
    export default {
    mounted() {
        console.log('ended mounted');
    },  
    beforeRouteUpdate(to, from, next) {
        console.log('ended update');
        next();
    },  
    beforeRouteEnter(to, from, next) {
        next(function(vm) {
            console.log('ended entered');
        }); 
    },  
    beforeRouteExit(to, from, next) {
        console.log('ended exit');
        next();
    }   
    }
</script>
