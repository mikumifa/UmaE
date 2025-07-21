<template>
    <div class="flex items-center space-x-1" :class="have ? 'text-black' : 'text-red-400 line-through'">
        <span>{{ name }}</span>
        <span v-if="!have">🚫</span>
    </div>
</template>

<script>
export default {
    name: 'SkillLabel',
    props: {
        name: {
            type: String,
            required: true,
        },
        have: {
            type: Boolean,
            default: false,
        },
    },
};
</script>
