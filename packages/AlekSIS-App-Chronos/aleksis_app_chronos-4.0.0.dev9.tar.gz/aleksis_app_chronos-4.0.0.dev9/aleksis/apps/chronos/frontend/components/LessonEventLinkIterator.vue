<script>
export default {
  name: "LessonEventLinkIterator",
  props: {
    items: {
      type: Array,
      required: true,
    },
    attr: {
      type: String,
      required: false,
      default: "name",
    },
    alternativeAttr: {
      type: String,
      required: false,
      default: null,
    },
  },
  methods: {
    getAttr(item) {
      let val = item[this.attr];
      if (val) return val;
      return this.alternativeAttr ? item[this.alternativeAttr] : val;
    },
  },
};
</script>

<template>
  <span v-bind="$attrs">
    <span v-for="(item, idx) in items" :key="idx">
      <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
      {{ getAttr(item) }}{{ idx + 1 < items.length ? "," : "" }}
    </span>
  </span>
</template>
